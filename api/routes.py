"""
FastAPI Routes
Defines the /chat endpoint
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .service import ChatService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GPTMemory API",
    description="Persistent memory system for ChatGPT",
    version="1.0.0"
)

# Initialize service
chat_service = ChatService()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"


class ChatResponse(BaseModel):
    response: str
    user_id: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GPTMemory API",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    Accepts a message and returns a response with memory
    """
    try:
        logger.info(f"Received message from user {request.user_id}: {request.message}")
        
        # Process message through service
        response = await chat_service.process_message(
            message=request.message,
            user_id=request.user_id
        )
        
        logger.info(f"Generated response for user {request.user_id}")
        
        return ChatResponse(
            response=response,
            user_id=request.user_id
        )
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "GPTMemory API",
        "endpoints": ["/", "/chat", "/health"]
    }