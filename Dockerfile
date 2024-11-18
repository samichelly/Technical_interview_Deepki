# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container (requirements.txt should be at the root of your project)
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (excluding files defined in .dockerignore)
COPY . /app/

# Set the default command to run the main.py script
CMD ["python", "project/__main__.py"]
