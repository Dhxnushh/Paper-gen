"""
FastAPI server for research paper generation system.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import os
import uuid
from datetime import datetime
from workflow import PaperWorkflow
from latex_converter import LaTeXConverter


app = FastAPI(
    title="Research Paper Generator API",
    description="AI-powered research paper generation with evaluation and LaTeX conversion",
    version="2.0.0"
)

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PaperRequest(BaseModel):
    """Request model for paper generation."""
    title: str
    sections: List[str]
    feedback: Optional[str] = ""
    threshold: Optional[int] = 32
    max_iterations: Optional[int] = 3


class JobResponse(BaseModel):
    """Response model for job creation."""
    job_id: str
    message: str
    status: str


class StatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: Optional[str] = None
    final_score: Optional[int] = None
    iterations: Optional[int] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


# Store jobs and their status
jobs: Dict[str, Dict] = {}

# Store the latest generated paper data (for backward compatibility)
latest_paper = {
    "json": None,
    "latex": None
}


def generate_paper_task(job_id: str, request: PaperRequest):
    """
    Background task to generate paper.
    
    Args:
        job_id: Unique job identifier
        request: Paper generation request
    """
    try:
        # Update status to processing
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = "Generating paper content..."
        
        print(f"\n{'='*80}")
        print(f"Job {job_id}: Starting paper generation")
        print(f"Title: {request.title}")
        print(f"Sections: {', '.join(request.sections)}")
        print(f"{'='*80}\n")
        
        # Initialize workflow
        workflow = PaperWorkflow()
        
        # Prepare input data as expected by workflow
        input_data = {
            "title": request.title,
            "sections": request.sections,
            "feedback": request.feedback or ""
        }
        
        # Run the workflow
        result = workflow.run_workflow(
            input_data=input_data
        )
        
        # Generate LaTeX
        jobs[job_id]["progress"] = "Converting to LaTeX..."
        latex_converter = LaTeXConverter()
        latex_content = latex_converter.generate_latex(
            result['title'],
            result['sections']
        )
        
        # Store results
        jobs[job_id]["json"] = result
        jobs[job_id]["latex"] = latex_content
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["final_score"] = result.get('total_score', 0)
        jobs[job_id]["iterations"] = result.get('iterations', 0)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
        # Also update latest_paper for backward compatibility
        latest_paper["json"] = result
        latest_paper["latex"] = latex_content
        
        # Save to files
        with open(f'output_paper_{job_id}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        latex_converter.save_latex(latex_content, f'output_paper_{job_id}.tex')
        
        print(f"\n{'='*80}")
        print(f"Job {job_id}: Paper generation complete")
        print(f"Final Score: {result.get('total_score', 0)}/{result.get('threshold_met', 'N/A')}")
        print(f"Iterations: {result.get('iterations', 0)}")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ Job {job_id} Error: {str(e)}\n")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Research Paper Generator API v2.0",
        "endpoints": {
            "/generate": "POST - Start paper generation (returns job_id)",
            "/status/{job_id}": "GET - Check generation status",
            "/paper/{job_id}/json": "GET - Get generated paper in JSON",
            "/paper/{job_id}/latex": "GET - Get generated paper in LaTeX",
            "/jobs": "GET - List all jobs",
            "/paper/json": "GET - Get latest paper in JSON (legacy)",
            "/paper/latex": "GET - Get latest paper in LaTeX (legacy)"
        },
        "workflow": {
            "1": "POST /generate with title and sections → Get job_id",
            "2": "Poll GET /status/{job_id} until status is 'completed'",
            "3": "GET /paper/{job_id}/json or /paper/{job_id}/latex"
        }
    }


@app.post("/generate", response_model=JobResponse)
def generate_paper(request: PaperRequest, background_tasks: BackgroundTasks):
    """
    Start paper generation in the background.
    Returns immediately with a job_id to track progress.
    
    Args:
        request: PaperRequest containing title, sections, and optional parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        JobResponse with job_id for tracking
    """
    # Generate unique job ID
    job_id = str(uuid.uuid4())[:8]
    
    # Initialize job record
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": "Job queued",
        "request": request.dict(),
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "json": None,
        "latex": None,
        "final_score": None,
        "iterations": None,
        "error": None
    }
    
    # Add background task
    background_tasks.add_task(generate_paper_task, job_id, request)
    
    print(f"\n{'='*80}")
    print(f"Created job {job_id} for paper generation")
    print(f"Title: {request.title}")
    print(f"{'='*80}\n")
    
    return JobResponse(
        job_id=job_id,
        message=f"Paper generation started. Use job_id '{job_id}' to check status.",
        status="pending"
    )


@app.get("/status/{job_id}", response_model=StatusResponse)
def get_job_status(job_id: str):
    """
    Check the status of a paper generation job.
    
    Args:
        job_id: Job identifier
        
    Returns:
        StatusResponse with current job status
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job = jobs[job_id]
    
    return StatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job.get("progress"),
        final_score=job.get("final_score"),
        iterations=job.get("iterations"),
        error=job.get("error"),
        created_at=job["created_at"],
        completed_at=job.get("completed_at")
    )


@app.get("/jobs")
def list_jobs():
    """
    List all jobs with their current status.
    
    Returns:
        Dictionary of all jobs
    """
    return {
        "total_jobs": len(jobs),
        "jobs": {
            job_id: {
                "status": job["status"],
                "title": job["request"]["title"],
                "created_at": job["created_at"],
                "completed_at": job.get("completed_at")
            }
            for job_id, job in jobs.items()
        }
    }


@app.get("/paper/{job_id}/json")
def get_paper_json_by_id(job_id: str):
    """
    Get the generated paper in JSON format for a specific job.
    
    Args:
        job_id: Job identifier
        
    Returns:
        JSONResponse with the complete paper data
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job {job_id} is not completed yet. Current status: {job['status']}"
        )
    
    if job["json"] is None:
        raise HTTPException(
            status_code=500,
            detail=f"Paper data not available for job {job_id}"
        )
    
    return JSONResponse(content=job["json"])


@app.get("/paper/{job_id}/latex", response_class=PlainTextResponse)
def get_paper_latex_by_id(job_id: str):
    """
    Get the generated paper in LaTeX format for a specific job.
    
    Args:
        job_id: Job identifier
        
    Returns:
        Plain text response with LaTeX content
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job {job_id} is not completed yet. Current status: {job['status']}"
        )
    
    if job["latex"] is None:
        raise HTTPException(
            status_code=500,
            detail=f"LaTeX data not available for job {job_id}"
        )
    
    return PlainTextResponse(content=job["latex"])


@app.get("/paper/json")
def get_paper_json():
    """
    Get the generated paper in JSON format.
    
    Returns:
        JSONResponse with the complete paper data
    """
    if latest_paper["json"] is None:
        raise HTTPException(
            status_code=404,
            detail="No paper has been generated yet. Please call /generate first."
        )
    
    return JSONResponse(content=latest_paper["json"])


@app.get("/paper/latex", response_class=PlainTextResponse)
def get_paper_latex():
    """
    Get the generated paper in LaTeX format.
    
    Returns:
        Plain text response with LaTeX content
    """
    if latest_paper["latex"] is None:
        raise HTTPException(
            status_code=404,
            detail="No paper has been generated yet. Please call /generate first."
        )
    
    return PlainTextResponse(content=latest_paper["latex"])


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Research Paper Generator API"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("Starting Research Paper Generator API Server")
    print("="*80 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
