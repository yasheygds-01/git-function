# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Copy requirements first (better cache usage)
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY main.py main.py 

# Run main.py with a sample event by default
CMD ["python", "main.py", "--sample", "--json", "--bucket", 
    "--name", "--metageneration", "--timeCreated", "--updated", 
    "--event-id", "--event-type"]
