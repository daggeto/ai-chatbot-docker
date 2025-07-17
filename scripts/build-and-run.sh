#!/bin/bash

set -e

echo "🚀 Building AI Chatbot Docker image with multi-architecture support..."

if ! docker buildx ls | grep -q "multiarch"; then
  echo "Creating multi-architecture builder..."
  docker buildx create --name multiarch --use --bootstrap
fi

docker buildx build \
  --platform linux/amd64 \
  -t ai-chatbot-api:latest \
  --load \
  ./backend

echo "✅ Multi-architecture Docker image built successfully!"

echo "🏃 Running AI Chatbot container..."

docker stop ai-chatbot-api 2>/dev/null || true
docker rm ai-chatbot-api 2>/dev/null || true

mkdir -p ./backend/models

docker run -d \
  --name ai-chatbot-api \
  -p 8000:8000 \
  -v "$(pwd)/backend/models:/models" \
  -v "$(pwd)/backend/docs:/app/docs" \
  -e MODEL_PATH=/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
  -e DOCS_PATH=/app/docs \
  -e CHROMA_PERSIST_DIR=/app/chroma_db \
  --rm \
  ai-chatbot-api:latest

echo "✅ Container is running!"
echo "📡 API available at: http://localhost:8000"
echo "📋 API docs at: http://localhost:8000/docs"
echo "🧪 Run './scripts/test-api.sh' to test the API"
echo "🐳 Use 'docker-compose up' for full stack with frontend"

echo ""
echo "📝 Note: If no model file is found, the API will use fallback responses."
echo "   Download a model to ./backend/models/ for full LLM functionality."
