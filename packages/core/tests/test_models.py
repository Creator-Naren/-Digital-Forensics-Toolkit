import pytest
from forensics_core.models import Case, Evidence, CustodyAction, CommandResult, ImageFormat

class TestCase:
    def test_create_case(self):
        case = Case(id="CASE-001", name="Incident 2026-0831", investigator="J.Smith")
        assert case.id == "CASE-001"
        assert case.status == "active"
        assert case.created_at is not None

    def test_case_requires_id_and_name(self):
        with pytest.raises(Exception):
            Case(name="Missing ID")

class TestEvidence:
    def test_create_evidence(self):
        evidence = Evidence(id="EV-001", case_id="CASE-001", source_path="/dev/sda", format=ImageFormat.E01)
        assert evidence.id == "EV-001"
        assert evidence.verified is False

    def test_evidence_requires_case_id(self):
        with pytest.raises(Exception):
            Evidence(id="EV-001", source_path="/dev/sda")

class TestImageFormat:
    def test_image_formats(self):
        assert ImageFormat.E01.value == "E01"
        assert ImageFormat.RAW.value == "RAW"
        assert ImageFormat.DD.value == "DD"

class TestCustodyAction:
    def test_create_custody_action(self):
        action = CustodyAction(evidence_id="EV-001", action="created", actor="J.Smith", hash_at_action="abc123")
        assert action.evidence_id == "EV-001"
        assert action.timestamp is not None

class TestCommandResult:
    def test_create_command_result(self):
        result = CommandResult(success=True, command="FTKImager", evidence_id="EV-001")
        assert result.success is True
        assert result.errors == []
        assert result.duration_seconds == 0.0

    def test_command_result_with_errors(self):
        result = CommandResult(success=False, command="FTKImager", evidence_id="EV-001", errors=["Failed to image"])
        assert result.success is False
        assert len(result.errors) == 1
