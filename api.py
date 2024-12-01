from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistant import get_rag_assistant, process_url, extract_content

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
        response = rag_assistant.run(payload.question)
        return {"answer": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))