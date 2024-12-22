import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the environment variables.")

LLM_HOST = os.getenv("BASE_LLM_HOST", "localhost")  
LLM_PORT = os.getenv("BASE_LLM_PORT", "8000")  
LLM_ENDPOINT = os.getenv("BASE_LLM_ENDPOINT", "/process_request/")  

LLM_API = f"http://{LLM_HOST}:{LLM_PORT}{LLM_ENDPOINT}"


BASE_LLM_HOST = os.getenv("BASE_LLM_HOST", "localhost")  
BASE_LLM_PORT = os.getenv("BASE_LLM_PORT", "8002")  
BASE_LLM_ENDPOINT = os.getenv("BASE_LLM_ENDPOINT", "/process_request/")  

BASE_LLM_API = f"http://{BASE_LLM_HOST}:{BASE_LLM_PORT}{BASE_LLM_ENDPOINT}"
