from forensics_core.database import Database
from forensics_core.models import Case, Evidence, CustodyAction, ImageFormat

class TestDatabase:
    def setup_method(self):
        self.db = Database(":memory:")

    def test_create_case(self):
        case = Case(id="CASE-001", name="Test Case", investigator="J.Smith")
        self.db.create_case(case)
        retrieved = self.db.get_case("CASE-001")
        assert retrieved is not None
        assert retrieved.id == "CASE-001"

    def test_list_cases(self):
        self.db.create_case(Case(id="C1", name="Case 1"))
        self.db.create_case(Case(id="C2", name="Case 2"))
        assert len(self.db.list_cases()) == 2

    def test_create_evidence(self):
        self.db.create_case(Case(id="C1", name="Test"))
        evidence = Evidence(id="EV-001", case_id="C1", source_path="/dev/sda", format=ImageFormat.E01)
        self.db.create_evidence(evidence)
        retrieved = self.db.get_evidence("EV-001")
        assert retrieved is not None
        assert retrieved.source_path == "/dev/sda"

    def test_list_evidence_for_case(self):
        self.db.create_case(Case(id="C1", name="Test"))
        self.db.create_evidence(Evidence(id="EV1", case_id="C1", source_path="/dev/sda", format=ImageFormat.E01))
        self.db.create_evidence(Evidence(id="EV2", case_id="C1", source_path="/dev/sdb", format=ImageFormat.RAW))
        assert len(self.db.list_evidence("C1")) == 2

    def test_add_custody_action(self):
        self.db.create_case(Case(id="C1", name="Test"))
        self.db.create_evidence(Evidence(id="EV1", case_id="C1", source_path="/dev/sda", format=ImageFormat.E01))
        action = CustodyAction(evidence_id="EV1", action="created", actor="J.Smith", hash_at_action="abc123")
        self.db.add_custody_action(action)
        log = self.db.get_custody_log("EV1")
        assert len(log) == 1
        assert log[0].action == "created"

    def test_update_evidence(self):
        self.db.create_case(Case(id="C1", name="Test"))
        evidence = Evidence(id="EV1", case_id="C1", source_path="/dev/sda", format=ImageFormat.E01)
        self.db.create_evidence(evidence)
        evidence.output_path = "/evidence/C1/EV1.E01"
        evidence.verified = True
        self.db.update_evidence(evidence)
        retrieved = self.db.get_evidence("EV1")
        assert retrieved.output_path == "/evidence/C1/EV1.E01"
        assert retrieved.verified is True
