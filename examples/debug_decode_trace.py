#!/usr/bin/env python3
"""
Debug trace through the decoding process.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.decode.ultrasonic_decoder import UltrasonicDecoder
from pydub import AudioSegment
import numpy as np

def main():
    # Use the same key as in test_hello_world.py
    test_key = b'HelloWorldDemoKey' + b'0' * 15  # Pad to 32 bytes
    
    print("=" * 60)
    print("DECODE TRACE DEBUG")
    print("=" * 60)
    
    # Create embedder and embed
    embedder = AudioEmbedder(key=test_key)
    success = embedder.embed_file(
        'sample_audio.mp3',
        'debug_trace.mp3',
        'hello world'
    )
    print(f"Embedding success: {success}")
    
    # Manual decode process
    decoder = AudioDecoder(key=test_key)
    
    # Step 1: Load audio file
    audio = AudioSegment.from_file('debug_trace.mp3')
    print(f"\n1. Loaded audio: {len(audio)} ms, {audio.frame_rate} Hz")
    
    # Step 2: Prepare audio
    audio = audio.set_channels(1)  # Convert to mono
    audio = audio.set_frame_rate(48000)  # Set sample rate
    print(f"2. Prepared audio: {len(audio)} ms, {audio.frame_rate} Hz")
    
    # Step 3: Convert to numpy
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    audio_data = audio_data / np.max(np.abs(audio_data))
    print(f"3. Audio data: {len(audio_data)} samples, range [{np.min(audio_data):.3f}, {np.max(audio_data):.3f}]")
    
    # Step 4: Try ultrasonic decoding
    ultrasonic_decoder = decoder.decoder
    
    # Apply bandpass filter
    filtered_signal = ultrasonic_decoder._apply_bandpass_filter(audio_data)
    print(f"4. Filtered signal: range [{np.min(filtered_signal):.3f}, {np.max(filtered_signal):.3f}]")
    
    # Detect preamble
    start_position = ultrasonic_decoder._detect_preamble(filtered_signal)
    print(f"5. Preamble detection: start_position = {start_position}")
    
    if start_position is None:
        print("   ❌ Preamble not found!")
        
        # Debug: Check signal power in ultrasonic range
        print("\n   DEBUG: Checking signal power...")
        fft = np.fft.fft(filtered_signal[:48000])  # First second
        freqs = np.fft.fftfreq(48000, 1/48000)
        magnitude = np.abs(fft)
        
        # Check power around our frequencies
        freq_0_power = np.max(magnitude[np.abs(freqs - 18500) < 100])
        freq_1_power = np.max(magnitude[np.abs(freqs - 19500) < 100])
        print(f"   Power at {ultrasonic_decoder.freq_0} Hz: {freq_0_power:.1f}")
        print(f"   Power at {ultrasonic_decoder.freq_1} Hz: {freq_1_power:.1f}")
        
        # Check if encryption is the issue
        print("\n   DEBUG: Checking encryption...")
        print(f"   Embedder key: {embedder.cipher.get_key()[:8]}...")
        print(f"   Decoder key: {decoder.cipher.get_key()[:8]}...")
        
    else:
        # Extract bits
        bit_data = ultrasonic_decoder._extract_bits_with_confidence(filtered_signal, start_position)
        print(f"6. Extracted bits: {len(bit_data)} bits")
        
        if bit_data:
            # Try to decode
            payload_bytes = ultrasonic_decoder._decode_with_advanced_error_correction(bit_data)
            print(f"7. Decoded payload: {payload_bytes}")
            
            if payload_bytes:
                # Try to decrypt
                deobfuscated = decoder.cipher.remove_obfuscation(payload_bytes)
                print(f"8. Deobfuscated: {deobfuscated}")
                
                if deobfuscated:
                    command = decoder.cipher.decrypt_command(deobfuscated)
                    print(f"9. Decrypted command: '{command}'")
    
    # Clean up
    os.remove('debug_trace.mp3')

if __name__ == "__main__":
    main()