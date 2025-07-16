from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import random

app = FastAPI(
    title="AI Chatbot API",
    description="Simple AI chatbot API with basic LLM simulation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: float

class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: float

conversations = {}

def simple_llm_response(message: str) -> str:
    """Simple LLM simulation - returns basic responses"""
    message_lower = message.lower()
    
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        responses = [
            "Hello! How can I help you today?",
            "Hi there! What would you like to chat about?",
            "Hey! I'm here to assist you."
        ]
    elif any(question in message_lower for question in ["how are you", "how do you do"]):
        responses = [
            "I'm doing great, thank you for asking! How are you?",
            "I'm functioning well and ready to help!",
            "I'm excellent! Thanks for checking in."
        ]
    elif any(word in message_lower for word in ["help", "assist", "support"]):
        responses = [
            "I'm here to help! What do you need assistance with?",
            "I'd be happy to assist you. What can I do for you?",
            "Sure, I can help! What would you like to know?"
        ]
    elif any(word in message_lower for word in ["bye", "goodbye", "see you"]):
        responses = [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Bye! Feel free to come back anytime."
        ]
    elif "?" in message:
        responses = [
            "That's an interesting question! Let me think about that.",
            "Great question! Here's what I think about that topic.",
            "I'd be happy to help answer that for you."
        ]
    else:
        responses = [
            "That's interesting! Tell me more about that.",
            "I understand. What else would you like to discuss?",
            "Thanks for sharing that with me. How can I help further?",
            "I see what you mean. What are your thoughts on this?",
            "That's a good point. What would you like to explore next?"
        ]
    
    return random.choice(responses)

@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "conversations": "GET /conversations/{conversation_id}"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "ai-chatbot-api"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    try:
        conversation_id = chat_message.conversation_id or f"conv_{int(time.time())}_{random.randint(1000, 9999)}"
        
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        user_message = {
            "role": "user",
            "content": chat_message.message,
            "timestamp": time.time()
        }
        conversations[conversation_id].append(user_message)
        
        ai_response = simple_llm_response(chat_message.message)
        
        ai_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": time.time()
        }
        conversations[conversation_id].append(ai_message)
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            timestamp=time.time()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
        "message_count": len(conversations[conversation_id])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
