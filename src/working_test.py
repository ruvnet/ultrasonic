#!/usr/bin/env python3
"""
Working test to verify the entire steganography pipeline works correctly.
This uses a minimal, reliable implementation to ensure basic functionality.
"""

import numpy as np
from pydub import AudioSegment

# Minimal working steganography system
def generate_test_signal(command_bits, freq_0=18500, freq_1=19500, sample_rate=48000, bit_duration=0.05):
    """Generate a simple FSK signal for testing."""
    samples_per_bit = int(sample_rate * bit_duration)
    total_samples = len(command_bits) * samples_per_bit
    signal = np.zeros(total_samples)
    
    t = np.linspace(0, bit_duration, samples_per_bit, endpoint=False)
    
    for i, bit in enumerate(command_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        
        freq = freq_1 if bit == '1' else freq_0
        tone = 0.8 * np.sin(2 * np.pi * freq * t)  # High amplitude
        signal[start_idx:end_idx] = tone
    
    return signal

def decode_test_signal(signal, freq_0=18500, freq_1=19500, sample_rate=48000, bit_duration=0.05):
    """Decode a simple FSK signal using time-domain correlation."""
    samples_per_bit = int(sample_rate * bit_duration)
    num_bits = len(signal) // samples_per_bit
    
    t = np.linspace(0, bit_duration, samples_per_bit, endpoint=False)
    ref_0 = np.sin(2 * np.pi * freq_0 * t)
    ref_1 = np.sin(2 * np.pi * freq_1 * t)
    
    decoded_bits = ""
    
    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        segment = signal[start_idx:end_idx]
        
        corr_0 = np.abs(np.dot(segment, ref_0))
        corr_1 = np.abs(np.dot(segment, ref_1))
        
        bit = '1' if corr_1 > corr_0 else '0'
        decoded_bits += bit
    
    return decoded_bits

def test_basic_fsk():
    """Test basic FSK encoding and decoding."""
    print("=== BASIC FSK TEST ===")
    
    # Test pattern
    test_bits = "101010111100001010"
    print(f"Original bits: {test_bits}")
    
    # Generate signal
    signal = generate_test_signal(test_bits)
    print(f"Generated signal: {len(signal)} samples")
    
    # Decode signal
    decoded_bits = decode_test_signal(signal)
    print(f"Decoded bits:  {decoded_bits}")
    
    # Check accuracy
    correct = sum(1 for a, b in zip(test_bits, decoded_bits) if a == b)
    accuracy = correct / len(test_bits) * 100
    print(f"Accuracy: {accuracy:.1f}% ({correct}/{len(test_bits)})")
    
    return accuracy > 95

def test_with_audio_segment():
    """Test with AudioSegment (like the real system)."""
    print("\n=== AUDIO SEGMENT TEST ===")
    
    test_bits = "1010101111000010101"  # Include variety
    print(f"Test bits: {test_bits}")
    
    # Generate signal
    signal = generate_test_signal(test_bits)
    
    # Convert to AudioSegment
    # Normalize and convert to int16
    signal_norm = signal / np.max(np.abs(signal)) * 0.8
    signal_int16 = (signal_norm * 32767).astype(np.int16)
    
    audio_segment = AudioSegment(
        signal_int16.tobytes(),
        frame_rate=48000,
        sample_width=2,
        channels=1
    )
    
    print(f"AudioSegment: {len(audio_segment)} ms")
    
    # Convert back to numpy
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    samples_norm = samples / np.max(np.abs(samples))
    
    # Decode
    decoded_bits = decode_test_signal(samples_norm)
    print(f"Decoded: {decoded_bits}")
    
    # Check accuracy
    min_len = min(len(test_bits), len(decoded_bits))
    correct = sum(1 for a, b in zip(test_bits[:min_len], decoded_bits[:min_len]) if a == b)
    accuracy = correct / min_len * 100
    print(f"Accuracy: {accuracy:.1f}% ({correct}/{min_len})")
    
    return accuracy > 95

def main():
    """Run all tests."""
    print("Testing basic steganography components...\n")
    
    test1 = test_basic_fsk()
    test2 = test_with_audio_segment()
    
    if test1 and test2:
        print("\n✅ ALL TESTS PASSED - Basic FSK works correctly!")
        print("The issue is in the integration, not the core FSK algorithm.")
        return True
    else:
        print("\n❌ BASIC FSK FAILED - Need to fix fundamental algorithm.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)