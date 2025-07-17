# AGENT.md

## Project Overview

This project is an AI Chatbot API designed to run in Docker containers, supporting both Intel and Apple Silicon (M1/M2) Mac processors. It provides a simple REST API for chat interactions, integrates a basic Large Language Model (LLM), and includes a Next.js frontend for testing and demonstration purposes. The project is structured for easy local development and multi-architecture deployment.

## AI Model Details

The current backend uses a simple rule-based function to simulate AI responses. This is not a true large language model (LLM), but provides basic chatbot behavior for demonstration and development purposes.

### Current Implementation
- The function `simple_llm_response` in `backend/app/main.py` returns canned responses based on message content (greetings, questions, etc.).
- No real machine learning or LLM inference is performed by default.

### Ready for Real LLM Integration
- The backend includes dependencies for Hugging Face Transformers (`transformers`, `torch`, `accelerate`), so you can easily swap in a real LLM.

### How to Add a Real Model
1. **Install Model Weights**: Make sure your Docker image has enough space and memory for the model you want to use.
2. **Import and Load Model**:
   - In `backend/app/main.py`, import the necessary classes from `transformers` (e.g., `pipeline`, `AutoModelForCausalLM`, `AutoTokenizer`).
   - Load your model and tokenizer at startup (outside the request handler for efficiency).
3. **Replace the Response Function**:
   - Replace the `simple_llm_response` function with a call to your Hugging Face pipeline or model.
   - Example:
     ```python
     from transformers import pipeline
     chat_pipeline = pipeline("text-generation", model="gpt2")
     def real_llm_response(message: str) -> str:
         result = chat_pipeline(message, max_length=100)
         return result[0]["generated_text"]
     ```
   - Update the `/chat` endpoint to use `real_llm_response` instead of `simple_llm_response`.
4. **Test and Tune**:
   - Test the API locally and in Docker to ensure the model loads and responds as expected.
   - Adjust model, tokenizer, and pipeline parameters as needed for your use case.

## Tech Stack

- **Backend**: FastAPI (Python) for serving the REST API and integrating the LLM.
- **Frontend**: Next.js (TypeScript) for the web interface and test client.
- **Containerization**: Docker, with multi-architecture support for both x86_64 and ARM64 platforms.
- **Dependency Management**: Poetry (Python) for backend dependencies, npm for frontend dependencies.

## Key Features

- REST API endpoints for chat and health checks
- Dockerized backend for consistent deployment
- Multi-architecture Docker builds
- Simple LLM integration for AI responses
- Next.js frontend for testing and demonstration

## Directory Structure

- `backend/`: FastAPI application, Dockerfile, and Python dependencies
- `frontend/`: Next.js application and related assets
- `scripts/`: Shell scripts for building, running, and testing the project

## Usage

- Build and run the backend using the provided shell script
- Test the API with `curl` or the provided frontend
- Easily extend or modify the backend and frontend for custom use cases
