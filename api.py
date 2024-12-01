from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from assistant import (
    get_rag_assistant,
    process_url,
    extract_content,
    calculate_confidence,
    is_response_relevant,
)

app = FastAPI()


class Question(BaseModel):
    url: str
    question: str


rag_assistant = get_rag_assistant()


@app.post("/ask")
def ask_question(payload: Question):
    try:
        documents = process_url(payload.url)
        documents = extract_content(documents)
        rag_assistant.knowledge_base.load_documents(documents, upsert=True)
        response = ""
        for delta in rag_assistant.run(payload.question):
            response += delta
        # Check if the response is relevant
        if is_response_relevant(response, documents):
            # Calculate confidence score
            confidence = calculate_confidence(response, documents)
            return {"answer": response, "confidence": f"{confidence * 100:.2f}%"}
        else:
            return {
                "answer": "The provided URL has no information available",
                "confidence": "0.00%",
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
