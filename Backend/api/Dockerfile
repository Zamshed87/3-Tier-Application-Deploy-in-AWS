FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make script executable
RUN chmod +x wait-for-queues.sh

ENTRYPOINT ["/app/wait-for-queues.sh"]
CMD ["python", "app.py"]
