FROM python:3.12-slim

WORKDIR /app

# Install ping and system dependencies
RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "app.py"]
