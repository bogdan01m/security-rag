import os
from dotenv import load_dotenv

from fastapi import APIRouter

from llm.logger import logger
from llm.security_rag import SecurityRAG
from llm.prompt import SECURITY_PROMPT_V1

from llm.models import UserRequest, RAGResponse


load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")

router = APIRouter()

logger.info("Initializing SecurityRAG")
security_rag = SecurityRAG(
    chroma_host=CHROMA_HOST,
    chroma_port=CHROMA_PORT,
    mistral_api=MISTRAL_API_KEY,
    prompt=SECURITY_PROMPT_V1,
)
logger.info("Successfully initialized SecurityRAG")


@router.post("/process_request/")
async def process_request(request: UserRequest) -> RAGResponse:
    user_id = request.user_id
    security_rag_response = await security_rag.arun(**request.as_input())

    return RAGResponse.from_response(user_id, security_rag_response)
