# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 3001

# Run using Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:3001", "app:app"]
