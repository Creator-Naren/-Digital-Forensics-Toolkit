from datetime import datetime, timezone

class AuditLogger:
    def __init__(self, case_id: str):
        self.case_id = case_id
        self.entries = []

    def log_start(self, command_name: str):
        self.entries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "case_id": self.case_id,
            "action": "start",
            "command": command_name
        })

    def log_complete(self, result: dict):
        self.entries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "case_id": self.case_id,
            "action": "complete",
            "details": result
        })

    def log_error(self, error: str):
        self.entries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "case_id": self.case_id,
            "action": "error",
            "details": error
        })
