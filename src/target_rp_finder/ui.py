"""Server-rendered HTML routes for Target RP Finder. Presentation only — no business logic."""
import threading
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.flag_review import (
    compute_view_stats,
    get_review_result,
    list_recent_batches,
    review_batch,
    submit_review,
)
from target_rp_finder.browse_service import _browse_lock, _browse_results, browse_folder_worker

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

router = APIRouter()

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request, "index.html", {"recent_batches": list_recent_batches()}
    )

@router.post("/browse/open")
async def open_folder_picker():
    """Spawn a native folder picker off the request thread, return a request id to poll."""
    request_id = str(uuid4())
    with _browse_lock:
        _browse_results[request_id] = "__pending__"
    thread = threading.Thread(target=browse_folder_worker, args=(request_id,), daemon=True)
    thread.start()
    return {"request_id": request_id}

@router.get("/browse/{request_id}")
async def poll_folder_picker(request_id: str):
    with _browse_lock:
        value = _browse_results.get(request_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Unknown request_id")
    if value == "__pending__":
        return {"status": "pending"}
    return {"status": "ready", "path": value or ""}

@router.post("/review")
async def scan_batch(request: Request, batch_path: str = Form(...)):
    """Scan a batch folder and redirect to its results page."""
    try:
        result = review_batch(batch_path)
    except ValueError as e:
        return templates.TemplateResponse(
            request, "index.html", {"error": str(e)}, status_code=400
        )
    return RedirectResponse(url=f"/batch/{result.revision_id}/view", status_code=303)

@router.get("/batch/{revision_id}/submit")
async def submit_confirmation(request: Request, revision_id: str):
    """Render the publish-confirmation screen for a working revision."""
    result = get_review_result(revision_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Revision not found")
    return templates.TemplateResponse(
        request,
        "submit.html",
        {"result": result, "stats": compute_view_stats(result)},
    )

@router.post("/batch/{revision_id}/submit")
async def publish_revision(request: Request, revision_id: str):
    """Freeze the revision into evidence, then show the published screen."""
    submit_review(revision_id)
    return RedirectResponse(url=f"/batch/{revision_id}/published", status_code=303)

@router.get("/batch/{revision_id}/published")
async def published(request: Request, revision_id: str):
    """Success screen shown after a revision is frozen into evidence."""
    return templates.TemplateResponse(
        request, "published.html", {"revision_id": revision_id}
    )

@router.get("/batch/{revision_id}/view")
async def view_results(request: Request, revision_id: str):
    """Render all samples for a revision; filtering happens client-side."""
    result = get_review_result(revision_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Revision not found")

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "result": result,
            "samples": result.samples,
            "stats": compute_view_stats(result),
        },
    )
