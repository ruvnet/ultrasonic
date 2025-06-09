"""Embedding modules for steganographic command insertion."""

from .audio_embedder import AudioEmbedder
from .ultrasonic_encoder import UltrasonicEncoder

# Video embedder is optional (requires moviepy)
try:
    from .video_embedder import VideoEmbedder
    __all__ = ['AudioEmbedder', 'VideoEmbedder', 'UltrasonicEncoder']
except ImportError:
    __all__ = ['AudioEmbedder', 'UltrasonicEncoder']