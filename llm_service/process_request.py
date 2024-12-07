from fastapi import APIRouter 
from pydantic import BaseModel 
from security_rag import security_rag
import asyncio
from loger import logger
router = APIRouter()

class UserRequest(BaseModel):
    user_id: int
    user_request: str
    base_llm_response: str

@router.post("/process_request/")
async def process_request(data: UserRequest)-> dict:
    user_id = data.user_id
    user_request = data.user_request 
    base_llm_response = data.base_llm_response
    security_rag_response = await security_rag(user_request, base_llm_response)
    logger.info(security_rag_response)
    response = {
        "user_id": user_id,
        "user_request": user_request,
        "base_llm_response": base_llm_response,
        "security_rag_response" : security_rag_response,
    }
    logger.info(response)
    return response