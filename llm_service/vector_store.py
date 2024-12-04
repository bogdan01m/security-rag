from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


persist_directory = "llm_service/chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

try:
    logger.info("Попытка загрузить векторное хранилище")
    vector_store = Chroma(
        collection_name="collection",
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
except Exception as e:
    logger.error(f"Не удалось загрузить векторное хранилище: {e}")
    logger.info("Сначала нужно запустить init_vector_store.py для инициализации векторного хранилища")
    