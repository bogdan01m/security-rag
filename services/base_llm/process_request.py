import os
from dotenv import load_dotenv
from fastapi import APIRouter
from base_llm.logger import logger
from base_llm.llm import get_llm_response
from base_llm.models import UserRequest, Base_LLM


load_dotenv()
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
LANGFUSE_PORT = os.getenv("LANGFUSE_PORT")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost") 
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434") 

router = APIRouter()

@router.post("/process_request/")
async def process_request(request: UserRequest) -> Base_LLM:
    user_id = request.user_id
    try:
        base_llm_response = await get_llm_response(prompt=request.user_request, 
                                                   langfuse_secret_key=LANGFUSE_SECRET_KEY,
                                                   langfuse_public_key=LANGFUSE_PUBLIC_KEY,
                                                   langfuse_host=LANGFUSE_HOST,
                                                   langfuse_port=LANGFUSE_PORT,
                                                   ollama_host=OLLAMA_HOST,
                                                   ollama_port=OLLAMA_PORT
                                                  )
        logger.info(f"Raw LLM Response: {base_llm_response}")
        
        return Base_LLM.from_response(user_id, base_llm_response)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return Base_LLM(user_id=user_id, base_llm_response="Извините, но я не могу обработать ваш запрос")