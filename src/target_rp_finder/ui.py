"""Server-rendered HTML routes for Target RP Finder. Presentation only — no business logic."""
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.flag_review import get_review_result, review_batch, submit_review

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

router = APIRouter()

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

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

@router.post("/batch/{revision_id}/submit")
async def publish_and_return_home(revision_id: str):
    """Freeze the revision into evidence, then return to the home page."""
    submit_review(revision_id)
    return RedirectResponse(url="/", status_code=303)

@router.get("/batch/{revision_id}/view")
async def view_results(
    request: Request,
    revision_id: str,
    status: str = "all",
    flagged_only: bool = False,
):
    """Render flagged compounds for a revision, filtered at render time only."""
    result = get_review_result(revision_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Revision not found")

    samples = result.samples
    if status != "all":
        samples = [s for s in samples if s.status == status]
    if flagged_only:
        samples = [s for s in samples if s.flagged_compounds]

    total_flagged = sum(len(s.flagged_compounds) for s in samples)

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "result": result,
            "samples": samples,
            "total_flagged": total_flagged,
            "status_filter": status,
            "flagged_only": flagged_only,
        },
    )
