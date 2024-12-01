# Stage 1: Install dependencies
FROM python:3.11-slim AS base

# Set the working directory
WORKDIR /app

# Copy the common requirements file
COPY requirements.txt /app/

# Install dependencies from the requirements file
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# Stage 2: Build API service
FROM base AS api

# Copy API-specific files into the container
COPY . /app/

# Expose the port for FastAPI
EXPOSE 8000

# Command to run the API using uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: Build UI (Streamlit) service
FROM base AS ui

# Copy UI-specific files into the container
COPY . /app/

# Expose the port for Streamlit
EXPOSE 8501

# Command to run Streamlit UI
CMD ["streamlit", "run", "app.py"]

# Stage 4: Build CLI service
FROM base AS cli

# Copy CLI-specific files into the container
COPY . /app/

# Command to run the CLI app
CMD ["python", "qa_agent.py"]