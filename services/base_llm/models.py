from __future__ import annotations

from typing import Any, Dict, Union
from pydantic import BaseModel

from base_llm.logger import logger


class UserRequest(BaseModel):
    user_id: int
    user_request: str
    

    def as_input(self) -> Dict[str, str]:
        return {
            "user_prompt": self.user_request,
        }



class Base_LLM(BaseModel):
    user_id: int
    base_llm_response: str

    @staticmethod
    def from_response(user_id: int, response: Union[Dict[str, str], Any]) -> Base_LLM:
        # Проверка, что ответ является словарем
        if not isinstance(response, dict):
            logger.warning(f"{user_id=} Not dict")
            return Base_LLM(user_id=user_id, base_llm_response="No valid response from LLM")
        
        # Проверка наличия ключа "answer" в ответе
        if "answer" not in response:
            logger.warning(f"{user_id=} 'answer' key not found in response")
            return Base_LLM(user_id=user_id, base_llm_response="No valid 'answer' in response")

        # Фильтруем только необходимые ключи
        filtered_response = {
            key: value
            for key, value in response.items()
            if key in Base_LLM.__annotations__
        }

        # Логирование отфильтрованного ответа
        logger.debug(f"{user_id=} {filtered_response}")

        # Возвращаем объект с нужным ответом
        return Base_LLM(user_id=user_id, base_llm_response=response["answer"])

