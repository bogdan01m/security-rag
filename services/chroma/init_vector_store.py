import logging

import argparse
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def initialize_vector_store(persist_directory: str):

    
    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

    logger.info("Инициализация нового векторного хранилища")

    try:
        logger.info("Попытка загрузить векторное хранилище")
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings_model,
        )
        logger.info(f"choosen embed model: {embeddings_model}")
        logger.info("Векторное хранилище успешно загружено.")
        return vector_store
    
    except Exception as e:
        logger.error(f"Не удалось загрузить векторное хранилище: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize vector store")
    parser.add_argument(
        "--persist_directory",
        type=str,required=True, 
        help="path to chroma_db"
    )
    args = parser.parse_args()

    initialize_vector_store(args.persist_directory)