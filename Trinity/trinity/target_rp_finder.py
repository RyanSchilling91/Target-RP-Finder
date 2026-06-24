"""Trinity entry surface for Target RP Finder app.

Provides the single persistence path for Batch, Revision, Sample, and Flagged Compound entities.
All reads/writes from flag_review must route through this module.
"""
import json
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path
import sqlite3

from .db import TrinityDB, DBConfig

class TargetRPFinderPersistence:
    """Entry point for Target RP Finder persistence through Trinity."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize persistence layer with optional custom DB path."""
        if db_path is None:
            # Store database in project-relative data/ folder for portability
            project_root = Path(__file__).parent.parent.parent
            db_path = project_root / "data" / "trinity.db"
        else:
            db_path = Path(db_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)

        config = DBConfig(
            db_path=db_path,
            schema_version=1,
            app_version="1.0"
        )
        self.trinity = TrinityDB(config)
        self.trinity.initialize()

        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row

    def create_batch(self, batch_path: str) -> str:
        """Create a new batch run and return run_id.

        Args:
            batch_path: Path to the .b folder

        Returns:
            run_id: System-generated unique identifier
        """
        run_id = str(uuid.uuid4())
        # display_id has a UNIQUE constraint; re-scanning the same .b folder
        # (a normal re-entry workflow) must not collide on the bare folder name.
        display_id = f"{Path(batch_path).name}_{run_id[:8]}"

        self.conn.execute(
            """
            INSERT INTO runs (run_id, display_id, created_at, created_by, run_status, run_year, source_context)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, display_id, datetime.utcnow().isoformat(), "system", "active", datetime.utcnow().year, batch_path)
        )
        self.conn.commit()
        return run_id

    def create_revision(self, run_id: str, based_on_revision_id: Optional[str] = None) -> str:
        """Create a new working revision for a batch.

        Args:
            run_id: Parent batch run_id
            based_on_revision_id: Prior revision ID if re-entering (optional)

        Returns:
            revision_id: System-generated unique identifier
        """
        revision_id = str(uuid.uuid4())

        cursor = self.conn.execute(
            "SELECT COALESCE(MAX(revision_number), 0) FROM revisions WHERE run_id = ?",
            (run_id,)
        )
        next_rev_num = cursor.fetchone()[0] + 1

        state_json = json.dumps({"samples": []})

        self.conn.execute(
            """
            INSERT INTO revisions
            (revision_id, run_id, revision_number, revision_status, working_state_version,
             state_json, created_at, created_by, based_on_revision_id, is_current_revision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (revision_id, run_id, next_rev_num, "working", 1, state_json,
             datetime.utcnow().isoformat(), "system", based_on_revision_id, 1)
        )
        self.conn.execute(
            "UPDATE runs SET current_revision_id = ? WHERE run_id = ?",
            (revision_id, run_id)
        )
        self.conn.commit()
        return revision_id

    def store_samples_and_compounds(self, revision_id: str, samples_data: dict) -> None:
        """Store parsed samples and flagged compounds in revision state.

        Args:
            revision_id: Target revision ID
            samples_data: Dict with structure {sample_id: {status, flagged_compounds: [...]}}
        """
        state_json = json.dumps({"samples": samples_data})
        self.conn.execute(
            "UPDATE revisions SET state_json = ? WHERE revision_id = ?",
            (state_json, revision_id)
        )
        self.conn.commit()

    def load_revision(self, revision_id: str) -> Optional[dict]:
        """Load a revision's samples and compounds data.

        Args:
            revision_id: Revision to load

        Returns:
            Dict with samples data or None if not found
        """
        cursor = self.conn.execute(
            "SELECT state_json FROM revisions WHERE revision_id = ?",
            (revision_id,)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def get_revision_context(self, revision_id: str) -> Optional[dict]:
        """Get the parent run_id and source batch path for a revision.

        Args:
            revision_id: Revision to look up

        Returns:
            Dict with run_id and batch_path, or None if not found
        """
        cursor = self.conn.execute(
            """
            SELECT r.run_id, ru.source_context, r.created_at
            FROM revisions r
            JOIN runs ru ON r.run_id = ru.run_id
            WHERE r.revision_id = ?
            """,
            (revision_id,)
        )
        row = cursor.fetchone()
        if row:
            return {"run_id": row[0], "batch_path": row[1], "created_at": row[2]}
        return None

    def list_recent_batches(self, limit: int = 50) -> list[dict]:
        """List published revisions for the home-page history, newest first.

        Sample and flagged-sample counts are derived from the stored revision
        state at read time — never persisted as standalone fields.

        Args:
            limit: Maximum number of rows to return

        Returns:
            List of dicts: revision_id, batch_name, batch_path, created_at,
            sample_count, flagged_count (samples carrying >=1 flagged compound)
        """
        cursor = self.conn.execute(
            """
            SELECT r.revision_id, r.created_at, r.state_json, ru.display_id, ru.source_context
            FROM revisions r
            JOIN runs ru ON r.run_id = ru.run_id
            WHERE r.revision_status = 'published'
            ORDER BY r.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = []
        for row in cursor.fetchall():
            state = json.loads(row["state_json"] or "{}")
            samples = state.get("samples", {})
            flagged_samples = sum(
                1 for s in samples.values() if s.get("flagged_compounds")
            )
            rows.append({
                "revision_id": row["revision_id"],
                "created_at": row["created_at"],
                "batch_name": Path(row["source_context"]).name if row["source_context"] else row["display_id"],
                "batch_path": row["source_context"],
                "sample_count": len(samples),
                "flagged_count": flagged_samples,
            })
        return rows

    def publish_revision(self, revision_id: str) -> None:
        """Publish a revision, marking it as immutable evidence.

        Args:
            revision_id: Revision to publish
        """
        self.conn.execute(
            """
            UPDATE revisions
            SET revision_status = 'published', superseded_at = NULL
            WHERE revision_id = ?
            """,
            (revision_id,)
        )
        self.conn.commit()

    def get_batch_revisions(self, run_id: str) -> list[dict]:
        """Get all revisions for a batch.

        Args:
            run_id: Batch run_id

        Returns:
            List of revision dicts with id, status, and created_at
        """
        cursor = self.conn.execute(
            """
            SELECT revision_id, revision_status, created_at, revision_number
            FROM revisions
            WHERE run_id = ?
            ORDER BY revision_number DESC
            """,
            (run_id,)
        )
        return [
            {"revision_id": row[0], "status": row[1], "created_at": row[2], "number": row[3]}
            for row in cursor.fetchall()
        ]

    def close(self) -> None:
        """Close both database connections (the app-level one and Trinity's own)."""
        if self.conn:
            self.conn.close()
        self.trinity.close()
