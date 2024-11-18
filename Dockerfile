# syntax=docker/dockerfile:1

# Use a minimal Python image
FROM python:3.11.5-slim

# Disable pyc files and enable immediate logging output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install wget and other system dependencies if necessary
RUN apt-get update && apt-get install -y wget ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy the dependencies and install them
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the script and the application code
COPY . .

# Make the bash script executable
RUN chmod +x download_and_extract_and_run.sh

# Default command to run the script
CMD ["./download_and_extract_and_run.sh"]
