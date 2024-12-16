import os
import requests


from fastapi import HTTPException
from datasets import load_dataset

from langsmith.client import Client

from dotenv import load_dotenv

load_dotenv("testing.env")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
# LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
HF_TOKEN = os.getenv("HF_TOKEN")

DATASET_ID = "ae09090b-b137-4e77-905b-a80314706bcc"
KEYS = ["prompt_harm_label", "response_refusal_label", "response_harm_label"]

# Define the /process_request/ endpoint URL
endpoint_url = (
    "http://localhost:8000/process_request/"  # Replace with the actual endpoint URL
)


def prompt_evaluator(run, example):
    return {
        "name": "prompt",
        "score": int(run.outputs.get(KEYS[0], "ERR") == example.outputs.get(KEYS[0], "ERR_")),
    }


def refusal_evaluator(run, example):
    return {
        "name": "refusal",
        "score": int(run.outputs.get(KEYS[1], "ERR") == example.outputs.get(KEYS[1], "ERR_")),
    }


def response_evaluator(run, example):
    return {
        "name": "response",
        "score": int(run.outputs.get(KEYS[2], "ERR") == example.outputs.get(KEYS[2], "ERR_")),
    }


def call_security_rag(example):
    user_id = 1  # Use the index as a unique user_id
    user_request = example["prompt"]
    base_llm_response = example["response"]

    try:
        # Run the RAG pipeline
        # Send request to /process_request/ endpoint
        response = requests.post(
            endpoint_url,
            json={
                "user_id": user_id,
                "user_request": user_request,
                "base_llm_response": base_llm_response,
            },
            timeout=10,
        )
        response = response.json()

    except HTTPException:
        response = {
            "prompt_harm_label": "ERR",
            "response_refusal_label": "ERR",
            "response_harm_label": "ERR",
        }

    return {k: response[k] for k in KEYS}


def main():
    ls_client = Client(api_key=LANGCHAIN_API_KEY)  # Replace with actual key
    ls_client.evaluate(
        call_security_rag,
        data=DATASET_ID,
        evaluators=[prompt_evaluator, refusal_evaluator, response_evaluator],
        experiment_prefix="SecurityRAGv0.1",
    )


if __name__ == "__main__":
    main()
