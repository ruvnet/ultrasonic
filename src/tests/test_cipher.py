"""
Tests for cipher service.
Tests encryption/decryption functionality and error handling.
"""

import pytest
import base64
from ..crypto.cipher import CipherService


class TestCipherService:
    """Test suite for CipherService."""
    
    def test_cipher_service_initializes_with_random_key_when_none_provided(self):
        """Test that CipherService generates random key when none provided."""
        cipher = CipherService()
        assert cipher.get_key() is not None
        assert len(cipher.get_key()) == 32  # AES-256 default
    
    def test_cipher_service_accepts_valid_key_sizes(self):
        """Test that CipherService accepts 16, 24, and 32 byte keys."""
        for key_size in [16, 24, 32]:
            key = b'x' * key_size
            cipher = CipherService(key)
            assert cipher.get_key() == key
    
    def test_cipher_service_rejects_invalid_key_sizes(self):
        """Test that CipherService rejects invalid key sizes."""
        invalid_sizes = [8, 15, 17, 33, 64]
        for size in invalid_sizes:
            key = b'x' * size
            with pytest.raises(ValueError, match="Key must be 16, 24, or 32 bytes"):
                CipherService(key)
    
    def test_encrypt_command_returns_bytes(self):
        """Test that encrypt_command returns bytes."""
        cipher = CipherService()
        command = "test command"
        encrypted = cipher.encrypt_command(command)
        assert isinstance(encrypted, bytes)
        assert len(encrypted) > len(command)  # Should be longer due to IV + auth tag
    
    def test_encrypt_command_rejects_non_string_input(self):
        """Test that encrypt_command rejects non-string input."""
        cipher = CipherService()
        with pytest.raises(ValueError, match="Command must be a string"):
            cipher.encrypt_command(b"bytes")
        with pytest.raises(ValueError, match="Command must be a string"):
            cipher.encrypt_command(123)
    
    def test_decrypt_command_recovers_original_string(self):
        """Test that decrypt_command recovers the original command."""
        cipher = CipherService()
        original_command = "ALERT:ExecuteOrder66"
        
        encrypted = cipher.encrypt_command(original_command)
        decrypted = cipher.decrypt_command(encrypted)
        
        assert decrypted == original_command
    
    def test_decrypt_command_returns_none_for_invalid_data(self):
        """Test that decrypt_command returns None for invalid data."""
        cipher = CipherService()
        
        # Test with too short data
        assert cipher.decrypt_command(b"short") is None
        
        # Test with random data
        assert cipher.decrypt_command(b"x" * 50) is None
        
        # Test with corrupted data
        encrypted = cipher.encrypt_command("test")
        corrupted = encrypted[:-1] + b'x'  # Corrupt last byte
        assert cipher.decrypt_command(corrupted) is None
    
    def test_decrypt_command_fails_with_wrong_key(self):
        """Test that decryption fails with wrong key."""
        cipher1 = CipherService(b'key1' * 8)  # 32 bytes
        cipher2 = CipherService(b'key2' * 8)  # 32 bytes
        
        encrypted = cipher1.encrypt_command("secret message")
        decrypted = cipher2.decrypt_command(encrypted)
        
        assert decrypted is None
    
    def test_set_key_updates_encryption_key(self):
        """Test that set_key updates the encryption key."""
        cipher = CipherService()
        new_key = b'newkey1234567890newkey1234567890'  # 32 bytes
        
        cipher.set_key(new_key)
        assert cipher.get_key() == new_key
        
        # Test encryption/decryption works with new key
        command = "test with new key"
        encrypted = cipher.encrypt_command(command)
        decrypted = cipher.decrypt_command(encrypted)
        assert decrypted == command
    
    def test_set_key_rejects_invalid_sizes(self):
        """Test that set_key rejects invalid key sizes."""
        cipher = CipherService()
        with pytest.raises(ValueError, match="Key must be 16, 24, or 32 bytes"):
            cipher.set_key(b"tooshort")
    
    def test_get_key_base64_returns_valid_base64(self):
        """Test that get_key_base64 returns valid base64 string."""
        cipher = CipherService()
        key_b64 = cipher.get_key_base64()
        
        # Should be valid base64
        decoded = base64.b64decode(key_b64)
        assert decoded == cipher.get_key()
    
    def test_set_key_from_base64_works_correctly(self):
        """Test that set_key_from_base64 works correctly."""
        cipher = CipherService()
        original_key = cipher.get_key()
        key_b64 = cipher.get_key_base64()
        
        # Create new cipher and set key from base64
        new_cipher = CipherService()
        new_cipher.set_key_from_base64(key_b64)
        
        assert new_cipher.get_key() == original_key
    
    def test_set_key_from_base64_rejects_invalid_base64(self):
        """Test that set_key_from_base64 rejects invalid base64."""
        cipher = CipherService()
        with pytest.raises(ValueError, match="Invalid base64 key"):
            cipher.set_key_from_base64("invalid base64!")
    
    def test_generate_key_creates_keys_of_correct_size(self):
        """Test that generate_key creates keys of correct sizes."""
        for size in [16, 24, 32]:
            key = CipherService.generate_key(size)
            assert len(key) == size
            assert isinstance(key, bytes)
    
    def test_generate_key_rejects_invalid_sizes(self):
        """Test that generate_key rejects invalid sizes."""
        with pytest.raises(ValueError, match="Key size must be 16, 24, or 32 bytes"):
            CipherService.generate_key(8)
    
    def test_add_obfuscation_adds_padding(self):
        """Test that add_obfuscation adds random padding."""
        cipher = CipherService()
        payload = b"test payload"
        
        obfuscated = cipher.add_obfuscation(payload)
        
        assert len(obfuscated) > len(payload)
        assert obfuscated[0] <= 32  # Padding size should be <= 32
        assert len(obfuscated) >= len(payload) + 1  # At least padding size byte
    
    def test_add_obfuscation_with_specific_padding_size(self):
        """Test add_obfuscation with specific padding size."""
        cipher = CipherService()
        payload = b"test payload"
        padding_size = 10
        
        obfuscated = cipher.add_obfuscation(payload, padding_size)
        
        assert obfuscated[0] == padding_size
        assert len(obfuscated) == 1 + padding_size + len(payload)
    
    def test_remove_obfuscation_recovers_original_payload(self):
        """Test that remove_obfuscation recovers original payload."""
        cipher = CipherService()
        original_payload = b"test payload for obfuscation"
        
        obfuscated = cipher.add_obfuscation(original_payload)
        recovered = cipher.remove_obfuscation(obfuscated)
        
        assert recovered == original_payload
    
    def test_remove_obfuscation_returns_none_for_invalid_data(self):
        """Test that remove_obfuscation returns None for invalid data."""
        cipher = CipherService()
        
        # Empty data
        assert cipher.remove_obfuscation(b"") is None
        
        # Too short data
        assert cipher.remove_obfuscation(b"x") is None
        
        # Invalid padding size
        invalid_data = bytes([50]) + b"x" * 10  # Claims 50 bytes padding but only has 10
        assert cipher.remove_obfuscation(invalid_data) is None
    
    def test_encryption_produces_different_outputs_each_time(self):
        """Test that encryption produces different outputs each time (due to random IV)."""
        cipher = CipherService()
        command = "same command"
        
        encrypted1 = cipher.encrypt_command(command)
        encrypted2 = cipher.encrypt_command(command)
        
        assert encrypted1 != encrypted2  # Should be different due to random IV
        
        # But both should decrypt to same command
        assert cipher.decrypt_command(encrypted1) == command
        assert cipher.decrypt_command(encrypted2) == command
    
    def test_empty_command_encryption_and_decryption(self):
        """Test encryption and decryption of empty command."""
        cipher = CipherService()
        command = ""
        
        encrypted = cipher.encrypt_command(command)
        decrypted = cipher.decrypt_command(encrypted)
        
        assert decrypted == command
    
    def test_unicode_command_encryption_and_decryption(self):
        """Test encryption and decryption of unicode commands."""
        cipher = CipherService()
        command = "🚀 Execute mission: αβγ δεζ"
        
        encrypted = cipher.encrypt_command(command)
        decrypted = cipher.decrypt_command(encrypted)
        
        assert decrypted == command
    
    def test_long_command_encryption_and_decryption(self):
        """Test encryption and decryption of long commands."""
        cipher = CipherService()
        command = "Very long command: " + "x" * 1000
        
        encrypted = cipher.encrypt_command(command)
        decrypted = cipher.decrypt_command(encrypted)
        
        assert decrypted == command