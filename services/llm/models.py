from __future__ import annotations

from typing import Any, Dict, Union
from pydantic import BaseModel

from llm.logger import logger


class UserRequest(BaseModel):
    user_id: int
    user_request: str
    base_llm_response: str

    def as_input(self) -> Dict[str, str]:
        return {
            "user_prompt": self.user_request,
            "model_response": self.base_llm_response,
        }


class RAGResponse(BaseModel):
    user_id: int
    prompt_harm_label: str = "harmful"
    response_refusal_label: str = "harmful"
    response_harm_label: str = "harmful"

    @staticmethod
    def from_response(
        user_id: int, response: Union[Dict[str, str], Any]
    ) -> RAGResponse:
        if not isinstance(response, dict):
            logger.warning(f"{user_id=} Not dict")
            return RAGResponse(user_id=user_id)

        # Filter only required keys
        filtered_response = {
            key: value
            for key, value in response.items()
            if key in RAGResponse.__annotations__
        }
        logger.debug(f"{user_id=} {filtered_response}")

        # Check if all required fields are present and valid
        if all(
            filtered_response.get(key, None) is not None
            for key in list(RAGResponse.__annotations__.keys())[1:]
        ):
            logger.debug(f"{user_id=} Passed test")
            return RAGResponse(user_id=user_id, **filtered_response)

        logger.warning(f"{user_id=} Didn't pass a test")
        return RAGResponse(user_id=user_id)
