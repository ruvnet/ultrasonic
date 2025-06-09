#!/usr/bin/env python3
"""
Simple test to check if our preamble detection fix works.
"""

import sys
sys.path.append('.')

import numpy as np
from .embed.ultrasonic_encoder import UltrasonicEncoder
from .decode.ultrasonic_decoder import UltrasonicDecoder

def simple_test():
    print("=== SIMPLE PREAMBLE TEST ===")
    
    # Create encoder and decoder
    encoder = UltrasonicEncoder(amplitude=0.8, bit_duration=0.05)
    decoder = UltrasonicDecoder(detection_threshold=0.001, bit_duration=0.05)
    
    print(f"Encoder parameters: freq_0={encoder.freq_0}, freq_1={encoder.freq_1}")
    print(f"Decoder threshold: {decoder.detection_threshold}")
    
    # Generate just the preamble
    preamble_pattern = encoder._generate_preamble()
    preamble_signal = encoder._generate_fsk_signal(preamble_pattern)
    
    print(f"Preamble pattern: '{preamble_pattern}' ({len(preamble_pattern)} bits)")
    print(f"Signal length: {len(preamble_signal)} samples")
    
    # Apply filtering
    filtered_signal = decoder._apply_bandpass_filter(preamble_signal)
    print(f"Filtered signal max: {np.max(np.abs(filtered_signal)):.3f}")
    
    # Test preamble detection
    detected_pos = decoder._detect_preamble(filtered_signal)
    expected_pos = len(preamble_pattern) * encoder.samples_per_bit
    
    print(f"Expected position: {expected_pos}")
    print(f"Detected position: {detected_pos}")
    
    if detected_pos is not None:
        print("✅ PREAMBLE DETECTION SUCCESS!")
        return True
    else:
        print("❌ PREAMBLE DETECTION FAILED!")
        
        # Debug the loop
        pattern_length = len(preamble_pattern) * encoder.samples_per_bit
        step_size = max(1, encoder.samples_per_bit // 8)
        max_start_pos = max(1, len(filtered_signal) - pattern_length + 1)
        
        print(f"\nDebug info:")
        print(f"  Pattern length: {pattern_length}")
        print(f"  Signal length: {len(filtered_signal)}")
        print(f"  Step size: {step_size}")
        print(f"  Max start pos: {max_start_pos}")
        print(f"  Range would be: 0 to {max_start_pos} step {step_size}")
        
        if max_start_pos > 0:
            # Test the first position manually
            segment = filtered_signal[:pattern_length]
            freq_sequence = []
            for bit in preamble_pattern:
                if bit == '0':
                    freq_sequence.append(encoder.freq_0)
                else:
                    freq_sequence.append(encoder.freq_1)
            
            correlation = decoder._correlate_with_pattern(segment, freq_sequence)
            print(f"  Manual correlation at pos 0: {correlation:.6f}")
            print(f"  Above threshold? {correlation > decoder.detection_threshold}")
        
        return False

if __name__ == "__main__":
    success = simple_test()
    sys.exit(0 if success else 1)