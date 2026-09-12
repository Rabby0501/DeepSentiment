"""
ModelManager

Locates, loads, and caches the trained Keras models and their
corresponding tokenizers.

Models are loaded once during application startup and then reused
from an in-process cache for inference.
"""

import logging
import pickle
import threading
from pathlib import Path
from typing import Dict, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

SUPPORTED_MODELS = ("rnn", "lstm", "gru")


class ModelLoadError(Exception):
    """Raised when a model or tokenizer cannot be located or loaded."""


class ModelManager:
    """
    Thread-safe model/tokenizer manager.

    Models and tokenizers are loaded once during application startup
    and reused for subsequent prediction requests.
    """

    def __init__(self):
        self._models: Dict[str, object] = {}
        self._tokenizers: Dict[str, object] = {}
        self._model_file_used: Dict[str, str] = {}
        self._load_errors: Dict[str, str] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def load_all_models(self) -> Dict[str, dict]:
        """
        Load all supported models and tokenizers.

        This should be called once during FastAPI application startup.
        """
        logger.info("Starting DeepSentiment model initialization...")

        results = {}

        for name in SUPPORTED_MODELS:
            try:
                self.get_model(name)
                self.get_tokenizer(name)

                results[name] = {
                    "loaded": True,
                    "error": None,
                }

                logger.info(
                    "%s model and tokenizer loaded successfully.",
                    name.upper(),
                )

            except ModelLoadError as exc:
                results[name] = {
                    "loaded": False,
                    "error": str(exc),
                }

                logger.error(
                    "Failed to initialize %s: %s",
                    name.upper(),
                    exc,
                )

        loaded_count = sum(
            1 for result in results.values() if result["loaded"]
        )

        logger.info(
            "DeepSentiment model initialization completed: "
            "%d/%d models loaded.",
            loaded_count,
            len(SUPPORTED_MODELS),
        )

        return results

    def availability(self) -> Dict[str, dict]:
        """
        Report model files, tokenizer files and current loading state.
        """
        report = {}

        for name in SUPPORTED_MODELS:
            model_path = self._resolve_model_path(name)
            tokenizer_path = (
                settings.TOKENIZERS_DIR
                / settings.TOKENIZER_FILES[name]
            )

            report[name] = {
                "model": name.upper(),
                "model_file_found": model_path is not None,
                "model_file": str(model_path) if model_path else None,
                "tokenizer_file_found": tokenizer_path.exists(),
                "tokenizer_file": str(tokenizer_path),
                "loaded": name in self._models,
                "error": self._load_errors.get(name),
            }

        return report

    def get_model(self, name: str):
        name = name.lower()
        self._validate_name(name)

        if name in self._models:
            return self._models[name]

        with self._lock:
            if name in self._models:
                return self._models[name]

            return self._load_model(name)

    def get_tokenizer(self, name: str):
        name = name.lower()
        self._validate_name(name)

        if name in self._tokenizers:
            return self._tokenizers[name]

        with self._lock:
            if name in self._tokenizers:
                return self._tokenizers[name]

            return self._load_tokenizer(name)

    def model_file_used(self, name: str) -> Optional[str]:
        return self._model_file_used.get(name.lower())

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _validate_name(self, name: str):
        if name not in SUPPORTED_MODELS:
            raise ModelLoadError(
                f"Unknown model '{name}'. Supported models: "
                f"{', '.join(SUPPORTED_MODELS)}."
            )

    def _resolve_model_path(self, name: str) -> Optional[Path]:
        """
        Deterministic priority: .h5 before .keras.
        """
        for filename in settings.MODEL_FILES[name]:
            candidate = settings.MODELS_DIR / filename

            if candidate.exists():
                return candidate

        return None

    def _load_model(self, name: str):
        model_path = self._resolve_model_path(name)

        if model_path is None:
            candidates = ", ".join(settings.MODEL_FILES[name])

            msg = (
                f"No model file found for '{name.upper()}'. "
                f"Expected one of [{candidates}] inside "
                f"{settings.MODELS_DIR}."
            )

            self._load_errors[name] = msg
            raise ModelLoadError(msg)

        try:
            from tensorflow.keras.models import load_model

            logger.info(
                "Loading %s model from %s",
                name.upper(),
                model_path,
            )

            model = load_model(
                str(model_path),
                compile=False,
            )

        except ImportError as exc:
            msg = (
                "TensorFlow is not installed. "
                "Run: pip install -r requirements.txt"
            )

            self._load_errors[name] = msg
            raise ModelLoadError(msg) from exc

        except Exception as exc:
            msg = (
                f"Failed to load {name.upper()} model from "
                f"{model_path.name}. Original error: {exc}"
            )

            self._load_errors[name] = msg
            logger.exception(msg)

            raise ModelLoadError(msg) from exc

        self._models[name] = model
        self._model_file_used[name] = model_path.name
        self._load_errors.pop(name, None)

        return model

    def _load_tokenizer(self, name: str):
        tokenizer_path = (
            settings.TOKENIZERS_DIR
            / settings.TOKENIZER_FILES[name]
        )

        if not tokenizer_path.exists():
            msg = (
                f"No tokenizer file found for '{name.upper()}'. "
                f"Expected {tokenizer_path}."
            )

            self._load_errors[name] = msg
            raise ModelLoadError(msg)

        try:
            with open(tokenizer_path, "rb") as f:
                tokenizer = pickle.load(f)

        except Exception as exc:
            msg = (
                f"Failed to load tokenizer for {name.upper()} "
                f"from {tokenizer_path.name}: {exc}"
            )

            self._load_errors[name] = msg
            logger.exception(msg)

            raise ModelLoadError(msg) from exc

        self._tokenizers[name] = tokenizer

        return tokenizer


# Singleton instance shared across the application.
model_manager = ModelManager()
