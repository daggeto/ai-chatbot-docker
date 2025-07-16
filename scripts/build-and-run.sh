#!/bin/bash


set -e

echo "🚀 Building AI Chatbot Docker image..."

docker build -t ai-chatbot-api:latest ./backend

echo "✅ Docker image built successfully!"

echo "🔄 Stopping any existing containers..."
docker stop ai-chatbot-container 2>/dev/null || true
docker rm ai-chatbot-container 2>/dev/null || true

echo "🚀 Starting AI Chatbot container..."
docker run -d \
  --name ai-chatbot-container \
  -p 8000:8000 \
  --restart unless-stopped \
  ai-chatbot-api:latest

echo "⏳ Waiting for container to start..."
sleep 5

echo "🔍 Checking container status..."
if docker ps | grep -q ai-chatbot-container; then
    echo "✅ Container is running successfully!"
    echo ""
    echo "📡 API is available at: http://localhost:8000"
    echo "🏥 Health check: http://localhost:8000/health"
    echo ""
    echo "📝 Test the API with:"
    echo "curl -X POST http://localhost:8000/chat \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"message\": \"Hello, how are you?\"}'"
    echo ""
    echo "📊 View logs with: docker logs ai-chatbot-container"
    echo "🛑 Stop with: docker stop ai-chatbot-container"
else
    echo "❌ Container failed to start. Check logs with: docker logs ai-chatbot-container"
    exit 1
fi
