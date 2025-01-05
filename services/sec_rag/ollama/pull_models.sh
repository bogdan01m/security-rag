#!/bin/bash

# Start Ollama in the background, binding it to localhost:11435
ollama serve
# Record Process ID.
pid=$!

HOST=$1
PORT=$2

echo "Starting Ollama with port $PORT"
# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieving model nomic-embed-text..."
ollama pull nomic-embed-text:latest
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
