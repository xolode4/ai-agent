FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем SSH ключи и настраиваем права
COPY gitlab_key /root/.ssh/id_ed25519
COPY gitlab_key.pub /root/.ssh/id_ed25519.pub
RUN chmod 600 /root/.ssh/id_ed25519 && \
    chmod 644 /root/.ssh/id_ed25519.pub && \
    echo "Host gitlab.home.lcl\n\tStrictHostKeyChecking no\n\tIdentityFile /root/.ssh/id_ed25519" > /root/.ssh/config

# Копируем остальные файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]