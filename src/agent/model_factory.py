import logging
from transformers import pipeline
from sentence_transformers import SentenceTransformer


class ModelFactory:
    """
    Factory class for creating instances of models and pipelines.
    Implements the Singleton pattern to ensure only one instance of each model is created.
    """

    _sentence_model = None
    _qa_pipeline = None

    # Configure logging to suppress warnings about unused weights
    logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

    @staticmethod
    def get_sentence_model():
        """
        Get the singleton instance of the sentence transformer model.
        :return: SentenceTransformer model instance.
        """
        if ModelFactory._sentence_model is None:
            ModelFactory._sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        return ModelFactory._sentence_model

    @staticmethod
    def get_qa_pipeline():
        """
        Get the singleton instance of the question-answering pipeline.
        :return: QA pipeline instance.
        """
        if ModelFactory._qa_pipeline is None:
            ModelFactory._qa_pipeline = pipeline(
                "question-answering",
                model="bert-large-uncased-whole-word-masking-finetuned-squad",
            )
        return ModelFactory._qa_pipeline
