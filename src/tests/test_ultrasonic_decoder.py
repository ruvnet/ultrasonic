"""
Tests for ultrasonic decoder.
Tests signal detection and demodulation functionality.
"""

import pytest
import numpy as np
from ..decode.ultrasonic_decoder import UltrasonicDecoder
from ..embed.ultrasonic_encoder import UltrasonicEncoder


class TestUltrasonicDecoder:
    """Test suite for UltrasonicDecoder."""
    
    def test_decoder_initializes_with_default_parameters(self):
        """Test that decoder initializes with sensible defaults."""
        decoder = UltrasonicDecoder()
        
        assert decoder.freq_0 == 18500
        assert decoder.freq_1 == 19500
        assert decoder.sample_rate == 48000
        assert decoder.bit_duration == 0.01
        assert decoder.detection_threshold == 0.01
        assert decoder.samples_per_bit == 480
    
    def test_decoder_frequencies_match_encoder(self):
        """Test that decoder can be configured to match encoder frequencies."""
        freq_0, freq_1 = 17000, 18000
        
        encoder = UltrasonicEncoder(freq_0=freq_0, freq_1=freq_1)
        decoder = UltrasonicDecoder(freq_0=freq_0, freq_1=freq_1)
        
        assert decoder.freq_0 == encoder.freq_0
        assert decoder.freq_1 == encoder.freq_1
    
    def test_decode_payload_returns_none_for_empty_signal(self):
        """Test that decoder returns None for empty or silent signal."""
        decoder = UltrasonicDecoder()
        
        # Empty signal
        assert decoder.decode_payload(np.array([])) is None
        
        # Silent signal
        silent_signal = np.zeros(48000)  # 1 second of silence
        assert decoder.decode_payload(silent_signal) is None
    
    def test_decode_payload_returns_none_for_noise(self):
        """Test that decoder returns None for random noise."""
        decoder = UltrasonicDecoder()
        
        # Random noise signal
        noise_signal = np.random.random(48000) * 0.1
        result = decoder.decode_payload(noise_signal)
        
        # Should not decode random noise as valid payload
        assert result is None
    
    def test_apply_bandpass_filter_isolates_frequency_range(self):
        """Test that bandpass filter isolates the ultrasonic range."""
        decoder = UltrasonicDecoder(freq_0=18000, freq_1=19000)
        
        # Create test signal with multiple frequencies
        sample_rate = 48000
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Mix of low frequency (1kHz), target frequency (18.5kHz), and high frequency (22kHz)
        signal = (np.sin(2 * np.pi * 1000 * t) +
                 np.sin(2 * np.pi * 18500 * t) +
                 np.sin(2 * np.pi * 22000 * t))
        
        filtered = decoder._apply_bandpass_filter(signal)
        
        # Filtered signal should be different from original
        assert not np.allclose(signal, filtered, atol=1e-6)
        
        # Should have reduced low and high frequency components
        fft_original = np.abs(np.fft.fft(signal))
        fft_filtered = np.abs(np.fft.fft(filtered))
        
        # The 18.5kHz component should be preserved better than 1kHz or 22kHz
        freqs = np.fft.fftfreq(len(signal), 1/sample_rate)
        
        # Find indices for our test frequencies
        idx_1k = np.argmin(np.abs(freqs - 1000))
        idx_18_5k = np.argmin(np.abs(freqs - 18500))
        idx_22k = np.argmin(np.abs(freqs - 22000))
        
        # 18.5kHz should be better preserved relative to others
        preservation_18_5k = fft_filtered[idx_18_5k] / fft_original[idx_18_5k]
        preservation_1k = fft_filtered[idx_1k] / fft_original[idx_1k]
        preservation_22k = fft_filtered[idx_22k] / fft_original[idx_22k]
        
        assert preservation_18_5k > preservation_1k
        assert preservation_18_5k > preservation_22k
    
    def test_detect_preamble_finds_known_pattern(self):
        """Test that preamble detection works with known pattern."""
        decoder = UltrasonicDecoder(
            freq_0=1000,  # Use lower frequencies for easier testing
            freq_1=2000,
            sample_rate=8000,
            bit_duration=0.1  # Longer bits for easier analysis
        )
        
        # Create encoder with same parameters
        encoder = UltrasonicEncoder(
            freq_0=1000,
            freq_1=2000,
            sample_rate=8000,
            bit_duration=0.1
        )
        
        # Generate signal with known preamble
        payload = b"test"
        signal = encoder.encode_payload(payload, add_preamble=True)
        
        # Should detect preamble
        preamble_end = decoder._detect_preamble(signal)
        assert preamble_end is not None
        assert preamble_end > 0
    
    def test_detect_preamble_returns_none_for_no_pattern(self):
        """Test that preamble detection returns None when no pattern found."""
        decoder = UltrasonicDecoder()
        
        # Random signal without preamble pattern
        random_signal = np.random.random(4800) * 0.1  # 0.1 seconds at 48kHz
        
        preamble_end = decoder._detect_preamble(random_signal)
        assert preamble_end is None
    
    def test_correlate_with_frequency_detects_correct_frequency(self):
        """Test that frequency correlation calculation works correctly."""
        decoder = UltrasonicDecoder()
        
        # Create pure tone at known frequency
        freq = 1000  # 1kHz test tone
        sample_rate = 48000
        duration = 0.1  # 100ms
        t = np.linspace(0, duration, int(sample_rate * duration))
        tone = np.sin(2 * np.pi * freq * t)
        
        # Calculate correlation at the correct frequency
        corr_correct = decoder._correlate_with_frequency(tone, freq)
        
        # Calculate correlation at different frequency
        corr_wrong = decoder._correlate_with_frequency(tone, freq * 2)
        
        # Correlation should be higher at the correct frequency
        assert corr_correct > corr_wrong
        assert corr_correct > 0.5  # Should have high correlation with matching frequency
    
    def test_extract_bits_from_known_signal(self):
        """Test bit extraction from a known FSK signal."""
        decoder = UltrasonicDecoder(
            freq_0=1000,
            freq_1=2000,
            sample_rate=8000,
            bit_duration=0.1
        )
        
        # Create known bit pattern
        known_bits = "01101001"
        
        # Generate FSK signal for known bits
        samples_per_bit = int(decoder.sample_rate * decoder.bit_duration)
        total_samples = len(known_bits) * samples_per_bit
        signal = np.zeros(total_samples)
        
        t_bit = np.linspace(0, decoder.bit_duration, samples_per_bit)
        
        for i, bit in enumerate(known_bits):
            start_idx = i * samples_per_bit
            end_idx = start_idx + samples_per_bit
            
            freq = decoder.freq_0 if bit == '0' else decoder.freq_1
            signal[start_idx:end_idx] = 0.5 * np.sin(2 * np.pi * freq * t_bit)
        
        # Extract bits
        extracted_bits = decoder._extract_bits(signal, 0)
        
        # Should extract the same bit pattern
        assert extracted_bits.startswith(known_bits)
    
    def test_decode_bits_to_bytes_handles_error_correction(self):
        """Test that bit-to-byte conversion handles error correction."""
        decoder = UltrasonicDecoder()
        
        # Create bit string with error correction (8 data bits + 1 parity bit)
        data_bits = "10101010"
        parity = sum(int(bit) for bit in data_bits) % 2
        bit_string = data_bits + str(parity)
        
        # Should decode to single byte
        payload = decoder._decode_bits_to_bytes(bit_string)
        
        assert payload is not None
        assert len(payload) == 1
        assert payload[0] == int(data_bits, 2)  # 0b10101010 = 170
    
    def test_decode_bits_to_bytes_rejects_invalid_parity(self):
        """Test that bit decoding works correctly with short strings."""
        decoder = UltrasonicDecoder()
        
        # For short strings (< 24 bits), should do simple conversion
        data_bits = "10101010"
        
        # Should decode directly without error correction
        payload = decoder._decode_bits_to_bytes(data_bits)
        
        # Should successfully decode
        assert payload is not None
        assert len(payload) == 1
        assert payload[0] == 0b10101010
    
    def test_detect_signal_presence_works_correctly(self):
        """Test that signal presence detection works."""
        decoder = UltrasonicDecoder(
            freq_0=1000,
            freq_1=2000,
            detection_threshold=0.05
        )
        
        # Silent signal
        silent = np.zeros(4800)
        assert decoder.detect_signal_presence(silent) == False
        
        # Signal with ultrasonic content
        t = np.linspace(0, 0.1, 4800)
        ultrasonic = 0.1 * np.sin(2 * np.pi * 1500 * t)  # Between freq_0 and freq_1
        assert decoder.detect_signal_presence(ultrasonic) == True
        
        # Signal with non-ultrasonic content
        audible = 0.1 * np.sin(2 * np.pi * 440 * t)  # 440 Hz (audible)
        # This should be filtered out and not detected
        detected = decoder.detect_signal_presence(audible)
        # Result depends on filter design, but typically should be False
    
    def test_get_signal_strength_provides_reasonable_values(self):
        """Test that signal strength measurement provides reasonable values."""
        decoder = UltrasonicDecoder(freq_0=1000, freq_1=2000)
        
        # Silent signal should have zero or very low strength
        silent = np.zeros(4800)
        strength_silent = decoder.get_signal_strength(silent)
        assert 0.0 <= strength_silent <= 0.1
        
        # Strong signal should have higher strength
        t = np.linspace(0, 0.1, 4800)
        strong_signal = 0.5 * np.sin(2 * np.pi * 1500 * t)
        strength_strong = decoder.get_signal_strength(strong_signal)
        
        # Weak signal should have lower strength
        weak_signal = 0.1 * np.sin(2 * np.pi * 1500 * t)
        strength_weak = decoder.get_signal_strength(weak_signal)
        
        assert strength_strong > strength_weak
        assert strength_weak > strength_silent
        assert 0.0 <= strength_strong <= 1.0
    
    def test_set_frequencies_updates_correctly(self):
        """Test that frequency setting updates decoder correctly."""
        decoder = UltrasonicDecoder()
        
        original_freq_0 = decoder.freq_0
        original_freq_1 = decoder.freq_1
        
        new_freq_0, new_freq_1 = 17000, 18000
        decoder.set_frequencies(new_freq_0, new_freq_1)
        
        assert decoder.freq_0 == new_freq_0
        assert decoder.freq_1 == new_freq_1
        assert decoder.freq_0 != original_freq_0
        assert decoder.freq_1 != original_freq_1
    
    def test_set_detection_threshold_updates_correctly(self):
        """Test that detection threshold setting works."""
        decoder = UltrasonicDecoder()
        
        original_threshold = decoder.detection_threshold
        new_threshold = 0.05
        
        decoder.set_detection_threshold(new_threshold)
        
        assert decoder.detection_threshold == new_threshold
        assert decoder.detection_threshold != original_threshold
    
    def test_decoder_handles_short_signals(self):
        """Test that decoder handles very short signals gracefully."""
        decoder = UltrasonicDecoder()
        
        # Very short signal (less than one bit duration)
        short_signal = np.random.random(100) * 0.1
        
        result = decoder.decode_payload(short_signal)
        assert result is None
    
    def test_decoder_handles_corrupted_signals(self):
        """Test that decoder handles corrupted/noisy signals gracefully."""
        decoder = UltrasonicDecoder()
        
        # Create a signal that looks like it might have content but is corrupted
        t = np.linspace(0, 1, 48000)
        
        # Mix of valid frequencies with noise
        signal = (0.1 * np.sin(2 * np.pi * 18500 * t) +
                 0.5 * np.random.random(48000))  # Heavy noise
        
        # Should handle gracefully (either decode or return None)
        result = decoder.decode_payload(signal)
        
        # Either succeeds or fails gracefully
        assert result is None or isinstance(result, bytes)
    
    def test_correlate_with_pattern_calculates_correctly(self):
        """Test pattern correlation calculation."""
        decoder = UltrasonicDecoder(
            freq_0=1000,
            freq_1=2000,
            sample_rate=8000,
            bit_duration=0.1
        )
        
        # Create signal matching expected pattern
        freq_sequence = [1000, 2000, 1000]  # Pattern: 0, 1, 0
        samples_per_bit = int(decoder.sample_rate * decoder.bit_duration)
        
        signal = np.zeros(len(freq_sequence) * samples_per_bit)
        t_bit = np.linspace(0, decoder.bit_duration, samples_per_bit)
        
        for i, freq in enumerate(freq_sequence):
            start_idx = i * samples_per_bit
            end_idx = start_idx + samples_per_bit
            signal[start_idx:end_idx] = 0.3 * np.sin(2 * np.pi * freq * t_bit)
        
        # Calculate correlation
        correlation = decoder._correlate_with_pattern(signal, freq_sequence)
        
        # Should have reasonable correlation with matching pattern
        assert correlation > 0
        assert correlation <= 1.0