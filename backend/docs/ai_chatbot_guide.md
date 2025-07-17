# AI Chatbot User Guide

## Overview
This AI chatbot is powered by a local Large Language Model (LLM) and uses Retrieval-Augmented Generation (RAG) to provide accurate and contextual responses based on the documentation provided.

## Features
- **Local LLM**: Uses Mistral-7B-Instruct model for natural language generation
- **RAG Integration**: Retrieves relevant context from documentation to enhance responses
- **Conversation Memory**: Maintains conversation history for context-aware interactions
- **Multi-platform Support**: Works on Intel and ARM architectures

## How to Use
1. Send a message to the `/chat` endpoint
2. The system will search for relevant documentation
3. Context is provided to the LLM along with your query
4. You receive a comprehensive response based on both the documentation and the LLM's knowledge

## Best Practices
- Be specific in your questions for better context retrieval
- Ask follow-up questions to dive deeper into topics
- Use clear, concise language for optimal results

## Technical Details
- Model: Mistral-7B-Instruct (quantized GGUF format)
- Embedding Model: all-MiniLM-L6-v2
- Vector Store: ChromaDB
- Context Window: 2048 tokens
