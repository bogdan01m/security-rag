from fastapi import FastAPI
from process_prompt import router as prompt_router

app = FastAPI()

app.include_router(prompt_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)