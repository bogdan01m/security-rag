import os
from dotenv import load_dotenv

from fastapi import APIRouter

from logger import logger
from security_rag import SecurityRAG
from prompt import SECURITY_PROMPT_V1

from models import UserRequest, RAGResponse


load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost") 
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11435") 
# LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
# LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
# LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
# LANGFUSE_PORT = os.getenv("LANGFUSE_PORT")

router = APIRouter()

logger.info("Initializing SecurityRAG")
security_rag = SecurityRAG(
    chroma_host=CHROMA_HOST,
    chroma_port=CHROMA_PORT,
    mistral_api=MISTRAL_API_KEY,
    prompt=SECURITY_PROMPT_V1,
    ollama_host=OLLAMA_HOST,
    ollama_port=OLLAMA_PORT,
    # langfuse_secret_key=LANGFUSE_SECRET_KEY,
    # langfuse_public_key=LANGFUSE_PUBLIC_KEY,
    # langfuse_host=LANGFUSE_HOST,
    # langfuse_port=LANGFUSE_PORT
)
logger.info("Successfully initialized SecurityRAG")


@router.post("/process_request_with_response/")
async def process_request(request: UserRequest) -> RAGResponse:
    user_id = request.user_id
    security_rag_response = await security_rag.arun(**request.as_input())

    return RAGResponse.from_response(user_id, security_rag_response)
