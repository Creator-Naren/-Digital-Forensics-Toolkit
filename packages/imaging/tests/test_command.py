import pytest
from forensics_core.database import Database
from forensics_core.models import Case
from forensics_imaging.command import ForensicCommand, ValidationError

class ConcreteCommand(ForensicCommand):
    def validate(self) -> bool:
        return True

    def execute(self) -> dict:
        return {"success": True}

    def report(self) -> dict:
        return {"command": "test"}

class TestForensicCommand:
    def setup_method(self):
        self.db = Database(":memory:")
        self.db.create_case(Case(id="C1", name="Test"))

    def test_run_validates_before_execute(self):
        cmd = ConcreteCommand(case_id="C1", evidence_id="EV-001", db=self.db)
        result = cmd.run()
        assert result["success"] is True

    def test_run_raises_on_validation_failure(self):
        class FailCommand(ForensicCommand):
            def validate(self) -> bool:
                return False
            def execute(self) -> dict:
                return {}
            def report(self) -> dict:
                return {}

        cmd = FailCommand(case_id="C1", evidence_id="EV-001", db=self.db)
        with pytest.raises(ValidationError):
            cmd.run()

    def test_run_logs_start_and_complete(self):
        cmd = ConcreteCommand(case_id="C1", evidence_id="EV-001", db=self.db)
        cmd.run()
        assert len(cmd.logger.entries) == 2
        assert cmd.logger.entries[0]["action"] == "start"
        assert cmd.logger.entries[1]["action"] == "complete"

    def test_cannot_instantiate_without_abstract_methods(self):
        with pytest.raises(TypeError):
            ForensicCommand(case_id="C1", evidence_id="EV-001", db=self.db)
