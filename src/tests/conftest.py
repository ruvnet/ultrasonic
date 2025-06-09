"""
Pytest configuration and fixtures for steganography tests.
"""

import pytest
import numpy as np
from pydub import AudioSegment
from ..crypto.cipher import CipherService


@pytest.fixture
def test_key():
    """Provide a consistent test encryption key."""
    return b'test_key_32_bytes_long_for_test!'


@pytest.fixture
def cipher_service(test_key):
    """Provide a configured cipher service."""
    return CipherService(test_key)


@pytest.fixture
def test_audio():
    """Provide a standard test audio segment."""
    return AudioSegment.silent(duration=1000, frame_rate=48000)


@pytest.fixture
def test_audio_long():
    """Provide a longer test audio segment for complex tests."""
    return AudioSegment.silent(duration=5000, frame_rate=48000)


@pytest.fixture
def test_command():
    """Provide a standard test command."""
    return "TEST_COMMAND_123"


@pytest.fixture
def test_payload():
    """Provide a standard test payload."""
    return b"test_payload_bytes"


@pytest.fixture
def random_signal():
    """Provide a random audio signal for testing."""
    return np.random.random(48000) * 0.1  # 1 second of random noise


@pytest.fixture
def pure_tone():
    """Provide a pure tone for testing."""
    sample_rate = 48000
    duration = 1.0
    frequency = 1000  # 1kHz
    t = np.linspace(0, duration, int(sample_rate * duration))
    return 0.5 * np.sin(2 * np.pi * frequency * t)


@pytest.fixture
def ultrasonic_tone():
    """Provide an ultrasonic tone for testing."""
    sample_rate = 48000
    duration = 1.0
    frequency = 18500  # 18.5kHz
    t = np.linspace(0, duration, int(sample_rate * duration))
    return 0.1 * np.sin(2 * np.pi * frequency * t)


class MockAudioSegment:
    """Mock AudioSegment for testing without actual audio processing."""
    
    def __init__(self, duration=1000, frame_rate=48000, channels=1):
        self.duration = duration
        self.frame_rate = frame_rate
        self.channels = channels
        self._data = np.zeros(int(frame_rate * duration / 1000))
    
    def __len__(self):
        return self.duration
    
    def set_frame_rate(self, frame_rate):
        new_mock = MockAudioSegment(self.duration, frame_rate, self.channels)
        return new_mock
    
    def set_channels(self, channels):
        new_mock = MockAudioSegment(self.duration, self.frame_rate, channels)
        return new_mock
    
    def overlay(self, other, position=0):
        # Simple mock overlay
        new_duration = max(self.duration, len(other) + position)
        return MockAudioSegment(new_duration, self.frame_rate, self.channels)
    
    def get_array_of_samples(self):
        return self._data.astype(np.int16)
    
    def export(self, *args, **kwargs):
        pass  # Mock export
    
    @staticmethod
    def silent(duration, frame_rate):
        return MockAudioSegment(duration, frame_rate)
    
    @staticmethod
    def from_mono_audiosegments(left, right):
        return MockAudioSegment(max(len(left), len(right)), left.frame_rate, 2)


@pytest.fixture
def mock_audio_segment():
    """Provide a mock AudioSegment for testing."""
    return MockAudioSegment()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "video: marks tests that require video processing"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark video tests
        if "video" in item.nodeid:
            item.add_marker(pytest.mark.video)
        
        # Mark slow tests
        if any(keyword in item.nodeid for keyword in ["performance", "long", "slow"]):
            item.add_marker(pytest.mark.slow)