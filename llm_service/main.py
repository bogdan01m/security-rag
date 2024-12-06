from fastapi import FastAPI
from process_request import router as request_router

app = FastAPI()

app.include_router(request_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)