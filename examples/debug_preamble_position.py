#!/usr/bin/env python3
"""
Debug preamble position detection.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.embed.ultrasonic_encoder import UltrasonicEncoder
from src.decode.ultrasonic_decoder import UltrasonicDecoder
from pydub import AudioSegment
import numpy as np

def main():
    print("=" * 60)
    print("PREAMBLE POSITION DEBUG")
    print("=" * 60)
    
    # Create a simple test case with known data
    encoder = UltrasonicEncoder(amplitude=0.5, bit_duration=0.01)
    decoder = UltrasonicDecoder(detection_threshold=0.001, bit_duration=0.01)
    
    # Create a simple bit pattern after preamble
    test_bits = "101010101111000010101010" + "11110000" * 10  # Preamble + test pattern
    print(f"Test pattern: {test_bits[:50]}...")
    
    # Generate signal
    signal = encoder._generate_fsk_signal(test_bits)
    
    # Apply bandpass filter
    filtered = decoder._apply_bandpass_filter(signal)
    
    # Find preamble
    preamble_pos = decoder._detect_preamble(filtered)
    print(f"\nPreamble found at: {preamble_pos} samples")
    print(f"Expected at: {24 * encoder.samples_per_bit} samples")
    
    if preamble_pos:
        # Extract a few bits after preamble
        print("\nExtracting bits after preamble:")
        position = preamble_pos
        for i in range(10):
            if position + decoder.samples_per_bit <= len(filtered):
                segment = filtered[position:position + decoder.samples_per_bit]
                
                # Calculate power for both frequencies
                t = np.linspace(0, decoder.bit_duration, len(segment), endpoint=False)
                ref_0 = np.sin(2 * np.pi * decoder.freq_0 * t)
                ref_1 = np.sin(2 * np.pi * decoder.freq_1 * t)
                
                power_0 = np.abs(np.dot(segment, ref_0))
                power_1 = np.abs(np.dot(segment, ref_1))
                
                bit = '0' if power_0 > power_1 else '1'
                confidence = abs(power_0 - power_1) / (power_0 + power_1) if (power_0 + power_1) > 0 else 0
                
                print(f"  Bit {i}: '{bit}' (power_0={power_0:.1f}, power_1={power_1:.1f}, conf={confidence:.3f})")
                
                position += decoder.samples_per_bit
    
    # Now test with actual embedding
    print("\n" + "=" * 60)
    print("TESTING WITH ACTUAL EMBEDDING")
    print("=" * 60)
    
    test_key = b'HelloWorldDemoKey' + b'0' * 15
    embedder = AudioEmbedder(key=test_key, amplitude=0.5, bit_duration=0.01)
    decoder = AudioDecoder(key=test_key, detection_threshold=0.001, bit_duration=0.01)
    
    # Create a WAV file to avoid MP3 compression
    success = embedder.embed_file(
        'sample_audio.mp3',
        'debug_preamble.wav',
        'TEST'
    )
    print(f"Embedding success: {success}")
    
    # Load and analyze
    audio = AudioSegment.from_file('debug_preamble.wav')
    audio = audio.set_channels(1).set_frame_rate(48000)
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Check signal power
    ultrasonic_decoder = decoder.decoder
    filtered_signal = ultrasonic_decoder._apply_bandpass_filter(audio_data)
    
    print(f"\nSignal analysis:")
    print(f"  Original max amplitude: {np.max(np.abs(audio_data)):.3f}")
    print(f"  Filtered max amplitude: {np.max(np.abs(filtered_signal)):.3f}")
    
    # Check frequency content
    fft = np.fft.fft(filtered_signal[:48000])  # First second
    freqs = np.fft.fftfreq(48000, 1/48000)
    magnitude = np.abs(fft)
    
    # Find peaks
    freq_0_idx = np.argmin(np.abs(freqs - 18500))
    freq_1_idx = np.argmin(np.abs(freqs - 19500))
    
    print(f"  Power at 18500 Hz: {magnitude[freq_0_idx]:.1f}")
    print(f"  Power at 19500 Hz: {magnitude[freq_1_idx]:.1f}")
    
    # Clean up
    os.remove('debug_preamble.wav')

if __name__ == "__main__":
    main()