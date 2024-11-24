import sys
from agent.content_processor import ContentProcessor
from agent.question_answering import QuestionAnswering
from agent.performance_monitor import PerformanceMonitor
from agent.error_handler import handle_error


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--url":
        print("Usage: python qa_agent.py --url <URL>")
        sys.exit(1)

    url = sys.argv[2]
    content_processor = ContentProcessor()
    question_answering = QuestionAnswering()

    if content_processor.validate_url(url):
        raw_content, urls = content_processor.crawl_and_extract_content(url, depth=0)
        if not raw_content.strip():
            print("No content could be extracted from the URL.")
            sys.exit(1)

        indexed_content = content_processor.index_content(raw_content)
        encoded_content, texts = content_processor.encode_content(indexed_content)
        print("Content successfully extracted, indexed, and encoded.")

        while True:
            print(
                "\nPlease enter your question or type 'exit' or 'quit' to end the session."
            )
            question = input("Your question: ")
            if question.lower() in ["exit", "quit"]:
                break
            answer = question_answering.process_question(
                question, encoded_content, texts, urls
            )
            print(f"\n{answer}")
            PerformanceMonitor().print_timings()
    else:
        raise handle_error("Provided URL is invalid.")


if __name__ == "__main__":
    main()
