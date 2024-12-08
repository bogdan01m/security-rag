import logging

import argparse
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def initialize_vector_store(csv_file_path: str, persist_directory: str, debug: bool):
    logger.info("Инициализация нового векторного хранилища")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        show_progress=True,
    )

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=10000,
    #     chunk_overlap=10,
    #     length_function=len,
    #     is_separator_regex=False,
    # )

    loader = CSVLoader(file_path=csv_file_path)
    data = loader.load()

    vector_store = Chroma(
        collection_name="collection",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )

    if debug:
        data = data[:100]
    vector_store.add_documents(data)

    logger.info("Векторное хранилище успешно создано и сохранено.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the vector store.")
    parser.add_argument(
        "--csv_file_path", type=str, required=True, help="Path to the CSV file"
    )
    parser.add_argument(
        "--persist_directory",
        type=str,
        required=True,
        help="Directory to persist the vector store",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        action=argparse.BooleanOptionalAction,
        help="Use only 100 prompts to build DB",
    )

    args = parser.parse_args()

    initialize_vector_store(args.csv_file_path, args.persist_directory, args.debug)
