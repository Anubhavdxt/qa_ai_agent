import unittest
from unittest.mock import patch, MagicMock
from agent.content_processor import ContentProcessor, Cache


class TestContentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ContentProcessor()
        self.processor.cache.cache = {}

    @patch("requests.get")
    def test_crawl_and_extract_content(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <p>This is a test document.</p>
                    <a href="/link1">Link 1</a>
                </body>
            </html>
        """
        mock_get.return_value = mock_response

        content, urls = self.processor.crawl_and_extract_content(
            "http://test.com", depth=0
        )
        self.assertIn("This is a test document.", content)
        self.assertIn("http://test.com", urls)

    def test_index_content(self):
        content = "This is a test document.\nAnother line."
        index = self.processor.index_content(content)
        self.assertIn("lines", index)
        self.assertEqual(len(index["lines"]), 2)

    @patch("agent.model_factory.ModelFactory.get_sentence_model")
    def test_encode_content(self, mock_get_sentence_model):
        mock_model = MagicMock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3]]
        mock_get_sentence_model.return_value = mock_model

        index = {"lines": [(0, "This is a test document.")]}
        embeddings, texts = self.processor.encode_content(index)
        self.assertEqual(len(embeddings), 1)
        self.assertEqual(len(texts), 1)


if __name__ == "__main__":
    unittest.main()
