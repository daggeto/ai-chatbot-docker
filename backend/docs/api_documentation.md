# API Documentation

## Endpoints

### GET /
Returns API information and available endpoints.

### GET /health
Health check endpoint for monitoring.

### POST /chat
Main chat endpoint for interacting with the AI.

**Request Body:**
```json
{
  "message": "Your question here",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "response": "AI response with context",
  "conversation_id": "unique-conversation-id",
  "timestamp": 1234567890.123
}
```

### GET /conversations/{conversation_id}
Retrieve conversation history.

### POST /admin/embed-documents
Admin endpoint to embed new documents into the vector store.

**Request Body:**
```json
{
  "documents": [
    {
      "content": "Document content",
      "metadata": {"source": "filename.md"}
    }
  ]
}
```

### GET /admin/vector-store/status
Get status of the vector store including document count.

## Authentication
Admin endpoints require authentication (implementation depends on deployment).

## Rate Limiting
Consider implementing rate limiting for production deployments.
