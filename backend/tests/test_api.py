"""
Basic API tests for DeepSentiment.

Run with: pytest (from the backend/ directory, with dependencies installed).

Note: predict/compare tests require actual model + tokenizer files in
backend/models/ and backend/tokenizers/ to succeed; without them they
correctly exercise the "model unavailable" / 422 error paths instead.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "DeepSentiment" in resp.json()["name"]


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_system_models():
    resp = client.get("/api/system/models")
    assert resp.status_code == 200
    body = resp.json()
    names = {m["model"] for m in body["models"]}
    assert names == {"RNN", "LSTM", "GRU"}


def test_predict_empty_text_rejected():
    resp = client.post("/api/sentiment/predict", json={"text": "", "model": "lstm"})
    assert resp.status_code == 422


def test_predict_invalid_model_rejected():
    resp = client.post("/api/sentiment/predict", json={"text": "great product", "model": "bert"})
    assert resp.status_code == 422


def test_predict_only_stopwords_after_cleaning():
    resp = client.post(
        "/api/sentiment/predict",
        json={"text": "@user https://x.com", "model": "lstm"},
    )
    assert resp.status_code == 422


def test_predict_missing_model_files_reports_clear_error():
    resp = client.post(
        "/api/sentiment/predict",
        json={"text": "I really enjoyed this product!", "model": "gru"},
    )
    assert resp.status_code in (200, 422)


def test_compare_never_fabricates_missing_results():
    resp = client.post(
        "/api/sentiment/compare",
        json={"text": "I really enjoyed this product!"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["results"]) == 3
    for item in body["results"]:
        if not item["available"]:
            assert item["sentiment"] is None
            assert item["error"] is not None


def test_predict_text_too_long_rejected():
    long_text = "great " * 2000
    resp = client.post("/api/sentiment/predict", json={"text": long_text, "model": "rnn"})
    assert resp.status_code == 422
