from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_chroma import Chroma
import logging
from itertools import chain


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


persist_directory = "llm_service/chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

logger.info('Инициализация нового векторного хранилища')

with open("llm_service/documents.txt") as f:
    text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([text])
logger.info(f"Количество документов для векторизации: {len(texts)}")


vector_store = Chroma(
    collection_name="collection",
    embedding_function=embeddings,
    persist_directory=persist_directory,
)
vector_store.add_documents(texts)
logger.info("Векторное хранилище успешно создано и сохранено.")