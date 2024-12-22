import httpx
import asyncio
from config import BASE_LLM_API, LLM_API

async def get_base_llm_response(user_id: int, question: str, retries: int = 3, delay: float = 2.0) -> dict:
    timeout = httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0)  # Тайм-аут для подключения, чтения, записи и пула
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(retries):
            try:
                response = await client.post(BASE_LLM_API, json={"user_id": user_id, "user_request": question})
                response.raise_for_status()  # Проверяем успешность ответа
                return response.json()  # Возвращаем результат, если запрос успешен
            except (httpx.RequestError, httpx.TimeoutException) as e:
                # Логируем ошибку и пробуем снова
                print(f"Попытка {attempt + 1} не удалась: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)  # Задержка перед следующей попыткой
                else:
                    raise  # Повторно выбрасываем исключение после последней попытки


async def get_security_rag_response(user_id: int, question: str, response: str, retries: int = 3, delay: float = 2.0) -> dict:
    timeout = httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=30.0)  # Тайм-аут для подключения, чтения, записи и пула
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(retries):
            try:
                response = await client.post(LLM_API, json={"user_id": user_id, "user_request": question})
                response.raise_for_status()  # Проверяем успешность ответа
                return response.json()  # Возвращаем результат, если запрос успешен
            except (httpx.RequestError, httpx.TimeoutException) as e:
                # Логируем ошибку и пробуем снова
                print(f"Попытка {attempt + 1} не удалась: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)  # Задержка перед следующей попыткой
                else:
                    raise  # Повторно выбрасываем исключение после последней попытки
