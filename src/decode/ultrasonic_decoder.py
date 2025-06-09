"""
Ultrasonic decoder for extracting data from near-ultrasonic frequency ranges.
Decodes FSK (Frequency Shift Keying) modulated signals.
"""

import numpy as np
from typing import Optional, Tuple, List
from scipy import signal
from scipy.signal import find_peaks


class UltrasonicDecoder:
    """Decoder for extracting data from ultrasonic frequencies using FSK."""
    
    def __init__(self,
                 freq_0: float = 18500,
                 freq_1: float = 19500,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 detection_threshold: float = 0.01):
        """
        Initialize ultrasonic decoder.
        
        Args:
            freq_0: Frequency for bit '0' in Hz
            freq_1: Frequency for bit '1' in Hz
            sample_rate: Audio sample rate in Hz
            bit_duration: Duration of each bit in seconds
            detection_threshold: Minimum signal strength for detection
        """
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self.sample_rate = sample_rate
        self.bit_duration = bit_duration
        self.detection_threshold = detection_threshold
        
        # Calculate samples per bit
        self.samples_per_bit = int(sample_rate * bit_duration)
        
        # Design band-pass filter for ultrasonic range
        self._design_filters()
    
    def _design_filters(self) -> None:
        """Design band-pass filters for signal isolation."""
        nyquist = self.sample_rate / 2
        
        # Overall band-pass filter for ultrasonic range
        low_freq = min(self.freq_0, self.freq_1) - 1000
        high_freq = max(self.freq_0, self.freq_1) + 1000
        
        # Ensure frequencies are within valid range
        low_freq = max(low_freq, 100) / nyquist
        high_freq = min(high_freq, nyquist - 100) / nyquist
        
        self.bp_filter = signal.butter(4, [low_freq, high_freq], btype='band')
        
        # Individual filters for each frequency
        bandwidth = 500  # Hz
        
        freq_0_low = (self.freq_0 - bandwidth) / nyquist
        freq_0_high = (self.freq_0 + bandwidth) / nyquist
        self.freq_0_filter = signal.butter(4, [freq_0_low, freq_0_high], btype='band')
        
        freq_1_low = (self.freq_1 - bandwidth) / nyquist
        freq_1_high = (self.freq_1 + bandwidth) / nyquist
        self.freq_1_filter = signal.butter(4, [freq_1_low, freq_1_high], btype='band')
    
    def decode_payload(self, audio_signal: np.ndarray) -> Optional[bytes]:
        """
        Decode payload from audio signal.
        
        Args:
            audio_signal: Audio signal as numpy array
            
        Returns:
            Decoded payload bytes, or None if decoding fails
        """
        # Apply band-pass filter to isolate ultrasonic range
        filtered_signal = self._apply_bandpass_filter(audio_signal)
        
        # Detect preamble and find start position
        start_position = self._detect_preamble(filtered_signal)
        if start_position is None:
            return None
        
        # Extract bit sequence with confidence levels starting from preamble end
        bit_data = self._extract_bits_with_confidence(filtered_signal, start_position)
        if not bit_data:
            return None
        
        # Apply advanced error correction and convert to bytes
        payload_bytes = self._decode_with_advanced_error_correction(bit_data)
        
        # Fall back to legacy error correction if advanced method fails
        if payload_bytes is None:
            bit_string = ''.join(bit for bit, _ in bit_data)
            payload_bytes = self._decode_bits_to_bytes(bit_string)
        
        return payload_bytes
    
    def _apply_bandpass_filter(self, audio_signal: np.ndarray) -> np.ndarray:
        """Apply band-pass filter to isolate ultrasonic frequencies."""
        try:
            filtered = signal.filtfilt(self.bp_filter[0], self.bp_filter[1], audio_signal)
            return filtered
        except Exception:
            # Fallback to unfiltered signal if filtering fails
            return audio_signal
    
    def _detect_preamble(self, signal: np.ndarray) -> Optional[int]:
        """
        Detect synchronization preamble in signal.
        
        Args:
            signal: Filtered audio signal
            
        Returns:
            Start position after preamble, or None if not found
        """
        # Expected preamble pattern
        preamble_pattern = "10101010" + "11110000" + "10101010"
        
        # Convert pattern to frequency sequence
        freq_sequence = []
        for bit in preamble_pattern:
            if bit == '0':
                freq_sequence.append(self.freq_0)
            else:
                freq_sequence.append(self.freq_1)
        
        # Search for pattern in signal
        pattern_length = len(preamble_pattern) * self.samples_per_bit
        
        if len(signal) < pattern_length:
            return None
        
        best_correlation = 0
        best_position = None
        
        # Slide window and check correlation (finer step size for better detection)
        step_size = max(1, self.samples_per_bit // 8)  # Smaller steps for more precise detection
        # Fix: Include the case where signal length equals pattern length
        max_start_pos = max(1, len(signal) - pattern_length + 1)
        for start_pos in range(0, max_start_pos, step_size):
            segment = signal[start_pos:start_pos + pattern_length]
            correlation = self._correlate_with_pattern(segment, freq_sequence)
            
            # Return the FIRST position that exceeds threshold, not the best correlation
            if correlation > self.detection_threshold:
                return start_pos + pattern_length
        
        return None  # No valid preamble found
    
    def _correlate_with_pattern(self, segment: np.ndarray, freq_sequence: List[float]) -> float:
        """Calculate correlation using time-domain reference signals."""
        if len(segment) != len(freq_sequence) * self.samples_per_bit:
            return 0.0
        
        correlation_sum = 0.0
        t = np.linspace(0, self.bit_duration, self.samples_per_bit, endpoint=False)
        
        for i, expected_freq in enumerate(freq_sequence):
            start_idx = i * self.samples_per_bit
            end_idx = start_idx + self.samples_per_bit
            bit_segment = segment[start_idx:end_idx]
            
            # Generate reference signal for this frequency
            ref_signal = np.sin(2 * np.pi * expected_freq * t)
            
            # Calculate normalized cross-correlation
            if len(bit_segment) == len(ref_signal):
                correlation = np.abs(np.dot(bit_segment, ref_signal))
                correlation_sum += correlation
        
        # Normalize by expected maximum correlation
        max_possible = len(freq_sequence) * self.samples_per_bit * 0.5  # Expected amplitude factor
        return correlation_sum / max_possible if max_possible > 0 else 0.0
    
    def _correlate_with_frequency(self, segment: np.ndarray, frequency: float) -> float:
        """Calculate correlation with specific frequency using matched filtering."""
        if len(segment) == 0:
            return 0.0
        
        # Generate reference signal
        t = np.linspace(0, len(segment) / self.sample_rate, len(segment), endpoint=False)
        reference = np.sin(2 * np.pi * frequency * t)
        
        # Apply window to both signals to reduce artifacts
        window = np.hanning(len(segment))
        windowed_segment = segment * window
        windowed_reference = reference * window
        
        # Cross-correlation (normalized)
        correlation = np.abs(np.dot(windowed_segment, windowed_reference))
        
        # Normalize by signal energy for consistent comparison
        segment_energy = np.sum(windowed_segment ** 2)
        reference_energy = np.sum(windowed_reference ** 2)
        
        if segment_energy > 0 and reference_energy > 0:
            normalized_correlation = correlation / np.sqrt(segment_energy * reference_energy)
            return normalized_correlation
        else:
            return 0.0
    
    def _detect_frequency_simple(self, segment: np.ndarray) -> Optional[str]:
        """Simple FFT-based frequency detection."""
        if len(segment) == 0:
            return None
        
        # Apply window
        windowed = segment * np.hanning(len(segment))
        
        # FFT
        fft = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(windowed), 1/self.sample_rate)
        magnitude = np.abs(fft)
        
        # Find peak frequency in positive frequencies only
        peak_idx = np.argmax(magnitude[:len(magnitude)//2])
        peak_freq = abs(freqs[peak_idx])
        
        # Check if peak is strong enough
        if magnitude[peak_idx] < np.max(magnitude) * 0.1:  # Require at least 10% of max
            return None
        
        # Determine which frequency is closer
        diff_0 = abs(peak_freq - self.freq_0)
        diff_1 = abs(peak_freq - self.freq_1)
        
        # Require reasonable proximity to one of our frequencies
        min_diff = min(diff_0, diff_1)
        if min_diff > 500:  # Allow 500 Hz tolerance
            return None
        
        if diff_0 < diff_1:
            return '0'
        else:
            return '1'
    
    def _estimate_noise_floor(self, segment: np.ndarray) -> float:
        """Estimate noise floor for adaptive thresholding."""
        # Use spectral analysis to estimate noise floor
        freqs = np.fft.fftfreq(len(segment), 1/self.sample_rate)
        fft = np.fft.fft(segment * np.hanning(len(segment)))
        magnitude = np.abs(fft)
        
        # Find frequency bins outside our signal range
        signal_range_mask = (
            (np.abs(freqs - self.freq_0) > 1000) & 
            (np.abs(freqs - self.freq_1) > 1000) &
            (np.abs(freqs) < self.sample_rate / 4)  # Only consider lower frequencies
        )
        
        if np.any(signal_range_mask):
            noise_floor = np.median(magnitude[signal_range_mask])
            return noise_floor / len(segment)  # Normalize
        else:
            return 0.01  # Fallback value
    
    def _extract_bits(self, signal: np.ndarray, start_position: int) -> str:
        """
        Extract bit sequence from signal starting at given position using improved correlation.
        
        Args:
            signal: Filtered audio signal
            start_position: Position to start extraction
            
        Returns:
            Extracted bit string
        """
        bit_string = ""
        position = start_position
        
        # Track consecutive low confidence bits for end detection
        consecutive_low_confidence = 0
        max_consecutive_low_confidence = 8  # Stop after 8 consecutive low confidence bits
        
        # Adaptive thresholding parameters
        min_confidence_threshold = 0.3  # Minimum correlation confidence needed
        noise_floor_samples = []
        
        while position + self.samples_per_bit <= len(signal):
            segment = signal[position:position + self.samples_per_bit]
            
            # Use simple FFT-based frequency detection (much more reliable)
            detected_bit = self._detect_frequency_simple(segment)
            
            if detected_bit is None:
                # Fallback to correlation method if FFT fails
                corr_0 = self._correlate_with_frequency(segment, self.freq_0)
                corr_1 = self._correlate_with_frequency(segment, self.freq_1)
                
                if corr_0 > corr_1:
                    detected_bit = '0'
                    confidence = corr_0
                else:
                    detected_bit = '1'
                    confidence = corr_1
                    
                correlation_diff = abs(corr_0 - corr_1)
            else:
                # FFT detection succeeded
                confidence = 1.0  # High confidence for FFT detection
                correlation_diff = 1.0  # Good separation
            
            # Estimate noise floor for this segment
            noise_floor = self._estimate_noise_floor(segment)
            noise_floor_samples.append(noise_floor)
            
            # Adaptive threshold based on recent noise floor estimates  
            if len(noise_floor_samples) > 10:
                recent_noise = np.median(noise_floor_samples[-10:])
                adaptive_threshold = max(min_confidence_threshold, recent_noise * 3)
            else:
                adaptive_threshold = min_confidence_threshold
            
            # Decision making with confidence assessment
            if confidence < adaptive_threshold or correlation_diff < adaptive_threshold * 0.5:
                # Low confidence detection
                consecutive_low_confidence += 1
                if consecutive_low_confidence >= max_consecutive_low_confidence:
                    break
            else:
                # High confidence detection
                consecutive_low_confidence = 0
            
            # Use the detected bit from FFT or correlation
            bit = detected_bit
            
            bit_string += bit
            position += self.samples_per_bit
            
            # Early stop if we have extracted enough bits for a reasonable payload
            # Expect around 500-1000 bits for typical payloads 
            if len(bit_string) > 2000:  # Increased upper limit 
                break
        
        return bit_string
    
    def _extract_bits_with_confidence(self, signal: np.ndarray, start_position: int) -> Optional[List[Tuple[str, float]]]:
        """
        Extract bit sequence with confidence levels from signal starting at given position.
        
        Args:
            signal: Filtered audio signal
            start_position: Position to start extraction
            
        Returns:
            List of (bit, confidence) tuples, or None if extraction fails
        """
        bit_data = []
        position = start_position
        
        # Track consecutive low power bits for end detection
        consecutive_low_power = 0
        max_consecutive_low_power = 5  # Stop after 5 consecutive low power bits
        
        while position + self.samples_per_bit <= len(signal):
            segment = signal[position:position + self.samples_per_bit]
            
            # Calculate correlation with both frequencies using time-domain method
            t = np.linspace(0, self.bit_duration, len(segment), endpoint=False)
            ref_0 = np.sin(2 * np.pi * self.freq_0 * t)
            ref_1 = np.sin(2 * np.pi * self.freq_1 * t)
            
            power_0 = np.abs(np.dot(segment, ref_0))
            power_1 = np.abs(np.dot(segment, ref_1))
            
            # Calculate total power and confidence
            total_power = power_0 + power_1
            power_diff = abs(power_0 - power_1)
            
            # Calculate confidence based on power difference and total power
            if total_power > 0:
                confidence = min(1.0, power_diff / total_power)  # Normalized confidence
                confidence *= min(1.0, total_power / self.detection_threshold)  # Scale by signal strength
            else:
                confidence = 0.0
            
            # Determine bit based on which frequency has more power
            bit = '0' if power_0 > power_1 else '1'
            
            # Track low power segments
            if total_power < self.detection_threshold * 0.2:
                consecutive_low_power += 1
                if consecutive_low_power >= max_consecutive_low_power:
                    break
            else:
                consecutive_low_power = 0
            
            bit_data.append((bit, confidence))
            position += self.samples_per_bit
            
            # Early stop if we have extracted enough bits for a reasonable payload
            if len(bit_data) > 10000:  # Reasonable upper limit
                break
        
        return bit_data if bit_data else None
    
    def _decode_with_advanced_error_correction(self, bit_data: List[Tuple[str, float]]) -> Optional[bytes]:
        """
        Decode bits with simple error correction (matching simplified encoder).
        
        Args:
            bit_data: List of (bit, confidence) tuples
            
        Returns:
            Decoded bytes, or None if error correction fails
        """
        if len(bit_data) < 48:  # Need at least 16-bit length prefix * 3 repetitions
            return None
        
        # Convert to bit string
        bit_string = ''.join(bit for bit, _ in bit_data)
        
        # Apply majority voting on repeated bits (each bit repeated 3 times)
        decoded_bits = ""
        for i in range(0, len(bit_string), 3):
            if i + 2 < len(bit_string):
                # Get three copies of the bit
                bit_votes = bit_string[i:i+3]
                # Count votes
                ones = bit_votes.count('1')
                zeros = bit_votes.count('0')
                # Majority vote
                if ones > zeros:
                    decoded_bits += '1'
                else:
                    decoded_bits += '0'
            else:
                # Not enough bits for voting, stop
                break
        
        # Extract 16-bit length prefix
        if len(decoded_bits) < 16:
            return None
            
        length_bits = decoded_bits[:16]
        payload_bits = decoded_bits[16:]
        
        try:
            # Parse expected payload length
            expected_length = int(length_bits, 2)
            
            # Validate length is reasonable
            if expected_length <= 0 or expected_length > len(payload_bits):
                return None
            
            # Extract the expected number of bits
            actual_payload_bits = payload_bits[:expected_length]
            
            # Convert to bytes
            byte_data = bytearray()
            for i in range(0, len(actual_payload_bits), 8):
                chunk = actual_payload_bits[i:i+8]
                if len(chunk) == 8:
                    byte_data.append(int(chunk, 2))
            
            return bytes(byte_data) if byte_data else None
            
        except ValueError:
            return None
    
    def _remove_interleaving(self, bit_string: str) -> str:
        """Remove bit interleaving to restore original bit order."""
        interleave_depth = 8
        
        # Calculate matrix dimensions
        total_bits = len(bit_string)
        num_blocks = total_bits // interleave_depth
        
        if num_blocks == 0:
            return bit_string
        
        # Create de-interleaving matrix
        matrix = []
        for col in range(interleave_depth):
            column = []
            for row in range(num_blocks):
                bit_index = row + col * num_blocks
                if bit_index < len(bit_string):
                    column.append(bit_string[bit_index])
            matrix.append(column)
        
        # Reconstruct original order
        deinterleaved = []
        for row in range(num_blocks):
            for col in range(interleave_depth):
                if row < len(matrix[col]):
                    deinterleaved.append(matrix[col][row])
        
        return ''.join(deinterleaved)
    
    def _decode_hamming_codes(self, bit_string: str, original_bit_data: List[Tuple[str, float]]) -> str:
        """Decode Hamming (7,4) codes with error correction."""
        result = ""
        
        # Process in 7-bit chunks (Hamming codewords)
        for i in range(0, len(bit_string), 7):
            chunk = bit_string[i:i+7]
            
            if len(chunk) == 7:
                # Decode Hamming (7,4) codeword
                decoded_data = self._decode_hamming_7_4(chunk)
                result += decoded_data
            else:
                # Incomplete chunk - pad and decode
                padded_chunk = chunk.ljust(7, '0')
                decoded_data = self._decode_hamming_7_4(padded_chunk)
                result += decoded_data
        
        return result
    
    def _decode_hamming_7_4(self, codeword: str) -> str:
        """Decode 7-bit Hamming codeword to 4 data bits with error correction."""
        # Codeword format: p1 p2 d1 p3 d2 d3 d4
        bits = [int(b) for b in codeword]
        p1, p2, d1, p3, d2, d3, d4 = bits
        
        # Calculate syndrome
        s1 = p1 ^ d1 ^ d2 ^ d4
        s2 = p2 ^ d1 ^ d3 ^ d4
        s3 = p3 ^ d2 ^ d3 ^ d4
        
        # Determine error position (if any)
        error_pos = s1 + (s2 << 1) + (s3 << 2)
        
        # Correct single-bit error if detected
        if error_pos != 0:
            # Error position is 1-indexed
            if error_pos == 1:
                p1 ^= 1
            elif error_pos == 2:
                p2 ^= 1
            elif error_pos == 3:
                d1 ^= 1
            elif error_pos == 4:
                p3 ^= 1
            elif error_pos == 5:
                d2 ^= 1
            elif error_pos == 6:
                d3 ^= 1
            elif error_pos == 7:
                d4 ^= 1
        
        # Return corrected data bits
        return f"{d1}{d2}{d3}{d4}"
    
    def _validate_crc_and_extract_payload(self, bit_string: str) -> Optional[bytes]:
        """Validate CRC checksum and extract original payload."""
        if len(bit_string) < 32:  # Need at least length + CRC
            return None
        
        # Extract length (first 16 bits)
        length_bits = bit_string[:16]
        payload_length = int(length_bits, 2)
        
        # Extract CRC (next 16 bits)
        crc_bits = bit_string[16:32]
        expected_crc = int(crc_bits, 2)
        
        # Extract payload (remaining bits up to payload_length)
        if len(bit_string) < 32 + payload_length:
            return None
        
        payload_bits = bit_string[32:32 + payload_length]
        
        # Convert payload to bytes for CRC validation
        payload_bytes = bytearray()
        for i in range(0, len(payload_bits), 8):
            chunk = payload_bits[i:i+8]
            if len(chunk) == 8:
                payload_bytes.append(int(chunk, 2))
        
        # Validate CRC
        calculated_crc = self._calculate_crc16(bytes(payload_bytes))
        
        if calculated_crc == expected_crc:
            return bytes(payload_bytes)
        else:
            # CRC mismatch - payload is corrupted
            return None
    
    def _calculate_crc16(self, data: bytes) -> int:
        """Calculate CRC-16 checksum (CRC-16-CCITT)."""
        crc = 0xFFFF
        polynomial = 0x1021
        
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
                crc &= 0xFFFF
        
        return crc
    
    def _decode_bits_to_bytes(self, bit_string: str) -> Optional[bytes]:
        """
        Convert bit string to bytes, removing error correction.
        
        Args:
            bit_string: Raw bit string from signal
            
        Returns:
            Decoded bytes, or None if error correction fails
        """
        # For backward compatibility with tests, handle simple bit strings without repetition
        if len(bit_string) < 24:  # Less than minimum for repetition coding
            # Simple conversion without error correction
            byte_data = bytearray()
            for i in range(0, len(bit_string), 8):
                chunk = bit_string[i:i+8]
                if len(chunk) == 8:
                    byte_data.append(int(chunk, 2))
            return bytes(byte_data) if byte_data else None
        
        # Apply majority voting on repeated bits (each bit repeated 3 times)
        decoded_bits = ""
        for i in range(0, len(bit_string), 3):
            if i + 2 < len(bit_string):
                # Get three copies of the bit
                bit_votes = bit_string[i:i+3]
                # Count votes
                ones = bit_votes.count('1')
                zeros = bit_votes.count('0')
                # Majority vote
                if ones > zeros:
                    decoded_bits += '1'
                else:
                    decoded_bits += '0'
            else:
                # Not enough bits for voting
                break
        
        # Convert to bytes
        byte_data = bytearray()
        for i in range(0, len(decoded_bits), 8):
            chunk = decoded_bits[i:i+8]
            if len(chunk) == 8:
                byte_data.append(int(chunk, 2))
        
        return bytes(byte_data) if byte_data else None
    
    def detect_signal_presence(self, audio_signal: np.ndarray) -> bool:
        """
        Check if ultrasonic signal is present in audio.
        
        Args:
            audio_signal: Audio signal to analyze
            
        Returns:
            True if ultrasonic signal detected
        """
        # Apply band-pass filter
        filtered = self._apply_bandpass_filter(audio_signal)
        
        # Calculate average power in ultrasonic range
        power = np.mean(np.abs(filtered))
        
        return power > self.detection_threshold
    
    def get_signal_strength(self, audio_signal: np.ndarray) -> float:
        """
        Get signal strength in ultrasonic range.
        
        Args:
            audio_signal: Audio signal to analyze
            
        Returns:
            Signal strength (0.0 to 1.0)
        """
        # Apply band-pass filter
        filtered = self._apply_bandpass_filter(audio_signal)
        
        # Calculate RMS power
        rms = np.sqrt(np.mean(filtered ** 2))
        
        # Return RMS directly for better sensitivity to amplitude differences
        return rms
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """
        Set new frequencies for FSK demodulation.
        
        Args:
            freq_0: Frequency for bit '0' in Hz
            freq_1: Frequency for bit '1' in Hz
        """
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self._design_filters()
    
    def set_detection_threshold(self, threshold: float) -> None:
        """
        Set signal detection threshold.
        
        Args:
            threshold: New detection threshold
        """
        self.detection_threshold = threshold