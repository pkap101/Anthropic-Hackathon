import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, List, Literal, Optional
import base64
import httpx

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Query, Form
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field

from service.llm_client import LLMClient
from service.rag import get_retriever
#from service.gradescope import GradescopeService

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Constants
API_KEY = os.getenv("API_KEY")

# FastAPI app initialization
app = FastAPI()
retriever = get_retriever()

# Class Definitions
class GradeRequest(BaseModel):
    question: str
    student_answer: str
    rubric: str

class GradeResponse(BaseModel):
    response: str
    tokens_used: int
    model: str


# Routes
@app.get("/")
async def root():
    return {"message": "welcome", "name": "grader"}


@app.get("/api/")
async def api_root():
    return {"message": "welcome", "name": "grader api"}


@app.get("/api/health")
async def health_check():
    claude_status = "configured" if API_KEY else "not_configured"
    return {
        "service": "Grader API",
        "status": "healthy",
        "version": "1.0.0",
        "claude_status": claude_status,
    }


@app.post("/api/grader", summary="auto grader", response_model=GradeResponse)
#async def grade_question(request: GradeRequest):
async def grade_question(
    question: str = Form(...),
    student_answer: str = Form(...),
    rubric: str = Form(...),
):
    if not API_KEY:
        logger.error("API key not configured")
        raise HTTPException(status_code=500, detail="API key not configured")
    
    logger.info(f"Processing chat request: {question[:50]}...")
    
    llm_client = LLMClient()
    #gradescope_client = GradescopeClient()

    retrieval_query = (
        f"Question: {question}\n"
        f"Student answer: {student_answer}\n"
        f"Rubric: {rubric}"
    )
    context_docs = retriever.get_relevant_documents(retrieval_query)
    context = "\n\n".join(d.page_content for d in context_docs)

    formatted_data = (
        f"Course Context:\n{context}\n\n"
        f"Rubric:\n{rubric}\n\n"
        f"Question:\n{question}\n\n"
        f"Student Answer:\n{student_answer}"
    )

    
    try:        
        result = await llm_client.analyze_question(
            question_data=formatted_data,
        )
        response = PlainTextResponse(content=result.response, media_type="text/plain")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during chat analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
    #finally:
     #   await gradescope_client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
