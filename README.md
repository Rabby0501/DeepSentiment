# DeepSentiment

**Text Sentiment Analysis System Based on RNN, LSTM and GRU**

DeepSentiment is a full-stack application for binary (Positive/Negative)
sentiment classification of text, built around three trained recurrent
neural network architectures — SimpleRNN, LSTM and GRU. It provides a
single sentiment-analysis tool, a side-by-side model comparison tool, and
reference pages explaining the methodology and the software itself.

## Features

- Single-text sentiment analysis with model selection (RNN / LSTM / GRU)
- Side-by-side comparison of all three models on the same input
- Consistent preprocessing pipeline (cleaning, stopword removal, stemming)
- Per-model tokenizers, lazy-loaded and cached in memory
- Clear "model unavailable" reporting — never fabricates a missing result
- Methodology and About pages describing the real pipeline, with no
  invented performance claims
- "Liquid Glass" dark UI: translucent cards, backdrop blur, restrained motion
- Fully responsive (desktop, tablet, mobile)
- Dockerized (backend + frontend + Nginx reverse proxy)

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full breakdown.

```
frontend (Vue 3 + Vite + Tailwind)  ──HTTP/JSON──▶  backend (FastAPI)
                                                          │
                                                 ModelManager (lazy cache)
                                                   RNN · LSTM · GRU
```

## Technology stack

| Layer      | Stack |
|------------|-------|
| Frontend   | Vue 3, Vite, Tailwind CSS, Vue Router, Axios, Lucide Vue Next |
| Backend    | Python, FastAPI, Uvicorn, Pydantic |
| ML         | TensorFlow/Keras, NumPy, Pandas, NLTK, scikit-learn |
| Deployment | Docker, Docker Compose, Nginx |

## Project structure

```
DeepSentiment/
├── frontend/         Vue 3 SPA (views, components, router, api service)
├── backend/          FastAPI app (api, core, preprocessing, prediction, schemas)
│   ├── models/        ← place your trained .h5/.keras files here
│   ├── tokenizers/     ← place your .pkl tokenizers here
│   └── embeddings/     ← optional: glove.6B.300d.txt
├── notebooks/        RNN_Level1.ipynb, LSTM_Level2.ipynb, GRU_Level3.ipynb
├── docs/              ARCHITECTURE.md, INSTALLATION.md, USER_MANUAL.md, SOFTWARE_DESCRIPTION.md
└── docker-compose.yml
```

## Required model files

This is an **inference** application — it does not train models. Before
running it, place your own trained assets here:

| File | Location |
|------|----------|
| RNN model | `backend/models/rnn_final_model.h5` |
| LSTM model | `backend/models/lstm_final_model.h5` |
| GRU model | `backend/models/gru_final_model.h5` |
| RNN tokenizer | `backend/tokenizers/tokenizer.pkl` |
| LSTM tokenizer | `backend/tokenizers/tokenizer_lstm.pkl` |
| GRU tokenizer | `backend/tokenizers/tokenizer_gru.pkl` |
| GloVe (optional) | `backend/embeddings/glove.6B.300d.txt` |

`.keras` files are also supported; `.h5` takes priority if both exist for
the same model. Any model without both its model file and tokenizer will
be reported as "unavailable" rather than faked — the app runs fine with
zero, one, two or three models present.

## Installation

Full details in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). Quick version:

### Backend (local)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m nltk.downloader stopwords
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (local)

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### Docker

```bash
docker compose up --build
```

```bash
docker compose down                 # stop
docker compose ps                   # status
docker compose logs backend         # logs
docker compose logs frontend
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/api/system/models` | Availability of RNN/LSTM/GRU models & tokenizers |
| POST | `/api/sentiment/predict` | Predict sentiment for one model |
| POST | `/api/sentiment/compare` | Predict sentiment across all three models |

**Predict example**

```bash
curl -X POST http://localhost:8000/api/sentiment/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I really enjoyed this product!", "model": "lstm"}'
```

**Compare example**

```bash
curl -X POST http://localhost:8000/api/sentiment/compare \
  -H "Content-Type: application/json" \
  -d '{"text": "I really enjoyed this product!"}'
```

## Testing

```bash
cd backend
pip install -r requirements.txt pytest httpx
pytest tests/ -v
```

The suite covers: health/root/system endpoints, empty text, invalid model
name, text that becomes empty after preprocessing, oversized text, and the
no-fabrication guarantee on `/compare` when a model is unavailable.

## Troubleshooting

- **"No model file found for 'X'"** — place the corresponding `.h5`/`.keras`
  file in `backend/models/`.
- **Keras/TensorFlow load errors** — usually a TensorFlow version mismatch
  between training and serving environments; the error message will name
  the underlying exception. Models are loaded with `compile=False` to
  avoid optimizer/loss deserialization issues.
- **CORS errors in the browser** — confirm `ALLOWED_ORIGINS` includes your
  frontend's actual origin (default: `http://localhost:5173`).
- **NLTK `stopwords` LookupError** — run
  `python -m nltk.downloader stopwords`, or let the app auto-download it
  on first request (already handled in `text_preprocessor.py`).

## Notes

- This is an inference-only application; it does not retrain models.
- No accuracy, F1, or other performance metrics are claimed anywhere in
  this project — only report metrics you have actually measured.
- No user text is sent to any third-party AI service; inference runs
  entirely on the backend you control.
