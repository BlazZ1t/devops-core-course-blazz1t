FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create persistence directory
RUN mkdir -p /data

# Declare volume
VOLUME ["/data"]

EXPOSE 5000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0"]
CMD ["--port", "5000"]