from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_chroma import Chroma
import pickle
import logging
from itertools import chain


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


persist_directory = "llm_service/chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

logger.info('Инициализация нового векторного хранилища')

with open("llm_service/documents.pkl", "rb") as f:
    documents = pickle.load(f)
    documents = [str(doc) for doc in documents if isinstance(doc, (str, float, int)) and doc is not None]
    documents = [doc.strip() for doc in documents if doc.strip()]

text_splitter = CharacterTextSplitter() 
splitted_documents = list(chain.from_iterable(text_splitter.split_text(doc) for doc in documents))

logger.info(f"Количество документов для векторизации: {len(splitted_documents)}")

langchain_documents = [Document(page_content=text) for text in splitted_documents]

vector_store = Chroma(
    collection_name="collection",
    embedding_function=embeddings,
    persist_directory=persist_directory,
)
vector_store.add_documents(langchain_documents)
vector_store.persist()
logger.info("Векторное хранилище успешно создано и сохранено.")