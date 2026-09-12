FROM python:3.11-slim

WORKDIR /app

# Use Tsinghua Debian mirror (works for both Debian sources.list and debian.sources)
RUN sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || true && \
    sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list 2>/dev/null || true

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Use Tsinghua PyPI mirror
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -r requirements.txt

# NLTK download (may fail in China; fallback provided)
RUN python -c "import nltk; nltk.download('stopwords', download_dir='/usr/share/nltk_data')" || \
    echo "WARNING: NLTK download failed. Please mount nltk_data as a volume."

COPY app ./app

# models/tokenizers/embeddings are mounted as volumes at runtime (see
# docker-compose.yml) so the image does not need to bundle large ML assets.
RUN mkdir -p /app/models /app/tokenizers /app/embeddings

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
