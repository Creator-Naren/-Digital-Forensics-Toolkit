import hashlib
import tempfile
from pathlib import Path
from forensics_core.hashing import compute_hash, verify_hash, compute_file_hashes

class TestComputeHash:
    def test_compute_md5(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            result = compute_hash(Path(f.name), algorithm="md5")
            assert len(result) == 32

    def test_compute_sha256(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            result = compute_hash(Path(f.name), algorithm="sha256")
            assert len(result) == 64

    def test_compute_md5_correctness(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            expected = hashlib.md5(b"test data").hexdigest()
            assert compute_hash(Path(f.name), algorithm="md5") == expected

    def test_compute_sha256_correctness(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            expected = hashlib.sha256(b"test data").hexdigest()
            assert compute_hash(Path(f.name), algorithm="sha256") == expected

    def test_same_content_same_hash(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='wb', delete=False) as f2:
            f1.write(b"identical")
            f2.write(b"identical")
            f1.flush()
            f2.flush()
            assert compute_hash(Path(f1.name)) == compute_hash(Path(f2.name))

class TestVerifyHash:
    def test_verify_matching_hash(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            file_hash = compute_hash(Path(f.name))
            assert verify_hash(Path(f.name), file_hash) is True

    def test_verify_non_matching_hash(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            assert verify_hash(Path(f.name), "wrong_hash") is False

class TestComputeFileHashes:
    def test_compute_all_algorithms(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            hashes = compute_file_hashes(Path(f.name))
            assert "md5" in hashes
            assert "sha1" in hashes
            assert "sha256" in hashes

    def test_compute_all_algorithms_correctness(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"test data")
            f.flush()
            hashes = compute_file_hashes(Path(f.name))
            assert hashes["md5"] == hashlib.md5(b"test data").hexdigest()
            assert hashes["sha1"] == hashlib.sha1(b"test data").hexdigest()
            assert hashes["sha256"] == hashlib.sha256(b"test data").hexdigest()
