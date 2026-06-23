"""Tests for rp_parser service."""
import pytest
from pathlib import Path
import tempfile
from .parser import parse_target_rp, FlaggedCompound

FIXTURE_DIR = Path(__file__).parent.parent.parent.parent / "input data"

class TestParseTargetRP:
    """Test Target.RP file parsing."""

    def test_parse_with_udel(self):
        fixture = FIXTURE_DIR / "Target.RP_with_Udel"
        if not fixture.exists():
            pytest.skip("Fixture file not found")

        flagged, unknown = parse_target_rp(fixture)

        assert len(flagged) == 7
        assert flagged[0].name == "d-limonene"
        assert flagged[0].review_code == "Udel"

        dubious_compounds = [c for c in flagged if c.review_code == "dubious"]
        assert len(dubious_compounds) == 6

    def test_parse_missing_file(self):
        flagged, unknown = parse_target_rp("/nonexistent/file.txt")
        assert flagged == []
        assert unknown == []

    def test_parse_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert flagged == []

    def test_flagged_compound_structure(self):
        fixture = FIXTURE_DIR / "Target.RP_with_Udel"
        if not fixture.exists():
            pytest.skip("Fixture file not found")

        flagged, _ = parse_target_rp(fixture)

        assert all(isinstance(c, FlaggedCompound) for c in flagged)
        assert all(c.name for c in flagged)
        assert all(c.review_code in {"Udel", "Udelete", "dubious"} for c in flagged)
        assert all(c.sample_id == "20181070022" for c in flagged)

    def test_unknown_tokens_logged(self):
        fixture = FIXTURE_DIR / "Target.RP_with_Udel"
        if not fixture.exists():
            pytest.skip("Fixture file not found")

        _, unknown = parse_target_rp(fixture)

        assert isinstance(unknown, list)
        assert all(isinstance(t, str) for t in unknown)

    def test_no_false_positives_on_empty_review_code(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 12345\n")
            f.write("Compounds                               REVIEW CODE\n")
            f.write("==========================              ===========\n")
            f.write("    1 compound-name                 123    0.5\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert len(flagged) == 0
            assert unknown == []

    def test_qualifier_suffix_not_treated_as_review_code(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 12345\n")
            f.write("Compounds                               REVIEW CODE\n")
            f.write("==========================              ===========\n")
            f.write("    1 phenol          94  10.780  10.776  (0.899)  10593  0.38005  0.0678(M)\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert len(flagged) == 0
            assert unknown == []
