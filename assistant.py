from typing import Optional, List

from phi.assistant import Assistant
from phi.document import Document
from phi.document.reader.website import WebsiteReader
from phi.knowledge import AssistantKnowledge
from phi.llm.ollama import Ollama
from phi.embedder.ollama import OllamaEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


def calculate_confidence(response: str, documents: List[Document]) -> float:
    """Calculate confidence score based on the similarity of the response to the documents"""
    if not response or not documents:
        return 0.0

    # Simple confidence based on the number of relevant documents retrieved
    relevant_docs_count = len(documents)
    return min(
        1.0, relevant_docs_count / 10.0
    )  # Max confidence score 1.0 for high relevance


def is_response_relevant(response: str, documents: List[Document]) -> bool:
    """Check if the response contains not available string"""
    not_available_str = "The provided URL has no information available"
    if not_available_str in response:
        return False
    return True


def get_rag_assistant(
    llm_model: str = "llama3.2",
    embeddings_model: str = "nomic-embed-text",
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = False,
    db_url: str = db_url,
) -> Assistant:
    """Get a Local RAG Assistant with confidence scoring."""

    # Define the embedder based on the embeddings model
    embedder = OllamaEmbedder(model=embeddings_model, dimensions=4096)
    embeddings_model_clean = embeddings_model.replace("-", "_")
    if embeddings_model == "nomic-embed-text":
        embedder = OllamaEmbedder(model=embeddings_model, dimensions=768)
    elif embeddings_model == "phi3":
        embedder = OllamaEmbedder(model=embeddings_model, dimensions=3072)
    # Define the knowledge base
    knowledge = AssistantKnowledge(
        vector_db=PgVector2(
            db_url=db_url,
            collection=f"local_rag_documents_{embeddings_model_clean}",
            embedder=embedder,
        ),
        # 3 references are added to the prompt
        num_documents=3,
    )

    return Assistant(
        name="local_rag_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=Ollama(model=llm_model),
        storage=PgAssistantStorage(table_name="local_rag_assistant", db_url=db_url),
        knowledge_base=knowledge,
        description="You are a help website QA AI agent and your task is to answer questions using the provided information",
        instructions=[
            "When a user asks a question, you will be provided with information about the question.",
            "Carefully read this information and provide a clear and concise answer to the user.",
            "Include the source URL for your answers when possible.",
            "Clearly indicate when information is not available in the provided context.",
            "If the information is not in the provided context, answer with 'The provided URL has no information available for this.'",
            "Do not include information from the internet for answers.",
        ],
        # Uncomment this setting adds chat history to the messages
        # add_chat_history_to_messages=True,
        # Uncomment this setting to customize the number of previous messages added from the chat history
        # num_history_messages=3,
        # This setting adds references from the knowledge_base to the user prompt
        add_references_to_prompt=True,
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )


def process_url(url: str) -> List[Document]:
    try:
        scraper = WebsiteReader(
            max_links=10, max_depth=3
        )  # Adjust max_links and max_depth as needed
        web_documents = scraper.read(url)
        if not web_documents:
            raise ValueError("No documents found at the provided URL.")
        return web_documents
    except Exception as e:
        raise ValueError(f"Error processing URL: {e}")


def extract_content(documents: List[Document]) -> List[Document]:
    processed_documents = []
    for doc in documents:
        # Implement content extraction logic here
        # Filter out navigation elements, headers, footers
        # Maintain context hierarchy
        processed_documents.append(doc)
    return processed_documents
