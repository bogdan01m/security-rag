FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./sec_rag

EXPOSE 8000

CMD ["uvicorn", "sec_rag.main:app", "--host", "0.0.0.0", "--port", "8000"]