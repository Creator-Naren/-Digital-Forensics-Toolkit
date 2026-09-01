import uuid
from .database import Database
from .models import Case, Evidence, CustodyAction, ImageFormat

class EvidenceManager:
    def __init__(self, db: Database):
        self.db = db

    def create_evidence(self, case_id: str, source_path: str, format: ImageFormat, actor: str) -> Evidence:
        evidence_id = f"EV-{uuid.uuid4().hex[:8].upper()}"
        evidence = Evidence(id=evidence_id, case_id=case_id, source_path=source_path, format=format)
        self.db.create_evidence(evidence)
        action = CustodyAction(evidence_id=evidence_id, action="created", actor=actor)
        self.db.add_custody_action(action)
        return evidence

    def update_evidence(self, evidence_id: str, source_hash: str = None, output_path: str = None,
                       output_hash: str = None, size_bytes: int = None, actor: str = "system") -> Evidence:
        evidence = self.db.get_evidence(evidence_id)
        if not evidence:
            raise ValueError(f"Evidence {evidence_id} not found")
        if source_hash is not None:
            evidence.source_hash = source_hash
        if output_path is not None:
            evidence.output_path = output_path
        if output_hash is not None:
            evidence.output_hash = output_hash
        if size_bytes is not None:
            evidence.size_bytes = size_bytes
        self.db.update_evidence(evidence)
        action = CustodyAction(evidence_id=evidence_id, action="updated", actor=actor,
                              hash_at_action=source_hash or output_hash)
        self.db.add_custody_action(action)
        return self.db.get_evidence(evidence_id)

    def export_case_json(self, case_id: str) -> dict:
        case = self.db.get_case(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        evidence_list = self.db.list_evidence(case_id)
        return {
            "case": case.model_dump(mode="json"),
            "evidence": [
                {
                    **e.model_dump(mode="json"),
                    "custody_log": [
                        a.model_dump(mode="json")
                        for a in self.db.get_custody_log(e.id)
                    ]
                }
                for e in evidence_list
            ]
        }
