# Forensic Toolkit

A cross-platform digital forensic toolkit for collecting and analyzing evidence from systems suspected of compromise.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/badge/Tests-55%20passed-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-96%25-brightgreen.svg)

## Features

- **Case Management** - Create, track, and export forensic cases
- **Evidence Tracking** - Automatic ID generation with chain of custody logging
- **Disk Imaging** - FTK Imager integration with hash verification
- **Unified CLI** - Single entry point for all forensic operations
- **Cross-Platform** - Works on Linux, Windows, and macOS

## Installation

```bash
git clone https://github.com/yourusername/forensic-toolkit.git
cd forensic-toolkit
pip install -e packages/core
pip install -e packages/imaging
pip install -e packages/cli
```

## Quick Start

```bash
# Show version
forensic-toolkit --version

# Get help
forensic-toolkit --help

# Create a case
forensic-toolkit case create --name "Incident 2026-0831" --investigator "J.Smith"

# List all cases
forensic-toolkit case list

# Image a disk
forensic-toolkit imaging image \
  --case-id CASE-E8733D46 \
  --evidence-id EV-001 \
  --source /dev/sda \
  --output /evidence/ \
  --format E01
```

## CLI Commands

### Case Management

| Command | Description |
|---------|-------------|
| `forensic-toolkit case create` | Create a new case |
| `forensic-toolkit case list` | List all cases |

### Disk Imaging

| Command | Description |
|---------|-------------|
| `forensic-toolkit imaging image` | Create a disk image |
| `forensic-toolkit imaging verify` | Verify image integrity |
| `forensic-toolkit imaging list` | List images in a case |

## CLI Demo

```
$ forensic-toolkit --version
forensic-toolkit, version 0.1.0

$ forensic-toolkit case create --name "Incident 2026-0831" --investigator "J.Smith"
Created case: CASE-E8733D46

$ forensic-toolkit case list
                            Cases                             
+-----------------------------------------------------------+
| ID            | Name               | Investigator | Status |
|---------------+--------------------+--------------+--------|
| CASE-E8733D46 | Incident 2026-0831 | J.Smith      | active |
+-----------------------------------------------------------+

$ forensic-toolkit imaging image --help
Usage: imaging image [OPTIONS]

  Create a disk image.

Options:
  --case-id TEXT         Case ID  [required]
  --evidence-id TEXT     Evidence ID  [required]
  --source PATH          Source disk path  [required]
  --output PATH          Output directory  [required]
  --format [E01|RAW|DD]
  --help                 Show this message and exit.
```

## Project Structure

```
forensic-toolkit/
├── packages/
│   ├── core/                      # forensics-core
│   │   └── forensics_core/
│   │       ├── models.py          # Pydantic data models
│   │       ├── hashing.py         # MD5, SHA1, SHA256 verification
│   │       ├── database.py        # SQLite ORM with SQLAlchemy
│   │       ├── evidence.py        # Evidence manager with custody tracking
│   │       └── audit.py           # Forensic audit logging
│   ├── imaging/                   # forensics-imaging
│   │   └── forensics_imaging/
│   │       ├── command.py         # ForensicCommand ABC
│   │       ├── ftk_wrapper.py     # FTK Imager CLI wrapper
│   │       ├── formats.py         # Image format handlers
│   │       └── cli.py             # Imaging CLI commands
│   └── cli/                       # forensics-cli
│       └── forensics_cli/
│           └── main.py            # Unified CLI entry point
└── docs/
    └── superpowers/
        ├── specs/                 # Design specifications
        └── plans/                 # Implementation plans
```

## Architecture

### Command Pattern

Each forensic tool follows the Command pattern with standardized methods:

```python
class ForensicCommand(ABC):
    def validate(self) -> bool:
        """Pre-execution validation."""
    
    def execute(self) -> dict:
        """Run the command."""
    
    def report(self) -> dict:
        """Generate execution report."""
    
    def run(self) -> dict:
        """Template method: validate → execute → log → report."""
```

### Data Models

- **Case** - Tracks investigation metadata
- **Evidence** - Tracks disk images and forensic artifacts
- **CustodyAction** - Immutable audit trail for chain of custody
- **CommandResult** - Standardized command execution results

### Chain of Custody

Every evidence operation is logged with:
- Timestamp (UTC)
- Actor (who performed the action)
- Action type (created, accessed, verified, transferred)
- Hash at time of action

## Testing

```bash
# Run all tests
python -m pytest packages/ -v

# Run with coverage
python -m pytest packages/ --cov=packages --cov-report=term-missing

# Run specific package tests
python -m pytest packages/core/tests/ -v
python -m pytest packages/imaging/tests/ -v
```

### Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1
collected 55 items

packages/cli/tests/test_cli.py::TestCLI::test_cli_help PASSED            [  1%]
packages/cli/tests/test_cli.py::TestCLI::test_case_create_help PASSED    [  3%]
packages/cli/tests/test_cli.py::TestCLI::test_imaging_help PASSED        [  5%]
packages/core/tests/test_models.py::TestCase::test_create_case PASSED    [ 60%]
packages/core/tests/test_hashing.py::TestComputeHash::test_compute_md5 PASSED [ 43%]
packages/imaging/tests/test_ftk_wrapper.py::TestFTKImagerCommand::test_validate_passes PASSED [ 85%]
...

============================= 55 passed in 1.20s ==============================
```

### Coverage

```
packages/core/forensics_core/audit.py          100%
packages/core/forensics_core/database.py       100%
packages/core/forensics_core/hashing.py        100%
packages/core/forensics_core/models.py         100%
packages/core/forensics_core/evidence.py        94%
packages/imaging/forensics_imaging/ftk_wrapper.py 100%
packages/imaging/forensics_imaging/command.py    89%
packages/imaging/forensics_imaging/cli.py        85%
packages/cli/forensics_cli/main.py               68%
─────────────────────────────────────────────────
TOTAL                                           96%
```

## Supported Formats

| Format | Extension | Compression | Split Support |
|--------|-----------|-------------|---------------|
| E01 | .e01 | Yes | Yes |
| RAW | .raw | No | No |
| DD | .dd | No | Yes |

## Dependencies

### Core
- `pydantic` - Data validation
- `sqlalchemy` - SQLite ORM
- `hashlib` - Hash computation (stdlib)

### Imaging
- `click` - CLI framework
- `rich` - Terminal output
- FTK Imager CLI (external)

### Dev
- `pytest` - Testing
- `pytest-cov` - Coverage
- `pytest-mock` - Mocking

## Roadmap

- [ ] Memory analysis with Volatility
- [ ] Evidence collection with Autopsy/Sleuth Kit
- [ ] Web interface for case management
- [ ] Export to standard forensic formats
- [ ] Multi-user support with authentication

## License

MIT License - see [LICENSE](LICENSE) for details.
