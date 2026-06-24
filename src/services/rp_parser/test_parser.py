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

    def test_e_code_recognition(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 20181070022\n")
            f.write("Compounds                               REVIEW CODE\n")
            f.write("==========================              ===========\n")
            f.write("    1 benzene                  100    10.500 10.450 (1.001)    100000    0.12345     0.0456(M)     E-Code\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert len(flagged) == 1
            assert flagged[0].review_code == "E-Code"
            assert "benzene" in flagged[0].name

    def test_okay_excluded_from_unknown_tokens(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 12345\n")
            f.write("Compounds                               REVIEW CODE\n")
            f.write("==========================              ===========\n")
            f.write("    1 compound-a               100    10.500 10.450 (1.001)    100000    0.12345     0.0456(M)     Okay\n")
            f.write("    2 compound-b               100    10.500 10.450 (1.001)    100000    0.12345     0.0456(M)     OK\n")
            f.write("    3 compound-c               100    10.500 10.450 (1.001)    100000    0.12345     0.0456(M)     OKAY\n")
            f.write("    4 compound-d               100    10.500 10.450 (1.001)    100000    0.12345     0.0456(M)     Unknown\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert "Okay" not in unknown
            assert "OK" not in unknown
            assert "OKAY" not in unknown
            assert "Unknown" in unknown

    def test_quad_erronious_on_column_non_numerical(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 12345\n")
            f.write("Compounds                               QUANT SIG                         ON-COLUMN    FINAL         REVIEW CODE\n")
            f.write("==========================              ====          ==== ======== ====== ========    =======    =======    ===========\n")
            f.write("    1 benzene                  100    10.500 10.450 (1.001)    100000    ERROR           0.0456(M)\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert len(flagged) == 1
            assert flagged[0].review_code == "Quad Erronious"
            assert flagged[0].has_quad_error is True
            assert "benzene" in flagged[0].name

    def test_on_column_numerical_no_flag(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Lab Smp Id: 12345\n")
            f.write("Compounds                               QUANT SIG                         ON-COLUMN    FINAL         REVIEW CODE\n")
            f.write("==========================              ====          ==== ======== ====== ========    =======    =======    ===========\n")
            f.write("    1 benzene                  100    10.500 10.450 (1.001)    100000    1.23456         0.0456(M)\n")
            f.flush()

            flagged, unknown = parse_target_rp(f.name)
            assert len(flagged) == 0
            assert unknown == []
