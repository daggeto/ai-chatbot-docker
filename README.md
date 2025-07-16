# AI Chatbot Docker API

A simple AI chatbot API that can be run in Docker containers, compatible with both Intel and M1/M2 Mac processors.

## Features

- Simple REST API for chat interactions
- Docker containerization with multi-architecture support
- Basic LLM integration
- NextJS test application
- Easy local development setup

## Quick Start

1. Build and run the Docker container:
```bash
./scripts/build-and-run.sh
```

2. Test the API:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

3. Run the test frontend:
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /chat` - Send a message and get AI response
- `GET /health` - Health check endpoint
- `GET /` - API information

## Architecture

- **Backend**: FastAPI with simple LLM integration
- **Frontend**: NextJS with TypeScript
- **Deployment**: Docker with multi-architecture support
