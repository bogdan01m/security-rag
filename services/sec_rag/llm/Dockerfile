FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./llm

EXPOSE 8001

CMD ["uvicorn", "llm.main:app", "--host", "0.0.0.0", "--port", "8001"]