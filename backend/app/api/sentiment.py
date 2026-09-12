"""Sentiment analysis endpoints: /api/sentiment/predict and /compare."""
import logging

from fastapi import APIRouter, HTTPException

from app.prediction.predictor import PredictionError, predict
from app.schemas.sentiment import (
    CompareRequest,
    CompareResponse,
    CompareResultItem,
    PredictRequest,
    PredictResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])

ALL_MODELS = ("rnn", "lstm", "gru")


@router.post("/predict", response_model=PredictResponse)
def predict_sentiment(payload: PredictRequest):
    try:
        result = predict(payload.text, payload.model)
    except PredictionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during prediction")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.") from exc

    return PredictResponse(
        model=result.model,
        sentiment=result.sentiment,
        probability=result.probability,
        confidence=result.confidence,
        processed_text=result.processed_text,
        model_file=result.model_file,
    )


@router.post("/compare", response_model=CompareResponse)
def compare_sentiment(payload: CompareRequest):
    results = []
    for model_name in ALL_MODELS:
        try:
            result = predict(payload.text, model_name)
            results.append(
                CompareResultItem(
                    model=result.model,
                    sentiment=result.sentiment,
                    probability=result.probability,
                    confidence=result.confidence,
                    processed_text=result.processed_text,
                    available=True,
                )
            )
        except PredictionError as exc:
            # Never fabricate a missing result - report unavailability clearly.
            results.append(
                CompareResultItem(
                    model=model_name.upper(),
                    available=False,
                    error=str(exc),
                )
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unexpected error comparing model=%s", model_name)
            results.append(
                CompareResultItem(
                    model=model_name.upper(),
                    available=False,
                    error="Internal server error during prediction.",
                )
            )

    return CompareResponse(text=payload.text, results=results)
