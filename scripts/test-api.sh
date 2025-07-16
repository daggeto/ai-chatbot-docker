#!/bin/bash


set -e

API_URL="http://localhost:8000"

echo "🧪 Testing AI Chatbot API..."

echo "📡 Testing health endpoint..."
curl -s "$API_URL/health" | jq '.' || echo "Health check failed"

echo ""
echo "💬 Testing chat endpoint..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}' | jq '.' || echo "Chat test failed"

echo ""
echo "📋 Testing root endpoint..."
curl -s "$API_URL/" | jq '.' || echo "Root endpoint test failed"

echo ""
echo "✅ API tests completed!"
