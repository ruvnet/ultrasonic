"""
Ultrasonic Agentics - Steganography Framework for Agentic Command Transmission

A comprehensive framework for embedding and extracting agentic commands in audio and video
media using ultrasonic frequencies and advanced steganographic techniques.

Key Features:
- Ultrasonic frequency encoding/decoding (FSK modulation)
- Video steganography using LSB techniques  
- Cryptographic security with AES-256-GCM encryption
- RESTful API for remote operations
- Real-time audio processing capabilities
- Comprehensive error correction and detection

Modules:
- embed: Encoding implementations for audio and video
- decode: Decoding implementations for audio and video
- crypto: Cryptographic services and key management
- server: HTTP API server for remote operations
- tests: Comprehensive test suite

Usage:
    Basic encoding/decoding:
    >>> from ultrasonic_agentics.embed import UltrasonicEncoder
    >>> from ultrasonic_agentics.decode import UltrasonicDecoder
    >>> 
    >>> encoder = UltrasonicEncoder()
    >>> decoder = UltrasonicDecoder()
    >>> 
    >>> command = "execute:status_check"
    >>> signal = encoder.encode_payload(command.encode())
    >>> decoded = decoder.decode_payload(signal)
    >>> print(decoded.decode('utf-8'))

    API server:
    >>> from ultrasonic_agentics.server.api import app
    >>> import uvicorn
    >>> uvicorn.run(app, host="0.0.0.0", port=8000)

Author: Ultrasonic Agentics Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Ultrasonic Agentics Team"
__email__ = "contact@ultrasonic-agentics.org"
__license__ = "MIT"
__url__ = "https://github.com/ultrasonic-agentics/ultrasonic-agentics"

# Version info tuple
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Package metadata
__title__ = "ultrasonic-agentics"
__description__ = "Steganography framework for ultrasonic agentic command transmission"
__keywords__ = [
    "steganography", "ultrasonic", "audio", "video", "agentic", "commands",
    "covert", "communication", "frequency", "embedding", "extraction"
]

# Import main classes for convenience
try:
    from .embed.ultrasonic_encoder import UltrasonicEncoder
    from .decode.ultrasonic_decoder import UltrasonicDecoder
    from .crypto.cipher import CipherService
    
    # Optional imports (may not be available in all environments)
    try:
        from .embed.audio_embedder import AudioEmbedder
        from .embed.video_embedder import VideoEmbedder
        from .decode.audio_decoder import AudioDecoder
        from .decode.video_decoder import VideoDecoder
    except ImportError:
        # These require additional dependencies
        pass
    
except ImportError as e:
    # Handle missing dependencies gracefully
    import warnings
    warnings.warn(f"Some modules could not be imported: {e}")

# Public API
__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "__url__",
    "VERSION_INFO",
    
    # Core classes
    "UltrasonicEncoder",
    "UltrasonicDecoder", 
    "CipherService",
    
    # High-level interfaces (if available)
    "AudioEmbedder",
    "VideoEmbedder",
    "AudioDecoder",
    "VideoDecoder",
]

# Configuration defaults
DEFAULT_CONFIG = {
    "ultrasonic": {
        "freq_0": 18500,
        "freq_1": 19500,
        "sample_rate": 48000,
        "bit_duration": 0.01,
        "amplitude": 0.1,
        "detection_threshold": 0.1
    },
    "crypto": {
        "algorithm": "AES-256-GCM",
        "key_length": 32
    },
    "server": {
        "host": "localhost",
        "port": 8000,
        "debug": False
    }
}

def get_version():
    """Get the current version string."""
    return __version__

def get_version_info():
    """Get version info as a tuple."""
    return VERSION_INFO

def get_config():
    """Get default configuration dictionary."""
    return DEFAULT_CONFIG.copy()

def check_dependencies():
    """Check if all dependencies are available."""
    missing_deps = []
    optional_deps = []
    
    # Core dependencies
    core_deps = {
        'numpy': 'numpy',
        'scipy': 'scipy', 
        'cryptography': 'cryptography'
    }
    
    # Optional dependencies
    opt_deps = {
        'pydub': 'pydub',
        'librosa': 'librosa',
        'opencv-python': 'cv2',
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn'
    }
    
    # Check core dependencies
    for name, import_name in core_deps.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_deps.append(name)
    
    # Check optional dependencies
    for name, import_name in opt_deps.items():
        try:
            __import__(import_name)
        except ImportError:
            optional_deps.append(name)
    
    return {
        'missing_required': missing_deps,
        'missing_optional': optional_deps,
        'all_available': len(missing_deps) == 0
    }

# Module initialization
def _initialize_module():
    """Initialize the module and check dependencies."""
    deps = check_dependencies()
    
    if deps['missing_required']:
        import warnings
        warnings.warn(
            f"Missing required dependencies: {', '.join(deps['missing_required'])}. "
            f"Install with: pip install {' '.join(deps['missing_required'])}"
        )
    
    if deps['missing_optional']:
        import warnings
        warnings.warn(
            f"Missing optional dependencies: {', '.join(deps['missing_optional'])}. "
            f"Some features may be unavailable. Install with: pip install {' '.join(deps['missing_optional'])}"
        )

# Initialize on import
_initialize_module()