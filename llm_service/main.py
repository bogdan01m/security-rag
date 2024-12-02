from fastapi import FastAPI
from process_prompt import prompt
app = FastAPI()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)