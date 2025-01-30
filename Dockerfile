# Dockerfile - Backend
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the backend code
COPY . .

# Set the Python path to your FastAPI app (you can use PYTHONPATH environment variable)
ENV PYTHONPATH=/app/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
