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

from logger import logger


class SecurityRAG:

    def __init__(
        self,
        chroma_host: str,
        chroma_port: int,
        mistral_api: str,
        # langfuse_secret_key: str,
        # langfuse_public_key: str,
        # langfuse_host: str,
        # langfuse_port: int,
        prompt: str,
        embeddings="nomic-embed-text"####"sentence-transformers/all-mpnet-base-v2",
    ):
        self.db_client = chromadb.Client(
            chromadb.Settings(
                chroma_server_host=chroma_host,
                chroma_server_http_port=chroma_port,
            )
        )
        self.llm_client = ChatMistralAI(
            mistral_api_key=mistral_api,
            model_name="mistral-large-latest",
            temperature=0.5, 
            max_tokens=128
        )
        logger.info(f"Mistal key: {mistral_api[:10]}")
        self.embeddings_model = OllamaEmbeddings(model=embeddings)
        self.vector_store = Chroma(
            client=self.db_client,
            embedding_function=self.embeddings_model,
        )
        self.document_chain = create_stuff_documents_chain(self.llm_client, prompt)
        self.retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(search_type='mmr'), self.document_chain
        )
        self.output_parser = JsonOutputParser()


        # self.langfuse_handler = CallbackHandler(
        #     secret_key=langfuse_secret_key,
        #     public_key=langfuse_public_key,
        #     host=f"http://{langfuse_host}:{langfuse_port}" # run on localhost
        # )


    def run(self, user_prompt: str, model_response: str):  # Apply rate limiting
        response = self.retrieval_chain.invoke(
            {
                "input": user_prompt,
                "model_response": model_response,
            }
            # , config={"callbacks": [self.langfuse_handler]}
        )
        logger.info(response)
        result = self.output_parser.parse(response["answer"])
        return result

    async def arun(
        self, user_prompt: str, model_response: str
    ):  # Apply rate limiting before asynchronous call
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