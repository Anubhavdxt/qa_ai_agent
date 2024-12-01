import sys
from assistant import get_rag_assistant, process_url, extract_content


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
        print(response)


if __name__ == "__main__":
    main()
