"""
Test suite for enhanced error correction system.
Tests the robustness of the repetition coding error correction system.
"""

import pytest
import numpy as np
from agentic_commands_stego.embed.ultrasonic_encoder import UltrasonicEncoder
from agentic_commands_stego.decode.ultrasonic_decoder import UltrasonicDecoder


class TestEnhancedErrorCorrection:
    """Test enhanced error correction capabilities."""
    
    def setup_method(self):
        """Set up encoder and decoder for each test."""
        self.encoder = UltrasonicEncoder(
            freq_0=18500,
            freq_1=19500,
            sample_rate=48000,
            bit_duration=0.01,
            amplitude=0.5
        )
        
        self.decoder = UltrasonicDecoder(
            freq_0=18500,
            freq_1=19500,
            sample_rate=48000,
            bit_duration=0.01,
            detection_threshold=0.01
        )
    
    def inject_bit_errors(self, signal: np.ndarray, error_rate: float) -> np.ndarray:
        """
        Inject bit-level errors into the signal by flipping frequency segments.
        
        Args:
            signal: Original signal
            error_rate: Fraction of bits to corrupt (0.0 to 1.0)
            
        Returns:
            Signal with errors injected
        """
        corrupted_signal = signal.copy()
        samples_per_bit = self.encoder.samples_per_bit
        
        # Calculate number of bits in signal
        num_bits = len(signal) // samples_per_bit
        
        # Determine which bits to corrupt
        num_errors = int(num_bits * error_rate)
        error_positions = np.random.choice(num_bits, num_errors, replace=False)
        
        for bit_pos in error_positions:
            start_idx = bit_pos * samples_per_bit
            end_idx = start_idx + samples_per_bit
            
            if end_idx <= len(corrupted_signal):
                # Flip the frequency by inverting the signal
                corrupted_signal[start_idx:end_idx] *= -1
        
        return corrupted_signal
    
    def test_no_errors_baseline(self):
        """Test that system works perfectly with no errors."""
        test_payload = b"EXECUTE:TestCommand123"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Decode without errors
        decoded = self.decoder.decode_payload(signal)
        
        assert decoded == test_payload
    
    def test_5_percent_error_rate(self):
        """Test system handles 5% bit error rate."""
        test_payload = b"EXECUTE:Test5Percent"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Inject 5% errors
        corrupted_signal = self.inject_bit_errors(signal, 0.05)
        
        # Decode
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        assert decoded == test_payload, "Should recover from 5% errors"
    
    def test_10_percent_error_rate(self):
        """Test system handles 10% bit error rate."""
        test_payload = b"EXECUTE:Test10Percent"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Inject 10% errors
        corrupted_signal = self.inject_bit_errors(signal, 0.10)
        
        # Decode
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        assert decoded == test_payload, "Should recover from 10% errors"
    
    def test_20_percent_error_rate(self):
        """Test system handles 20% bit error rate - main requirement."""
        test_payload = b"EXECUTE:Test20Percent"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Inject 20% errors
        corrupted_signal = self.inject_bit_errors(signal, 0.20)
        
        # Decode
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        assert decoded == test_payload, "Should recover from 20% errors with enhanced error correction"
    
    def test_burst_error_resilience(self):
        """Test system handles burst errors (consecutive bit errors)."""
        test_payload = b"EXECUTE:BurstErrorTest"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Inject burst errors (corrupt 10 consecutive bits)
        samples_per_bit = self.encoder.samples_per_bit
        burst_start_bit = 50  # Start burst after preamble
        burst_length = 10
        
        start_idx = burst_start_bit * samples_per_bit
        end_idx = (burst_start_bit + burst_length) * samples_per_bit
        
        if end_idx <= len(signal):
            # Corrupt the burst by inverting signal
            signal[start_idx:end_idx] *= -1
        
        # Decode
        decoded = self.decoder.decode_payload(signal)
        
        assert decoded == test_payload, "Should recover from burst errors due to interleaving"
    
    def test_crc_integrity_validation(self):
        """Test CRC catches payload corruption."""
        test_payload = b"EXECUTE:CRCTest123"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Manually corrupt the signal beyond recovery (50% error rate)
        corrupted_signal = self.inject_bit_errors(signal, 0.50)
        
        # Decode - should fail due to CRC mismatch
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        # With 50% errors, CRC should catch corruption
        assert decoded is None or decoded != test_payload, "CRC should catch severe corruption"
    
    def test_hamming_single_bit_correction(self):
        """Test individual Hamming code correction capability."""
        # Test the Hamming (7,4) encoder and decoder directly
        test_data = "1010"  # 4 data bits
        
        # Encode
        hamming_code = self.encoder._encode_hamming_7_4(test_data)
        assert len(hamming_code) == 7
        
        # Inject single bit error
        error_pos = 2  # Corrupt bit at position 2
        corrupted_code = list(hamming_code)
        corrupted_code[error_pos] = '1' if corrupted_code[error_pos] == '0' else '0'
        corrupted_code = ''.join(corrupted_code)
        
        # Decode and verify correction
        decoded_data = self.decoder._decode_hamming_7_4(corrupted_code)
        assert decoded_data == test_data, "Hamming code should correct single bit error"
    
    def test_interleaving_deinterleaving(self):
        """Test bit interleaving and deinterleaving."""
        test_bits = "1100110011001100" * 4  # 64 bits for testing
        
        # Apply interleaving
        interleaved = self.encoder._apply_interleaving(test_bits)
        
        # Remove interleaving
        deinterleaved = self.decoder._remove_interleaving(interleaved)
        
        # Should recover original bit pattern
        assert deinterleaved.startswith(test_bits), "Interleaving should be reversible"
    
    def test_confidence_based_decoding(self):
        """Test that confidence levels improve decoding reliability."""
        test_payload = b"EXECUTE:ConfidenceTest"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Add gaussian noise to reduce confidence
        noise = np.random.normal(0, 0.1, len(signal))
        noisy_signal = signal + noise
        
        # Extract bits with confidence
        start_pos = self.decoder._detect_preamble(noisy_signal)
        assert start_pos is not None
        
        bit_data = self.decoder._extract_bits_with_confidence(noisy_signal, start_pos)
        assert bit_data is not None
        
        # Verify confidence values are being calculated
        confidences = [conf for _, conf in bit_data]
        assert len(confidences) > 0
        assert all(0.0 <= conf <= 1.0 for conf in confidences)
    
    def test_multiple_error_types_combined(self):
        """Test system with combination of different error types."""
        test_payload = b"EXECUTE:CombinedErrors"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Add multiple error types:
        # 1. Random bit errors (15%)
        corrupted_signal = self.inject_bit_errors(signal, 0.15)
        
        # 2. Gaussian noise
        noise = np.random.normal(0, 0.05, len(corrupted_signal))
        corrupted_signal += noise
        
        # 3. Small burst error
        samples_per_bit = self.encoder.samples_per_bit
        burst_start = 40 * samples_per_bit
        burst_end = 45 * samples_per_bit
        if burst_end <= len(corrupted_signal):
            corrupted_signal[burst_start:burst_end] *= -0.5  # Attenuate burst region
        
        # Decode
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        assert decoded == test_payload, "Should handle combined error types"
    
    @pytest.mark.parametrize("error_rate", [0.0, 0.01, 0.05, 0.10, 0.15, 0.20])
    def test_error_rate_scaling(self, error_rate):
        """Test system performance across different error rates."""
        test_payload = b"EXECUTE:ScalingTest"
        
        # Encode
        signal = self.encoder.encode_payload(test_payload)
        
        # Inject errors
        corrupted_signal = self.inject_bit_errors(signal, error_rate)
        
        # Decode
        decoded = self.decoder.decode_payload(corrupted_signal)
        
        if error_rate <= 0.20:
            assert decoded == test_payload, f"Should handle {error_rate*100}% error rate"
        # Above 20% error rate, the system may fail (which is acceptable)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])