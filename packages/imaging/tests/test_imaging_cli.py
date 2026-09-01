import tempfile
import os
from click.testing import CliRunner
from forensics_core.database import Database
from forensics_core.models import Case
from forensics_imaging.cli import imaging
from unittest.mock import patch, MagicMock

class TestImagingCLI:
    def setup_method(self):
        self.db = Database(":memory:")
        self.db.create_case(Case(id="C1", name="Test"))

    def test_imaging_help(self):
        runner = CliRunner()
        result = runner.invoke(imaging, ["--help"])
        assert result.exit_code == 0
        assert "Disk imaging" in result.output

    def test_image_help(self):
        runner = CliRunner()
        result = runner.invoke(imaging, ["image", "--help"])
        assert result.exit_code == 0
        assert "Create a disk image" in result.output

    def test_verify_help(self):
        runner = CliRunner()
        result = runner.invoke(imaging, ["verify", "--help"])
        assert result.exit_code == 0
        assert "Verify image integrity" in result.output

    def test_list_help(self):
        runner = CliRunner()
        result = runner.invoke(imaging, ["list", "--help"])
        assert result.exit_code == 0
        assert "List images in a case" in result.output

    @patch("forensics_imaging.ftk_wrapper.FTKImagerCommand")
    def test_image_command_execution(self, MockCommand):
        mock_cmd = MagicMock()
        mock_cmd.run.return_value = {
            "success": True,
            "source_hash": "abc123",
            "output_hash": "def456"
        }
        MockCommand.return_value = mock_cmd

        runner = CliRunner()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            source_path = tmp.name
        try:
            result = runner.invoke(imaging, [
                "image", "--case-id", "C1", "--evidence-id", "EV-001",
                "--source", source_path, "--output", "/tmp/out"
            ])
            assert result.exit_code == 0
            assert "Image created successfully" in result.output
        finally:
            os.unlink(source_path)