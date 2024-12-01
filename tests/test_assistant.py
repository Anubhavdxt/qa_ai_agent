import pytest
from assistant import get_rag_assistant, process_url, extract_content

def test_get_rag_assistant():
    assistant = get_rag_assistant()
    assert assistant is not None

def test_process_url():
    url = "https://help.example.com"
    documents = process_url(url)
    assert len(documents) > 0

def test_extract_content():
    url = "https://help.example.com"
    documents = process_url(url)
    extracted_documents = extract_content(documents)
    assert len(extracted_documents) > 0