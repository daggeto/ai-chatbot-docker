# Multi-stage build for better caching and smaller final image
ARG BUILDPLATFORM
FROM --platform=$BUILDPLATFORM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only=main

# Production stage
FROM --platform=$BUILDPLATFORM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create directories for models and vector store
RUN mkdir -p /models /app/chroma_db

# Download model if not present (fallback for development)
RUN if [ ! -f /models/mistral-7b-instruct-v0.1.Q4_K_M.gguf ]; then \
    echo "Model file not found, downloading..."; \
    wget -O /models/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
    "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf" || \
    echo "Model download failed, will use fallback responses"; \
    fi

# Copy application code
COPY . .

# Set environment variables
ENV MODEL_PATH=/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
ENV DOCS_PATH=/app/docs
ENV CHROMA_PERSIST_DIR=/app/chroma_db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
