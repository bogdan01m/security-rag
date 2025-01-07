# Security-RAG: LLM Vulnerability Detection using RAG as Guardrail
<p align="center">
  <a href="https://colab.research.google.com/drive/1IkgCnvOo3xt-TJUDOkKOPAl6XS3xKjtt#scrollTo=K4bDXI3jSCF2b">
    <img src="https://colab.research.google.com/assets/colab-badge.svg">
  </a>
  <a href="https://huggingface.co/datasets/Bogdan01m/wildguardmix-cleaned">
    <img src="https://img.shields.io/badge/🤗-Dataset-orange">
  </a>
  <a href="https://drive.google.com/file/d/1DiZfkkMxhKhJ_gJjjlSo6vBV2e3vBlgi/view?usp=sharing">
    <img src="https://img.shields.io/badge/🗃️-Chroma_DB-green">
  </a>
</p>

**Authors:**
[Bogdan Minko](https://github.com/bogdan01m) ⭐,
[Nikita Zinovich](https://github.com/zeinovich) ⭐,

**security-rag** is a project designed to detect vulnerabilities in Large Language Models (LLMs) by using a Retrieval-Augmented Generation (RAG) approach as a guardrail. The system classifies various aspects of LLM responses to ensure safety, compliance, and ethical behavior.


## Features

- **User Request Harmfulness Classification**: The system analyzes the user input to classify whether the request contains harmful or inappropriate content.
- **LLM Response Classification**: The LLM response is classified to determine if it provides harmful or potentially dangerous information.
- **LLM Refusal Classification**: The system detects whether the LLM refuses to provide harmful content and classifies the nature of this refusal.

## Video Demonstration

<video width="640" height="360" controls>
  <source src="demonstration.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

[link to video](https://drive.google.com/file/d/1BdPGZccXnk5G_v1CMLkSqb9iqhJaxUYf/view?usp=sharing)

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

| Service         | Description                                | URL                                      | Notes                                   |
|------------------|--------------------------------------------|------------------------------------------|-----------------------------------------|
| Chroma DB       | Vector database for RAG                   | http://localhost:8000                   | Uses `CHROMA_PERSIST_DIRECTORY`         |
| LLM API         | API for the main LLM service              | http://localhost:8001/process_request_with_response/ | Requires `MISTRAL_API_KEY`            |
| Base LLM        | Victim model                              | http://localhost:8002/process_request/  | -                                       |
| Telegram Bot    | Telegram bot for interaction              | -                                        | Requires `BOT_TOKEN`                   |
| Ollama          | Hosting embeddings and models             | http://localhost:11434                  | Requires `nomic-embed-text`,  `gemma2:2b`                                      |
| Langfuse        | Monitoring of LLM and Base LLM services   | http://localhost:3000                   | Requires `LANGFUSE_SECRET_KEY` and `LANGFUSE_PUBLIC_KEY` |



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

## 5.0 Run docker compose (CUDA)
If you have nvidia graphic card and ollama is able to use `cuda`
```
docker compose up
```
This will start the full security-rag instance

## 5.1 Run docker compose (CPU)
If you don't have any nvidia-card or just want to run application on RAM with CPU
```
docker compose -f docker-compose-cpu.yml up
```
This will start the full security-rag instance.

## 5.2 Run docker compose base (GPU) (only security-rag with LLM and Chroma)
By default it uses `cuda` 
```
docker compose -f docker-compose-base(gpu).yml up
```
This will start the default security-rag instance.

## Resources
- For running on GPU you will need at least 8GB of RAM and 4GB of VRAM or more
- For running on CPU you will need at least 12 GB of RAM or more

## Testing
After running the application with docker compose, you can test Chroma API, LLM_API (security-rag llm) and BASE_LLM_API
using pytest

go to :
```
cd tests
```
run 
```
pip install requirements.txt
```

after initialize pytest.ini
```
pytest
```




## Evaluation

Test sample : <a href="https://huggingface.co/datasets/allenai/wildguardmix">
  <img src="https://img.shields.io/badge/🤗-Dataset-orange">
</a>

The evaluation showed that Security-RAG (RAG-based approach) outperformed the other models in Response Harm detection when considering the F1-weighted score, establishing a new state-of-the-art for this label, with an F1-weighted score of 89.9%. For Prompt Harm detection, Security-RAG ranked third, after GPT-4 and WILDGUARD, achieving 86.5%. In Refusal Detection, Security-RAG took second place after GPT-4, with an F1 score of 92.0%.

Research part is available in [google collab](https://colab.research.google.com/drive/1IkgCnvOo3xt-TJUDOkKOPAl6XS3xKjtt#scrollTo=K4bDXI3jSCF2b)

for more research information visit [NPL-Course.ODS.Autumn-2024](https://github.com/bogdan01m/NPL-Course.ODS.Autumn-2024) repository.
| **Model**                  | **Prompt Harm (\%)** | **Response Harm (\%)** | **Refusal Detection (\%)** |
|----------------------------|----------------------|------------------------|----------------------------|
| Llama-Guard                | 56.0                 | 50.5                   | 51.4                       |
| Llama-Guard2               | 70.9                 | 66.5                   | 53.8                       |
| Aegis-Guard-D              | 78.5                 | 49.1                   | 41.8                       |
| Aegis-Guard-P              | 71.5                 | 56.4                   | 46.9                       |
| HarmB-Llama                | -                    | 45.7                   | 73.1                       |
| HarmB-Mistral              | -                    | 60.1                   | 58.6                       |
| MD-Judge                   | -                    | 76.8                   | 55.5                       |
| BeaverDam                  | -                    | 63.4                   | 54.1                       |
| LibrAI-LongFormer-harm     | -                    | 62.3                   | 62.3                       |
| LibrAI-LongFormer-ref      | -                    | 63.2                   | 63.2                       |
| Keyword-based              | -                    | 70.1                   | 70.1                       |
| OAI Mod. API               | 12.1                 | 16.9                   | 66.3                       |
| GPT-4                      | 87.9                 | 77.3                   | **92.4**                   |
| WILDGUARD                  | **88.9**             | 75.4                   | 88.6                       |                   |
| **Security-RAG**           | 86.5                 | **89.9**               | **92.0**                   |

