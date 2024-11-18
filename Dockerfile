# syntax=docker/dockerfile:1

# Use a minimal Python image
FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install wget, bash and other system dependencies if necessary
RUN apt-get update && \
    apt-get install -y wget ca-certificates bash && \
    rm -rf /var/lib/apt/lists/*

# Copy the dependencies and install them
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the script and the application code
COPY . .

# Ensure the bash script is executable
RUN chmod +x /app/download_and_extract_and_run.sh

# Default command to run the script
CMD ["bash", "/app/download_and_extract_and_run.sh"]
