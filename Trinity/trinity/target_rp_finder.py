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
            db_path = Path.home() / ".local" / "share" / "TargetRPFinder" / "trinity.db"
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
        batch_name = Path(batch_path).name

        self.conn.execute(
            """
            INSERT INTO runs (run_id, display_id, created_at, created_by, run_status, run_year, source_context)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, batch_name, datetime.utcnow().isoformat(), "system", "active", datetime.utcnow().year, batch_path)
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
        """Close the database connection."""
        if self.conn:
            self.conn.close()
