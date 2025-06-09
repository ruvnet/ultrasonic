"""
Simple calibration test to quickly identify the issue.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from pydub import AudioSegment
from agentic_commands_stego.embed.audio_embedder import AudioEmbedder
from agentic_commands_stego.decode.audio_decoder import AudioDecoder
from agentic_commands_stego.crypto.cipher import CipherService


def test_basic_roundtrip():
    """Test basic encoding and decoding with debug output."""
    key = CipherService.generate_key(32)
    test_command = "TEST"
    
    # Use higher amplitude and lower threshold
    embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
    decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
    
    # Create test audio
    test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
    
    print(f"\n1. Original command: {test_command}")
    
    # Embed
    stego_audio = embedder.embed(test_audio, test_command)
    print(f"2. Embedded audio length: {len(stego_audio)} ms")
    
    # Check if signal exists
    audio_data = np.array(stego_audio.get_array_of_samples(), dtype=np.float32)
    max_val = np.max(np.abs(audio_data))
    print(f"3. Max signal amplitude: {max_val}")
    
    # Decode with debug
    decoded = decoder.decode_audio_segment(stego_audio)
    print(f"4. Decoded command: {decoded}")
    
    # Check signal detection
    if max_val > 0:
        audio_data = audio_data / max_val
    detected = decoder.decoder.detect_signal_presence(audio_data)
    print(f"5. Signal detected: {detected}")
    
    # Get signal strength
    strength = decoder.decoder.get_signal_strength(audio_data)
    print(f"6. Signal strength: {strength}")
    
    # Try manual decode
    payload = decoder.decoder.decode_payload(audio_data)
    print(f"7. Raw payload bytes: {payload}")
    
    return decoded == test_command


def test_encoder_decoder_sync():
    """Test that encoder and decoder parameters match."""
    from agentic_commands_stego.embed.ultrasonic_encoder import UltrasonicEncoder
    from agentic_commands_stego.decode.ultrasonic_decoder import UltrasonicDecoder
    
    encoder = UltrasonicEncoder()
    decoder = UltrasonicDecoder()
    
    print(f"\nEncoder parameters:")
    print(f"  freq_0: {encoder.freq_0}")
    print(f"  freq_1: {encoder.freq_1}")
    print(f"  sample_rate: {encoder.sample_rate}")
    print(f"  bit_duration: {encoder.bit_duration}")
    print(f"  amplitude: {encoder.amplitude}")
    
    print(f"\nDecoder parameters:")
    print(f"  freq_0: {decoder.freq_0}")
    print(f"  freq_1: {decoder.freq_1}")
    print(f"  sample_rate: {decoder.sample_rate}")
    print(f"  bit_duration: {decoder.bit_duration}")
    print(f"  detection_threshold: {decoder.detection_threshold}")
    
    assert encoder.freq_0 == decoder.freq_0
    assert encoder.freq_1 == decoder.freq_1
    assert encoder.sample_rate == decoder.sample_rate
    assert encoder.bit_duration == decoder.bit_duration


if __name__ == "__main__":
    print("Running basic roundtrip test...")
    success = test_basic_roundtrip()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
    
    print("\n" + "="*50)
    print("Checking encoder/decoder sync...")
    test_encoder_decoder_sync()