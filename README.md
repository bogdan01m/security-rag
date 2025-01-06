# Security-rag

Project for LLM vulnerability detection using RAG as guardrail.

# System Design
                        +----------------+
                        | Telegram Bot   |
                        | (user request) |
                        +----------------+
                                |
                                | Sends queries
                                v
                      +---------------------+
                      |      Base LLM       |------|
                      +---------------------+      |
                                |                  |
                                | Responses        | 
                                v                  v
                      +---------------------+    +----------------+
                      |       LLM API       |    |    Langfuse    |
                      |   (RAG Pipeline,    |--> |  (Monitoring)  |
                      |   Uses Mistral API) |    +----------------+
                      +---------------------+           
                                ^                       
                                |                       
                      +----------------+                
                      |   Chroma DB    |                
                      | (Vector Store) |                
                      +----------------+                

## Services 

| Service         | Description                                | Host        | Port  |
|------------------|--------------------------------------------|-------------|-------|
| Chroma DB       | Vector database for RAG                   | localhost   | 8000  |
| LLM API         | API for the main LLM service              | localhost   | 8001  |
| Base LLM        | Victim model                              | localhost   | 8002  |
| Telegram Bot    | Telegram bot for interaction              | localhost   | -     |
| Ollama          | Hosting embeddings and models             | localhost   | 11434 |
| Langfuse        | Monitoring of LLM and Base LLM services| localhost   | 3000  |


# How to use

## 1. Get Security-Rag repository
get a copy of security-rag repository
```
git clone https://github.com/bogdan01m/security-rag.git
```

## 2. Configure Ollama
For Linux-based distros: 
1. Make sure that you already got [Ollama](https://ollama.com/) on your local machine and it runs with port: `11434` (Ollama always runs on this port by default)
2. in Ollama you should pull 2 models:
- `nomic-embed-text`
- `gemma2:2b`

For Windows and MacOS it should work like with Linux, but you maybe should configure `.env` file at yourself with Ollama `host` and `port`.
Example of `.env` file is available in `.env_example`

## 3. Chroma vector database
In this project is used chromadb, so you can download this zip file from [google drive](https://drive.google.com/file/d/1DiZfkkMxhKhJ_gJjjlSo6vBV2e3vBlgi/view?usp=sharing)
and `unzip` it .
After you should get folder with name `chroma_db`
Add this folder in `services/sec_rag/chroma/` so dockerfile with chromadb initialization will see that. 
This vector store is created with train sample of [Wildguardmix Dataset](https://huggingface.co/datasets/allenai/wildguardmix) after cleaning from missing values.
Cleaned WildguardMix Dataset is available [here](https://huggingface.co/datasets/Bogdan01m/wildguardmix-cleaned)


Else you can make your own chroma vector database, but you should make sure that it is in the same format as in this project, use `nomic-embed-text` from `ollama embeddings` to create one. 

## 4. Self-hosting integration with [Langfuse](https://langfuse.com/self-hosting/local) (optionaly)

go to services directory of this security-rag project
```
cd services
```


Get a copy of the latest Langfuse repository:

```
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```
Run the langfuse docker compose

```
docker compose up
```

#### WARNING
If you don't wanna use langfuse in your project, then ignore this part, but else you will get langfuse errors (this will not affect on working other services, but you will get logs about langfuse errors).

For removing langfuse errors while running the application just delete langfuse callbacks from `services/sec_rag/llm/security_rag.py` and `services/base_llm/llm.py`



## Env settings
Are available in `.env_example`
you should create your own `.env` file with your own settings, based on example

## 5. Run docker compose (CUDA)
If you have nvidia graphic card and ollama is able to use `cuda`
```
docker compose up
```
This will start the default security-rag instance (without langfuse)

## 5.1 Run docker compose (CPU)
If you don't have any nvidia-card or just wanna run application on RAM with CPU
```
docker compose -f docker-compose-cpu.yml up
```
This will start the default security-rag instance.


## Resources
- For running on GPU you will need at least 8GB of RAM and 4GB of VRAM or more
- For running on CPU you will need at least 12 GB of RAM or more