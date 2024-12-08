#!/bin/sh

# Download the CSV file
FILE_ID="1Rqi8m5JPdJ_CYjEE-8BNu-Qgit6iNzz3"
URL="https://drive.google.com/uc?id=$FILE_ID"
LOCAL_FILE="${CSV_FILE_PATH:-documents.csv}"
curl -L "$URL" -o "$LOCAL_FILE"

if [ $? -eq 0 ]; then
  echo "Файл успешно загружен и сохранен как $LOCAL_FILE"
else
  echo "Ошибка при скачивании файла"
  exit 1
fi
