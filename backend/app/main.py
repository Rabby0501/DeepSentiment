"""
DeepSentiment API entrypoint.

Text Sentiment Analysis System Based on RNN, LSTM and GRU.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import sentiment, system
from app.core.config import settings
from app.core.model_manager import model_manager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle.

    Load all ML models and tokenizers once when the API starts.
    """

    logger.info("Starting DeepSentiment API...")

    model_results = model_manager.load_all_models()

    loaded_count = sum(
        1
        for result in model_results.values()
        if result["loaded"]
    )

    logger.info(
        "DeepSentiment startup complete: %d/%d models loaded.",
        loaded_count,
        len(model_results),
    )

    yield

    logger.info("DeepSentiment API shutting down.")


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sentiment.router)
app.include_router(system.router)


@app.get("/")
def root():
    return {
        "name": "DeepSentiment API",
        "description": settings.API_DESCRIPTION,
        "version": settings.API_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    availability = model_manager.availability()

    loaded_models = sum(
        1
        for item in availability.values()
        if item["loaded"]
    )

    total_models = len(availability)

    if loaded_models == total_models:
        status = "ok"
    elif loaded_models > 0:
        status = "degraded"
    else:
        status = "unhealthy"

    return {
        "status": status,
        "models_loaded": loaded_models,
        "models_total": total_models,
    }
