FROM python:3.10-slim

# создаем рабочую папку внутри сервера
WORKDIR /app

# копируем файл рекв
COPY requirements.txt .

# обновляем pip и устанавливаем ревы
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# копируем код проекта
COPY . .

# команда для запуска бота
CMD ["python", "main.py"]