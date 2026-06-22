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
