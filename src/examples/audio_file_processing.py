#!/usr/bin/env python3
"""
Audio File Processing Example for Ultrasonic Agentics

This example demonstrates how to embed and extract commands from audio files,
including mixing with existing audio content.
"""

import os
import numpy as np
from pydub import AudioSegment
from ultrasonic_agentics.embed.ultrasonic_encoder import UltrasonicEncoder
from ultrasonic_agentics.decode.ultrasonic_decoder import UltrasonicDecoder


def create_test_audio():
    """Create a test audio file with some background content."""
    print("Creating test audio file...")
    
    # Generate a simple audio track (sine wave with some complexity)
    duration = 5.0  # 5 seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a multi-frequency audio signal
    audio = (
        0.3 * np.sin(2 * np.pi * 440 * t) +      # A note
        0.2 * np.sin(2 * np.pi * 660 * t) +      # E note
        0.1 * np.sin(2 * np.pi * 880 * t)        # High A
    )
    
    # Add some noise for realism
    noise = np.random.normal(0, 0.02, len(audio))
    audio += noise
    
    # Convert to int16 and create AudioSegment
    audio_int16 = (audio * 32767).astype(np.int16)
    audio_segment = AudioSegment(
        audio_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    
    # Save test file
    test_file = "test_background_audio.wav"
    audio_segment.export(test_file, format="wav")
    print(f"Created test audio: {test_file} ({duration}s)")
    
    return test_file, audio_segment


def embed_command_in_audio():
    """Embed a command into an existing audio file."""
    print("\n=== Embedding Command in Audio File ===")
    
    # Create test audio
    test_file, original_audio = create_test_audio()
    
    # Initialize encoder
    encoder = UltrasonicEncoder(
        freq_0=19000,
        freq_1=20000,
        sample_rate=44100,  # Match the test audio
        amplitude=0.15      # Moderate amplitude to avoid overwhelming the original audio
    )
    
    # Command to embed
    command = "execute:background_task"
    print(f"Embedding command: {command}")
    
    # Encode the command
    encoded_signal = encoder.encode_payload(command.encode())
    
    # Load original audio as numpy array
    original_samples = np.array(original_audio.get_array_of_samples()).astype(np.float32) / 32767.0
    
    # Mix the encoded signal with the original audio
    mixed_audio = mix_audio_signals(original_samples, encoded_signal, encoder.sample_rate)
    
    # Convert back to AudioSegment
    mixed_int16 = (mixed_audio * 32767).astype(np.int16)
    mixed_segment = AudioSegment(
        mixed_int16.tobytes(),
        frame_rate=encoder.sample_rate,
        sample_width=2,
        channels=1
    )
    
    # Save mixed audio
    output_file = "audio_with_embedded_command.wav"
    mixed_segment.export(output_file, format="wav")
    print(f"Saved mixed audio: {output_file}")
    
    # Test decoding
    decoder = UltrasonicDecoder(
        freq_0=encoder.freq_0,
        freq_1=encoder.freq_1,
        sample_rate=encoder.sample_rate,
        detection_threshold=0.05  # Lower threshold for mixed audio
    )
    
    decoded_bytes = decoder.decode_payload(mixed_audio)
    
    if decoded_bytes:
        decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
        print(f"Decoded command: {decoded_command}")
        
        if decoded_command == command:
            print("✓ Command successfully embedded and decoded!")
        else:
            print(f"✗ Command mismatch")
    else:
        print("✗ Could not decode command from mixed audio")
    
    # Clean up
    cleanup_files([test_file, output_file])
    
    return output_file if decoded_bytes else None


def mix_audio_signals(background: np.ndarray, ultrasonic: np.ndarray, sample_rate: int) -> np.ndarray:
    """Mix background audio with ultrasonic signal."""
    # Ensure both signals have the same length
    max_length = max(len(background), len(ultrasonic))
    
    # Pad shorter signal with zeros
    if len(background) < max_length:
        background = np.pad(background, (0, max_length - len(background)))
    if len(ultrasonic) < max_length:
        ultrasonic = np.pad(ultrasonic, (0, max_length - len(ultrasonic)))
    
    # Mix signals (simple addition)
    mixed = background + ultrasonic
    
    # Normalize to prevent clipping
    max_amplitude = np.max(np.abs(mixed))
    if max_amplitude > 1.0:
        mixed = mixed / max_amplitude * 0.95  # Leave some headroom
    
    return mixed


def steganographic_embedding():
    """Demonstrate steganographic embedding that's harder to detect."""
    print("\n=== Steganographic Embedding Example ===")
    
    # Create longer background audio
    duration = 10.0
    sample_rate = 48000
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create more complex background (music-like)
    background = (
        0.4 * np.sin(2 * np.pi * 261.63 * t) * np.exp(-t * 0.5) +  # C note decay
        0.3 * np.sin(2 * np.pi * 329.63 * t) * np.exp(-(t-1) * 0.5) * (t > 1) +  # E note
        0.2 * np.sin(2 * np.pi * 392.00 * t) * np.exp(-(t-2) * 0.5) * (t > 2)    # G note
    )
    
    # Add realistic noise
    background += np.random.normal(0, 0.01, len(background))
    
    # Initialize encoder with very low amplitude for steganography
    encoder = UltrasonicEncoder(
        freq_0=20500,
        freq_1=21500,
        sample_rate=sample_rate,
        amplitude=0.05  # Very low amplitude - harder to detect
    )
    
    command = "stealth:covert_operation"
    print(f"Embedding steganographic command: {command}")
    
    # Encode with minimal amplitude
    encoded_signal = encoder.encode_payload(command.encode())
    
    # Embed at a random position in the audio
    embed_position = int(len(background) * 0.3)  # 30% into the audio
    mixed_audio = background.copy()
    
    # Ensure we don't exceed array bounds
    end_position = min(embed_position + len(encoded_signal), len(mixed_audio))
    actual_signal_length = end_position - embed_position
    
    mixed_audio[embed_position:end_position] += encoded_signal[:actual_signal_length]
    
    # Save steganographic audio
    stego_int16 = (mixed_audio * 32767).astype(np.int16)
    stego_segment = AudioSegment(
        stego_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    
    stego_file = "steganographic_audio.wav"
    stego_segment.export(stego_file, format="wav")
    print(f"Saved steganographic audio: {stego_file}")
    
    # Test detection and decoding
    decoder = UltrasonicDecoder(
        freq_0=encoder.freq_0,
        freq_1=encoder.freq_1,
        sample_rate=sample_rate,
        detection_threshold=0.02  # Very sensitive for steganographic detection
    )
    
    # Check if signal is detected
    signal_detected = decoder.detect_signal_presence(mixed_audio)
    print(f"Ultrasonic signal detected: {signal_detected}")
    
    if signal_detected:
        signal_strength = decoder.get_signal_strength(mixed_audio)
        print(f"Signal strength: {signal_strength:.6f}")
        
        # Try to decode
        decoded_bytes = decoder.decode_payload(mixed_audio)
        
        if decoded_bytes:
            decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
            print(f"Decoded steganographic command: {decoded_command}")
            
            if decoded_command == command:
                print("✓ Steganographic embedding successful!")
            else:
                print("✗ Steganographic decoding produced incorrect result")
        else:
            print("✗ Could not decode steganographic command")
    else:
        print("✗ Steganographic signal not detected (too weak)")
    
    cleanup_files([stego_file])


def batch_processing_example():
    """Demonstrate batch processing of multiple audio files."""
    print("\n=== Batch Processing Example ===")
    
    # Create multiple test files
    test_files = []
    commands = [
        "batch:file_1",
        "batch:file_2", 
        "batch:file_3"
    ]
    
    encoder = UltrasonicEncoder(amplitude=0.2)
    
    print("Creating batch of test files...")
    for i, command in enumerate(commands):
        # Create unique audio for each file
        duration = 3.0
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Different frequency for each file
        freq = 440 * (i + 1)  # 440, 880, 1320 Hz
        audio = 0.3 * np.sin(2 * np.pi * freq * t)
        audio += np.random.normal(0, 0.02, len(audio))
        
        # Embed command
        encoded_signal = encoder.encode_payload(command.encode())
        mixed_audio = mix_audio_signals(audio, encoded_signal, sample_rate)
        
        # Save file
        filename = f"batch_test_{i+1}.wav"
        mixed_int16 = (mixed_audio * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            mixed_int16.tobytes(),
            frame_rate=sample_rate,
            sample_width=2,
            channels=1
        )
        audio_segment.export(filename, format="wav")
        test_files.append(filename)
        print(f"  Created {filename} with command: {command}")
    
    # Batch decode all files
    print("\nDecoding batch files...")
    decoder = UltrasonicDecoder(
        freq_0=encoder.freq_0,
        freq_1=encoder.freq_1,
        sample_rate=encoder.sample_rate
    )
    
    success_count = 0
    for i, filename in enumerate(test_files):
        # Load audio file
        audio_segment = AudioSegment.from_wav(filename)
        audio_array = np.array(audio_segment.get_array_of_samples()).astype(np.float32) / 32767.0
        
        # Decode
        decoded_bytes = decoder.decode_payload(audio_array)
        
        if decoded_bytes:
            decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
            expected_command = commands[i]
            
            if decoded_command == expected_command:
                print(f"  ✓ {filename}: {decoded_command}")
                success_count += 1
            else:
                print(f"  ✗ {filename}: Expected {expected_command}, got {decoded_command}")
        else:
            print(f"  ✗ {filename}: Decode failed")
    
    print(f"\nBatch processing results: {success_count}/{len(test_files)} successful")
    
    # Clean up batch files
    cleanup_files(test_files)


def format_conversion_test():
    """Test encoding/decoding across different audio formats."""
    print("\n=== Audio Format Conversion Test ===")
    
    encoder = UltrasonicEncoder(amplitude=0.25)
    decoder = UltrasonicDecoder(freq_0=encoder.freq_0, freq_1=encoder.freq_1, sample_rate=encoder.sample_rate)
    
    command = "format:test_command"
    
    # Create base audio
    duration = 4.0
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    base_audio = 0.2 * np.sin(2 * np.pi * 1000 * t)  # 1kHz tone
    
    # Embed command
    encoded_signal = encoder.encode_payload(command.encode())
    mixed_audio = mix_audio_signals(base_audio, encoded_signal, sample_rate)
    
    # Test different formats
    formats = ['wav', 'mp3', 'ogg']  # Remove 'flac' if not supported
    test_files = []
    
    for fmt in formats:
        try:
            # Create AudioSegment
            mixed_int16 = (mixed_audio * 32767).astype(np.int16)
            audio_segment = AudioSegment(
                mixed_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            
            # Export in different format
            filename = f"format_test.{fmt}"
            
            if fmt == 'mp3':
                audio_segment.export(filename, format="mp3", bitrate="192k")
            elif fmt == 'ogg':
                audio_segment.export(filename, format="ogg")
            else:  # wav
                audio_segment.export(filename, format="wav")
            
            test_files.append(filename)
            print(f"  Created {filename}")
            
            # Load and test decoding
            loaded_segment = AudioSegment.from_file(filename)
            loaded_array = np.array(loaded_segment.get_array_of_samples()).astype(np.float32) / 32767.0
            
            # Handle stereo if necessary
            if loaded_segment.channels == 2:
                # Convert stereo to mono by averaging channels
                loaded_array = loaded_array.reshape(-1, 2).mean(axis=1)
            
            decoded_bytes = decoder.decode_payload(loaded_array)
            
            if decoded_bytes:
                decoded_command = decoded_bytes.decode('utf-8', errors='ignore')
                if decoded_command == command:
                    print(f"    ✓ {fmt.upper()} format: Decode successful")
                else:
                    print(f"    ✗ {fmt.upper()} format: Decode mismatch")
            else:
                print(f"    ✗ {fmt.upper()} format: Decode failed")
                
        except Exception as e:
            print(f"    ✗ {fmt.upper()} format: Error - {e}")
    
    # Clean up
    cleanup_files(test_files)


def cleanup_files(file_list):
    """Clean up temporary files."""
    for file_path in file_list:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass


if __name__ == "__main__":
    print("Ultrasonic Agentics - Audio File Processing Examples")
    print("=" * 60)
    
    # Run all examples
    embed_command_in_audio()
    steganographic_embedding()
    batch_processing_example()
    format_conversion_test()
    
    print("\n" + "=" * 60)
    print("Audio file processing examples completed!")