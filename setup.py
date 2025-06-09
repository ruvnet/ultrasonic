#!/usr/bin/env python3
"""
Setup script for Ultrasonic Agentics

A comprehensive steganography framework for embedding and extracting agentic commands
in audio and video media using ultrasonic frequencies.
"""

from setuptools import setup, find_packages
import os
import re


def get_version():
    """Get version from __init__.py"""
    init_path = os.path.join('agentic_commands_stego', '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
            version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", content)
            if version_match:
                return version_match.group(1)
    return '1.0.1'


def get_long_description():
    """Get long description from README"""
    readme_path = os.path.join('agentic_commands_stego', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return """
Ultrasonic Agentics is a comprehensive steganography framework for embedding and extracting 
agentic commands in audio and video media using ultrasonic frequencies. This project provides 
tools for covert communication and command transmission through multimedia channels.
"""


def get_requirements():
    """Get requirements from requirements.txt"""
    req_path = os.path.join('agentic_commands_stego', 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Fallback requirements
    return [
        'numpy>=1.20.0',
        'scipy>=1.7.0',
        'pydub>=0.25.0',
        'cryptography>=3.4.0',
        'fastapi>=0.70.0',
        'uvicorn>=0.15.0',
        'python-multipart>=0.0.5',
        'librosa>=0.9.0',
        'opencv-python>=4.5.0'
    ]


# Package metadata
PACKAGE_NAME = "ultrasonic-agentics"
PACKAGE_DIR = "agentic_commands_stego"
VERSION = get_version()
DESCRIPTION = "Steganography framework for ultrasonic agentic command transmission"
LONG_DESCRIPTION = get_long_description()
AUTHOR = "Ultrasonic Agentics Team"
AUTHOR_EMAIL = "contact@ultrasonic-agentics.org"
URL = "https://github.com/ultrasonic-agentics/ultrasonic-agentics"
LICENSE = "MIT"

# Classifiers for PyPI
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio",
    "Topic :: Multimedia :: Video",
    "Topic :: Security :: Cryptography",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Keywords for PyPI search
KEYWORDS = [
    "steganography", "ultrasonic", "audio", "video", "agentic", "commands", 
    "covert", "communication", "frequency", "embedding", "extraction", 
    "cryptography", "security", "AI", "automation"
]

# Entry points for command-line tools
ENTRY_POINTS = {
    'console_scripts': [
        'ultrasonic-agentics=agentic_commands_stego.mcp_tools.cli:main',
        'ultrasonic-server=agentic_commands_stego.mcp_tools.server:run_server',
        'ultrasonic-api=agentic_commands_stego.server.api:main',
    ],
}

# Package data to include
PACKAGE_DATA = {
    PACKAGE_DIR: [
        'README.md',
        'requirements.txt',
        'docs/*.md',
        'examples/*.py',
        'examples/README.md',
        'tests/*.py',
    ]
}

# Additional data files
DATA_FILES = [
    ('share/ultrasonic-agentics/docs', [
        'agentic_commands_stego/docs/user-guide.md',
        'agentic_commands_stego/docs/api-reference.md',
        'agentic_commands_stego/docs/advanced-usage.md',
    ]),
    ('share/ultrasonic-agentics/examples', [
        'agentic_commands_stego/examples/basic_encoding.py',
        'agentic_commands_stego/examples/audio_file_processing.py',
        'agentic_commands_stego/examples/api_client.py',
        'agentic_commands_stego/examples/README.md',
    ]),
]

# Development dependencies
EXTRAS_REQUIRE = {
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.12.0',
        'pytest-asyncio>=0.15.0',
        'black>=21.0.0',
        'flake8>=3.9.0',
        'mypy>=0.910',
        'isort>=5.9.0',
        'pre-commit>=2.15.0',
    ],
    'docs': [
        'sphinx>=4.0.0',
        'sphinx-rtd-theme>=0.5.0',
        'myst-parser>=0.15.0',
    ],
    'examples': [
        'matplotlib>=3.3.0',
        'jupyter>=1.0.0',
        'ipython>=7.0.0',
    ],
    'performance': [
        'numba>=0.54.0',
        'cython>=0.29.0',
    ],
    'all': [
        # Includes all optional dependencies
        'pytest>=6.0.0', 'pytest-cov>=2.12.0', 'pytest-asyncio>=0.15.0',
        'black>=21.0.0', 'flake8>=3.9.0', 'mypy>=0.910', 'isort>=5.9.0',
        'sphinx>=4.0.0', 'sphinx-rtd-theme>=0.5.0', 'myst-parser>=0.15.0',
        'matplotlib>=3.3.0', 'jupyter>=1.0.0', 'ipython>=7.0.0',
        'numba>=0.54.0', 'cython>=0.29.0', 'pre-commit>=2.15.0',
    ]
}

# Python version requirement
PYTHON_REQUIRES = ">=3.8"

# Project URLs for PyPI
PROJECT_URLS = {
    "Homepage": URL,
    "Documentation": f"{URL}/docs",
    "Repository": URL,
    "Bug Tracker": f"{URL}/issues",
    "Changelog": f"{URL}/blob/main/CHANGELOG.md",
    "Examples": f"{URL}/tree/main/agentic_commands_stego/examples",
}

# Setup configuration
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    
    # Package discovery
    packages=find_packages(include=[PACKAGE_DIR, f"{PACKAGE_DIR}.*"]),
    package_data=PACKAGE_DATA,
    data_files=DATA_FILES,
    include_package_data=True,
    zip_safe=False,
    
    # Dependencies
    python_requires=PYTHON_REQUIRES,
    install_requires=get_requirements(),
    extras_require=EXTRAS_REQUIRE,
    
    # Entry points
    entry_points=ENTRY_POINTS,
    
    # PyPI metadata
    classifiers=CLASSIFIERS,
    keywords=", ".join(KEYWORDS),
    
    # Additional metadata
    platforms=["any"],
    
    # Options
    options={
        'build_py': {
            'compile': True,
            'optimize': 1,
        },
        'bdist_wheel': {
            'universal': False,
        },
    },
)

# Print installation instructions
if __name__ == '__main__':
    print(f"""
Ultrasonic Agentics v{VERSION}
{'=' * 50}

Installation modes:

# Basic installation:
pip install {PACKAGE_NAME}

# Development installation:
pip install {PACKAGE_NAME}[dev]

# Full installation with all features:
pip install {PACKAGE_NAME}[all]

# From source (development):
git clone {URL}
cd ultrasonic-agentics
pip install -e .[dev]

Command-line tools available after installation:
- ultrasonic-agentics  : Main CLI with embed/decode/analyze/config commands
- ultrasonic-server    : Start MCP server for protocol communication  
- ultrasonic-api       : Start HTTP API server

For documentation and examples:
https://github.com/ultrasonic-agentics/ultrasonic-agentics/docs

""")