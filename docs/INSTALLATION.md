# Installation

## Requirements

- Python 3.11 (recommended)
- Node.js 20 LTS
- npm
- Docker Desktop or Docker Engine (for containerized deployment)
- Git (optional)

## 1. Place your trained ML assets

Before running the app, copy your trained files into these exact locations:

```
backend/models/rnn_final_model.h5
backend/models/lstm_final_model.h5
backend/models/gru_final_model.h5

backend/tokenizers/tokenizer.pkl
backend/tokenizers/tokenizer_lstm.pkl
backend/tokenizers/tokenizer_gru.pkl

backend/embeddings/glove.6B.300d.txt   (optional — only needed if you
                                         re-train; trained models already
                                         contain their embedding weights)
```

`.keras` files are also supported (`rnn_final_model.keras`, etc.) — `.h5`
is preferred if both exist for the same model.

## 2. Backend — local

### Linux / macOS

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m nltk.downloader stopwords
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m nltk.downloader stopwords
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend: http://localhost:8000
Swagger UI: http://localhost:8000/docs

## 3. Frontend — local

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## 4. Docker (both services)

From the project root:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

Rebuild after changes:

```bash
docker compose up --build
```

Check status / logs:

```bash
docker compose ps
docker compose logs backend
docker compose logs frontend
```
