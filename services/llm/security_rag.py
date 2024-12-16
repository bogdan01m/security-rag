import time

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
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
        prompt: str,
        embeddings="sentence-transformers/all-MiniLM-L6-v2",
        api_rate_limit=1.0,  # Calls per second (default: 1 call per second)
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
        )
        logger.info(f"Mistal key: {mistral_api[:10]}")
        self.embeddings_model = HuggingFaceEmbeddings(model_name=embeddings)
        self.vector_store = Chroma(
            client=self.db_client,
            embedding_function=self.embeddings_model,
        )
        self.document_chain = create_stuff_documents_chain(self.llm_client, prompt)
        self.retrieval_chain = create_retrieval_chain(
            self.vector_store.as_retriever(), self.document_chain
        )
        self.output_parser = JsonOutputParser()
        self.api_rate_limit = api_rate_limit
        self.last_api_call = 0  # Timestamp of the last API call

    def _rate_limit(self):
        """
        Ensures API calls adhere to the rate limit.
        """
        current_time = time.time()
        elapsed = current_time - self.last_api_call

        if elapsed < 1.0 / self.api_rate_limit:
            time.sleep(1.0 / self.api_rate_limit - elapsed)

        self.last_api_call = time.time()

    def run(self, user_prompt: str, model_response: str):
        self._rate_limit()  # Apply rate limiting
        response = self.retrieval_chain.invoke(
            {
                "input": user_prompt,
                "model_response": model_response,
            }
        )
        logger.info(response["answer"])
        result = self.output_parser.parse(response["answer"])
        return result

    async def arun(self, user_prompt: str, model_response: str):
        self._rate_limit()  # Apply rate limiting before asynchronous call
        response = await self.retrieval_chain.ainvoke(
            {
                "input": user_prompt,
                "model_response": model_response,
            }
        )
        logger.info(response["answer"])
        result = self.output_parser.parse(response["answer"])
        logger.info(result)
        return result
