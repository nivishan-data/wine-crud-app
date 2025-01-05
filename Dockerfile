# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Create a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app with uvicorn
CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
