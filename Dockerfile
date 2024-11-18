# syntax=docker/dockerfile:1

# Base image with the desired Python version
FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/project:$PYTHONPATH"

# Set working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Create necessary directories with proper permissions
RUN mkdir -p /app/html_files && chmod 775 /app/html_files

# Copy the application code
COPY . .

# Ensure the bash script is executable
RUN chmod +x download_and_extract_and_run.sh

# Set default command
CMD ["./download_and_extract_and_run.sh"]
