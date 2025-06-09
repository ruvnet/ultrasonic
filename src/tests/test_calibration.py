"""
Calibration tests to find optimal signal detection parameters.
"""

import numpy as np
import pytest
from pydub import AudioSegment
from ..embed.audio_embedder import AudioEmbedder
from ..decode.audio_decoder import AudioDecoder
from ..crypto.cipher import CipherService


class TestCalibration:
    """Test suite for calibrating signal detection parameters."""
    
    def test_parameter_sweep(self):
        """Sweep through different parameter combinations to find optimal values."""
        # Test parameters
        test_command = "CALIBRATION_TEST"
        key = CipherService.generate_key(32)
        
        # Parameter ranges to test
        amplitudes = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
        thresholds = [0.001, 0.005, 0.01, 0.05, 0.1, 0.2]
        bit_durations = [0.005, 0.01, 0.02, 0.05, 0.1]
        
        results = []
        
        for amplitude in amplitudes:
            for threshold in thresholds:
                for bit_duration in bit_durations:
                    # Create embedder and decoder with test parameters
                    embedder = AudioEmbedder(
                        key=key,
                        amplitude=amplitude,
                        bit_duration=bit_duration
                    )
                    
                    decoder = AudioDecoder(
                        key=key,
                        detection_threshold=threshold,
                        bit_duration=bit_duration
                    )
                    
                    # Create test audio (3 seconds of silence)
                    test_audio = AudioSegment.silent(duration=3000, frame_rate=48000)
                    
                    # Try embedding and decoding
                    try:
                        stego_audio = embedder.embed(test_audio, test_command)
                        decoded = decoder.decode_audio_segment(stego_audio)
                        
                        success = decoded == test_command
                        
                        results.append({
                            'amplitude': amplitude,
                            'threshold': threshold,
                            'bit_duration': bit_duration,
                            'success': success,
                            'decoded': decoded
                        })
                        
                        if success:
                            print(f"✓ Success with amp={amplitude}, thresh={threshold}, bit_dur={bit_duration}")
                    except Exception as e:
                        results.append({
                            'amplitude': amplitude,
                            'threshold': threshold,
                            'bit_duration': bit_duration,
                            'success': False,
                            'error': str(e)
                        })
        
        # Find successful combinations
        successful = [r for r in results if r.get('success', False)]
        
        if successful:
            print(f"\nFound {len(successful)} successful parameter combinations:")
            for params in successful[:5]:  # Show first 5
                print(f"  amp={params['amplitude']}, thresh={params['threshold']}, bit_dur={params['bit_duration']}")
        else:
            print("\nNo successful combinations found!")
            print("Sample failures:")
            for params in results[:5]:
                print(f"  amp={params['amplitude']}, thresh={params['threshold']}, bit_dur={params['bit_duration']}")
                print(f"    decoded: {params.get('decoded', 'None')}")
        
        # At least one combination should work
        assert len(successful) > 0, "No parameter combinations worked!"
    
    def test_signal_analysis(self):
        """Analyze the actual signal being generated."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.5, bit_duration=0.05)
        
        # Create test audio
        test_audio = AudioSegment.silent(duration=3000, frame_rate=48000)
        test_command = "SIGNAL_TEST"
        
        # Embed command
        stego_audio = embedder.embed(test_audio, test_command)
        
        # Convert to numpy array
        audio_data = np.array(stego_audio.get_array_of_samples(), dtype=np.float32)
        
        # Normalize
        if len(audio_data) > 0:
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                audio_data = audio_data / max_val
        
        # Analyze signal properties
        print(f"\nSignal Analysis:")
        print(f"  Length: {len(audio_data)} samples")
        print(f"  Max amplitude: {np.max(np.abs(audio_data)):.4f}")
        print(f"  Mean amplitude: {np.mean(np.abs(audio_data)):.4f}")
        print(f"  RMS: {np.sqrt(np.mean(audio_data**2)):.4f}")
        
        # Check if there's actually a signal
        assert np.max(np.abs(audio_data)) > 0.01, "Signal amplitude too low!"
    
    def test_preamble_detection(self):
        """Test if preamble is being correctly detected."""
        from ..decode.ultrasonic_decoder import UltrasonicDecoder
        from ..embed.ultrasonic_encoder import UltrasonicEncoder
        
        # Create encoder and decoder
        encoder = UltrasonicEncoder(amplitude=0.5, bit_duration=0.05)
        decoder = UltrasonicDecoder(detection_threshold=0.01, bit_duration=0.05)
        
        # Generate just a preamble
        preamble_bits = "10101010" + "11110000" + "10101010"
        preamble_signal = encoder._modulate_fsk(preamble_bits)
        
        # Try to detect it
        filtered = decoder._apply_bandpass_filter(preamble_signal)
        position = decoder._detect_preamble(filtered)
        
        print(f"\nPreamble Detection:")
        print(f"  Signal length: {len(preamble_signal)}")
        print(f"  Filtered length: {len(filtered)}")
        print(f"  Detection position: {position}")
        print(f"  Expected position: ~{len(preamble_bits) * encoder.samples_per_bit}")
        
        assert position is not None, "Preamble not detected!"