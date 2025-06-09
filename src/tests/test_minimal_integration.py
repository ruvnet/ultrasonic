"""
Minimal integration test to debug the core issue.
"""

import pytest
from pydub import AudioSegment
from ..embed.audio_embedder import AudioEmbedder
from ..decode.audio_decoder import AudioDecoder
from ..crypto.cipher import CipherService


def test_minimal_roundtrip():
    """Test the absolute minimal roundtrip case."""
    # Use same key
    key = CipherService.generate_key(32)
    embedder = AudioEmbedder(key=key, amplitude=1.0, bit_duration=0.1)
    decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.1)
    
    # Very short command
    command = "HI"
    
    # Long audio to ensure signal fits
    test_audio = AudioSegment.silent(duration=20000, frame_rate=48000)
    
    # Embed
    stego_audio = embedder.embed(test_audio, command)
    
    # Decode
    decoded_command = decoder.decode_audio_segment(stego_audio)
    
    assert decoded_command == command, f"Expected '{command}', got '{decoded_command}'"


def test_without_encryption():
    """Test without encryption to isolate FSK issues."""
    from ..embed.ultrasonic_encoder import UltrasonicEncoder
    from ..decode.ultrasonic_decoder import UltrasonicDecoder
    
    encoder = UltrasonicEncoder(amplitude=1.0, bit_duration=0.1)
    decoder = UltrasonicDecoder(detection_threshold=0.001, bit_duration=0.1)
    
    # Simple payload
    test_payload = b"TEST"
    
    # Encode and decode
    signal = encoder.encode_payload(test_payload)
    decoded_payload = decoder.decode_payload(signal)
    
    assert decoded_payload == test_payload, f"Expected {test_payload}, got {decoded_payload}"


if __name__ == "__main__":
    test_without_encryption()
    print("✅ FSK test passed")
    
    test_minimal_roundtrip()
    print("✅ Full integration test passed")