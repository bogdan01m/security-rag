from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html
from utils import get_base_llm_response,  get_security_rag_response
from services.tg_bot.logger import logger
import json
import traceback
import re
from aiogram.enums.parse_mode import ParseMode

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, о чем поговорим сегодня? ")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        question = message.text.strip()  # Убираем лишние пробелы
        if not question:
            await message.answer("Пожалуйста, задайте вопрос.")
            return

        question = re.sub(r"([*_`\[\]()<>])", r"\\\1", question)  # Экранируем символы, которые могут вызывать ошибку

        user_id = message.from_user.id
        response = await get_base_llm_response(user_id,question)
        logger.info(f"Response from API: {response}")
        

        await message.answer(response['base_llm_response'], parse_mode=ParseMode.HTML) 
        
        rag_response = await get_security_rag_response(user_id, question, response['base_llm_response'])
        logger.info(f"Response from API: {rag_response}")

        rag_response_str = (
            f"prompt_harm_label: {rag_response.get('prompt_harm_label', 'Не указано')}\n"
            f"response_refusal_label: {rag_response.get('response_refusal_label', 'Не указано')}\n"
            f"response_harm_label: {rag_response.get('response_harm_label', 'Не указано')}"
        )

        await message.answer(rag_response_str, parse_mode=ParseMode.MARKDOWN_V2) 

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")


        # Отправка очищенного ответа пользователю
        await message.answer(response['base_llm_response'])

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        logger.error(f"Трассировка стека: {traceback.format_exc()}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")


    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")

