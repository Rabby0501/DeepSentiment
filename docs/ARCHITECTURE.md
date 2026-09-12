# Architecture

## Overview

DeepSentiment is a two-tier application:

```
┌─────────────────┐      HTTP / JSON       ┌──────────────────┐
│   Vue 3 SPA      │ ─────────────────────▶ │   FastAPI backend │
│   (frontend)     │ ◀───────────────────── │   (backend)        │
└─────────────────┘                        └──────────────────┘
                                                     │
                                                     ▼
                                    ┌───────────────────────────────┐
                                    │ ModelManager (lazy load/cache) │
                                    │  RNN │ LSTM │ GRU + tokenizers │
                                    └───────────────────────────────┘
```

## Backend layout

```
backend/app/
├── main.py                 FastAPI app, CORS, route registration
├── api/
│   ├── sentiment.py        POST /api/sentiment/predict, /compare
│   └── system.py           GET  /api/system/models
├── core/
│   ├── config.py           Environment-driven settings
│   └── model_manager.py    Lazy-loading, in-memory model/tokenizer cache
├── preprocessing/
│   └── text_preprocessor.py  Cleaning + stemming pipeline
├── prediction/
│   └── predictor.py        Orchestrates preprocess → tokenize → pad → predict
└── schemas/
    └── sentiment.py        Pydantic request/response models
```

## Request flow (single prediction)

1. Frontend sends `POST /api/sentiment/predict` with `{ text, model }`.
2. `predictor.predict()` validates the text and runs `clean_text()`.
3. `ModelManager` loads (or reuses a cached) Keras model + tokenizer for
   the requested architecture.
4. The cleaned text is tokenized and padded to `MAX_SEQ_LENGTH=30`.
5. The model outputs a sigmoid probability; it is mapped to
   Positive/Negative with a confidence score.
6. The result is returned as JSON and rendered by `PredictionResult.vue`.

## Model loading strategy

Models and tokenizers are **not** loaded at server startup and **not**
reloaded on every request. `ModelManager` loads each model lazily on its
first use and caches it in memory for the lifetime of the process, guarded
by a lock for thread safety. `.h5` files are preferred over `.keras` files
when both exist, in a deterministic, documented order.

## Frontend layout

```
frontend/src/
├── views/              One component per route (Dashboard, SentimentAnalysis, ...)
├── components/
│   ├── layout/          Navbar, Footer
│   ├── sentiment/       ModelSelector, PredictionResult
│   ├── comparison/      ComparisonCard
│   ├── dashboard/       ModelCard
│   └── ui/               GlassCard, StatCard, LoadingState, ErrorMessage
├── services/api.js      Single Axios instance; all HTTP calls go through here
└── router/index.js      Vue Router route table
```

## Deployment

Docker Compose runs two services: `backend` (FastAPI on 8000) and
`frontend` (static Vue build served by Nginx on 5173, proxying `/api/` to
`backend:8000`). Model, tokenizer and embedding files are mounted as
volumes so they can be swapped without rebuilding images.
