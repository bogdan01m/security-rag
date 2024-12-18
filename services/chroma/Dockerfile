# Stage 1: Build stage
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y curl

# Set the working directory
WORKDIR /app

# Copy the initialization scripts and requirements
COPY init_vector_store.py .
COPY load_data.sh .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV CSV_FILE_PATH=documents.csv
ENV CHROMA_PERSIST_DIRECTORY=llm_service/chroma_vector_store

# Download the CSV file and initialize the vector store
RUN sh load_data.sh && python init_vector_store.py --csv_file_path $CSV_FILE_PATH --persist_directory $CHROMA_PERSIST_DIRECTORY

# Stage 2: Final stage
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

RUN pip install --no-cache-dir chromadb
# Copy the vector store from the build stage
COPY --from=builder /app/${CHROMA_PERSIST_DIRECTORY} /app/${CHROMA_PERSIST_DIRECTORY}
RUN ls /app

# Set environment variables
ENV CHROMA_PERSIST_DIRECTORY=${CHROMA_PERSIST_DIRECTORY}

# Expose the port the Chroma DB runs on
EXPOSE 8000

# Command to run the Chroma DB service
CMD ["chroma", "run",  "--path", "llm_service/chroma_vector_store"]
