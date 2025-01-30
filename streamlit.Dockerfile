# Dockerfile - Streamlit
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Streamlit code
COPY streamlitapp /app
# Expose the port Streamlit runs on
EXPOSE 8501

# Command to start the application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
