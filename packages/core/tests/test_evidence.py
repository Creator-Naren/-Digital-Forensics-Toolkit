import pytest

from forensics_core.database import Database
from forensics_core.evidence import EvidenceManager
from forensics_core.models import Case, Evidence, ImageFormat

class TestEvidenceManager:
    def setup_method(self):
        self.db = Database(":memory:")
        self.db.create_case(Case(id="C1", name="Test"))
        self.manager = EvidenceManager(self.db)

    def test_create_evidence_generates_id(self):
        evidence = self.manager.create_evidence(
            case_id="C1", source_path="/dev/sda", format=ImageFormat.E01, actor="J.Smith"
        )
        assert evidence.id.startswith("EV-")
        assert evidence.source_path == "/dev/sda"

    def test_create_evidence_logs_custody(self):
        evidence = self.manager.create_evidence(
            case_id="C1", source_path="/dev/sda", format=ImageFormat.E01, actor="J.Smith"
        )
        log = self.db.get_custody_log(evidence.id)
        assert len(log) == 1
        assert log[0].action == "created"
        assert log[0].actor == "J.Smith"

    def test_update_evidence_with_hash(self):
        evidence = self.manager.create_evidence(
            case_id="C1", source_path="/dev/sda", format=ImageFormat.E01, actor="J.Smith"
        )
        updated = self.manager.update_evidence(
            evidence_id=evidence.id,
            source_hash="abc123",
            size_bytes=1024,
            actor="J.Smith"
        )
        assert updated.source_hash == "abc123"
        assert updated.size_bytes == 1024

    def test_export_case_json(self):
        self.manager.create_evidence(
            case_id="C1", source_path="/dev/sda", format=ImageFormat.E01, actor="J.Smith"
        )
        export = self.manager.export_case_json("C1")
        assert export["case"]["id"] == "C1"
        assert len(export["evidence"]) == 1
        assert "custody_log" in export["evidence"][0]

    def test_update_nonexistent_evidence_raises(self):
        with pytest.raises(ValueError, match="not found"):
            self.manager.update_evidence(evidence_id="NONEXISTENT", source_hash="abc", actor="J.Smith")

    def test_export_nonexistent_case_raises(self):
        with pytest.raises(ValueError, match="not found"):
            self.manager.export_case_json("NONEXISTENT")
