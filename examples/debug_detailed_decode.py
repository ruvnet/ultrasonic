#!/usr/bin/env python3
"""
Detailed debug of the decoding process.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder
from src.decode.ultrasonic_decoder import UltrasonicDecoder
from src.crypto.cipher import CipherService
from pydub import AudioSegment
import numpy as np

def decode_with_logging(decoder, bit_data):
    """Decode with detailed logging."""
    print(f"\nDecoding {len(bit_data)} bits...")
    
    if len(bit_data) < 48:
        print("ERROR: Not enough bits for length prefix")
        return None
    
    # Convert to bit string
    bit_string = ''.join(bit for bit, _ in bit_data)
    print(f"Raw bit string (first 120 bits): {bit_string[:120]}")
    
    # Apply majority voting on repeated bits
    decoded_bits = ""
    for i in range(0, len(bit_string), 3):
        if i + 2 < len(bit_string):
            bit_votes = bit_string[i:i+3]
            ones = bit_votes.count('1')
            zeros = bit_votes.count('0')
            if ones > zeros:
                decoded_bits += '1'
            else:
                decoded_bits += '0'
    
    print(f"After majority voting: {len(decoded_bits)} bits")
    print(f"Decoded bits (first 40): {decoded_bits[:40]}")
    
    # Extract 16-bit length prefix
    length_bits = decoded_bits[:16]
    print(f"Length prefix bits: {length_bits}")
    
    try:
        payload_length = int(length_bits, 2)
        print(f"Payload length: {payload_length} bits")
    except:
        print("ERROR: Invalid length prefix")
        return None
    
    # Validate length
    if payload_length == 0 or payload_length > len(decoded_bits) - 16:
        print(f"ERROR: Invalid payload length {payload_length} (available: {len(decoded_bits) - 16})")
        return None
    
    # Extract payload bits
    payload_bits = decoded_bits[16:16 + payload_length]
    print(f"Extracted payload: {len(payload_bits)} bits")
    
    # Convert to bytes
    if len(payload_bits) % 8 != 0:
        print(f"WARNING: Payload not byte-aligned ({len(payload_bits)} bits)")
        payload_bits = payload_bits[:-(len(payload_bits) % 8)]
    
    payload_bytes = bytearray()
    for i in range(0, len(payload_bits), 8):
        byte_bits = payload_bits[i:i+8]
        payload_bytes.append(int(byte_bits, 2))
    
    print(f"Payload bytes: {len(payload_bytes)} bytes")
    print(f"Payload hex: {bytes(payload_bytes).hex()}")
    
    return bytes(payload_bytes)

def main():
    # Use the same key as in test_hello_world.py
    test_key = b'HelloWorldDemoKey' + b'0' * 15  # Pad to 32 bytes
    
    print("=" * 60)
    print("DETAILED DECODE DEBUG")
    print("=" * 60)
    
    # First, let's see what the encoder produces
    cipher = CipherService(test_key)
    command = "hello world"
    encrypted = cipher.encrypt_command(command)
    obfuscated = cipher.add_obfuscation(encrypted)
    print(f"\nExpected payload:")
    print(f"  Command: '{command}'")
    print(f"  Encrypted: {len(encrypted)} bytes")
    print(f"  Obfuscated: {len(obfuscated)} bytes")
    print(f"  Obfuscated hex: {obfuscated.hex()}")
    
    # Create embedder and embed
    embedder = AudioEmbedder(key=test_key)
    success = embedder.embed_file(
        'sample_audio.mp3',
        'debug_detailed.mp3',
        command
    )
    print(f"\nEmbedding success: {success}")
    
    # Manual decode process
    decoder = AudioDecoder(key=test_key)
    
    # Load and prepare audio
    audio = AudioSegment.from_file('debug_detailed.mp3')
    audio = audio.set_channels(1).set_frame_rate(48000)
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Ultrasonic decoding
    ultrasonic_decoder = decoder.decoder
    filtered_signal = ultrasonic_decoder._apply_bandpass_filter(audio_data)
    start_position = ultrasonic_decoder._detect_preamble(filtered_signal)
    
    if start_position is None:
        print("\nERROR: Preamble not found!")
        return
    
    print(f"\nPreamble found at position: {start_position}")
    
    # Extract bits
    bit_data = ultrasonic_decoder._extract_bits_with_confidence(filtered_signal, start_position)
    
    if not bit_data:
        print("ERROR: No bits extracted!")
        return
    
    # Manual decode with logging
    payload_bytes = decode_with_logging(ultrasonic_decoder, bit_data)
    
    if payload_bytes:
        print("\nAttempting decryption...")
        # Try to remove obfuscation
        deobfuscated = cipher.remove_obfuscation(payload_bytes)
        if deobfuscated:
            print(f"Deobfuscated: {len(deobfuscated)} bytes")
            print(f"Deobfuscated hex: {deobfuscated.hex()}")
            
            # Try to decrypt
            decrypted = cipher.decrypt_command(deobfuscated)
            print(f"Decrypted: '{decrypted}'")
        else:
            print("Deobfuscation failed - trying direct decryption")
            decrypted = cipher.decrypt_command(payload_bytes)
            print(f"Direct decrypted: '{decrypted}'")
    
    # Clean up
    os.remove('debug_detailed.mp3')

if __name__ == "__main__":
    main()