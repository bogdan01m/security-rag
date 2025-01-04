import re
import json
import traceback
from aiogram import html
from aiogram.types import Message
from utils import get_base_llm_response, get_security_rag_response
from logger import logger
from aiogram import Dispatcher
from aiogram.filters import CommandStart

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, о чем поговорим сегодня? ")


def sanitize_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = html.quote(text)
    
    return text

@dp.message()
async def echo_handler(message: Message) -> str:
    try:
        question = message.text.strip()
        if not question:
            await message.answer("Пожалуйста, задайте вопрос.")
            return

        # Экранируем специальные символы в вопросе
        question = re.sub(r"([*_`\[\]()<>])", r"\\\1", question)
        user_id = message.from_user.id

        # Получение ответа от базового LLM
        response = await get_base_llm_response(user_id, question)
        base_response = response.get('base_llm_response', '')

        # Санитаризация ответа перед отправкой
        sanitized_base_response = sanitize_html(base_response)
        await message.answer(sanitized_base_response)

        # Получение ответа от RAG-API
        rag_response = await get_security_rag_response(user_id, question, base_response)
        logger.info(f"Ответ от RAG: {rag_response}")

        # Санитаризация JSON-ответа
        sanitized_rag_response = sanitize_html(json.dumps(rag_response, indent=4))
        await message.answer(sanitized_rag_response)
    
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        logger.error(f"Трассировка стека: {traceback.format_exc()}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")