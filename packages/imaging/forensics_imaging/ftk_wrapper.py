import shutil
import subprocess
from pathlib import Path
from forensics_core.database import Database
from .formats import ImageFormat, FORMAT_CONFIG
from forensics_core.hashing import compute_hash
from .command import ForensicCommand

class FTKImagerCommand(ForensicCommand):
    def __init__(self, source: Path, output_dir: Path, image_format: ImageFormat,
                 case_id: str, evidence_id: str, db: Database):
        super().__init__(case_id, evidence_id, db)
        self.source = source
        self.output_dir = output_dir
        self.image_format = image_format

    def validate(self) -> bool:
        if not self.source.exists():
            return False
        if not shutil.which("ftkimager"):
            return False
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return True

    def execute(self) -> dict:
        config = FORMAT_CONFIG[self.image_format]
        output_file = self.output_dir / f"{self.evidence_id}{config['extension']}"

        source_hash = compute_hash(self.source)

        cmd = [
            "ftkimager",
            str(self.source),
            str(output_file.with_suffix("")),
            "--format", self.image_format.value
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {"success": False, "errors": [result.stderr]}

        output_hash = compute_hash(output_file) if output_file.exists() else None

        return {
            "success": True,
            "source_hash": source_hash,
            "output_hash": output_hash,
            "output_path": str(output_file),
            "size_bytes": output_file.stat().st_size if output_file.exists() else 0
        }

    def report(self) -> dict:
        return {
            "command": "FTKImager",
            "source": str(self.source),
            "format": self.image_format.value,
            "output_dir": str(self.output_dir)
        }
