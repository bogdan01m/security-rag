# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./base_llm

# Expose the port the app runs on
EXPOSE 8002

# Command to run the application
CMD ["uvicorn", "base_llm.main:app", "--host", "0.0.0.0", "--port", "8002"]
