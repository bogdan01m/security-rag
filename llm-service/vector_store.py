import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

persist_directory = "./chroma_vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

try:
    vector_store = Chroma(
        collection_name="collection",
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
except Exception as e:
    print(f"Не удалось загрузить векторное хранилище: {e}")
    print('инициализация векторного хранилища')
    loader = CSVLoader(file_path='llm-service/sample.csv')
    data = loader.load()

    text_splitter = CharacterTextSplitter()
    documents = text_splitter.split_documents(data)

    vector_store = Chroma(
        collection_name="collection",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )

    vector_store.persist()