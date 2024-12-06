# Security-rag

Project for LLM vulnerability detection using RAG

## Tree
```
RAG_Chatbot_Project/
│
├── docker/                   # Настройки и конфигурации Docker
│   ├── Dockerfile            # Базовый Dockerfile для сервиса
│   ├── docker-compose.yml    # Компоновка контейнеров
│
├── app/                      # Основной код приложения
│   ├── __init__.py
│   ├── main.py               # Точка входа
│   ├── inference/            # Модели и логика чат-ботов
│   │   ├── mistral_client.py # Подключение к Mistral API
│   │   ├── rag_pipeline.py   # Логика RAG
│   │   ├── toxic_filter.py   # Фильтрация токсичных промптов
│   │   └── prompt_classifier.py # Классификатор запросов
│   ├── db/                   # Работа с базой данных
│   │   ├── chromadb_client.py
│   │   └── data_ingestion.py # Векторизация данных
│   ├── monitoring/           # Мониторинг системы
│       └── langfuse_logger.py # Интеграция с Langfuse
│
├── data/                     # Хранилище данных
│   ├── raw/                  # Исходные данные (.parquet)
│   ├── processed/            # Обработанные данные
│
├── notebooks/                # Jupyter Notebooks для анализа и тестирования
│   ├── vectorization.ipynb   # Сценарии векторизации данных
│
├── tests/                    # Тесты
│   ├── test_pipeline.py      # Тесты для RAG
│   └── test_filter.py        # Тесты для фильтрации
│
└── requirements.txt          # Python-зависимости
```

## 
Перед запуском приложения необходимо:
запустить `llm_service/init_vector_store.py` для инициализации векторного хранилища;

Далее можно запустить
`llm_service/main.py` и например через `postman` покидать запросы по адресу : 
`http://localhost:8000/process_prompt/`

Также можно запустить `prompt_rag.py` для проверки в терминале