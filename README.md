# AI-powered Question-Answering Agent

This project implements an AI-powered question-answering agent that extracts content from a URL, indexes it, and allows users to ask questions based on the content. The system uses a combination of pre-trained models (e.g. `llama3.2`, `nomic-embed-text`) to process and respond to user queries.

[CLI Demo Video](https://drive.google.com/file/d/1pBg-2wbLPAIk_bWWrzodTJ1GpKtpACB1/view?usp=sharing)
[API Docs](https://drive.google.com/file/d/1noUVGuo2UkQk9gAMsFCcO0VgAnOobOq7/view?usp=sharing)
[UI Demo](https://drive.google.com/file/d/1QIFHCtgngIWolR5Yca7QCShFufD7_hZz/view?usp=sharing)

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [Dependencies](#dependencies)
3. [Usage Examples](#usage-examples)
4. [Design Decisions](#design-decisions)
5. [Known Limitations](#known-limitations)

## Setup Instructions

To run this project locally or in a Docker container, follow the steps below.

### 1. Clone the Repository

Clone the repository to your local machine:

```shell
git clone https://github.com/anubhavdxt/qa_ai_agent.git
cd qa-agent
```

### 1. [Install](https://ollama.com/) ollama and pull models

Pull the LLM you'd like to use:

```shell
ollama pull llama3
```

Pull the Embeddings model:

```shell
ollama pull nomic-embed-text
```

### 2. Create a virtual environment

```shell
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/bin/activate
```

### 3. Install libraries

```shell
pip install -r requirements.txt
```

### 4. Run PgVector

> Install [docker desktop](https://docs.docker.com/desktop/install/mac-install/) first.

- Run using a helper script

```shell
./run_pgvector.sh
```

- OR run using the docker run command

```shell
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

### 5. Run the CLI application

- Run application in CLI:

```shell
python qa_agent.py --url http://help.zluri.com
```

- Run unit tests:

```shell
python -m unittest discover -s src/tests
```

### 6. Run API App

```shell
uvicorn api:app --reload
```

Open [localhost:8000](http://localhost:8000) to view your local RAG app.

### 7. Run UI App

```shell
streamlit run app.py
```

Open [localhost:8501](http://localhost:8501) to view your local RAG app.

## Dependencies

### ollama

Provides integration with Ollama for large language models and embedding models.

### pgvector

Provides PostgreSQL support for vector data types, useful for storing and querying vector embeddings.

### phidata

A framework for data-driven applications, providing utilities for handling data processing, embedding models, and managing AI workflows.

### psycopg

PostgreSQL adapter for Python, used for database interactions with PostgreSQL databases.

### sqlalchemy

SQL toolkit and Object-Relational Mapping (ORM) library for Python, used for managing database schemas and interactions.

### streamlit

Framework for creating web applications in Python, used for building the UI of the application.

### bs4 (BeautifulSoup)

Library for parsing HTML and XML documents, used for extracting data from web pages.

### fastapi

Web framework for building APIs with Python, used for creating RESTful API endpoints.

### uvicorn

ASGI server for serving FastAPI applications, used to run the FastAPI web server.

### docker

(Optional) Tool for containerizing applications, used to create and manage containers for the application if Docker is utilized.

## Usage Examples

### Run the application in CLI

```shell
python src/agent/qa_agent.py --url http://help.zluri.com
```

### Run the application API

```shell
uvicorn api:app --reload
```

Open [localhost:8000](http://localhost:8000) to view your local RAG app.

### Run the application UI

```shell
streamlit run app.py
```

Open [localhost:8501](http://localhost:8501) to view your local RAG app.

## Design Decisions

### 1. Model Choice

- _Llama3.2_ is being used for question-answering and _nomic-embed-text_ for embeddings.
- These models were chosen because they are pre-trained on large datasets and are capable of RAG.

### 2. Modularity

- The application is designed to be modular. Different components such as content processing, question answering, and performance monitoring are separated into individual classes and modules. This promotes maintainability and ease of testing.

### 3. Dockerisation

- Docker is used to containerize the application to ensure that it runs consistently across different environments.
- Docker Compose simplifies managing the application’s dependencies, especially if you need to run the app with multiple services.

### 4. Logging

- Logging has been set up to track the time taken for key steps (encoding, QA processing) and to suppress warnings from unused model weights making the application easier to monitor and debug.

## Known Limitations

### 1. Limited Recursion Depth

- The web scraping functionality has a recursion depth limit to prevent excessive resource usage when crawling deeply nested websites. This can be adjusted by changing the `max_depth` in the `process_url` function of _assistant.py_ file.

### 2. Model Size and Performance

- The Llama3.2 model used for question answering is large and may consume significant resources. If performance is a concern, consider using Llama3.2:1B or running the application on machines with sufficient resources.

### 3. Non-interactive Mode

- The application uses input() for interactive question input, which is not suited for running in detached Docker containers.

### 4. Web Scraping Limitations

- The content extraction relies on BeautifulSoup and works best with well-structured HTML. Some dynamic content generated by JavaScript may not be captured by this method. Future improvements could involve integrating with headless browsers (e.g., Selenium) for more complex web scraping.

### 5. Handling Large Web Pages

- For very large web pages, performance may degrade, especially when dealing with substantial amounts of text. Implementing more advanced techniques, such as extracting content based on section headers, could improve efficiency.
