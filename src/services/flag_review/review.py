"""Aggregate flagged compounds and manage persistence through Trinity."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "Trinity"))

from trinity.target_rp_finder import TargetRPFinderPersistence
from services.batch_discovery import discover_samples
from services.rp_parser import parse_target_rp

@dataclass
class SampleReview:
    """Review result for a single sample."""
    sample_id: str
    status: str
    flagged_compounds: list = field(default_factory=list)
    unknown_tokens: list = field(default_factory=list)

@dataclass
class ReviewResult:
    """Overall review result for a batch."""
    run_id: str
    revision_id: str
    batch_path: str
    samples: list[SampleReview] = field(default_factory=list)
    total_flagged: int = 0
    scanned_at: str = ""


def _code_class(code: str) -> str:
    """Map a review code to its presentation CSS class (matches design tokens)."""
    c = (code or "").lower()
    if c == "dubious":
        return "code-dubious"
    if c in ("udel", "udelete"):
        return "code-udel"
    return "code-other"


def _format_scan_date(raw: str) -> str:
    """Trim an ISO timestamp to 'YYYY-MM-DD HH:MM' for display."""
    if not raw:
        return ""
    text = raw.replace("T", " ")
    # Keep date + HH:MM only (drop seconds/microseconds).
    if len(text) >= 16:
        return text[:16]
    return text


def compute_view_stats(result: "ReviewResult") -> dict:
    """Compute derived display stats for the results screen.

    All counts are derived from the in-memory result at display time and are
    never persisted (see STATE_CLASSIFICATION.md).
    """
    samples = result.samples
    code_counts: dict[str, int] = {}
    for s in samples:
        for c in s.flagged_compounds:
            code = c.get("review_code", "") if isinstance(c, dict) else getattr(c, "review_code", "")
            code_counts[code] = code_counts.get(code, 0) + 1

    code_tiles = [
        {"code": code, "count": count, "css_class": _code_class(code)}
        for code, count in sorted(code_counts.items(), key=lambda kv: -kv[1])
    ]

    return {
        "total": len(samples),
        "parsed": sum(1 for s in samples if s.status == "parsed"),
        "missing": sum(1 for s in samples if s.status == "missing"),
        "malformed": sum(1 for s in samples if s.status == "malformed"),
        "flagged": sum(len(s.flagged_compounds) for s in samples),
        "code_tiles": code_tiles,
    }


def list_recent_batches(db_path: Optional[str] = None, limit: int = 50) -> list[dict]:
    """Return published-revision history for the home page, newest first.

    The only caller path into Trinity for the home-page history. Counts are
    derived at read time by the persistence layer, never stored.
    """
    persistence = TargetRPFinderPersistence(db_path=db_path)
    rows = persistence.list_recent_batches(limit=limit)
    persistence.close()
    for row in rows:
        row["scan_date"] = _format_scan_date(row.get("created_at", ""))
        row["scan_date_iso"] = (row.get("created_at", "") or "")[:10]
    return rows

def review_batch(batch_path: str, db_path: Optional[str] = None) -> ReviewResult:
    """Scan and review a batch folder for flagged compounds.

    Workflow:
    1. Discover sample folders in the batch
    2. Parse each sample's Target.RP file
    3. Aggregate results
    4. Persist through Trinity
    5. Return review result

    Args:
        batch_path: Path to the .b batch folder
        db_path: Optional custom Trinity database path

    Returns:
        ReviewResult with parsed samples and flagged compounds
    """
    batch_path = Path(batch_path)
    if not batch_path.is_dir():
        raise ValueError(f"Batch path does not exist or is not a directory: {batch_path}")

    persistence = TargetRPFinderPersistence(db_path=db_path)

    run_id = persistence.create_batch(str(batch_path))
    revision_id = persistence.create_revision(run_id)

    samples = discover_samples(batch_path)
    review_samples = []
    total_flagged = 0
    unknown_tokens_all = set()

    for sample in samples:
        target_rp_path = sample.path / "Target.RP"

        if not target_rp_path.exists():
            review_samples.append(SampleReview(
                sample_id=sample.name,
                status="missing",
                flagged_compounds=[],
                unknown_tokens=[]
            ))
            continue

        try:
            flagged, unknown = parse_target_rp(target_rp_path)
            unknown_tokens_all.update(unknown)

            review_samples.append(SampleReview(
                sample_id=sample.name,
                status="parsed",
                flagged_compounds=[
                    {
                        "name": c.name,
                        "review_code": c.review_code,
                        "sample_id": c.sample_id
                    }
                    for c in flagged
                ],
                unknown_tokens=list(unknown)
            ))
            total_flagged += len(flagged)

        except Exception as e:
            review_samples.append(SampleReview(
                sample_id=sample.name,
                status="malformed",
                flagged_compounds=[],
                unknown_tokens=[]
            ))

    samples_data = {
        sample.sample_id: {
            "status": sample.status,
            "flagged_compounds": sample.flagged_compounds,
            "unknown_tokens": sample.unknown_tokens
        }
        for sample in review_samples
    }

    persistence.store_samples_and_compounds(revision_id, samples_data)
    persistence.close()

    return ReviewResult(
        run_id=run_id,
        revision_id=revision_id,
        batch_path=str(batch_path),
        samples=review_samples,
        total_flagged=total_flagged
    )

def get_review_result(revision_id: str, db_path: Optional[str] = None) -> Optional[ReviewResult]:
    """Load a previously persisted review result by revision_id.

    Args:
        revision_id: Revision to load
        db_path: Optional custom Trinity database path

    Returns:
        ReviewResult rebuilt from Trinity state, or None if not found
    """
    persistence = TargetRPFinderPersistence(db_path=db_path)
    state = persistence.load_revision(revision_id)
    if state is None:
        persistence.close()
        return None

    context = persistence.get_revision_context(revision_id) or {}
    persistence.close()

    samples_data = state.get("samples", {})
    review_samples = [
        SampleReview(
            sample_id=sample_id,
            status=info.get("status", "unknown"),
            flagged_compounds=info.get("flagged_compounds", []),
            unknown_tokens=info.get("unknown_tokens", [])
        )
        for sample_id, info in samples_data.items()
    ]
    total_flagged = sum(len(s.flagged_compounds) for s in review_samples)

    return ReviewResult(
        run_id=context.get("run_id", ""),
        revision_id=revision_id,
        batch_path=context.get("batch_path", ""),
        samples=review_samples,
        total_flagged=total_flagged,
        scanned_at=_format_scan_date(context.get("created_at", ""))
    )

def submit_review(revision_id: str, db_path: Optional[str] = None) -> None:
    """Publish a working revision, freezing it into immutable evidence.

    Args:
        revision_id: Revision to publish
        db_path: Optional custom Trinity database path
    """
    persistence = TargetRPFinderPersistence(db_path=db_path)
    persistence.publish_revision(revision_id)
    persistence.close()
