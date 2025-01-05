import os
import time
# from langfuse.callback import CallbackHandler

import chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_mistralai.chat_models import ChatMistralAI

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from langchain_core.output_parsers import JsonOutputParser

from llm.logger import logger


class SecurityRAG:

    def __init__(
        self,
        chroma_host: str,
        chroma_port: int,
        mistral_api: str,
        ollama_host: str,
        ollama_port,
        # langfuse_secret_key: str,
        # langfuse_public_key: str,
        # langfuse_host: str,
        # langfuse_port: int,
        prompt: str,
        embeddings="nomic-embed-text"####"sentence-transformers/all-mpnet-base-v2",
    ):  
        self.chroma_host = chroma_host
        self.chroma_port = chroma_port
        self.prompt = prompt
        self.embeddings = embeddings

        self.llm_client = ChatMistralAI(
            mistral_api_key=mistral_api,
            model_name="mistral-large-latest",
            temperature=0.5, 
            max_tokens=128
        )

        logger.info(f"Mistal key: {mistral_api[:10]}")

        self.ollama_url= f"http://{ollama_host}:{ollama_port}" 

        logger.info(self.ollama_url)

        


        # self.langfuse_handler = CallbackHandler(
        #     secret_key=langfuse_secret_key,
        #     public_key=langfuse_public_key,
        #     host=f"http://{langfuse_host}:{langfuse_port}" # run on localhost
        # )
      

    async def arun(self, user_prompt: str, model_response: str):  # Apply rate limiting before asynchronous call
        self.db_client = chromadb.HttpClient(
                host=self.chroma_host,
                port=self.chroma_port,
        )
        

        self.embeddings_model = OllamaEmbeddings(model=self.embeddings, base_url= self.ollama_url)
        self.vector_store = Chroma(
            client=self.db_client,
            embedding_function=self.embeddings_model,
        )
        logger.info('Chroma async client initialized successfully.')
        self.document_chain = create_stuff_documents_chain(self.llm_client, self.prompt)
        self.retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(search_type='mmr'), self.document_chain
        )
        self.output_parser = JsonOutputParser()
    
        response = await self.retrieval_chain.ainvoke(
            {
                "input": user_prompt,
                "model_response": model_response,
            }
            # , config={"callbacks": [self.langfuse_handler]}
        )
        logger.info(response)
        result = self.output_parser.parse(response["answer"])
        logger.info(result)
        return result