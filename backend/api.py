import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import json
from .agent import RAGAgent # Corrected import
from .main import main_async, DocusaurusEmbeddingPipeline # Import main_async for ingestion
from pydantic import BaseModel
from .retrieving import RAGRetriever

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Get frontend URLs from environment variables
FRONTEND_URL_DEV = os.getenv("FRONTEND_URL_DEV", "http://localhost:3000")
FRONTEND_URL_PROD = os.getenv("FRONTEND_URL_PROD", "https://new-hack-final-rag-kvxh.vercel.app")

# Define allowed origins for CORS
origins = [
    FRONTEND_URL_DEV,
    FRONTEND_URL_PROD,
]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_agent: RAGAgent = None
rag_retriever: RAGRetriever = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize the RAGAgent and RAGRetriever on application startup.
    """
    global rag_agent, rag_retriever
    rag_agent = RAGAgent()
    rag_retriever = RAGRetriever()
    logger.info("RAGAgent and RAGRetriever initialized.")

class Question(BaseModel):
    question: str

class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/ask")
async def ask_question(question: Question):
    """
    Receives a question, processes it with the RAGAgent, and returns the answer.
    """
    if not rag_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAGAgent is not initialized. Please wait a moment and try again."
        )
        
    logger.info(f"Received question: {question.question}")
    try:
        # Await the asynchronous query_agent method
        answer = await rag_agent.query_agent(question.question)
        # Return the answer in a JSON response
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing question: {e}")

@app.post("/retrieve")
async def retrieve_information(request: RetrieveRequest):
    """
    Retrieves information using the RAGRetriever based on a query.
    """
    if not rag_retriever:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAGRetriever is not initialized. Please wait a moment and try again."
        )
    logger.info(f"Received retrieval request: {request.query}, top_k: {request.top_k}")
    try:
        results = rag_retriever.retrieve(query_text=request.query, top_k=request.top_k)
        return JSONResponse(content=json.loads(results))
    except Exception as e:
        logger.error(f"Error retrieving information: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving information: {e}")

@app.options("/ask")
async def options_ask():
    return JSONResponse(content={})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)