from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ImageFormat(str, Enum):
    E01 = "E01"
    RAW = "RAW"
    DD = "DD"

class Case(BaseModel):
    id: str
    name: str
    investigator: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"

class Evidence(BaseModel):
    id: str
    case_id: str
    source_path: str
    source_hash: Optional[str] = None
    format: ImageFormat
    output_path: Optional[str] = None
    output_hash: Optional[str] = None
    size_bytes: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    verified: bool = False

class CustodyAction(BaseModel):
    evidence_id: str
    action: str
    actor: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Optional[dict] = None
    hash_at_action: Optional[str] = None

class CommandResult(BaseModel):
    success: bool
    command: str
    evidence_id: str
    output_path: Optional[str] = None
    source_hash: Optional[str] = None
    output_hash: Optional[str] = None
    duration_seconds: float = 0.0
    errors: list[str] = Field(default_factory=list)
