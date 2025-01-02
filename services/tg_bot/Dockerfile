FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./tg_bot

CMD ["python", "tg_bot/bot.py"]
