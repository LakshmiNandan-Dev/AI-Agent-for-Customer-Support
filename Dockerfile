FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embeddings model to avoid runtime timeout
# This downloads the model during build, so it's cached in the image
RUN python -c "from sentence_transformers import SentenceTransformer; \
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); \
    print('Model downloaded successfully')"

COPY app/ ./app/
COPY frontend/ ./frontend/
COPY data/ ./data/
COPY faiss_index/ ./faiss_index/
COPY .env .env

# Set environment variables for HuggingFace
ENV HF_HOME=/app/.cache/huggingface
ENV HF_HUB_DOWNLOAD_TIMEOUT=300
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV PYTHONUNBUFFERED=1

# Create cache directory
RUN mkdir -p /app/.cache/huggingface

# Expose ports that app listens on
EXPOSE 8000
EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port 8080 --server.address 0.0.0.0"]
