#!/bin/bash

set -e

API_URL="http://localhost:8000"

echo "🧪 Testing AI Chatbot API with LLM and RAG..."

echo "📡 Testing health endpoint..."
curl -s "$API_URL/health" | jq '.' || echo "Health check failed"

echo ""
echo "📋 Testing root endpoint..."
curl -s "$API_URL/" | jq '.' || echo "Root endpoint test failed"

echo ""
echo "💬 Testing chat endpoint..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}' | jq '.' || echo "Chat test failed"

echo ""
echo "🤖 Testing AI question..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How does this AI chatbot work?"}' | jq '.' || echo "AI question test failed"

echo ""
echo "📚 Testing RAG functionality..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the deployment options?"}' | jq '.' || echo "RAG test failed"

echo ""
echo "🔧 Testing admin vector store status..."
curl -s "$API_URL/admin/vector-store/status" | jq '.' || echo "Vector store status test failed"

echo ""
echo "📄 Testing document embedding..."
curl -s -X POST "$API_URL/admin/embed-documents" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "This is a test document for the AI chatbot. It contains information about testing the RAG functionality.",
        "metadata": {"source": "test_document.md", "type": "test"}
      }
    ]
  }' | jq '.' || echo "Document embedding test failed"

echo ""
echo "✅ All API tests completed!"
echo "🌐 Visit http://localhost:8000/docs for interactive API documentation"
