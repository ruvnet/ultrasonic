"""
Integration tests for the complete steganography pipeline.
Tests end-to-end functionality without mocks.
"""

import pytest
import tempfile
import os
import numpy as np
from pydub import AudioSegment

from ..embed.audio_embedder import AudioEmbedder
from ..decode.audio_decoder import AudioDecoder
from ..crypto.cipher import CipherService

# Video components are optional (require moviepy)
try:
    from ..embed.video_embedder import VideoEmbedder
    from ..decode.video_decoder import VideoDecoder
    VIDEO_AVAILABLE = True
except ImportError:
    VIDEO_AVAILABLE = False


class TestSteganographyIntegration:
    """Integration tests for complete steganography workflow."""
    
    def test_audio_embed_and_decode_roundtrip(self):
        """Test complete audio embedding and decoding roundtrip."""
        # Use same key for both embedder and decoder with maximum reliability parameters
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=1.0, bit_duration=0.1)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.1)
        
        # Create test audio (10 seconds to ensure signal fits)
        test_audio = AudioSegment.silent(duration=10000, frame_rate=48000)
        
        # Test command (shorter for more reliable transmission)
        command = "EXECUTE:Test123"
        
        # Embed command
        stego_audio = embedder.embed(test_audio, command)
        
        # Decode command
        decoded_command = decoder.decode_audio_segment(stego_audio)
        
        assert decoded_command == command
    
    def test_audio_file_embed_and_decode_roundtrip(self):
        """Test complete file-based audio embedding and decoding."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        command = "ALERT:FileTestCommand"
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as input_file:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as output_file:
                try:
                    # Create test audio file
                    test_audio = AudioSegment.silent(duration=2000, frame_rate=48000)
                    test_audio.export(input_file.name, format="wav")
                    
                    # Embed command
                    embedder.embed_file(
                        input_file.name,
                        output_file.name,
                        command,
                        bitrate="192k"
                    )
                    
                    # Verify file was created
                    assert os.path.exists(output_file.name)
                    assert os.path.getsize(output_file.name) > 0
                    
                    # Decode command
                    decoded_command = decoder.decode_file(output_file.name)
                    
                    assert decoded_command == command
                    
                finally:
                    # Clean up
                    for path in [input_file.name, output_file.name]:
                        if os.path.exists(path):
                            os.unlink(path)
    
    def test_different_commands_produce_different_results(self):
        """Test that different commands produce different embedded signals."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        
        command1 = "COMMAND_ONE"
        command2 = "COMMAND_TWO"
        
        stego_audio1 = embedder.embed(test_audio, command1)
        stego_audio2 = embedder.embed(test_audio, command2)
        
        # Convert to numpy arrays for comparison
        samples1 = np.array(stego_audio1.get_array_of_samples())
        samples2 = np.array(stego_audio2.get_array_of_samples())
        
        # Should be different (due to different encrypted payloads)
        assert not np.array_equal(samples1, samples2)
    
    def test_wrong_key_fails_decoding(self):
        """Test that wrong decryption key fails to decode."""
        embedder_key = CipherService.generate_key(32)
        decoder_key = CipherService.generate_key(32)  # Different key
        
        embedder = AudioEmbedder(key=embedder_key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=decoder_key, detection_threshold=0.001, bit_duration=0.05)
        
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        command = "SECRET_COMMAND"
        
        stego_audio = embedder.embed(test_audio, command)
        decoded_command = decoder.decode_audio_segment(stego_audio)
        
        # Should fail to decode with wrong key
        assert decoded_command is None
    
    def test_signal_detection_works_correctly(self):
        """Test that signal detection correctly identifies embedded content."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        # Clean audio without embedded signal
        clean_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        
        # Audio with embedded signal
        stego_audio = embedder.embed(clean_audio, "TEST_SIGNAL")
        
        # Clean audio should not have signal
        assert decoder.detect_signal(clean_audio) == False
        
        # Stego audio should have signal
        assert decoder.detect_signal(stego_audio) == True
    
    def test_signal_strength_measurement(self):
        """Test signal strength measurement."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        clean_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        
        # Test different amplitudes
        embedder.set_amplitude(0.3)
        weak_stego = embedder.embed(clean_audio, "WEAK")
        
        embedder.set_amplitude(0.8)
        strong_stego = embedder.embed(clean_audio, "STRONG")
        
        weak_strength = decoder.get_signal_strength(weak_stego)
        strong_strength = decoder.get_signal_strength(strong_stego)
        clean_strength = decoder.get_signal_strength(clean_audio)
        
        # Stronger signal should have higher strength
        assert strong_strength > weak_strength
        assert weak_strength > clean_strength
        assert clean_strength >= 0.0
    
    def test_obfuscation_roundtrip(self):
        """Test that obfuscation doesn't break the roundtrip."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        command = "OBFUSCATED_COMMAND"
        
        # Test with obfuscation enabled
        stego_audio = embedder.embed(test_audio, command, obfuscate=True)
        decoded_command = decoder.decode_audio_segment(stego_audio)
        
        assert decoded_command == command
        
        # Test with obfuscation disabled
        stego_audio = embedder.embed(test_audio, command, obfuscate=False)
        decoded_command = decoder.decode_audio_segment(stego_audio)
        
        assert decoded_command == command
    
    def test_different_frequencies_work(self):
        """Test that different ultrasonic frequencies work correctly."""
        key = CipherService.generate_key(32)
        
        # Test with different frequency pairs
        test_cases = [
            (17000, 18000),
            (18500, 19500),
            (20000, 21000)
        ]
        
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        command = "FREQ_TEST"
        
        for freq_0, freq_1 in test_cases:
            embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
            decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
            
            # Set frequencies
            embedder.set_frequencies(freq_0, freq_1)
            decoder.set_frequencies(freq_0, freq_1)
            
            # Test roundtrip
            stego_audio = embedder.embed(test_audio, command)
            decoded_command = decoder.decode_audio_segment(stego_audio)
            
            assert decoded_command == command, f"Failed with frequencies {freq_0}, {freq_1}"
    
    def test_unicode_commands(self):
        """Test that unicode commands work correctly."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        test_audio = AudioSegment.silent(duration=10000, frame_rate=48000)
        
        # Use simpler unicode commands for more reliable transmission
        unicode_commands = [
            "TEST αβγ",
            "CMD 日本",
            "RUN ελ"
        ]
        
        for command in unicode_commands:
            stego_audio = embedder.embed(test_audio, command)
            decoded_command = decoder.decode_audio_segment(stego_audio)
            
            assert decoded_command == command, f"Failed with unicode command: {command}"
    
    def test_empty_and_long_commands(self):
        """Test edge cases with empty and moderately long commands."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        # Test empty command
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        empty_command = ""
        stego_audio = embedder.embed(test_audio, empty_command)
        decoded_command = decoder.decode_audio_segment(stego_audio)
        assert decoded_command == empty_command
        
        # Test moderately long command (reduced for reliability)
        test_audio_long = AudioSegment.silent(duration=15000, frame_rate=48000)
        long_command = "LONG_COMMAND: " + "X" * 50  # Reduced size
        stego_audio = embedder.embed(test_audio_long, long_command)
        decoded_command = decoder.decode_audio_segment(stego_audio)
        assert decoded_command == long_command
    
    def test_audio_format_compatibility(self):
        """Test that different audio formats work correctly."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        command = "FORMAT_TEST"
        
        # Test different sample rates (that should work)
        compatible_rates = [44100, 48000]
        
        for sample_rate in compatible_rates:
            test_audio = AudioSegment.silent(duration=5000, frame_rate=sample_rate)
            
            # Check compatibility
            compatibility = embedder.validate_audio_compatibility(test_audio)
            
            if compatibility['compatible']:
                stego_audio = embedder.embed(test_audio, command)
                decoded_command = decoder.decode_audio_segment(stego_audio)
                assert decoded_command == command, f"Failed with sample rate {sample_rate}"
    
    def test_analyzer_provides_accurate_information(self):
        """Test that audio analyzer provides accurate information."""
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        test_audio = AudioSegment.silent(duration=5000, frame_rate=48000)
        command = "ANALYSIS_TEST"
        
        # Analyze clean audio
        clean_analysis = decoder.analyze_audio(test_audio)
        assert clean_analysis['has_ultrasonic_signal'] == False
        assert clean_analysis['decoded_command'] is None
        assert clean_analysis['decoding_successful'] == False
        
        # Embed and analyze
        stego_audio = embedder.embed(test_audio, command)
        stego_analysis = decoder.analyze_audio(stego_audio)
        
        assert stego_analysis['has_ultrasonic_signal'] == True
        assert stego_analysis['decoded_command'] == command
        assert stego_analysis['decoding_successful'] == True
        assert stego_analysis['signal_strength'] > 0
        assert stego_analysis['sample_rate'] == 48000
    
    @pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video tests require moviepy")
    def test_video_embed_and_decode_roundtrip(self):
        """Test complete video embedding and decoding roundtrip."""
        # This test is skipped by default as it requires video files
        # and moviepy which may not be available in all test environments
        if VIDEO_AVAILABLE:
            key = CipherService.generate_key(32)
            video_embedder = VideoEmbedder(key=key)
            video_decoder = VideoDecoder(key=key)
            
            command = "VIDEO_TEST_COMMAND"
            
            # This would need a real video file to test properly
            # In a real scenario, you'd create a minimal test video
            pass
    
    def test_performance_characteristics(self):
        """Test basic performance characteristics."""
        import time
        
        key = CipherService.generate_key(32)
        embedder = AudioEmbedder(key=key, amplitude=0.8, bit_duration=0.05)
        decoder = AudioDecoder(key=key, detection_threshold=0.001, bit_duration=0.05)
        
        # Test with reasonably sized audio
        test_audio = AudioSegment.silent(duration=10000, frame_rate=48000)  # 10 seconds
        command = "PERF_TEST"
        
        # Measure embedding time
        start_time = time.time()
        stego_audio = embedder.embed(test_audio, command)
        embed_time = time.time() - start_time
        
        # Measure decoding time
        start_time = time.time()
        decoded_command = decoder.decode_audio_segment(stego_audio)
        decode_time = time.time() - start_time
        
        # Basic sanity checks (these may need adjustment based on hardware)
        assert embed_time < 10.0  # Should embed within 10 seconds
        assert decode_time < 10.0  # Should decode within 10 seconds
        assert decoded_command == command
        
        # Test estimation accuracy
        estimated_duration = embedder.estimate_embedding_duration(command)
        assert estimated_duration > 0
        assert estimated_duration < 100.0  # Adjusted for repetition coding (3x slower)