"""FastAPI entry point for Target RP Finder."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.flag_review import review_batch

app = FastAPI(title="Target RP Finder")

class BatchReviewRequest(BaseModel):
    batch_path: str

class BatchReviewResponse(BaseModel):
    run_id: str
    revision_id: str
    batch_path: str
    total_flagged: int
    samples_count: int

@app.get("/")
async def root():
    return {"message": "Target RP Finder API", "version": "1.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/batch/review")
async def submit_batch_review(request: BatchReviewRequest):
    """Scan and review a batch folder for flagged compounds.

    Args:
        batch_path: Path to the .b batch folder

    Returns:
        Review result with run_id, revision_id, and summary
    """
    try:
        result = review_batch(request.batch_path)
        return BatchReviewResponse(
            run_id=result.run_id,
            revision_id=result.revision_id,
            batch_path=result.batch_path,
            total_flagged=result.total_flagged,
            samples_count=len(result.samples)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}")

@app.get("/batch/{revision_id}")
async def get_batch_results(revision_id: str):
    """Get the full results for a batch review.

    Args:
        revision_id: The revision ID from the initial review

    Returns:
        Full results with all samples and flagged compounds
    """
    raise HTTPException(status_code=501, detail="Not yet implemented")
