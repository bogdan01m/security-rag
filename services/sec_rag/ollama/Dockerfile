FROM ollama/ollama

COPY ./services/sec_rag/ollama/pull_models.sh /tmp/pull_models.sh

WORKDIR /tmp

RUN chmod +x /tmp/pull_models.sh  

EXPOSE 11435

ENTRYPOINT ["/bin/sh", "/tmp/pull_models.sh"]
