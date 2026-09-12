"""
Application configuration.

All values can be overridden via environment variables (or a .env file
loaded by python-dotenv). Sensible local-development defaults are provided.
"""
import os
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/


def _env_list(name: str, default: List[str]) -> List[str]:
    raw = os.getenv(name)
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    # --- API ---
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_TITLE: str = "DeepSentiment API"
    API_DESCRIPTION: str = "Text Sentiment Analysis System Based on RNN, LSTM and GRU"
    API_VERSION: str = "1.0.0"

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] = _env_list(
        "ALLOWED_ORIGINS",
        ["http://localhost:5173", "http://127.0.0.1:5173"],
    )

    # --- Paths ---
    MODELS_DIR: Path = Path(os.getenv("MODELS_DIR", BASE_DIR / "models"))
    TOKENIZERS_DIR: Path = Path(os.getenv("TOKENIZERS_DIR", BASE_DIR / "tokenizers"))
    EMBEDDINGS_DIR: Path = Path(os.getenv("EMBEDDINGS_DIR", BASE_DIR / "embeddings"))

    # --- Model file names (priority order: .h5 first, then .keras) ---
    MODEL_FILES = {
        "rnn": ["rnn_final_model.h5", "rnn_final_model.keras"],
        "lstm": ["lstm_final_model.h5", "lstm_final_model.keras"],
        "gru": ["gru_final_model.h5", "gru_final_model.keras"],
    }
    TOKENIZER_FILES = {
        "rnn": "tokenizer_rnn.pkl",
        "lstm": "tokenizer_lstm.pkl",
        "gru": "tokenizer_gru.pkl",
    }

    # --- ML pipeline constants (must match training notebooks) ---
    MAX_SEQ_LENGTH: int = int(os.getenv("MAX_SEQ_LENGTH", "30"))
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "300"))
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "5000"))
    GLOVE_FILE: str = os.getenv("GLOVE_FILE", "glove.6B.300d.txt")


settings = Settings()
