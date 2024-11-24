import unittest
from unittest.mock import patch, MagicMock
from agent.question_answering import QuestionAnswering, DefaultQuestionAnsweringStrategy
import torch


class TestQuestionAnswering(unittest.TestCase):
    @patch("agent.model_factory.ModelFactory.get_sentence_model")
    @patch("agent.model_factory.ModelFactory.get_qa_pipeline")
    def test_process_question(self, mock_get_qa_pipeline, mock_get_sentence_model):
        mock_sentence_model = MagicMock()
        mock_sentence_model.encode.return_value = torch.tensor([[0.1, 0.2, 0.3]])
        mock_get_sentence_model.return_value = mock_sentence_model

        mock_qa_pipeline = MagicMock()
        mock_qa_pipeline.return_value = {"answer": "Test answer", "score": 0.99}
        mock_get_qa_pipeline.return_value = mock_qa_pipeline

        strategy = DefaultQuestionAnsweringStrategy()
        question_answering = QuestionAnswering(strategy=strategy)

        encoded_content = torch.tensor([[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]])
        texts = ["This is a test document.", "This is another test document."]
        urls = ["http://test.com/doc1", "http://test.com/doc2"]

        question = "What is this test document about?"
        expected_answer = (
            "Answer: Test answer\n"
            "Confidence Score: 0.9900\n\n"
            "Source URLs:\n"
            "- http://test.com/doc1\n"
            "- http://test.com/doc2"
        )

        result = question_answering.process_question(
            question, encoded_content, texts, urls
        )
        self.assertEqual(result, expected_answer)

    @patch("agent.model_factory.ModelFactory.get_sentence_model")
    @patch("agent.model_factory.ModelFactory.get_qa_pipeline")
    def test_no_information_found(self, mock_get_qa_pipeline, mock_get_sentence_model):
        mock_sentence_model = MagicMock()
        mock_sentence_model.encode.return_value = torch.tensor([[0.1, 0.2, 0.3]])
        mock_get_sentence_model.return_value = mock_sentence_model

        mock_qa_pipeline = MagicMock()
        mock_qa_pipeline.return_value = {"answer": "", "score": 0.0}
        mock_get_qa_pipeline.return_value = mock_qa_pipeline

        strategy = DefaultQuestionAnsweringStrategy()
        question_answering = QuestionAnswering(strategy=strategy)

        encoded_content = torch.tensor([[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]])
        texts = ["This is a test document.", "This is another test document."]
        urls = ["http://test.com/doc1", "http://test.com/doc2"]

        question = "What is this test document about?"
        expected_answer = (
            "Sorry, I couldn't find any information to answer your question."
        )

        result = question_answering.process_question(
            question, encoded_content, texts, urls
        )
        self.assertEqual(result, expected_answer)


if __name__ == "__main__":
    unittest.main()
