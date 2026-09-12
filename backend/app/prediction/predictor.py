"""
Prediction engine.

Turns raw user text into a sentiment prediction for a given model
(RNN, LSTM or GRU):

    raw text -> clean_text() -> tokenizer.texts_to_sequences()
             -> pad_sequences(maxlen=30) -> model.predict() -> sigmoid probability
"""
import logging
from dataclasses import dataclass

import numpy as np

from app.core.config import settings
from app.core.model_manager import ModelLoadError, model_manager
from app.preprocessing.text_preprocessor import clean_text

logger = logging.getLogger(__name__)


class PredictionError(Exception):
    """Raised for any error that prevents producing a prediction."""


@dataclass
class PredictionResult:
    model: str
    sentiment: str
    probability: float
    confidence: float
    processed_text: str
    model_file: str


def _sentiment_from_probability(probability: float):
    """
    probability >= 0.5 -> Positive, confidence = probability
    probability <  0.5 -> Negative, confidence = 1 - probability
    """
    if probability >= 0.5:
        return "Positive", probability
    return "Negative", 1.0 - probability


def predict(text: str, model_name: str) -> PredictionResult:
    model_name = model_name.lower()

    if not text or not text.strip():
        raise PredictionError("Input text must not be empty.")
    if len(text) > settings.MAX_TEXT_LENGTH:
        raise PredictionError(
            f"Input text exceeds the maximum allowed length of {settings.MAX_TEXT_LENGTH} characters."
        )

    processed_text = clean_text(text)
    if not processed_text:
        raise PredictionError(
            "The text became empty after preprocessing (e.g. it consisted only of "
            "URLs, mentions, punctuation or stopwords). Please provide different text."
        )

    try:
        model = model_manager.get_model(model_name)
        tokenizer = model_manager.get_tokenizer(model_name)
    except ModelLoadError as exc:
        raise PredictionError(str(exc)) from exc

    try:
        from tensorflow.keras.preprocessing.sequence import pad_sequences

        sequence = tokenizer.texts_to_sequences([processed_text])
        padded = pad_sequences(sequence, maxlen=settings.MAX_SEQ_LENGTH)
        raw_output = model.predict(padded, verbose=0)
        probability = float(np.ravel(raw_output)[0])
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed for model=%s", model_name)
        raise PredictionError(f"Inference failed for {model_name.upper()}: {exc}") from exc

    sentiment, confidence = _sentiment_from_probability(probability)

    return PredictionResult(
        model=model_name.upper(),
        sentiment=sentiment,
        probability=round(probability, 4),
        confidence=round(confidence, 4),
        processed_text=processed_text,
        model_file=model_manager.model_file_used(model_name) or "",
    )
