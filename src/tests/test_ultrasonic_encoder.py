"""
Tests for ultrasonic encoder.
Tests signal generation and audio segment creation.
"""

import pytest
import numpy as np
from pydub import AudioSegment
from ..embed.ultrasonic_encoder import UltrasonicEncoder


class TestUltrasonicEncoder:
    """Test suite for UltrasonicEncoder."""
    
    def test_encoder_initializes_with_default_parameters(self):
        """Test that encoder initializes with sensible defaults."""
        encoder = UltrasonicEncoder()
        
        assert encoder.freq_0 == 18500
        assert encoder.freq_1 == 19500
        assert encoder.sample_rate == 48000
        assert encoder.bit_duration == 0.01
        assert encoder.amplitude == 0.1
        assert encoder.samples_per_bit == 480  # 48000 * 0.01
    
    def test_encoder_rejects_frequencies_above_nyquist(self):
        """Test that encoder rejects frequencies above Nyquist frequency."""
        sample_rate = 48000
        nyquist = sample_rate / 2
        
        with pytest.raises(ValueError, match="Frequencies must be below Nyquist frequency"):
            UltrasonicEncoder(freq_0=nyquist + 1000, sample_rate=sample_rate)
        
        with pytest.raises(ValueError, match="Frequencies must be below Nyquist frequency"):
            UltrasonicEncoder(freq_1=nyquist + 1000, sample_rate=sample_rate)
    
    def test_encode_payload_returns_numpy_array(self):
        """Test that encode_payload returns numpy array."""
        encoder = UltrasonicEncoder()
        payload = b"test"
        
        signal = encoder.encode_payload(payload)
        
        assert isinstance(signal, np.ndarray)
        assert len(signal) > 0
        assert signal.dtype in [np.float32, np.float64]
    
    def test_encode_payload_length_scales_with_data_size(self):
        """Test that signal length scales appropriately with data size."""
        encoder = UltrasonicEncoder()
        
        short_payload = b"x"
        long_payload = b"x" * 10
        
        short_signal = encoder.encode_payload(short_payload, add_preamble=False)
        long_signal = encoder.encode_payload(long_payload, add_preamble=False)
        
        # Longer payload should produce longer signal
        assert len(long_signal) > len(short_signal)
    
    def test_encode_payload_includes_preamble_when_requested(self):
        """Test that preamble is included when add_preamble=True."""
        encoder = UltrasonicEncoder()
        payload = b"test"
        
        with_preamble = encoder.encode_payload(payload, add_preamble=True)
        without_preamble = encoder.encode_payload(payload, add_preamble=False)
        
        # Signal with preamble should be longer
        assert len(with_preamble) > len(without_preamble)
    
    def test_payload_to_bits_converts_correctly(self):
        """Test that _payload_to_bits converts bytes correctly."""
        encoder = UltrasonicEncoder()
        
        # Test single byte
        payload = b"\x42"  # 01000010 in binary
        bits = encoder._payload_to_bits(payload)
        assert bits == "01000010"
        
        # Test multiple bytes
        payload = b"\x42\xFF"  # 01000010 11111111
        bits = encoder._payload_to_bits(payload)
        assert bits == "0100001011111111"
    
    def test_generate_preamble_returns_consistent_pattern(self):
        """Test that preamble generation is consistent."""
        encoder = UltrasonicEncoder()
        
        preamble1 = encoder._generate_preamble()
        preamble2 = encoder._generate_preamble()
        
        assert preamble1 == preamble2
        assert len(preamble1) > 0
        assert all(bit in "01" for bit in preamble1)
    
    def test_add_error_correction_adds_parity_bits(self):
        """Test that error correction adds repetition coding."""
        encoder = UltrasonicEncoder()
        
        # 8 bits should become 72 bits with repetition coding (16 bit length + 8 data bits) * 3
        bit_string = "10101010"
        corrected = encoder._add_error_correction(bit_string)
        
        # Expected: 16-bit length prefix + 8 data bits = 24 bits, each repeated 3 times = 72
        assert len(corrected) == 72
        
        # Check that each bit is repeated 3 times
        for i in range(0, len(corrected), 3):
            if i + 2 < len(corrected):
                assert corrected[i] == corrected[i+1] == corrected[i+2]
    
    def test_add_error_correction_handles_incomplete_chunks(self):
        """Test error correction with incomplete 8-bit chunks."""
        encoder = UltrasonicEncoder()
        
        # 5 bits with repetition coding: (16 bit length + 5 data bits) * 3 = 63
        bit_string = "10101"
        corrected = encoder._add_error_correction(bit_string)
        
        # Expected: 16-bit length prefix + 5 data bits = 21 bits, each repeated 3 times = 63
        assert len(corrected) == 63
    
    def test_generate_fsk_signal_produces_correct_frequencies(self):
        """Test that FSK signal contains expected frequencies."""
        encoder = UltrasonicEncoder(
            freq_0=1000,  # Use lower frequencies for easier testing
            freq_1=2000,
            sample_rate=8000,
            bit_duration=0.1  # Longer duration for analysis
        )
        
        # Generate signal for known bit pattern
        bit_string = "01"  # One '0' bit, one '1' bit
        signal = encoder._generate_fsk_signal(bit_string)
        
        # Should have two segments of equal length
        samples_per_bit = int(encoder.sample_rate * encoder.bit_duration)
        assert len(signal) == 2 * samples_per_bit
        
        # Analyze frequency content (simplified check)
        first_bit_signal = signal[:samples_per_bit]
        second_bit_signal = signal[samples_per_bit:]
        
        # First bit ('0') should have different spectrum than second bit ('1')
        first_fft = np.abs(np.fft.fft(first_bit_signal))
        second_fft = np.abs(np.fft.fft(second_bit_signal))
        
        # Peak frequencies should be different
        freqs = np.fft.fftfreq(samples_per_bit, 1/encoder.sample_rate)
        first_peak_freq = freqs[np.argmax(first_fft[:len(first_fft)//2])]
        second_peak_freq = freqs[np.argmax(second_fft[:len(second_fft)//2])]
        
        assert abs(first_peak_freq - encoder.freq_0) < 100  # Within 100 Hz
        assert abs(second_peak_freq - encoder.freq_1) < 100  # Within 100 Hz
    
    def test_apply_windowing_reduces_artifacts(self):
        """Test that windowing is applied to tone segments."""
        encoder = UltrasonicEncoder()
        
        # Create a simple tone
        samples = 1000
        tone = np.ones(samples)  # Rectangular signal
        
        windowed = encoder._apply_windowing(tone)
        
        # Windowed signal should have smooth edges
        window_size = samples // 10
        if window_size > 0:
            # Edges should be different from middle
            assert windowed[0] != windowed[samples//2]
            assert windowed[-1] != windowed[samples//2]
            # But not zero (unless original was zero)
            assert windowed[0] > 0
            assert windowed[-1] > 0
    
    def test_create_audio_segment_returns_correct_format(self):
        """Test that create_audio_segment returns proper AudioSegment."""
        encoder = UltrasonicEncoder()
        
        # Create test signal
        signal = np.sin(2 * np.pi * 1000 * np.linspace(0, 1, encoder.sample_rate))
        
        audio_segment = encoder.create_audio_segment(signal)
        
        assert isinstance(audio_segment, AudioSegment)
        assert audio_segment.frame_rate == encoder.sample_rate
        assert audio_segment.sample_width == 2  # 16-bit
        assert audio_segment.channels == 1  # Mono
        assert len(audio_segment) > 0
    
    def test_estimate_payload_duration_calculates_correctly(self):
        """Test that duration estimation is reasonable."""
        encoder = UltrasonicEncoder(bit_duration=0.01)  # 10ms per bit
        
        # 1 byte = 8 bits, plus preamble and error correction
        payload_size = 1
        duration = encoder.estimate_payload_duration(payload_size)
        
        # Should include preamble (~24 bits) + ((16-bit length + 8 data bits) * 3 repetition)
        # Preamble: 24 bits, Data with repetition: (16 + 8) * 3 = 72 bits
        # Total ~96 bits * 0.01s = ~0.96s
        assert duration > 0.9
        assert duration < 1.2  # Should be reasonable
    
    def test_get_frequency_range_returns_correct_range(self):
        """Test that frequency range is returned correctly."""
        freq_0, freq_1 = 18000, 19000
        encoder = UltrasonicEncoder(freq_0=freq_0, freq_1=freq_1)
        
        range_min, range_max = encoder.get_frequency_range()
        
        assert range_min == min(freq_0, freq_1)
        assert range_max == max(freq_0, freq_1)
    
    def test_set_frequencies_updates_correctly(self):
        """Test that frequency setting works correctly."""
        encoder = UltrasonicEncoder()
        
        new_freq_0, new_freq_1 = 17000, 18000
        encoder.set_frequencies(new_freq_0, new_freq_1)
        
        assert encoder.freq_0 == new_freq_0
        assert encoder.freq_1 == new_freq_1
    
    def test_set_frequencies_rejects_invalid_frequencies(self):
        """Test that invalid frequencies are rejected."""
        encoder = UltrasonicEncoder(sample_rate=48000)
        nyquist = 24000
        
        with pytest.raises(ValueError, match="Frequencies must be below Nyquist frequency"):
            encoder.set_frequencies(nyquist + 1000, 20000)
    
    def test_set_amplitude_updates_correctly(self):
        """Test that amplitude setting works correctly."""
        encoder = UltrasonicEncoder()
        
        new_amplitude = 0.5
        encoder.set_amplitude(new_amplitude)
        
        assert encoder.amplitude == new_amplitude
    
    def test_set_amplitude_rejects_invalid_values(self):
        """Test that invalid amplitude values are rejected."""
        encoder = UltrasonicEncoder()
        
        with pytest.raises(ValueError, match="Amplitude must be between 0.0 and 1.0"):
            encoder.set_amplitude(-0.1)
        
        with pytest.raises(ValueError, match="Amplitude must be between 0.0 and 1.0"):
            encoder.set_amplitude(1.1)
    
    def test_encode_empty_payload(self):
        """Test encoding of empty payload."""
        encoder = UltrasonicEncoder()
        
        signal = encoder.encode_payload(b"", add_preamble=True)
        
        # Should still have preamble
        assert len(signal) > 0
    
    def test_encoded_signal_amplitude_is_within_bounds(self):
        """Test that encoded signal amplitude doesn't exceed limits."""
        encoder = UltrasonicEncoder(amplitude=0.8)
        payload = b"test payload"
        
        signal = encoder.encode_payload(payload)
        
        # Signal should not exceed amplitude bounds
        assert np.max(np.abs(signal)) <= encoder.amplitude
    
    def test_different_bit_durations_produce_different_lengths(self):
        """Test that different bit durations affect signal length."""
        payload = b"x"
        
        encoder_fast = UltrasonicEncoder(bit_duration=0.005)  # 5ms
        encoder_slow = UltrasonicEncoder(bit_duration=0.02)   # 20ms
        
        signal_fast = encoder_fast.encode_payload(payload, add_preamble=False)
        signal_slow = encoder_slow.encode_payload(payload, add_preamble=False)
        
        # Slower encoder should produce longer signal
        assert len(signal_slow) > len(signal_fast)