from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import random
import os
import logging
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Chatbot API",
    description="AI chatbot API with local LLM and RAG capabilities",
    version="2.0.0"
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

class DocumentInput(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class EmbedDocumentsRequest(BaseModel):
    documents: List[DocumentInput]

conversations = {}

class AIService:
    def __init__(self):
        self.llm = None
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self.initialize()
    
    def initialize(self):
        try:
            model_path = os.getenv("MODEL_PATH", "/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
            docs_path = os.getenv("DOCS_PATH", "/app/docs")
            chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR", "/app/chroma_db")
            
            logger.info("Initializing AI service...")
            
            if os.path.exists(model_path):
                logger.info(f"Loading LLM from {model_path}")
                self.llm = Llama(
                    model_path=model_path,
                    n_ctx=2048,
                    n_threads=4,
                    verbose=False
                )
            else:
                logger.warning(f"Model file not found at {model_path}, using fallback responses")
            
            logger.info("Loading embedding model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            logger.info("Initializing ChromaDB...")
            self.chroma_client = chromadb.PersistentClient(
                path=chroma_persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            
            self.collection = self.chroma_client.get_or_create_collection(
                name="docs",
                metadata={"hnsw:space": "cosine"}
            )
            
            if self.collection.count() == 0:
                logger.info("No documents found in vector store, loading initial documents...")
                self._load_initial_documents(docs_path)
            
            logger.info("AI service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing AI service: {e}")
            raise
    
    def _load_initial_documents(self, docs_path: str):
        try:
            docs_dir = Path(docs_path)
            if not docs_dir.exists():
                logger.warning(f"Docs directory {docs_path} not found")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in docs_dir.glob("*.md"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                chunks = self._chunk_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        "source": file_path.name,
                        "chunk_id": i,
                        "file_path": str(file_path)
                    })
                    ids.append(f"{file_path.stem}_{i}")
            
            if documents:
                embeddings = self.embedding_model.encode(documents).tolist()
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
                logger.info(f"Loaded {len(documents)} document chunks into vector store")
        
        except Exception as e:
            logger.error(f"Error loading initial documents: {e}")
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def embed_documents(self, documents: List[DocumentInput]) -> Dict[str, Any]:
        try:
            doc_texts = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(documents):
                chunks = self._chunk_text(doc.content)
                for j, chunk in enumerate(chunks):
                    doc_texts.append(chunk)
                    metadata = doc.metadata or {}
                    metadata.update({"chunk_id": j})
                    metadatas.append(metadata)
                    ids.append(f"doc_{int(time.time())}_{i}_{j}")
            
            if doc_texts:
                embeddings = self.embedding_model.encode(doc_texts).tolist()
                self.collection.add(
                    documents=doc_texts,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
            
            return {
                "status": "success",
                "documents_processed": len(documents),
                "chunks_created": len(doc_texts),
                "total_documents_in_store": self.collection.count()
            }
        
        except Exception as e:
            logger.error(f"Error embedding documents: {e}")
            raise HTTPException(status_code=500, detail=f"Error embedding documents: {str(e)}")
    
    def retrieve_context(self, query: str, n_results: int = 3) -> List[str]:
        try:
            if not self.embedding_model or not self.collection:
                return []
            
            query_embedding = self.embedding_model.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            return results['documents'][0] if results['documents'] else []
        
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def generate_response(self, message: str, context: List[str] = None) -> str:
        try:
            if self.llm and context:
                context_text = "\n".join(context)
                prompt = f"Context: {context_text}\n\nUser: {message}\nAssistant:"
                
                response = self.llm(
                    prompt,
                    max_tokens=512,
                    temperature=0.7,
                    stop=["User:", "\n\n"],
                    echo=False
                )
                
                return response['choices'][0]['text'].strip()
            
            elif self.llm:
                prompt = f"User: {message}\nAssistant:"
                response = self.llm(
                    prompt,
                    max_tokens=512,
                    temperature=0.7,
                    stop=["User:", "\n\n"],
                    echo=False
                )
                
                return response['choices'][0]['text'].strip()
            
            else:
                return self._fallback_response(message)
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(message)
    
    def _fallback_response(self, message: str) -> str:
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
            responses = [
                "Hello! I'm an AI assistant powered by local LLM and RAG. How can I help you today?",
                "Hi there! I can help answer questions using my knowledge base. What would you like to know?",
                "Hey! I'm here to assist you with information from my documentation. What can I help with?"
            ]
        elif any(question in message_lower for question in ["how are you", "how do you do"]):
            responses = [
                "I'm functioning well with my local LLM and vector database! How can I assist you?",
                "I'm doing great! My RAG system is ready to help answer your questions.",
                "I'm excellent! My knowledge base is loaded and ready to help."
            ]
        elif any(word in message_lower for word in ["help", "assist", "support"]):
            responses = [
                "I'm here to help! I can answer questions using my documentation and knowledge base. What do you need assistance with?",
                "I'd be happy to assist you! I use RAG to provide accurate answers from my documentation. What would you like to know?",
                "Sure, I can help! I have access to documentation and can provide detailed answers. What's your question?"
            ]
        elif "?" in message:
            responses = [
                "That's an interesting question! Let me search my knowledge base for relevant information.",
                "Great question! I'll use my RAG system to find the most relevant context to help answer that.",
                "I'd be happy to help answer that! Let me retrieve relevant information from my documentation."
            ]
        else:
            responses = [
                "I understand. I can help provide more information using my knowledge base. What specific aspect would you like to explore?",
                "Thanks for sharing that! I can search my documentation for related information. What would you like to know more about?",
                "That's interesting! I can use my RAG system to find relevant context. What questions do you have about this topic?"
            ]
        
        return random.choice(responses)
    
    def get_vector_store_status(self) -> Dict[str, Any]:
        try:
            return {
                "status": "healthy",
                "document_count": self.collection.count() if self.collection else 0,
                "embedding_model": "all-MiniLM-L6-v2",
                "llm_loaded": self.llm is not None,
                "vector_store": "ChromaDB"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

ai_service = AIService()


@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API with LLM and RAG",
        "version": "2.0.0",
        "features": [
            "Local LLM inference with llama-cpp-python",
            "RAG with ChromaDB and sentence-transformers",
            "Multi-architecture Docker support"
        ],
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "conversations": "GET /conversations/{conversation_id}",
            "admin_embed": "POST /admin/embed-documents",
            "admin_status": "GET /admin/vector-store/status"
        }
    }

@app.get("/health")
async def health_check():
    vector_status = ai_service.get_vector_store_status()
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "ai-chatbot-api",
        "llm_loaded": ai_service.llm is not None,
        "vector_store": vector_status
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
        
        context = ai_service.retrieve_context(chat_message.message)
        ai_response = ai_service.generate_response(chat_message.message, context)
        
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

@app.post("/admin/embed-documents")
async def embed_documents(request: EmbedDocumentsRequest):
    try:
        result = ai_service.embed_documents(request.documents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding documents: {str(e)}")

@app.get("/admin/vector-store/status")
async def get_vector_store_status():
    return ai_service.get_vector_store_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
