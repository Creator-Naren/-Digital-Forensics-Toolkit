import hashlib
from pathlib import Path
from typing import Literal

HashAlgorithm = Literal["md5", "sha1", "sha256"]
CHUNK_SIZE = 8192

def compute_hash(file_path: Path, algorithm: HashAlgorithm = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_hash(file_path: Path, expected_hash: str, algorithm: HashAlgorithm = "sha256") -> bool:
    actual_hash = compute_hash(file_path, algorithm)
    return actual_hash.lower() == expected_hash.lower()

def compute_file_hashes(file_path: Path) -> dict[str, str]:
    return {
        "md5": compute_hash(file_path, "md5"),
        "sha1": compute_hash(file_path, "sha1"),
        "sha256": compute_hash(file_path, "sha256"),
    }
