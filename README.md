# Security-rag

Project for LLM vulnerability detection using RAG as guardrail.

# Usage

## Default Security-rag
get a copy of stable security-rag repository
```
git clone https://github.com/bogdan01m/security-rag.git
```
run docker compose
```
docker compose up
```
This will start the default security-rag instance.

## Self-hosting with [Langfuse](https://langfuse.com/self-hosting/local)

go to services directory (optionaly)
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

## Env settings
Are available in `.env_example`
you should create your own `.env` file with your own settings, based on `.env_example`

services/chroma/chroma.log
services/chroma/chroma_db