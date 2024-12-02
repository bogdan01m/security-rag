from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import polars as pl
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


persist_directory = "llm_service/chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# try:
#     logger.info("Попытка загрузить векторное хранилище")
#     vector_store = Chroma(
#         collection_name="collection",
#         persist_directory=persist_directory,
#         embedding_function=embeddings,
#     )
# except Exception as e:
# logger.error(f"Не удалось загрузить векторное хранилище: {e}")
logger.info('Инициализация нового векторного хранилища')

df = pl.read_csv('llm_service/rag_data.csv')

if 'prompt' not in df.columns or 'threat_type' not in df.columns:
    raise ValueError("CSV-файл должен содержать колонки 'prompt' и 'threat_type'")

# Объединение колонок в текстовые документы
df['document'] = df['prompt'] + " " + df['threat_type']
documents = df['document'].tolist()

text_splitter = CharacterTextSplitter()
splitted_documents = text_splitter.split_text(documents)
logger.info(f"Количество документов для векторизации: {len(splitted_documents)}")

vector_store = Chroma.from_documents(
    documents=splitted_documents,
    collection_name="collection",
    embedding_function=embeddings,
    persist_directory=persist_directory,
)

vector_store.add_documents(splitted_documents)
vector_store.persist()
