"""Tests for batch_discovery service."""
import pytest
from pathlib import Path
import tempfile
from .discovery import classify_folder, discover_samples, ClassifiedFolder

class TestClassifyFolder:
    """Test folder classification by name."""

    def test_cal_prefix_case_insensitive(self):
        assert classify_folder("cal_001") == "calibration"
        assert classify_folder("CAL_001") == "calibration"
        assert classify_folder("Cal_001") == "calibration"

    def test_ccv_prefix_case_insensitive(self):
        assert classify_folder("ccv_001") == "ccv"
        assert classify_folder("CCV_001") == "ccv"

    def test_tpc_prefixes(self):
        assert classify_folder("cstpc_001") == "tpc"
        assert classify_folder("CSTPC_001") == "tpc"
        assert classify_folder("tpc_001") == "tpc"
        assert classify_folder("TPC_001") == "tpc"

    def test_idl_prefix(self):
        assert classify_folder("idl_001") == "idl"
        assert classify_folder("IDL_001") == "idl"

    def test_blank_prefix(self):
        assert classify_folder("peb_001") == "blank"
        assert classify_folder("PEB_001") == "blank"

    def test_11_digit_sample(self):
        assert classify_folder("20181070022") == "sample"
        assert classify_folder("20191050001") == "sample"

    def test_11_digit_prep_blank(self):
        assert classify_folder("20191059001") == "prep_blank"
        assert classify_folder("20181079999") == "prep_blank"

    def test_11_digit_surrogate(self):
        assert classify_folder("20191058001") == "surrogate"
        assert classify_folder("20181088999") == "surrogate"

    def test_unclassified(self):
        assert classify_folder("unknown") == "unclassified"
        assert classify_folder("12345") == "unclassified"
        assert classify_folder("") == "unclassified"

class TestDiscoverSamples:
    """Test sample discovery in batch folders."""

    def test_discover_samples_empty_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            samples = discover_samples(tmpdir)
            assert samples == []

    def test_discover_samples_mixed_folders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            Path(tmppath / "20181070022").mkdir()
            Path(tmppath / "20181070023").mkdir()
            Path(tmppath / "cal_001").mkdir()
            Path(tmppath / "peb_blank").mkdir()

            samples = discover_samples(tmppath)
            assert len(samples) == 2
            assert samples[0].name == "20181070022"
            assert samples[0].folder_type == "sample"
            assert samples[1].name == "20181070023"

    def test_discover_samples_sorted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            Path(tmppath / "20181070023").mkdir()
            Path(tmppath / "20181070022").mkdir()
            Path(tmppath / "20181070021").mkdir()

            samples = discover_samples(tmppath)
            names = [s.name for s in samples]
            assert names == ["20181070021", "20181070022", "20181070023"]

    def test_discover_samples_skips_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            Path(tmppath / "20181070022").mkdir()
            Path(tmppath / "file.txt").write_text("test")

            samples = discover_samples(tmppath)
            assert len(samples) == 1
            assert samples[0].name == "20181070022"

    def test_discover_samples_invalid_path(self):
        samples = discover_samples("/nonexistent/path")
        assert samples == []
