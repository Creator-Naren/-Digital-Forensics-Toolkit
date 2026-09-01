from abc import ABC, abstractmethod
from forensics_core.database import Database
from forensics_core.audit import AuditLogger

class ValidationError(Exception):
    pass

class ForensicCommand(ABC):
    """Base class for forensic tool commands.
    
    Subclasses must implement validate(), execute(), and report().
    Use run() to execute the command with validation and audit logging.
    """
    
    def __init__(self, case_id: str, evidence_id: str, db: Database):
        self.case_id = case_id
        self.evidence_id = evidence_id
        self.db = db
        self.logger = AuditLogger(case_id)

    @abstractmethod
    def validate(self) -> bool:
        """Validate preconditions before execution.
        
        Returns True if the command can proceed, False otherwise.
        """
        pass

    @abstractmethod
    def execute(self) -> dict:
        """Execute the forensic command.
        
        Returns a dict with command results.
        """
        pass

    @abstractmethod
    def report(self) -> dict:
        """Generate a report of the command execution.
        
        Returns a dict with report data.
        """
        pass

    def run(self):
        self.logger.log_start(self.__class__.__name__)
        if not self.validate():
            raise ValidationError("Validation failed")
        result = self.execute()
        self.logger.log_complete(result)
        return result
