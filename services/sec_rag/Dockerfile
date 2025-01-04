FROM python:3.10-slim

WORKDIR /sec_rag

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /sec_rag

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]