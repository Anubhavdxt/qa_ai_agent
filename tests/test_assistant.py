import unittest
from assistant import (
    process_url,
    extract_content,
    is_response_relevant,
    calculate_confidence,
)
from phi.document import Document


class TestAssistant(unittest.TestCase):

    def test_process_url(self):
        url = "https://help.zluri.com"
        documents = process_url(url)
        self.assertGreater(len(documents), 0)

    def test_extract_content(self):
        documents = [
            Document(
                content="<html><body><h1>Title</h1><p>Paragraph.</p></body></html>"
            )
        ]
        extracted_documents = extract_content(documents)
        self.assertEqual(len(extracted_documents), 1)
        self.assertIn("Title", extracted_documents[0].content)
        self.assertIn("Paragraph", extracted_documents[0].content)

    def test_is_response_relevant(self):
        response = "This is a test response."
        documents = [Document(content="This is a test response.")]
        self.assertTrue(is_response_relevant(response, documents))

        response = "This is not relevant."
        self.assertFalse(is_response_relevant(response, documents))

    def test_calculate_confidence(self):
        response = "This is a test response."
        documents = [Document(content="This is a test response.")]
        confidence = calculate_confidence(response, documents)
        self.assertEqual(confidence, 0.1)


if __name__ == "__main__":
    unittest.main()
