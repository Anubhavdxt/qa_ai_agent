# Use an official Python runtime as a parent image
FROM python:3.11.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src /app/src
COPY data /app/data

# Set the PYTHONPATH to include /app/src
ENV PYTHONPATH=/app/src

# Expose port 8000 for the application
EXPOSE 8000

# Default command to run the application
CMD ["sh", "-c", "python src/agent/qa_agent.py --url ${URL:-http://example.com}"]