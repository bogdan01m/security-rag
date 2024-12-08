from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_vector_store():

    logger.info('Инициализация нового векторного хранилища')
    persist_directory = "llm_service/chroma_vector_store"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    file_path = "documents.csv"


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=10,
        length_function=len,
        is_separator_regex=False,
    )


    loader = CSVLoader(file_path=file_path)
    data = loader.load()


    vector_store = Chroma(
        collection_name="collection",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(data)
    logger.info("Векторное хранилище успешно создано и сохранено.")