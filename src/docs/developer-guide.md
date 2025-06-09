# Ultrasonic Agentics - Developer Guide

A comprehensive guide for developers who want to contribute to the Ultrasonic Agentics project, a steganography framework for embedding and extracting agentic commands in audio and video media using ultrasonic frequencies.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Code Organization and Architecture](#code-organization-and-architecture)
3. [Contributing Guidelines and Workflow](#contributing-guidelines-and-workflow)
4. [Testing Framework](#testing-framework)
5. [Code Style and Formatting](#code-style-and-formatting)
6. [Pull Request Process](#pull-request-process)
7. [Issue Reporting Guidelines](#issue-reporting-guidelines)
8. [Development Tools and IDE Setup](#development-tools-and-ide-setup)
9. [Building and Packaging](#building-and-packaging)
10. [Release Process and Versioning](#release-process-and-versioning)
11. [Documentation Contribution](#documentation-contribution)
12. [Community Guidelines](#community-guidelines)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- FFmpeg (for audio/video processing)
- Virtual environment tools (venv, conda, or virtualenv)

### System Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-venv ffmpeg portaudio19-dev
```

#### macOS
```bash
brew install python ffmpeg portaudio
```

#### Windows
- Install Python from python.org
- Install FFmpeg from https://ffmpeg.org/download.html
- Add FFmpeg to your PATH

### Project Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ultrasonic-agentics/ultrasonic-agentics.git
   cd ultrasonic-agentics
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development-specific dependencies
   ```

4. **Install in development mode**
   ```bash
   pip install -e .
   ```

5. **Verify installation**
   ```bash
   python -m pytest tests/ -v
   ```

### Environment Variables

Create a `.env` file in the project root:
```bash
# Development settings
ULTRASONIC_DEBUG=true
ULTRASONIC_LOG_LEVEL=DEBUG

# API settings
API_HOST=localhost
API_PORT=8000

# Test settings
TEST_SAMPLE_RATE=48000
TEST_TIMEOUT=30
```

## Code Organization and Architecture

### Project Structure

```
agentic_commands_stego/
├── __init__.py                 # Package initialization and public API
├── requirements.txt            # Project dependencies
├── crypto/                     # Cryptographic services
│   ├── __init__.py
│   └── cipher.py              # AES-256-GCM encryption/decryption
├── embed/                      # Encoding implementations
│   ├── __init__.py
│   ├── ultrasonic_encoder.py  # Core FSK ultrasonic encoding
│   ├── audio_embedder.py      # High-level audio file processing
│   └── video_embedder.py      # Video steganography
├── decode/                     # Decoding implementations
│   ├── __init__.py
│   ├── ultrasonic_decoder.py  # Core FSK ultrasonic decoding
│   ├── audio_decoder.py       # High-level audio file processing
│   └── video_decoder.py       # Video steganography extraction
├── server/                     # REST API server
│   ├── __init__.py
│   └── api.py                 # FastAPI server implementation
├── tests/                      # Comprehensive test suite
│   ├── conftest.py            # Pytest configuration and fixtures
│   ├── test_*.py              # Individual test modules
│   └── ...
├── examples/                   # Usage examples and demos
│   ├── README.md
│   ├── basic_encoding.py
│   ├── audio_file_processing.py
│   └── api_client.py
└── docs/                      # Documentation
    ├── user-guide.md
    ├── api-reference.md
    ├── advanced-usage.md
    └── developer-guide.md
```

### Architecture Overview

The Ultrasonic Agentics framework follows a modular architecture with clear separation of concerns:

#### Core Components

1. **Ultrasonic Encoder/Decoder** (`embed/ultrasonic_encoder.py`, `decode/ultrasonic_decoder.py`)
   - Implements FSK (Frequency Shift Keying) modulation
   - Operates in 18-20 kHz frequency range
   - Handles bit-level encoding/decoding with preambles and checksums

2. **High-Level Audio/Video Processors** (`embed/audio_embedder.py`, `decode/audio_decoder.py`, etc.)
   - File I/O operations
   - Audio format conversion
   - Integration with multimedia libraries (pydub, moviepy)

3. **Cryptographic Layer** (`crypto/cipher.py`)
   - AES-256-GCM encryption for secure transmission
   - Key management and derivation
   - Authentication and integrity verification

4. **REST API Server** (`server/api.py`)
   - FastAPI-based HTTP interface
   - File upload/download endpoints
   - Asynchronous processing

#### Data Flow

```
Command → Encryption → Ultrasonic Encoding → Audio/Video Embedding → Output File
                                                                         ↓
Input File → Audio/Video Extraction → Ultrasonic Decoding → Decryption → Command
```

#### Key Design Patterns

- **Factory Pattern**: For creating encoder/decoder instances with different configurations
- **Strategy Pattern**: For swapping between different encoding algorithms
- **Observer Pattern**: For monitoring encoding/decoding progress
- **Dependency Injection**: For testing with mock components

### Module Dependencies

```python
# Core dependencies (required)
numpy>=1.21.0          # Numerical operations
scipy>=1.7.0           # Signal processing
pycryptodome>=3.15.0   # Cryptography

# Audio/Video processing
pydub>=0.25.1          # Audio manipulation
moviepy>=1.0.3         # Video processing
ffmpeg-python>=0.2.0   # FFmpeg integration
sounddevice>=0.4.4     # Real-time audio I/O

# Web API
fastapi>=0.68.0        # REST API framework
uvicorn>=0.15.0        # ASGI server
python-multipart>=0.0.5 # File upload support

# Testing
pytest>=6.2.4         # Test framework
pytest-mock>=3.6.1    # Mocking utilities
pytest-asyncio>=0.15.1 # Async test support
```

## Contributing Guidelines and Workflow

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes** following our coding standards
5. **Write tests** for new functionality
6. **Run the test suite** to ensure everything works
7. **Submit a pull request** with a clear description

### Branch Naming Convention

- `feature/description-of-feature` - New features
- `bugfix/description-of-bug` - Bug fixes
- `hotfix/critical-issue` - Critical production fixes
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring
- `test/test-improvements` - Test-related changes

### Commit Message Format

Follow the Conventional Commits specification:

```
type(scope): brief description

Detailed explanation of changes (if needed)

Fixes #issue-number
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes
- `ci`: CI/CD changes

Examples:
```
feat(encoder): add support for custom frequency ranges

Allows users to specify custom frequency pairs for FSK modulation,
enabling adaptation to different audio environments.

Fixes #123
```

### Code Review Process

1. **Self-review** your changes before submitting
2. **Ensure CI passes** - all tests and linting must pass
3. **Request review** from at least one maintainer
4. **Address feedback** promptly and thoroughly
5. **Squash commits** if requested before merge

### What to Contribute

**High Priority:**
- Bug fixes and security improvements
- Performance optimizations
- Documentation improvements
- Test coverage expansion
- Cross-platform compatibility

**Medium Priority:**
- New encoding algorithms
- Additional audio/video formats
- API enhancements
- Example applications

**Low Priority:**
- Refactoring for style
- Non-critical feature additions

## Testing Framework

### Test Structure

The project uses pytest with a comprehensive test suite organized by component:

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── test_ultrasonic_encoder.py     # Core encoder tests
├── test_ultrasonic_decoder.py     # Core decoder tests
├── test_audio_embedder.py         # Audio processing tests
├── test_cipher.py                 # Cryptography tests
├── test_integration.py            # End-to-end integration tests
├── test_calibration.py            # Frequency calibration tests
└── ...
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_ultrasonic_encoder.py

# Run tests with coverage
pytest --cov=agentic_commands_stego --cov-report=html

# Run only fast tests (exclude slow markers)
pytest -m "not slow"

# Run integration tests only
pytest -m integration

# Run tests in parallel
pytest -n auto
```

### Test Categories

Tests are marked with custom markers:

- `@pytest.mark.slow` - Long-running tests (>5 seconds)
- `@pytest.mark.integration` - End-to-end integration tests
- `@pytest.mark.video` - Tests requiring video processing
- `@pytest.mark.performance` - Performance benchmarking tests

### Writing Tests

#### Test Naming Convention
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

#### Example Test Structure
```python
"""
Tests for ultrasonic encoder functionality.
"""

import pytest
import numpy as np
from agentic_commands_stego.embed.ultrasonic_encoder import UltrasonicEncoder


class TestUltrasonicEncoder:
    """Test suite for UltrasonicEncoder."""
    
    def test_encoder_initializes_with_default_parameters(self):
        """Test that encoder initializes with expected defaults."""
        encoder = UltrasonicEncoder()
        assert encoder.freq_0 == 18500
        assert encoder.freq_1 == 19500
        assert encoder.sample_rate == 48000
    
    def test_encode_payload_returns_correct_length(self, test_payload):
        """Test that encoded payload has expected length."""
        encoder = UltrasonicEncoder()
        signal = encoder.encode_payload(test_payload)
        
        expected_bits = len(test_payload) * 8
        expected_samples = expected_bits * encoder.samples_per_bit
        
        assert len(signal) >= expected_samples
    
    @pytest.mark.slow
    def test_large_payload_encoding_performance(self):
        """Test encoding performance with large payloads."""
        encoder = UltrasonicEncoder()
        large_payload = b'x' * 10000  # 10KB payload
        
        import time
        start_time = time.time()
        signal = encoder.encode_payload(large_payload)
        end_time = time.time()
        
        assert end_time - start_time < 5.0  # Should complete in <5 seconds
        assert len(signal) > 0
```

#### Fixtures Usage
Use the shared fixtures from `conftest.py`:

```python
def test_cipher_encryption_roundtrip(cipher_service, test_payload):
    """Test encryption and decryption roundtrip."""
    encrypted = cipher_service.encrypt(test_payload)
    decrypted = cipher_service.decrypt(encrypted)
    assert decrypted == test_payload
```

### Test Data Management

- Use fixtures for consistent test data
- Store large test files in `tests/data/` (Git LFS recommended)
- Generate synthetic test data when possible
- Mock external dependencies (network, file system)

### Continuous Integration

Tests run automatically on:
- Pull request creation/updates
- Pushes to main branch
- Nightly builds for performance monitoring

CI pipeline includes:
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Multiple operating systems (Ubuntu, macOS, Windows)
- Code coverage reporting
- Security vulnerability scanning

## Code Style and Formatting

### Python Style Guide

Follow PEP 8 with these specific guidelines:

#### Code Formatting
- Use **Black** for automatic code formatting
- Line length: 88 characters (Black default)
- Use double quotes for strings
- Use trailing commas in multi-line structures

#### Import Organization
```python
# Standard library imports
import os
import sys
from typing import Optional, List, Dict

# Third-party imports
import numpy as np
import pytest
from fastapi import FastAPI

# Local imports
from ..crypto.cipher import CipherService
from .base import BaseEncoder
```

#### Naming Conventions
- **Classes**: PascalCase (`UltrasonicEncoder`)
- **Functions/methods**: snake_case (`encode_payload`)
- **Variables**: snake_case (`sample_rate`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_SAMPLE_RATE`)
- **Private methods**: Leading underscore (`_validate_input`)

#### Type Annotations
Use type hints for all public functions:

```python
def encode_payload(
    self, 
    payload: bytes, 
    add_preamble: bool = True
) -> np.ndarray:
    """
    Encode payload bytes into ultrasonic audio signal.
    
    Args:
        payload: Binary payload to encode
        add_preamble: Whether to add sync preamble
        
    Returns:
        NumPy array containing the encoded audio signal
        
    Raises:
        ValueError: If payload is empty or too large
    """
```

#### Documentation Strings
Use Google-style docstrings:

```python
class UltrasonicEncoder:
    """Encoder for embedding data in ultrasonic frequencies using FSK.
    
    This class implements Frequency Shift Keying (FSK) modulation to embed
    binary data in near-ultrasonic frequency ranges (18-20 kHz).
    
    Attributes:
        freq_0: Frequency for representing bit '0' in Hz
        freq_1: Frequency for representing bit '1' in Hz
        sample_rate: Audio sample rate in Hz
        
    Example:
        >>> encoder = UltrasonicEncoder(freq_0=18000, freq_1=19000)
        >>> signal = encoder.encode_payload(b"hello")
        >>> print(f"Encoded {len(signal)} samples")
    """
```

### Development Tools

#### Pre-commit Hooks
Install pre-commit hooks to automatically format and check code:

```bash
pip install pre-commit
pre-commit install
```

Configuration in `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

#### Code Quality Tools
```bash
# Format code
black agentic_commands_stego/

# Sort imports
isort agentic_commands_stego/

# Lint code
flake8 agentic_commands_stego/

# Type checking
mypy agentic_commands_stego/

# Security scanning
bandit -r agentic_commands_stego/
```

#### Editor Configuration
`.editorconfig`:
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.{yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
   ```bash
   pytest tests/ -v
   ```

2. **Run code quality checks**
   ```bash
   black --check agentic_commands_stego/
   flake8 agentic_commands_stego/
   mypy agentic_commands_stego/
   ```

3. **Update documentation** if needed

4. **Add/update tests** for new functionality

5. **Update CHANGELOG.md** for user-facing changes

### Pull Request Template

When creating a PR, use this template:

```markdown
## Description
Brief description of the changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding changes to documentation made
- [ ] No new warnings introduced

## Related Issues
Fixes #(issue number)

## Screenshots (if applicable)
Add screenshots to help explain your changes.
```

### Review Process

1. **Automated checks** must pass (CI, code quality)
2. **At least one review** required from a maintainer
3. **All conversations resolved** before merge
4. **Squash and merge** for feature branches
5. **Linear history** maintained on main branch

### Review Criteria

Reviewers will check for:
- **Correctness**: Does the code do what it's supposed to do?
- **Testing**: Are there adequate tests with good coverage?
- **Documentation**: Is the code well-documented?
- **Performance**: Are there any performance implications?
- **Security**: Are there any security concerns?
- **Maintainability**: Is the code easy to understand and maintain?

## Issue Reporting Guidelines

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** to ensure issue still exists
3. **Check documentation** for expected behavior
4. **Prepare minimal reproduction** case

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.5]
- Package version: [e.g. 1.0.0]
- Dependencies: [relevant package versions]

**Additional Context**
Add any other context about the problem here.

**Minimal Reproduction Code**
```python
# Minimal code to reproduce the issue
from agentic_commands_stego import UltrasonicEncoder

encoder = UltrasonicEncoder()
# ... rest of reproduction code
```

### Feature Requests

Use this template for feature requests:

```markdown
**Feature Description**
A clear and concise description of what you want to happen.

**Motivation**
Why would this feature be useful? What problem does it solve?

**Proposed Solution**
Describe the solution you'd like to see.

**Alternative Solutions**
Describe any alternative solutions or features you've considered.

**Additional Context**
Add any other context or screenshots about the feature request here.
```

### Issue Labels

Issues are tagged with labels for organization:

- **Type**: `bug`, `feature`, `documentation`, `question`
- **Priority**: `critical`, `high`, `medium`, `low`
- **Component**: `encoder`, `decoder`, `crypto`, `api`, `tests`
- **Status**: `needs-triage`, `confirmed`, `in-progress`, `blocked`
- **Difficulty**: `good-first-issue`, `help-wanted`, `expert-level`

## Development Tools and IDE Setup

### Recommended IDEs

#### Visual Studio Code
Install these extensions:
- Python (Microsoft)
- Python Docstring Generator
- Black Formatter
- isort
- Pylint
- MyPy Type Checker
- GitLens

`.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true
    }
}
```

#### PyCharm
1. Open project in PyCharm
2. Configure Python interpreter to virtual environment
3. Enable pytest as test runner
4. Configure code style to follow Black formatting
5. Enable type checking with MyPy

### Command Line Tools

#### Makefile Commands
```bash
# Setup development environment
make setup

# Run tests
make test

# Run all quality checks
make check

# Format code
make format

# Build documentation
make docs

# Clean build artifacts
make clean
```

#### Development Scripts
```bash
# Run development server
python -m agentic_commands_stego.server.api

# Run benchmarks
python scripts/benchmark.py

# Generate test coverage report
python scripts/coverage_report.py

# Profile performance
python scripts/profile.py
```

### Debugging Tools

#### Python Debugger
Use the built-in `pdb` or `ipdb` for debugging:

```python
import pdb; pdb.set_trace()  # Set breakpoint

# Or for IPython enhanced debugger
import ipdb; ipdb.set_trace()
```

#### Audio Analysis Tools
- **Audacity**: For visual audio analysis
- **SoX**: Command-line audio processing
- **FFmpeg**: Audio/video format conversion

```bash
# Analyze frequency content with FFmpeg
ffmpeg -i input.wav -af "showfreqs=mode=line:fscale=log" -f null -

# Generate spectrograms
ffmpeg -i input.wav -lavfi showspectrumpic=s=1024x512 spectrum.png
```

## Building and Packaging

### Local Development Build

```bash
# Install in development mode
pip install -e .

# Build wheel
python setup.py bdist_wheel

# Build source distribution
python setup.py sdist

# Build both
python setup.py sdist bdist_wheel
```

### Package Configuration

`setup.py` configuration:
```python
from setuptools import setup, find_packages

setup(
    name="ultrasonic-agentics",
    version="1.0.0",
    description="Steganography framework for ultrasonic agentic command transmission",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ultrasonic Agentics Team",
    author_email="contact@ultrasonic-agentics.org",
    url="https://github.com/ultrasonic-agentics/ultrasonic-agentics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pycryptodome>=3.15.0",
        # ... other dependencies
    ],
    extras_require={
        "audio": ["pydub>=0.25.1", "sounddevice>=0.4.4"],
        "video": ["moviepy>=1.0.3", "opencv-python>=4.5.0"],
        "server": ["fastapi>=0.68.0", "uvicorn>=0.15.0"],
        "dev": ["pytest>=6.2.4", "black>=22.3.0", "flake8>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "ultrasonic-agentics=agentic_commands_stego.cli:main",
        ],
    },
)
```

### Docker Support

`Dockerfile`:
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install package
RUN pip install -e .

# Expose API port
EXPOSE 8000

# Run server
CMD ["uvicorn", "agentic_commands_stego.server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  ultrasonic-agentics:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ULTRASONIC_DEBUG=false
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./data:/app/data
```

### Distribution

```bash
# Build for PyPI
python setup.py sdist bdist_wheel

# Check package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Release Process and Versioning

### Versioning Scheme

Follow Semantic Versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Types

#### Patch Release (1.0.0 → 1.0.1)
- Bug fixes
- Security patches
- Documentation updates
- Performance improvements

#### Minor Release (1.0.0 → 1.1.0)
- New features
- New APIs (non-breaking)
- Deprecation warnings
- Significant improvements

#### Major Release (1.0.0 → 2.0.0)
- Breaking API changes
- Removed deprecated features
- Major architectural changes
- Minimum version requirement changes

### Release Process

1. **Prepare Release**
   ```bash
   # Create release branch
   git checkout -b release/v1.2.0
   
   # Update version in __init__.py
   # Update CHANGELOG.md
   # Update documentation
   ```

2. **Test Release**
   ```bash
   # Run full test suite
   pytest tests/
   
   # Run integration tests
   pytest -m integration
   
   # Test package build
   python setup.py sdist bdist_wheel
   ```

3. **Create Release**
   ```bash
   # Commit changes
   git commit -m "chore: prepare release v1.2.0"
   
   # Merge to main
   git checkout main
   git merge release/v1.2.0
   
   # Tag release
   git tag -a v1.2.0 -m "Release v1.2.0"
   
   # Push to remote
   git push origin main --tags
   ```

4. **Publish Release**
   ```bash
   # Build packages
   python setup.py sdist bdist_wheel
   
   # Upload to PyPI
   twine upload dist/*
   
   # Create GitHub release
   gh release create v1.2.0 --title "v1.2.0" --notes-file CHANGELOG.md
   ```

### Changelog Format

Use Keep a Changelog format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature descriptions

### Changed
- Changes in existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Features removed in this version

### Fixed
- Bug fixes

### Security
- Security improvements

## [1.2.0] - 2023-12-01

### Added
- Support for custom frequency ranges in UltrasonicEncoder
- New calibration API endpoint
- Performance monitoring tools

### Fixed
- Memory leak in video processing
- Incorrect frequency detection in noisy environments

## [1.1.0] - 2023-11-15
...
```

### Pre-release Process

For beta/alpha releases:

```bash
# Tag pre-release
git tag v1.2.0-beta.1

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install and test
pip install --index-url https://test.pypi.org/simple/ ultrasonic-agentics==1.2.0b1
```

## Documentation Contribution

### Documentation Structure

```
docs/
├── user-guide.md          # End-user documentation
├── api-reference.md       # API documentation
├── advanced-usage.md      # Advanced tutorials
├── developer-guide.md     # This document
├── tutorials/             # Step-by-step tutorials
├── examples/              # Code examples
└── architecture/          # Technical architecture docs
```

### Writing Guidelines

#### Documentation Standards
- Use clear, concise language
- Include practical examples
- Provide code snippets that users can copy-paste
- Use consistent terminology
- Include cross-references to related sections

#### Markdown Style
- Use ATX-style headers (`# Header`)
- Include table of contents for long documents
- Use code fences with language specification
- Use descriptive link text
- Include alt text for images

#### Code Documentation
```python
def encode_payload(self, payload: bytes, add_preamble: bool = True) -> np.ndarray:
    """Encode payload bytes into ultrasonic audio signal.
    
    This method converts binary payload data into an ultrasonic audio signal
    using Frequency Shift Keying (FSK) modulation. The resulting signal can
    be embedded into audio files or transmitted in real-time.
    
    Args:
        payload: Binary data to encode. Maximum size depends on bit duration
            and target audio length. For 10ms bit duration, approximately
            100 bytes per second of audio.
        add_preamble: Whether to prepend a synchronization preamble to aid
            in detection and timing recovery. Recommended for most use cases.
            
    Returns:
        NumPy array containing the encoded audio signal as float32 values
        in the range [-1.0, 1.0]. Sample rate matches the encoder's 
        configured sample_rate.
        
    Raises:
        ValueError: If payload is empty or exceeds maximum encodable size.
        TypeError: If payload is not bytes-like object.
        
    Example:
        >>> encoder = UltrasonicEncoder(freq_0=18000, freq_1=19000)
        >>> command = b"execute:status_check"
        >>> signal = encoder.encode_payload(command)
        >>> print(f"Encoded {len(command)} bytes into {len(signal)} samples")
        Encoded 20 bytes into 9600 samples
        
    Note:
        The generated signal should be mixed with existing audio content
        rather than played alone, as ultrasonic frequencies may not be
        audible for verification.
    """
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build HTML documentation (if using Sphinx)
cd docs/
make html

# Serve documentation locally
python -m http.server 8080 -d _build/html/

# Build and check for warnings
make html SPHINXOPTS="-W"
```

### Documentation Review

Documentation changes should be reviewed for:
- **Accuracy**: Is the information correct?
- **Completeness**: Are all necessary details included?
- **Clarity**: Is it easy to understand?
- **Examples**: Are there sufficient code examples?
- **Structure**: Is the information well-organized?

## Community Guidelines

### Code of Conduct

#### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

#### Our Standards

**Examples of behavior that contributes to creating a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

#### Enforcement

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, questions
- **GitHub Discussions**: General discussions, ideas, Q&A
- **Discord**: Real-time chat and community support
- **Email**: Security issues, private concerns

### Getting Help

1. **Check documentation** first
2. **Search existing issues** on GitHub
3. **Ask in GitHub Discussions** for general questions
4. **Create an issue** for bugs or feature requests
5. **Join Discord** for real-time community support

### Recognition

Contributors are recognized through:
- **Contributors file** in the repository
- **Release notes** acknowledgments
- **GitHub contributor statistics**
- **Community highlights** in project updates

### Security

For security issues:
1. **Do not** create public issues
2. **Email** security@ultrasonic-agentics.org
3. **Include** detailed description and reproduction steps
4. **Wait** for response before public disclosure
5. **Follow** responsible disclosure guidelines

---

## Conclusion

This developer guide provides a comprehensive foundation for contributing to the Ultrasonic Agentics project. By following these guidelines, you'll help maintain code quality, project consistency, and a positive community environment.

For questions about this guide or the development process, please:
- Open an issue on GitHub
- Join our Discord community
- Contact the maintainers directly

Thank you for contributing to Ultrasonic Agentics!

---

**Last Updated:** December 2023  
**Version:** 1.0.0  
**Maintainers:** Ultrasonic Agentics Team