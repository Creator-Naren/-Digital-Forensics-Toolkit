from click.testing import CliRunner
from forensics_cli.main import cli

class TestCLI:
    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Forensic Toolkit" in result.output

    def test_case_create_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["case", "create", "--help"])
        assert result.exit_code == 0

    def test_imaging_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["imaging", "--help"])
        assert result.exit_code == 0

    def test_case_list_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["case", "list", "--help"])
        assert result.exit_code == 0

    def test_imaging_image_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["imaging", "image", "--help"])
        assert result.exit_code == 0

    def test_imaging_verify_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["imaging", "verify", "--help"])
        assert result.exit_code == 0

    def test_imaging_list_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["imaging", "list", "--help"])
        assert result.exit_code == 0


def test_case_create():
    runner = CliRunner()
    result = runner.invoke(cli, ["case", "create", "--name", "Test Case", "--investigator", "J.Smith"])
    assert result.exit_code == 0
    assert "Created case:" in result.output