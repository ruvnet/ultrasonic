"""MCP tools for system configuration."""

import os
import base64
from typing import Dict, Any
from ..schemas.config import ConfigFrequenciesRequest, ConfigKeyRequest, ConfigResponse
from agentic_commands_stego.crypto.cipher import CipherService
from .embed_tools import set_cipher_key as set_embed_cipher_key
from .decode_tools import set_cipher_key as set_decode_cipher_key


# Global configuration state
_current_config: Dict[str, Any] = {
    "frequencies": {
        "freq_0": 18500,
        "freq_1": 19500
    },
    "encryption": {
        "key_set": False,
        "algorithm": "AES-256-GCM"
    },
    "signal": {
        "amplitude": 0.1,
        "bit_duration": 0.01,
        "sample_rate": 48000
    }
}


def configure_frequencies(request: ConfigFrequenciesRequest) -> ConfigResponse:
    """
    Configure the ultrasonic frequencies used for FSK modulation.
    
    This tool sets the two frequencies used for binary FSK (Frequency Shift Keying)
    modulation. freq_0 represents binary '0' and freq_1 represents binary '1'.
    The frequencies should be in the ultrasonic range (>17kHz) for human inaudibility.
    
    Args:
        request: Frequency configuration with freq_0 and freq_1 values
        
    Returns:
        ConfigResponse with success status and applied configuration
        
    Raises:
        ValueError: If frequencies are invalid or too close together
    """
    global _current_config
    
    try:
        # Validate frequency values
        if request.freq_0 <= 0 or request.freq_1 <= 0:
            raise ValueError("Frequencies must be positive values")
        
        if abs(request.freq_0 - request.freq_1) < 500:
            raise ValueError("Frequencies must be at least 500 Hz apart for reliable FSK")
        
        if request.freq_0 < 17000 or request.freq_1 < 17000:
            raise ValueError("Frequencies should be above 17kHz for ultrasonic operation")
        
        if request.freq_0 > 22000 or request.freq_1 > 22000:
            raise ValueError("Frequencies should be below 22kHz for compatibility")
        
        # Store previous config
        previous_config = _current_config["frequencies"].copy()
        
        # Update configuration
        _current_config["frequencies"]["freq_0"] = request.freq_0
        _current_config["frequencies"]["freq_1"] = request.freq_1
        
        # TODO: Update embedders and decoders with new frequencies
        # This would require accessing the global embedders/decoders
        
        applied_config = {
            "freq_0": request.freq_0,
            "freq_1": request.freq_1,
            "separation": abs(request.freq_1 - request.freq_0)
        }
        
        return ConfigResponse(
            success=True,
            message=f"Frequencies updated successfully: {request.freq_0} Hz and {request.freq_1} Hz",
            applied_config=applied_config,
            previous_config=previous_config
        )
        
    except Exception as e:
        return ConfigResponse(
            success=False,
            message=f"Frequency configuration failed: {str(e)}",
            applied_config={},
            previous_config=_current_config["frequencies"].copy()
        )


def configure_encryption_key(request: ConfigKeyRequest) -> ConfigResponse:
    """
    Configure the encryption key used for command encryption.
    
    This tool sets the AES-256 encryption key used to encrypt commands before
    embedding them in media files. The key can be provided as base64, loaded
    from a file, or generated randomly.
    
    Args:
        request: Key configuration with various input options
        
    Returns:
        ConfigResponse with success status and key information (key not exposed)
        
    Raises:
        ValueError: If key format is invalid
        FileNotFoundError: If key file doesn't exist
    """
    global _current_config
    
    try:
        previous_config = _current_config["encryption"].copy()
        new_key = None
        key_source = ""
        
        if request.generate_new:
            # Generate new random key
            new_key = CipherService.generate_key(32)
            key_source = "generated_random"
            
        elif request.key_base64:
            # Use provided base64 key
            try:
                new_key = base64.b64decode(request.key_base64)
                if len(new_key) != 32:
                    raise ValueError("Key must be exactly 32 bytes (256 bits)")
                key_source = "base64_input"
            except Exception as e:
                raise ValueError(f"Invalid base64 key: {str(e)}")
                
        elif request.key_file_path:
            # Load key from file
            if not os.path.exists(request.key_file_path):
                raise FileNotFoundError(f"Key file not found: {request.key_file_path}")
            
            with open(request.key_file_path, 'rb') as f:
                new_key = f.read()
            
            if len(new_key) != 32:
                # Try base64 decoding if raw bytes aren't 32
                try:
                    new_key = base64.b64decode(new_key)
                    if len(new_key) != 32:
                        raise ValueError("Key file must contain exactly 32 bytes")
                except:
                    raise ValueError("Key file must contain exactly 32 bytes or base64-encoded 32 bytes")
            
            key_source = f"file: {request.key_file_path}"
            
        else:
            raise ValueError("Must specify key_base64, key_file_path, or generate_new=True")
        
        # Update global cipher key for embedders and decoders
        set_embed_cipher_key(new_key)
        set_decode_cipher_key(new_key)
        
        # Update configuration
        _current_config["encryption"]["key_set"] = True
        
        applied_config = {
            "key_source": key_source,
            "key_length_bytes": len(new_key),
            "algorithm": "AES-256-GCM"
        }
        
        return ConfigResponse(
            success=True,
            message=f"Encryption key configured successfully from {key_source}",
            applied_config=applied_config,
            previous_config=previous_config
        )
        
    except Exception as e:
        return ConfigResponse(
            success=False,
            message=f"Key configuration failed: {str(e)}",
            applied_config={},
            previous_config=_current_config["encryption"].copy()
        )


def get_current_config() -> Dict[str, Any]:
    """
    Get the current system configuration.
    
    Returns the current configuration settings including frequencies, encryption
    status, and signal parameters. Sensitive information like encryption keys
    are not included in the response.
    
    Returns:
        Dict with current configuration (excluding sensitive data)
    """
    global _current_config
    
    # Return a copy without sensitive information
    config_copy = _current_config.copy()
    
    # Add some computed values
    freq_sep = abs(config_copy["frequencies"]["freq_1"] - config_copy["frequencies"]["freq_0"])
    config_copy["frequencies"]["separation_hz"] = freq_sep
    
    # Add status indicators
    config_copy["status"] = {
        "encryption_configured": config_copy["encryption"]["key_set"],
        "frequencies_configured": True,
        "ready_for_operations": config_copy["encryption"]["key_set"]
    }
    
    return config_copy