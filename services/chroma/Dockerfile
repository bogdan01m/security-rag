FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


ENV CHROMA_PERSIST_DIRECTORY=/app/chroma_db

RUN python init_vector_store.py --persist_directory $CHROMA_PERSIST_DIRECTORY

EXPOSE 8000

CMD ["chroma", "run",  "--path", "/app/chroma_db"]
