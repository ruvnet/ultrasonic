#!/usr/bin/env python3
"""
Test embedding with different amplitude settings.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embed.audio_embedder import AudioEmbedder
from src.decode.audio_decoder import AudioDecoder

def test_amplitude(amplitude):
    """Test with specific amplitude."""
    test_key = b'HelloWorldDemoKey' + b'0' * 15
    
    embedder = AudioEmbedder(key=test_key, amplitude=amplitude)
    decoder = AudioDecoder(key=test_key)
    
    output_file = f'test_amp_{amplitude}.mp3'
    
    success = embedder.embed_file(
        'sample_audio.mp3',
        output_file,
        'hello world'
    )
    
    if success:
        result = decoder.decode_file(output_file)
        is_detected = decoder.detect_signal(output_file)
        
        if is_detected:
            strength = decoder.get_signal_strength(output_file)
        else:
            strength = 0.0
        
        os.remove(output_file)
        
        return result, is_detected, strength
    else:
        return None, False, 0.0

def main():
    print("=" * 60)
    print("AMPLITUDE TESTING")
    print("=" * 60)
    
    # Test different amplitudes
    amplitudes = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for amp in amplitudes:
        result, detected, strength = test_amplitude(amp)
        status = "SUCCESS" if result == "hello world" else "FAILED"
        print(f"\nAmplitude {amp}:")
        print(f"  Signal detected: {detected}")
        print(f"  Signal strength: {strength:.3f}")
        print(f"  Decoded result: '{result}'")
        print(f"  Status: {status}")
    
    # Now let's try with the default parameters but using WAV
    print("\n" + "=" * 60)
    print("TESTING WITH WAV OUTPUT")
    print("=" * 60)
    
    test_key = b'HelloWorldDemoKey' + b'0' * 15
    embedder = AudioEmbedder(key=test_key)  # Default amplitude
    decoder = AudioDecoder(key=test_key)
    
    # Test with WAV
    success = embedder.embed_file(
        'sample_audio.mp3',
        'test_default.wav',
        'hello world'
    )
    
    if success:
        result = decoder.decode_file('test_default.wav')
        print(f"\nWAV with default amplitude (0.1):")
        print(f"  Decoded result: '{result}'")
        print(f"  Status: {'SUCCESS' if result == 'hello world' else 'FAILED'}")
        os.remove('test_default.wav')

if __name__ == "__main__":
    main()