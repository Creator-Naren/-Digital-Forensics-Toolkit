from forensics_core.audit import AuditLogger

class TestAuditLogger:
    def test_log_start(self):
        logger = AuditLogger("CASE-001")
        logger.log_start("FTKImagerCommand")
        assert len(logger.entries) == 1
        assert logger.entries[0]["action"] == "start"

    def test_log_complete(self):
        logger = AuditLogger("CASE-001")
        logger.log_complete({"success": True})
        assert len(logger.entries) == 1
        assert logger.entries[0]["action"] == "complete"

    def test_log_error(self):
        logger = AuditLogger("CASE-001")
        logger.log_error("Something failed")
        assert logger.entries[0]["action"] == "error"
        assert logger.entries[0]["details"] == "Something failed"
