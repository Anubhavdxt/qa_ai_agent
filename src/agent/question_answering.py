from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
from .model_factory import ModelFactory
from .performance_monitor import PerformanceMonitor

# Default prompt to be added to every question
default_prompt = "Given the following processed documentation, please provide a accurate and as much detailed answer as possible to the question and clearly indicate when the information is not available in the documentation:"


class QuestionAnsweringStrategy:
    """
    Abstract strategy class for question answering.
    """

    def process_question(self, question, encoded_content, texts, urls):
        pass


class DefaultQuestionAnsweringStrategy(QuestionAnsweringStrategy):
    """
    Default strategy for question answering using the provided models.
    """

    def process_question(self, question, encoded_content, texts, urls):
        """
        Process the natural language question and find the relevant content using semantic search.
        :param question: The user's question as a string.
        :param encoded_content: The encoded content.
        :param texts: The original texts corresponding to the encoded content.
        :param urls: The list of URLs corresponding to the texts.
        :return: The answer to the question with a confidence score.
        """
        monitor = PerformanceMonitor()
        monitor.start_timing("total_processing")

        # Encoding step
        monitor.start_timing("encoding")
        question_embedding = ModelFactory.get_sentence_model().encode(
            question, convert_to_tensor=True
        )
        monitor.stop_timing("encoding")

        # Calculate similarity scores
        similarities = util.pytorch_cos_sim(question_embedding, encoded_content)[0]

        # Find the indices of the most similar content
        top_k = min(10, len(texts))  # Increase top k to 10 for more context
        top_k_indices = torch.topk(similarities, k=top_k).indices

        # Combine top k contents for better context
        combined_context = "\n".join([texts[i] for i in top_k_indices])
        combined_urls = [urls[i] for i in top_k_indices]

        if not combined_context:
            monitor.stop_timing("total_processing")
            return "Sorry, I couldn't find any information to answer your question."

        # Prepend the default prompt to the question
        full_question = f"{default_prompt} {question}"

        # QA pipeline step
        monitor.start_timing("qa_pipeline")
        result = ModelFactory.get_qa_pipeline()(
            question=full_question, context=combined_context
        )
        monitor.stop_timing("qa_pipeline")

        answer = result["answer"]
        confidence = result["score"]

        if not answer.strip():
            monitor.stop_timing("total_processing")
            return "Sorry, I couldn't find any information to answer your question."

        # Retrieve the source URLs of the top contexts
        source_urls = "\n".join(f"- {url}" for url in combined_urls)

        monitor.stop_timing("total_processing")

        return f"Answer: {answer}\nConfidence Score: {confidence:.4f}\n\nSource URLs:\n{source_urls}"


class QuestionAnswering:
    """
    Context class that uses a strategy for question answering.
    """

    def __init__(self, strategy=DefaultQuestionAnsweringStrategy()):
        self._strategy = strategy

    def set_strategy(self, strategy):
        """
        Set the strategy for question answering.
        :param strategy: An instance of a class implementing QuestionAnsweringStrategy.
        """
        self._strategy = strategy

    def process_question(self, question, encoded_content, texts, urls):
        """
        Process the question using the current strategy.
        :param question: The user's question.
        :param encoded_content: The encoded content.
        :param texts: The original texts.
        :param urls: The list of URLs.
        :return: The answer to the question with a confidence score.
        """
        return self._strategy.process_question(question, encoded_content, texts, urls)
