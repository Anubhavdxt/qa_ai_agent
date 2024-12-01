import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import time
from assistant import get_rag_assistant, process_url, extract_content


class TestPerformance(unittest.TestCase):

    def benchmark_assistant(self):
        url = "https://help.zluri.com"
        question = "What integrations are available?"

        # Process URL
        start_time = time.time()
        documents = process_url(url)
        documents = extract_content(documents)
        processing_time = time.time() - start_time
        print(f"Processing time: {processing_time:.2f} seconds")

        # Get assistant and load documents
        assistant = get_rag_assistant()
        assistant.knowledge_base.load_documents(documents, upsert=True)

        # Query assistant
        start_time = time.time()
        response = ""
        for delta in assistant.run(question):
            response += delta
        query_time = time.time() - start_time
        print(f"Query time: {query_time:.2f} seconds")
        print(f"Response: {response}")

    def test_benchmark(self):
        self.benchmark_assistant()


if __name__ == "__main__":
    unittest.main()
