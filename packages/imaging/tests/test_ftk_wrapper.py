import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from forensics_core.database import Database
from forensics_core.models import Case
from forensics_imaging.formats import ImageFormat
from forensics_imaging.ftk_wrapper import FTKImagerCommand

class TestFTKImagerCommand:
    def setup_method(self):
        self.db = Database(":memory:")
        self.db.create_case(Case(id="C1", name="Test"))

    def test_validate_fails_if_source_missing(self):
        cmd = FTKImagerCommand(
            source=Path("/nonexistent"),
            output_dir=Path("/tmp/output"),
            image_format=ImageFormat.E01,
            case_id="C1",
            evidence_id="EV-001",
            db=self.db
        )
        assert cmd.validate() is False

    @patch("shutil.which", return_value=None)
    def test_validate_fails_if_ftk_not_installed(self, mock_which):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            cmd = FTKImagerCommand(
                source=Path(f.name),
                output_dir=Path("/tmp/output"),
                image_format=ImageFormat.E01,
                case_id="C1",
                evidence_id="EV-001",
                db=self.db
            )
            assert cmd.validate() is False

    @patch("shutil.which", return_value="/usr/bin/ftkimager")
    def test_validate_passes(self, mock_which):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            with tempfile.TemporaryDirectory() as outdir:
                cmd = FTKImagerCommand(
                    source=Path(f.name),
                    output_dir=Path(outdir),
                    image_format=ImageFormat.E01,
                    case_id="C1",
                    evidence_id="EV-001",
                    db=self.db
                )
                assert cmd.validate() is True

    @patch("shutil.which", return_value="/usr/bin/ftkimager")
    @patch("subprocess.run")
    def test_execute_returns_success(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        with tempfile.NamedTemporaryFile(delete=False) as f:
            with tempfile.TemporaryDirectory() as outdir:
                cmd = FTKImagerCommand(
                    source=Path(f.name),
                    output_dir=Path(outdir),
                    image_format=ImageFormat.E01,
                    case_id="C1",
                    evidence_id="EV-001",
                    db=self.db
                )
                result = cmd.execute()
                assert result["success"] is True
                assert "source_hash" in result

    @patch("shutil.which", return_value="/usr/bin/ftkimager")
    @patch("subprocess.run")
    def test_execute_returns_failure(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error: disk not found")
        with tempfile.NamedTemporaryFile(delete=False) as f:
            with tempfile.TemporaryDirectory() as outdir:
                cmd = FTKImagerCommand(
                    source=Path(f.name),
                    output_dir=Path(outdir),
                    image_format=ImageFormat.E01,
                    case_id="C1",
                    evidence_id="EV-001",
                    db=self.db
                )
                result = cmd.execute()
                assert result["success"] is False
                assert "Error: disk not found" in result["errors"]

    def test_report_returns_metadata(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            with tempfile.TemporaryDirectory() as outdir:
                cmd = FTKImagerCommand(
                    source=Path(f.name),
                    output_dir=Path(outdir),
                    image_format=ImageFormat.E01,
                    case_id="C1",
                    evidence_id="EV-001",
                    db=self.db
                )
                report = cmd.report()
                assert report["command"] == "FTKImager"
                assert report["format"] == "E01"