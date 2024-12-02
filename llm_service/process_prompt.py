from fastapi import APIRouter 
from pydantic import BaseModel 
from llm_service.prompt_rag import prompt_rag_response
import asyncio
router = APIRouter()

class UserRequest(BaseModel):
    user_id: int
    user_prompt: str

@router.post("/process_prompt/")
async def process_prompt(data: UserRequest)-> dict:
    user_id = data.user_id
    user_prompt = data.llm_answer
    response = prompt_rag_response(user_prompt)
    prompt = {
        "message": "Successfully processed the prompt",
        "user_id": user_id,
        "user_prompt": user_prompt,
        "response" : response,
    }

    return prompt
