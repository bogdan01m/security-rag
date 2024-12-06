from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from loger import logger
from init_vector_store import initialize_vector_store  



persist_directory = "llm_service/chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def load_vector_store():
    """Загружает векторное хранилище, если оно существует."""
    try:
        logger.info("Попытка загрузить векторное хранилище")
        vector_store = Chroma(
            collection_name="collection",
            persist_directory=persist_directory,
            embedding_function=embeddings,
        )
        logger.info("Векторное хранилище успешно загружено.")
        return vector_store
    except Exception as e:
        logger.error(f"Не удалось загрузить векторное хранилище: {e}")
        return None

# Основная логика
vector_store = load_vector_store()

if vector_store is None:
    logger.info("Векторное хранилище не найдено. Инициализация...")
    vector_store = initialize_vector_store() 

if vector_store is not None:
    logger.info("Векторное хранилище успешно создано и загружено после инициализации.")
else:
    logger.error("Не удалось создать или загрузить векторное хранилище.")