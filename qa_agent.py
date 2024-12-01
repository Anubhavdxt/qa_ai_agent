import sys
from assistant import (
    get_rag_assistant,
    process_url,
    extract_content,
    is_response_relevant,
    calculate_confidence,
)


def main():
    if len(sys.argv) < 3:
        print("Usage: python qa_agent.py --url <URL>")
        sys.exit(1)

    if sys.argv[1] != "--url":
        print("Usage: python qa_agent.py --url <URL>")
        sys.exit(1)

    url = sys.argv[2]

    try:
        documents = process_url(url)
        documents = extract_content(documents)
    except ValueError as e:
        print(e)
        sys.exit(1)

    rag_assistant = get_rag_assistant()
    rag_assistant.knowledge_base.load_documents(documents, upsert=True)

    print("You can now ask questions. Type 'exit' or 'quit' to stop.")

    while True:
        question = input("> ")
        if question.lower() in ["exit", "quit"]:
            break
        response = ""
        for delta in rag_assistant.run(question):
            response += delta
        # Check if the response is relevant
        if is_response_relevant(response, documents):
            # Calculate confidence score
            confidence = calculate_confidence(response, documents)
            print(f"Answer: {response}")
            print(f"Confidence: {confidence * 100:.2f}%")
        else:
            print("The provided URL has no information available for this.")


if __name__ == "__main__":
    main()
