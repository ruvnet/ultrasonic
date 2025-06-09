"""
Comprehensive API endpoint tests using FastAPI TestClient.
Tests all REST endpoints with various scenarios and edge cases.
"""

import pytest
import os
import tempfile
import base64
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from io import BytesIO

# Import the FastAPI app
from agentic_commands_stego.server.api import app
from agentic_commands_stego.crypto.cipher import CipherService


class TestAPIEndpoints:
    """Test suite for FastAPI REST endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)
    
    @pytest.fixture
    def sample_audio_file(self):
        """Create a mock audio file for testing."""
        # Create a simple WAV header for a valid audio file
        wav_header = b'RIFF' + b'\x00' * 4 + b'WAVE' + b'fmt ' + b'\x10\x00\x00\x00'
        wav_header += b'\x01\x00\x02\x00' + b'\x44\xac\x00\x00' + b'\x10\xb1\x02\x00'
        wav_header += b'\x04\x00\x10\x00' + b'data' + b'\x00' * 4
        # Add some audio data
        audio_data = b'\x00' * 1000
        return BytesIO(wav_header + audio_data)
    
    @pytest.fixture
    def sample_video_file(self):
        """Create a mock video file for testing."""
        # Simple MP4 file signature
        mp4_header = b'\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2mp41'
        return BytesIO(mp4_header + b'\x00' * 1000)
    
    def test_api_info_endpoint(self, client):
        """Test GET /info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Agentic Commands Steganography API"
        assert data["version"] == "1.0.0"
        assert "audio" in data["supported_formats"]
        assert "video" in data["supported_formats"]
        assert data["encryption"] == "AES-256-GCM"
        assert data["steganography"] == "Ultrasonic FSK"
    
    def test_health_check_endpoint(self, client):
        """Test GET /health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
    
    @patch('agentic_commands_stego.embed.audio_embedder.AudioEmbedder.embed_file')
    def test_embed_audio_success(self, mock_embed, client, sample_audio_file):
        """Test successful audio embedding."""
        # Mock the embedding process
        mock_embed.return_value = None
        
        files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
        data = {
            "command": "test command",
            "obfuscate": "true",
            "bitrate": "192k",
            "ultrasonic_freq": "18500",
            "amplitude": "0.1"
        }
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            with patch('os.path.exists', return_value=True):
                with patch('agentic_commands_stego.server.api.FileResponse') as mock_response:
                    mock_response.return_value = MagicMock(status_code=200)
                    
                    response = client.post("/embed/audio", files=files, data=data)
                    assert response.status_code == 200
                    mock_embed.assert_called_once()
    
    def test_embed_audio_invalid_format(self, client):
        """Test audio embedding with invalid file format."""
        files = {"file": ("test.txt", BytesIO(b"not an audio file"), "text/plain")}
        data = {"command": "test command"}
        
        response = client.post("/embed/audio", files=files, data=data)
        assert response.status_code == 400
        assert "Unsupported audio format" in response.json()["detail"]
    
    def test_embed_audio_missing_command(self, client, sample_audio_file):
        """Test audio embedding without command parameter."""
        files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
        
        response = client.post("/embed/audio", files=files)
        assert response.status_code == 422  # Unprocessable Entity
    
    @patch('agentic_commands_stego.embed.video_embedder.VideoEmbedder.embed_file')
    def test_embed_video_success(self, mock_embed, client, sample_video_file):
        """Test successful video embedding."""
        mock_embed.return_value = None
        
        files = {"file": ("test.mp4", sample_video_file, "video/mp4")}
        data = {
            "command": "test video command",
            "obfuscate": "true",
            "audio_bitrate": "192k",
            "ultrasonic_freq": "18500",
            "amplitude": "0.1"
        }
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.mp4"
            with patch('os.path.exists', return_value=True):
                with patch('agentic_commands_stego.server.api.FileResponse') as mock_response:
                    mock_response.return_value = MagicMock(status_code=200)
                    
                    response = client.post("/embed/video", files=files, data=data)
                    assert response.status_code == 200
                    mock_embed.assert_called_once()
    
    def test_embed_video_invalid_format(self, client):
        """Test video embedding with invalid file format."""
        files = {"file": ("test.gif", BytesIO(b"GIF89a"), "image/gif")}
        data = {"command": "test command"}
        
        response = client.post("/embed/video", files=files, data=data)
        assert response.status_code == 400
        assert "Unsupported video format" in response.json()["detail"]
    
    @patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.decode_file')
    @patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.analyze_audio')
    def test_decode_audio_success(self, mock_analyze, mock_decode, client, sample_audio_file):
        """Test successful audio decoding."""
        mock_decode.return_value = "decoded command"
        mock_analyze.return_value = {"ultrasonic_detected": True, "confidence": 0.95}
        
        files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            
            response = client.post("/decode/audio", files=files)
            assert response.status_code == 200
            
            data = response.json()
            assert data["command"] == "decoded command"
            assert data["success"] is True
            assert "analysis" in data
            assert data["analysis"]["ultrasonic_detected"] is True
    
    def test_decode_audio_no_command(self, client, sample_audio_file):
        """Test audio decoding when no command is found."""
        with patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.decode_file', return_value=None):
            with patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.analyze_audio', 
                      return_value={"ultrasonic_detected": False}):
                
                files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
                
                with patch('tempfile.NamedTemporaryFile') as mock_temp:
                    mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
                    
                    response = client.post("/decode/audio", files=files)
                    assert response.status_code == 200
                    
                    data = response.json()
                    assert data["command"] is None
                    assert data["success"] is False
    
    @patch('agentic_commands_stego.decode.video_decoder.VideoDecoder.decode_file')
    @patch('agentic_commands_stego.decode.video_decoder.VideoDecoder.analyze_video')
    def test_decode_video_success(self, mock_analyze, mock_decode, client, sample_video_file):
        """Test successful video decoding."""
        mock_decode.return_value = "video command"
        mock_analyze.return_value = {
            "audio_track_present": True,
            "ultrasonic_detected": True,
            "confidence": 0.88
        }
        
        files = {"file": ("test.mp4", sample_video_file, "video/mp4")}
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.mp4"
            
            response = client.post("/decode/video", files=files)
            assert response.status_code == 200
            
            data = response.json()
            assert data["command"] == "video command"
            assert data["success"] is True
            assert data["analysis"]["audio_track_present"] is True
    
    @patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.analyze_audio')
    def test_analyze_audio_endpoint(self, mock_analyze, client, sample_audio_file):
        """Test audio analysis endpoint."""
        mock_analyze.return_value = {
            "ultrasonic_detected": True,
            "peak_frequencies": [18500, 19500],
            "confidence": 0.92,
            "signal_strength": -20.5
        }
        
        files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            
            response = client.post("/analyze/audio", files=files)
            assert response.status_code == 200
            
            data = response.json()
            assert data["ultrasonic_detected"] is True
            assert len(data["peak_frequencies"]) == 2
            assert data["confidence"] == 0.92
    
    @patch('agentic_commands_stego.decode.video_decoder.VideoDecoder.analyze_video')
    def test_analyze_video_endpoint(self, mock_analyze, client, sample_video_file):
        """Test video analysis endpoint."""
        mock_analyze.return_value = {
            "audio_track_present": True,
            "video_duration": 120.5,
            "ultrasonic_detected": False,
            "video_codec": "h264",
            "audio_codec": "aac"
        }
        
        files = {"file": ("test.mp4", sample_video_file, "video/mp4")}
        
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.mp4"
            
            response = client.post("/analyze/video", files=files)
            assert response.status_code == 200
            
            data = response.json()
            assert data["audio_track_present"] is True
            assert data["video_duration"] == 120.5
            assert data["ultrasonic_detected"] is False
    
    def test_configure_frequencies_endpoint(self, client):
        """Test frequency configuration endpoint."""
        data = {
            "freq_0": "18000",
            "freq_1": "19000"
        }
        
        with patch('agentic_commands_stego.embed.audio_embedder.AudioEmbedder.set_frequencies'):
            with patch('agentic_commands_stego.embed.video_embedder.VideoEmbedder.set_frequencies'):
                with patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.set_frequencies'):
                    with patch('agentic_commands_stego.decode.video_decoder.VideoDecoder.set_frequencies'):
                        response = client.post("/config/frequencies", data=data)
                        assert response.status_code == 200
                        
                        result = response.json()
                        assert result["success"] is True
                        assert result["freq_0"] == 18000
                        assert result["freq_1"] == 19000
    
    def test_configure_frequencies_invalid(self, client):
        """Test frequency configuration with invalid values."""
        data = {
            "freq_0": "-1000",  # Negative frequency
            "freq_1": "19000"
        }
        
        with patch('agentic_commands_stego.embed.audio_embedder.AudioEmbedder.set_frequencies',
                  side_effect=ValueError("Invalid frequency")):
            response = client.post("/config/frequencies", data=data)
            assert response.status_code == 400
            assert "Invalid frequencies" in response.json()["detail"]
    
    def test_configure_key_endpoint(self, client):
        """Test encryption key configuration endpoint."""
        key = CipherService.generate_key(32)
        key_base64 = base64.b64encode(key).decode()
        
        data = {"key_base64": key_base64}
        
        with patch('agentic_commands_stego.crypto.cipher.CipherService.set_key_from_base64'):
            with patch('agentic_commands_stego.crypto.cipher.CipherService.get_key', return_value=key):
                response = client.post("/config/key", data=data)
                assert response.status_code == 200
                
                result = response.json()
                assert result["success"] is True
                assert "Encryption key updated" in result["message"]
    
    def test_configure_key_invalid_base64(self, client):
        """Test key configuration with invalid base64."""
        data = {"key_base64": "not-valid-base64!!!"}
        
        with patch('agentic_commands_stego.crypto.cipher.CipherService.set_key_from_base64',
                  side_effect=ValueError("Invalid base64")):
            response = client.post("/config/key", data=data)
            assert response.status_code == 400
            assert "Invalid key" in response.json()["detail"]
    
    def test_concurrent_requests(self, client, sample_audio_file):
        """Test handling of concurrent requests."""
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        async def make_request():
            files = {"file": ("test.wav", BytesIO(sample_audio_file.getvalue()), "audio/wav")}
            return client.post("/analyze/audio", files=files)
        
        with patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.analyze_audio',
                  return_value={"ultrasonic_detected": False}):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
                
                # Make 10 concurrent requests
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = []
                    for _ in range(10):
                        files = {"file": ("test.wav", BytesIO(sample_audio_file.getvalue()), "audio/wav")}
                        future = executor.submit(client.post, "/analyze/audio", files=files)
                        futures.append(future)
                    
                    # All requests should succeed
                    for future in futures:
                        response = future.result()
                        assert response.status_code == 200
    
    def test_large_file_handling(self, client):
        """Test handling of large files."""
        # Create a large mock file (10MB)
        large_file = BytesIO(b'RIFF' + b'\x00' * (10 * 1024 * 1024))
        files = {"file": ("large.wav", large_file, "audio/wav")}
        data = {"command": "test"}
        
        with patch('agentic_commands_stego.embed.audio_embedder.AudioEmbedder.embed_file',
                  side_effect=MemoryError("File too large")):
            with patch('tempfile.NamedTemporaryFile') as mock_temp:
                mock_temp.return_value.__enter__.return_value.name = "/tmp/large.wav"
                
                response = client.post("/embed/audio", files=files, data=data)
                assert response.status_code == 500
                assert "Embedding failed" in response.json()["detail"]
    
    def test_error_handling_file_cleanup(self, client, sample_audio_file):
        """Test that temporary files are cleaned up even on error."""
        files = {"file": ("test.wav", sample_audio_file, "audio/wav")}
        
        temp_file_path = None
        
        class MockTempFile:
            def __init__(self, *args, **kwargs):
                self.name = "/tmp/test_cleanup.wav"
                global temp_file_path
                temp_file_path = self.name
            
            def __enter__(self):
                return self
            
            def __exit__(self, *args):
                pass
            
            def write(self, data):
                pass
        
        with patch('tempfile.NamedTemporaryFile', MockTempFile):
            with patch('agentic_commands_stego.decode.audio_decoder.AudioDecoder.analyze_audio',
                      side_effect=Exception("Analysis error")):
                with patch('os.unlink') as mock_unlink:
                    response = client.post("/analyze/audio", files=files)
                    assert response.status_code == 500
                    
                    # Verify cleanup was attempted
                    mock_unlink.assert_called_with(temp_file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])