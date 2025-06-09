"""
Cryptographic cipher service for encrypting and decrypting agentic commands.
Uses AES-256-GCM for authenticated encryption.
"""

import os
import base64
from typing import Tuple, Optional
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class CipherService:
    """Service for encrypting and decrypting command payloads."""
    
    def __init__(self, key: bytes = None):
        """
        Initialize cipher service with optional key.
        
        Args:
            key: 32-byte AES-256 key. If None, a random key is generated.
        """
        if key is None:
            self.key = get_random_bytes(32)  # AES-256
        else:
            if len(key) not in [16, 24, 32]:
                raise ValueError("Key must be 16, 24, or 32 bytes for AES")
            self.key = key
    
    def encrypt_command(self, command: str) -> bytes:
        """
        Encrypt a command string.
        
        Args:
            command: The command string to encrypt
            
        Returns:
            Encrypted payload with IV, ciphertext, and auth tag
        """
        if not isinstance(command, str):
            raise ValueError("Command must be a string")
        
        # Convert command to bytes
        plaintext = command.encode('utf-8')
        
        # Generate random IV
        iv = get_random_bytes(16)
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        
        # Encrypt and get auth tag
        ciphertext, auth_tag = cipher.encrypt_and_digest(plaintext)
        
        # Combine IV + ciphertext + auth_tag
        encrypted_payload = iv + ciphertext + auth_tag
        
        return encrypted_payload
    
    def decrypt_command(self, encrypted_payload: bytes) -> Optional[str]:
        """
        Decrypt an encrypted payload.
        
        Args:
            encrypted_payload: Encrypted data with IV, ciphertext, and auth tag
            
        Returns:
            Decrypted command string, or None if decryption fails
        """
        try:
            if len(encrypted_payload) < 32:  # 16 (IV) + 16 (min auth tag)
                return None
            
            # Extract components
            iv = encrypted_payload[:16]
            auth_tag = encrypted_payload[-16:]
            ciphertext = encrypted_payload[16:-16]
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
            
            # Decrypt and verify
            plaintext = cipher.decrypt_and_verify(ciphertext, auth_tag)
            
            # Convert back to string
            return plaintext.decode('utf-8')
            
        except (ValueError, UnicodeDecodeError):
            return None
    
    def get_key(self) -> bytes:
        """Get the encryption key."""
        return self.key
    
    def set_key(self, key: bytes) -> None:
        """
        Set a new encryption key.
        
        Args:
            key: New encryption key (16, 24, or 32 bytes)
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes for AES")
        self.key = key
    
    def get_key_base64(self) -> str:
        """Get the encryption key as base64 string."""
        return base64.b64encode(self.key).decode('ascii')
    
    def set_key_from_base64(self, key_b64: str) -> None:
        """
        Set encryption key from base64 string.
        
        Args:
            key_b64: Base64 encoded key string
        """
        try:
            key = base64.b64decode(key_b64)
            self.set_key(key)
        except Exception as e:
            raise ValueError(f"Invalid base64 key: {e}")
    
    @staticmethod
    def generate_key(key_size: int = 32) -> bytes:
        """
        Generate a random encryption key.
        
        Args:
            key_size: Key size in bytes (16, 24, or 32)
            
        Returns:
            Random encryption key
        """
        if key_size not in [16, 24, 32]:
            raise ValueError("Key size must be 16, 24, or 32 bytes")
        return get_random_bytes(key_size)
    
    def add_obfuscation(self, payload: bytes, padding_size: int = None) -> bytes:
        """
        Add obfuscation to encrypted payload.
        
        Args:
            payload: Encrypted payload
            padding_size: Random padding size. If None, random between 1-32 bytes
            
        Returns:
            Obfuscated payload with random padding
        """
        if padding_size is None:
            padding_size = int.from_bytes(os.urandom(1), 'big') % 32 + 1
        
        # Add random padding
        padding = get_random_bytes(padding_size)
        
        # Prepend padding size (1 byte) and padding
        obfuscated = bytes([padding_size]) + padding + payload
        
        return obfuscated
    
    def remove_obfuscation(self, obfuscated_payload: bytes) -> Optional[bytes]:
        """
        Remove obfuscation from payload.
        
        Args:
            obfuscated_payload: Obfuscated payload with padding
            
        Returns:
            Original encrypted payload, or None if invalid
        """
        try:
            if len(obfuscated_payload) < 1:
                return None
            
            padding_size = obfuscated_payload[0]
            
            if len(obfuscated_payload) < 1 + padding_size:
                return None
            
            # Extract original payload (skip padding size byte and padding)
            original_payload = obfuscated_payload[1 + padding_size:]
            
            return original_payload
            
        except (IndexError, ValueError):
            return None