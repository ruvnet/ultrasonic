"""
Ultrasonic encoder for embedding data in near-ultrasonic frequency ranges.
Uses FSK (Frequency Shift Keying) modulation in the 18-20 kHz range.
"""

import numpy as np
from typing import Optional, Tuple
from pydub import AudioSegment
import hashlib


class UltrasonicEncoder:
    """Encoder for embedding data in ultrasonic frequencies using FSK."""
    
    def __init__(self, 
                 freq_0: float = 18500,
                 freq_1: float = 19500,
                 sample_rate: int = 48000,
                 bit_duration: float = 0.01,
                 amplitude: float = 0.1):
        """
        Initialize ultrasonic encoder.
        
        Args:
            freq_0: Frequency for bit '0' in Hz
            freq_1: Frequency for bit '1' in Hz 
            sample_rate: Audio sample rate in Hz
            bit_duration: Duration of each bit in seconds
            amplitude: Signal amplitude (0.0 to 1.0)
        """
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self.sample_rate = sample_rate
        self.bit_duration = bit_duration
        self.amplitude = amplitude
        
        # Calculate samples per bit
        self.samples_per_bit = int(sample_rate * bit_duration)
        
        # Validate frequency range
        nyquist = sample_rate / 2
        if freq_0 >= nyquist or freq_1 >= nyquist:
            raise ValueError(f"Frequencies must be below Nyquist frequency ({nyquist} Hz)")
    
    def encode_payload(self, payload: bytes, add_preamble: bool = True) -> np.ndarray:
        """
        Encode payload bytes into ultrasonic audio signal.
        
        Args:
            payload: Binary payload to encode
            add_preamble: Whether to add sync preamble
            
        Returns:
            Audio signal as numpy array
        """
        # Convert payload to bit string
        bit_string = self._payload_to_bits(payload)
        
        # Add error correction to payload only
        bit_string = self._add_error_correction(bit_string)
        
        # Add preamble for synchronization (after error correction)
        if add_preamble:
            preamble = self._generate_preamble()
            bit_string = preamble + bit_string
        
        # Generate FSK signal
        signal = self._generate_fsk_signal(bit_string)
        
        return signal
    
    def _payload_to_bits(self, payload: bytes) -> str:
        """Convert payload bytes to bit string."""
        bit_string = ""
        for byte in payload:
            bit_string += format(byte, '08b')
        return bit_string
    
    def _generate_preamble(self) -> str:
        """Generate synchronization preamble pattern."""
        # Alternating pattern for easy detection
        return "10101010" + "11110000" + "10101010"
    
    def _add_error_correction(self, bit_string: str) -> str:
        """Add simple but reliable error correction."""
        # Add 16-bit length prefix
        length_bits = format(len(bit_string), '016b')
        
        # Add simple repetition coding (3x) for robustness
        # Each bit is repeated 3 times, decoder uses majority voting
        repeated_bits = ""
        for bit in (length_bits + bit_string):
            repeated_bits += bit * 3  # Repeat each bit 3 times
        
        return repeated_bits
    
    def _add_crc_checksum(self, bit_string: str) -> str:
        """Add CRC-16 checksum for payload integrity validation."""
        # Convert bit string to bytes for CRC calculation
        byte_data = bytearray()
        for i in range(0, len(bit_string), 8):
            chunk = bit_string[i:i+8]
            if len(chunk) == 8:
                byte_data.append(int(chunk, 2))
            else:
                # Pad incomplete chunk
                padded_chunk = chunk.ljust(8, '0')
                byte_data.append(int(padded_chunk, 2))
        
        # Calculate CRC-16
        crc = self._calculate_crc16(bytes(byte_data))
        crc_bits = format(crc, '016b')
        
        # Prepend length information (16 bits) and CRC
        length_bits = format(len(bit_string), '016b')
        return length_bits + crc_bits + bit_string
    
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
    
    def _apply_hamming_codes(self, bit_string: str) -> str:
        """Apply Hamming (7,4) codes for forward error correction."""
        result = ""
        
        # Process in 4-bit chunks (data bits)
        for i in range(0, len(bit_string), 4):
            chunk = bit_string[i:i+4]
            
            # Pad incomplete chunk
            if len(chunk) < 4:
                chunk = chunk.ljust(4, '0')
            
            # Apply Hamming (7,4) encoding
            hamming_block = self._encode_hamming_7_4(chunk)
            result += hamming_block
        
        return result
    
    def _encode_hamming_7_4(self, data_bits: str) -> str:
        """Encode 4 data bits into 7-bit Hamming code."""
        # Data bits: d1, d2, d3, d4
        d1, d2, d3, d4 = [int(b) for b in data_bits]
        
        # Calculate parity bits
        p1 = d1 ^ d2 ^ d4  # Parity for positions 1,2,4
        p2 = d1 ^ d3 ^ d4  # Parity for positions 1,3,4
        p3 = d2 ^ d3 ^ d4  # Parity for positions 2,3,4
        
        # Hamming (7,4) codeword: p1 p2 d1 p3 d2 d3 d4
        return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"
    
    def _apply_interleaving(self, bit_string: str) -> str:
        """Apply bit interleaving to spread burst errors."""
        # Use block interleaving with depth 8
        interleave_depth = 8
        
        # Pad bit string to be divisible by interleave depth
        padding_needed = (interleave_depth - (len(bit_string) % interleave_depth)) % interleave_depth
        padded_bits = bit_string + '0' * padding_needed
        
        # Create interleaving matrix
        num_blocks = len(padded_bits) // interleave_depth
        matrix = []
        
        for i in range(num_blocks):
            block = padded_bits[i * interleave_depth:(i + 1) * interleave_depth]
            matrix.append(list(block))
        
        # Transpose matrix to interleave bits
        if matrix:
            interleaved = []
            for col in range(interleave_depth):
                for row in range(num_blocks):
                    if row < len(matrix) and col < len(matrix[row]):
                        interleaved.append(matrix[row][col])
            
            return ''.join(interleaved)
        
        return bit_string
    
    def _generate_fsk_signal(self, bit_string: str) -> np.ndarray:
        """Generate FSK modulated signal from bit string."""
        return self._modulate_fsk(bit_string)
    
    def _modulate_fsk(self, bit_string: str) -> np.ndarray:
        """
        Perform Frequency Shift Keying modulation on a bit string.
        
        Args:
            bit_string: String of '0' and '1' characters to modulate
            
        Returns:
            Modulated signal as numpy array
        """
        total_samples = len(bit_string) * self.samples_per_bit
        signal = np.zeros(total_samples)
        
        t = np.linspace(0, self.bit_duration, self.samples_per_bit, endpoint=False)
        
        for i, bit in enumerate(bit_string):
            start_idx = i * self.samples_per_bit
            end_idx = start_idx + self.samples_per_bit
            
            if bit == '0':
                freq = self.freq_0
            else:
                freq = self.freq_1
            
            # Generate sinusoidal tone for this bit
            tone = self.amplitude * np.sin(2 * np.pi * freq * t)
            
            # Apply windowing to reduce clicks
            tone = self._apply_windowing(tone)
            
            signal[start_idx:end_idx] = tone
        
        return signal
    
    def _apply_windowing(self, tone: np.ndarray) -> np.ndarray:
        """Apply minimal windowing to reduce spectral artifacts."""
        window_size = max(1, len(tone) // 100)  # 1% instead of 5% to preserve frequency content
        
        # Create gentle transitions that preserve frequency purity
        if window_size > 0:
            # Use gentler transitions (0.9-1.0 instead of 0.5-1.0)
            fade_in = np.linspace(0.9, 1, window_size)
            fade_out = np.linspace(1, 0.9, window_size)
            
            # Apply windowing
            tone[:window_size] *= fade_in
            tone[-window_size:] *= fade_out
        
        return tone
    
    def create_audio_segment(self, signal: np.ndarray) -> AudioSegment:
        """
        Convert numpy signal to AudioSegment.
        
        Args:
            signal: Audio signal as numpy array
            
        Returns:
            AudioSegment object
        """
        # Normalize signal to int16 range
        if signal.dtype != np.int16:
            # Scale to int16 range
            signal = signal / np.max(np.abs(signal)) * 0.8  # Leave headroom
            signal = (signal * 32767).astype(np.int16)
        
        # Create AudioSegment
        audio_segment = AudioSegment(
            signal.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,  # 16-bit
            channels=1
        )
        
        return audio_segment
    
    def estimate_payload_duration(self, payload_size: int) -> float:
        """
        Estimate duration needed for payload.
        
        Args:
            payload_size: Size of payload in bytes
            
        Returns:
            Duration in seconds
        """
        # Account for preamble, error correction, and bit encoding
        preamble_bits = len(self._generate_preamble())
        payload_bits = payload_size * 8
        
        # Add error correction overhead:
        # - 16-bit length prefix
        # - 3x repetition coding
        length_prefix_bits = 16
        data_with_prefix_bits = length_prefix_bits + payload_bits
        
        # Total bits after repetition coding
        total_payload_bits = data_with_prefix_bits * 3
        
        total_bits = preamble_bits + total_payload_bits
        
        return total_bits * self.bit_duration
    
    def get_frequency_range(self) -> Tuple[float, float]:
        """Get the frequency range used for encoding."""
        return (min(self.freq_0, self.freq_1), max(self.freq_0, self.freq_1))
    
    def set_frequencies(self, freq_0: float, freq_1: float) -> None:
        """
        Set new frequencies for FSK modulation.
        
        Args:
            freq_0: Frequency for bit '0' in Hz
            freq_1: Frequency for bit '1' in Hz
        """
        nyquist = self.sample_rate / 2
        if freq_0 >= nyquist or freq_1 >= nyquist:
            raise ValueError(f"Frequencies must be below Nyquist frequency ({nyquist} Hz)")
        
        self.freq_0 = freq_0
        self.freq_1 = freq_1
    
    def set_amplitude(self, amplitude: float) -> None:
        """
        Set signal amplitude.
        
        Args:
            amplitude: Signal amplitude (0.0 to 1.0)
        """
        if not 0.0 <= amplitude <= 1.0:
            raise ValueError("Amplitude must be between 0.0 and 1.0")
        
        self.amplitude = amplitude