# AI Chatbot Docker with LLM and RAG

A sophisticated AI chatbot API built with FastAPI, featuring local LLM inference with llama-cpp-python and Retrieval-Augmented Generation (RAG) using ChromaDB. Containerized with Docker and supporting multi-architecture deployment for Intel and ARM processors.

## Features

- **Local LLM Inference**: Uses llama-cpp-python with quantized GGUF models (Mistral-7B-Instruct)
- **RAG Integration**: ChromaDB vector store with sentence-transformers for document retrieval
- **Multi-Architecture Docker**: Supports linux/amd64 and linux/arm64 platforms
- **Document Management**: Admin endpoints for embedding custom documentation
- **Conversation Memory**: Maintains conversation history with context awareness
- **NextJS Frontend**: Modern React-based chat interface
- **Cloud Deployment Ready**: Configurations for Render, Fly.io, and AWS Fargate

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start the full stack (API + Frontend)
docker-compose up --build

# Access the applications
# - API: http://localhost:8000
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/docs
```

### Manual Docker Build

```bash
# Build and run the API only
./scripts/build-and-run.sh

# Test the API
./scripts/test-api.sh
```

## Setup Instructions

### 1. Model Download (Optional)

The Docker container will attempt to download the Mistral-7B-Instruct model automatically. For faster startup, you can pre-download:

```bash
mkdir -p backend/models
cd backend/models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

### 2. Document Embedding

Add your own documentation to the `backend/docs/` directory or use the admin API:

```bash
curl -X POST "http://localhost:8000/admin/embed-documents" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Your document content here...",
        "metadata": {"source": "your_doc.md"}
      }
    ]
  }'
```

### 3. Local Development

```bash
# Backend development
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm run dev
```

## Multi-Architecture Build

Build for multiple platforms:

```bash
# Build for both Intel and ARM
docker buildx build --platform linux/amd64,linux/arm64 -t ai-chatbot-api:latest ./backend

# Build for specific platform
docker buildx build --platform linux/arm64 -t ai-chatbot-api:arm64 ./backend
```

## API Endpoints

### Core Endpoints
- `POST /chat` - Chat with the AI (includes RAG retrieval)
- `GET /conversations/{conversation_id}` - Retrieve conversation history
- `GET /health` - Health check with LLM and vector store status
- `GET /` - API information and features

### Admin Endpoints
- `POST /admin/embed-documents` - Embed new documents into vector store
- `GET /admin/vector-store/status` - Get vector store statistics

### Example Chat Request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I deploy this chatbot?",
    "conversation_id": "optional-id"
  }'
```

## Cloud Deployment

### Render

1. Connect your GitHub repository to Render
2. Use the provided `deploy/render.yaml` configuration
3. Set environment variables for model configuration
4. Deploy with Docker option

### Fly.io

```bash
# Install flyctl and login
fly auth login

# Deploy using provided configuration
fly launch --config deploy/fly.toml
fly deploy
```

### AWS Fargate

See `deploy/aws-fargate.md` for detailed AWS deployment instructions using ECS Fargate and AWS Copilot.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf` | Path to GGUF model file |
| `DOCS_PATH` | `/app/docs` | Path to documentation directory |
| `CHROMA_PERSIST_DIR` | `/app/chroma_db` | ChromaDB persistence directory |
| `MAX_TOKENS` | `512` | Maximum tokens for LLM generation |
| `TEMPERATURE` | `0.7` | LLM temperature setting (0.0-1.0) |

## Architecture

- **Backend**: FastAPI with llama-cpp-python and ChromaDB
- **Frontend**: NextJS with TypeScript
- **LLM**: Mistral-7B-Instruct (quantized GGUF)
- **Vector Store**: ChromaDB with sentence-transformers
- **Deployment**: Multi-architecture Docker with cloud deployment options

## Resource Requirements

- **Memory**: 4GB minimum, 8GB recommended
- **CPU**: 2 cores minimum
- **Storage**: 10GB for model and vector store
- **Platforms**: Linux (amd64/arm64), macOS (Intel/M1/M2)

## Development

The project uses Poetry for Python dependency management and includes a multi-stage Docker build for optimal image size and caching. The RAG system automatically embeds documents from the `backend/docs/` directory on startup.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./scripts/test-api.sh`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
