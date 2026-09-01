import json
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from .models import Case, Evidence, CustodyAction, ImageFormat

class Base(DeclarativeBase):
    pass

class CaseRow(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    investigator = Column(String)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, default="active")

class EvidenceRow(Base):
    __tablename__ = "evidence"
    id = Column(String, primary_key=True)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    source_path = Column(String, nullable=False)
    source_hash = Column(String)
    format = Column(String, nullable=False)
    output_path = Column(String)
    output_hash = Column(String)
    size_bytes = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)

class CustodyRow(Base):
    __tablename__ = "custody_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    evidence_id = Column(String, ForeignKey("evidence.id"), nullable=False)
    action = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    details = Column(Text)
    hash_at_action = Column(String)

class Database:
    def __init__(self, db_path: str = "forensics.db"):
        if db_path == ":memory:":
            self.engine = create_engine("sqlite:///:memory:")
        else:
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def _get_session(self) -> Session:
        return self.SessionLocal()

    def create_case(self, case: Case) -> None:
        with self._get_session() as session:
            row = CaseRow(id=case.id, name=case.name, investigator=case.investigator,
                         created_at=case.created_at, status=case.status)
            session.add(row)
            session.commit()

    def get_case(self, case_id: str) -> Optional[Case]:
        with self._get_session() as session:
            row = session.query(CaseRow).filter(CaseRow.id == case_id).first()
            if row:
                return Case(id=row.id, name=row.name, investigator=row.investigator,
                           created_at=row.created_at, status=row.status)
            return None

    def list_cases(self) -> list[Case]:
        with self._get_session() as session:
            rows = session.query(CaseRow).all()
            return [Case(id=r.id, name=r.name, investigator=r.investigator,
                        created_at=r.created_at, status=r.status) for r in rows]

    def create_evidence(self, evidence: Evidence) -> None:
        with self._get_session() as session:
            row = EvidenceRow(id=evidence.id, case_id=evidence.case_id,
                            source_path=evidence.source_path, source_hash=evidence.source_hash,
                            format=evidence.format.value, output_path=evidence.output_path,
                            output_hash=evidence.output_hash, size_bytes=evidence.size_bytes,
                            created_at=evidence.created_at, verified=evidence.verified)
            session.add(row)
            session.commit()

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        with self._get_session() as session:
            row = session.query(EvidenceRow).filter(EvidenceRow.id == evidence_id).first()
            if row:
                return Evidence(id=row.id, case_id=row.case_id, source_path=row.source_path,
                              source_hash=row.source_hash, format=ImageFormat(row.format),
                              output_path=row.output_path, output_hash=row.output_hash,
                              size_bytes=row.size_bytes, created_at=row.created_at,
                              verified=row.verified)
            return None

    def list_evidence(self, case_id: str) -> list[Evidence]:
        with self._get_session() as session:
            rows = session.query(EvidenceRow).filter(EvidenceRow.case_id == case_id).all()
            return [Evidence(id=r.id, case_id=r.case_id, source_path=r.source_path,
                           source_hash=r.source_hash, format=ImageFormat(r.format),
                           output_path=r.output_path, output_hash=r.output_hash,
                           size_bytes=r.size_bytes, created_at=r.created_at,
                           verified=r.verified) for r in rows]

    def update_evidence(self, evidence: Evidence) -> None:
        with self._get_session() as session:
            row = session.query(EvidenceRow).filter(EvidenceRow.id == evidence.id).first()
            if row:
                row.source_hash = evidence.source_hash
                row.output_path = evidence.output_path
                row.output_hash = evidence.output_hash
                row.size_bytes = evidence.size_bytes
                row.verified = evidence.verified
                session.commit()

    def add_custody_action(self, action: CustodyAction) -> None:
        with self._get_session() as session:
            row = CustodyRow(evidence_id=action.evidence_id, action=action.action,
                           actor=action.actor, timestamp=action.timestamp,
                           details=json.dumps(action.details) if action.details else None,
                           hash_at_action=action.hash_at_action)
            session.add(row)
            session.commit()

    def get_custody_log(self, evidence_id: str) -> list[CustodyAction]:
        with self._get_session() as session:
            rows = session.query(CustodyRow).filter(
                CustodyRow.evidence_id == evidence_id
            ).order_by(CustodyRow.timestamp).all()
            return [CustodyAction(
                evidence_id=r.evidence_id, action=r.action, actor=r.actor,
                timestamp=r.timestamp,
                details=json.loads(r.details) if r.details else None,
                hash_at_action=r.hash_at_action
            ) for r in rows]
