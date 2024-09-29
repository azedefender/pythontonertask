# Используем образ с python и устанавливаем библиотеку Pillow
FROM python:latest

RUN pip install Pillow

# Копируем код в контейнер
COPY . /app
WORKDIR /app

# Запускаем код при создании контейнера
CMD ["python", "script.py"]
