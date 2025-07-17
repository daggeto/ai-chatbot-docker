# AI Agent Instructions

## Project Overview

This is an advanced AI chatbot API built with FastAPI, featuring local LLM inference with llama-cpp-python and Retrieval-Augmented Generation (RAG) using ChromaDB. The project includes both backend API and frontend NextJS application, containerized with multi-architecture Docker support.

## Current Architecture

- **Backend**: FastAPI with local LLM (Mistral-7B-Instruct) and RAG capabilities
- **Frontend**: NextJS application with TypeScript
- **LLM Engine**: llama-cpp-python with quantized GGUF models
- **Vector Store**: ChromaDB with sentence-transformers embeddings
- **Deployment**: Multi-architecture Docker with cloud deployment options
- **Dependencies**: Poetry for Python package management

## Key Files and Structure

```
ai-chatbot-docker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py          # FastAPI application with LLM and RAG
│   ├── docs/                # Documentation for RAG
│   │   ├── ai_chatbot_guide.md
│   │   ├── deployment_guide.md
│   │   └── api_documentation.md
│   ├── models/              # LLM model files (GGUF format)
│   ├── Dockerfile           # Multi-arch backend container
│   ├── pyproject.toml       # Python dependencies with LLM packages
│   └── poetry.lock
├── frontend/
│   ├── src/app/
│   │   └── page.tsx         # Main chat interface
│   ├── Dockerfile           # Frontend container
│   ├── package.json         # Node.js dependencies
│   └── ...
├── deploy/                  # Cloud deployment configurations
│   ├── render.yaml          # Render deployment
│   ├── fly.toml             # Fly.io deployment
│   └── aws-fargate.md       # AWS Fargate guide
├── scripts/
│   ├── build-and-run.sh     # Multi-arch Docker build and run
│   └── test-api.sh          # Comprehensive API testing
├── docker-compose.yml       # Full stack local development
└── README.md               # Complete setup and usage guide
```

## Current Implementation

### Backend (FastAPI with LLM and RAG)
- **Main file**: `backend/app/main.py`
- **LLM Engine**: llama-cpp-python with Mistral-7B-Instruct GGUF model
- **Vector Store**: ChromaDB with persistent storage
- **Embeddings**: sentence-transformers 'all-MiniLM-L6-v2'
- **RAG Pipeline**: Document chunking, embedding, retrieval, and context injection

### Core Endpoints
- `POST /chat` - Enhanced chat with LLM and RAG retrieval
- `GET /health` - Health check with LLM and vector store status
- `GET /conversations/{id}` - Conversation history
- `GET /` - API info with features list

### Admin Endpoints
- `POST /admin/embed-documents` - Embed new documents into vector store
- `GET /admin/vector-store/status` - Vector store statistics

### AI Service Class
The `AIService` class handles:
- LLM initialization and inference
- ChromaDB vector store management
- Document embedding and chunking
- Context retrieval for RAG
- Fallback responses when LLM unavailable

### Frontend (NextJS)
- **Main file**: `frontend/src/app/page.tsx`
- **Features**: Enhanced chat interface, message history, API integration
- **API URL**: Configured to connect to backend API
- **Docker**: Containerized for production deployment

### Docker Setup
- **Multi-architecture**: Supports linux/amd64 and linux/arm64
- **Base image**: `python:3.11-slim` with build dependencies
- **Model handling**: Automatic download or volume mounting
- **Environment variables**: Configurable paths and settings
- **Health checks**: Comprehensive API and service monitoring

## Development Workflow

### Local Development
```bash
# Full stack with Docker Compose
docker-compose up --build

# Backend only
./scripts/build-and-run.sh

# Test all functionality
./scripts/test-api.sh

# Frontend development
cd frontend && npm install && npm run dev
```

### Model Management
```bash
# Pre-download model for faster startup
mkdir -p backend/models
cd backend/models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

## Dependencies

### Backend
- **Core**: fastapi, uvicorn, pydantic
- **LLM**: llama-cpp-python
- **RAG**: chromadb, sentence-transformers
- **ML**: transformers, torch, accelerate
- **Utilities**: python-multipart

### Frontend
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- React hooks for state management

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf` | Path to GGUF model |
| `DOCS_PATH` | `/app/docs` | Documentation directory |
| `CHROMA_PERSIST_DIR` | `/app/chroma_db` | Vector store persistence |
| `MAX_TOKENS` | `512` | LLM generation limit |
| `TEMPERATURE` | `0.7` | LLM creativity setting |

## RAG Implementation Details

### Document Processing
1. **Chunking**: Text split into 500-word chunks with 50-word overlap
2. **Embedding**: Using sentence-transformers 'all-MiniLM-L6-v2'
3. **Storage**: ChromaDB with cosine similarity search
4. **Retrieval**: Top 3 relevant chunks for context

### Prompt Format
```
Context: <doc_chunk1>
<doc_chunk2>
<doc_chunk3>

User: <user_query>
Assistant:
```

### Fallback Behavior
- If LLM unavailable: Intelligent fallback responses
- If no context found: General LLM response
- Error handling: Graceful degradation

## Instructions for AI Agents

When working on this project:

### Understanding the System
1. **Review the AIService class** in `main.py` for LLM and RAG logic
2. **Check vector store status** via `/admin/vector-store/status`
3. **Test RAG functionality** with document-related queries
4. **Monitor health endpoint** for system status

### Making Changes
1. **Test locally first** using docker-compose or build scripts
2. **Verify LLM responses** are contextually relevant
3. **Check document embedding** works correctly
4. **Test multi-architecture builds** if modifying Docker
5. **Update documentation** when adding features

### Common Tasks

#### Adding New Documents
```bash
# Via filesystem
cp your_docs.md backend/docs/

# Via API
curl -X POST "http://localhost:8000/admin/embed-documents" \
  -H "Content-Type: application/json" \
  -d '{"documents": [{"content": "...", "metadata": {...}}]}'
```

#### Testing RAG Functionality
```bash
# Test document retrieval
curl -X POST "http://localhost:8000/chat" \
  -d '{"message": "What are the deployment options?"}'

# Check vector store
curl "http://localhost:8000/admin/vector-store/status"
```

#### Debugging LLM Issues
1. Check model file exists at `MODEL_PATH`
2. Verify sufficient memory (4GB+ recommended)
3. Monitor logs for initialization errors
4. Test with fallback responses if needed

### Performance Considerations
- **Memory**: LLM requires 4-8GB RAM
- **CPU**: Multi-threading for inference
- **Storage**: Model files ~4GB, vector store grows with documents
- **Startup**: Initial model loading takes 30-60 seconds

### Cloud Deployment
- **Render**: Use provided `deploy/render.yaml`
- **Fly.io**: Use `deploy/fly.toml` configuration
- **AWS**: Follow `deploy/aws-fargate.md` guide
- **Resource requirements**: 4GB+ memory, 2+ CPU cores

## Troubleshooting

### Common Issues
1. **Model not loading**: Check file path and permissions
2. **RAG not working**: Verify ChromaDB initialization
3. **Slow responses**: Check available memory and CPU
4. **Docker build fails**: Ensure buildx is available

### Debugging Commands
```bash
# Check container logs
docker logs ai-chatbot-api

# Test API health
curl http://localhost:8000/health

# Verify vector store
curl http://localhost:8000/admin/vector-store/status

# Test document embedding
./scripts/test-api.sh
```

## Future Enhancements

The project is designed to be extended with:
- **Additional LLM models**: Support for different GGUF models
- **Enhanced RAG**: Hybrid search, reranking, query expansion
- **Authentication**: Admin endpoint security
- **Monitoring**: Metrics and logging integration
- **Scaling**: Kubernetes deployment configurations
- **Fine-tuning**: Custom model training capabilities
