"""
FastAPI main application with new RAG pipeline architecture
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from typing import Dict, Any
from dotenv import load_dotenv
from services.pipeline import PipelineService

# Load environment variables
load_dotenv()

app = FastAPI(title="API Playground Backend")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    output: Dict[str, Any]
    max_answers: int = 50  # Default to 50 if not specified

async def log_message(message: str):
    """Helper to format log messages"""
    return f"data: {json.dumps({'type': 'log', 'message': message})}\n\n"

async def log_result(data: Dict[str, Any]):
    """Helper to format result messages"""
    return f"data: {json.dumps({'type': 'result', 'data': data})}\n\n"

@app.post("/fetch")
async def fetch_data(request: QueryRequest):
    """Main endpoint that orchestrates the entire pipeline"""
    
    async def generate():
        try:
            # Initialize pipeline service
            pipeline = PipelineService()
            
            # Process the query with streaming
            result = None
            async for log_message_text in pipeline.process_query_streaming(
                query=request.query,
                schema=request.output,
                num_urls=10,
                max_answers=request.max_answers
            ):
                if isinstance(log_message_text, dict):
                    # This is the final result
                    result = log_message_text
                    yield await log_result(result)
                else:
                    # This is a log message
                    yield await log_message(log_message_text)
                
        except Exception as e:
            yield await log_message(f"Error: {str(e)}")
            yield await log_result({
                "query": request.query,
                "results": [],
                "total_found": 0,
                "error": str(e)
            })
    
    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)