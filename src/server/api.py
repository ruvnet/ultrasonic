"""
FastAPI server for steganography service.
Provides REST endpoints for embedding and decoding commands.
"""

import asyncio
import os
import tempfile
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ..embed.audio_embedder import AudioEmbedder
from ..embed.video_embedder import VideoEmbedder
from ..decode.audio_decoder import AudioDecoder
from ..decode.video_decoder import VideoDecoder
from ..crypto.cipher import CipherService


# Initialize FastAPI app
app = FastAPI(
    title="Agentic Commands Steganography API",
    description="API for embedding and decoding encrypted commands in audio/video files",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global encryption key (in production, manage this securely)
SECRET_KEY = CipherService.generate_key(32)  # AES-256

# Initialize services
audio_embedder = AudioEmbedder(key=SECRET_KEY)
video_embedder = VideoEmbedder(key=SECRET_KEY)
audio_decoder = AudioDecoder(key=SECRET_KEY)
video_decoder = VideoDecoder(key=SECRET_KEY)


@app.post("/embed/audio")
async def embed_audio_command(
    file: UploadFile = File(...),
    command: str = Form(...),
    obfuscate: bool = Form(True),
    bitrate: str = Form("192k"),
    ultrasonic_freq: float = Form(18500),
    amplitude: float = Form(0.1)
):
    """Embed command into audio file."""
    if not file.filename.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as input_temp:
        input_path = input_temp.name
        content = await file.read()
        input_temp.write(content)
    
    output_path = input_path.replace(os.path.splitext(input_path)[1], "_embedded.mp3")
    
    try:
        # Configure embedder
        audio_embedder.set_frequencies(ultrasonic_freq, ultrasonic_freq + 1000)
        audio_embedder.set_amplitude(amplitude)
        
        # Perform embedding in thread to avoid blocking
        await asyncio.to_thread(
            audio_embedder.embed_file,
            input_path,
            output_path,
            command,
            obfuscate,
            bitrate
        )
        
        # Return the file
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename=f"embedded_{file.filename}",
            background=None  # Will be cleaned up manually
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
    
    finally:
        # Clean up input file
        try:
            os.unlink(input_path)
        except OSError:
            pass


@app.post("/embed/video")
async def embed_video_command(
    file: UploadFile = File(...),
    command: str = Form(...),
    obfuscate: bool = Form(True),
    audio_bitrate: str = Form("192k"),
    ultrasonic_freq: float = Form(18500),
    amplitude: float = Form(0.1)
):
    """Embed command into video file."""
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as input_temp:
        input_path = input_temp.name
        content = await file.read()
        input_temp.write(content)
    
    output_path = input_path.replace(os.path.splitext(input_path)[1], "_embedded.mp4")
    
    try:
        # Configure embedder
        video_embedder.set_frequencies(ultrasonic_freq, ultrasonic_freq + 1000)
        video_embedder.set_amplitude(amplitude)
        
        # Perform embedding in thread to avoid blocking
        await asyncio.to_thread(
            video_embedder.embed_file,
            input_path,
            output_path,
            command,
            obfuscate,
            audio_bitrate
        )
        
        # Return the file
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=f"embedded_{file.filename}",
            background=None  # Will be cleaned up manually
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
    
    finally:
        # Clean up input file
        try:
            os.unlink(input_path)
        except OSError:
            pass


@app.post("/decode/audio")
async def decode_audio_command(file: UploadFile = File(...)):
    """Decode command from audio file."""
    if not file.filename.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)
    
    try:
        # Perform decoding in thread to avoid blocking
        result = await asyncio.to_thread(audio_decoder.decode_file, temp_path)
        
        # Also get analysis
        analysis = await asyncio.to_thread(audio_decoder.analyze_audio, temp_path)
        
        return JSONResponse({
            "command": result,
            "analysis": analysis,
            "success": result is not None
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decoding failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.post("/decode/video")
async def decode_video_command(file: UploadFile = File(...)):
    """Decode command from video file."""
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)
    
    try:
        # Perform decoding in thread to avoid blocking
        result = await asyncio.to_thread(video_decoder.decode_file, temp_path)
        
        # Also get analysis
        analysis = await asyncio.to_thread(video_decoder.analyze_video, temp_path)
        
        return JSONResponse({
            "command": result,
            "analysis": analysis,
            "success": result is not None
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decoding failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.post("/analyze/audio")
async def analyze_audio_file(file: UploadFile = File(...)):
    """Analyze audio file for steganographic content."""
    if not file.filename.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)
    
    try:
        # Perform analysis in thread to avoid blocking
        analysis = await asyncio.to_thread(audio_decoder.analyze_audio, temp_path)
        
        return JSONResponse(analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.post("/analyze/video")
async def analyze_video_file(file: UploadFile = File(...)):
    """Analyze video file for steganographic content."""
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)
    
    try:
        # Perform analysis in thread to avoid blocking
        analysis = await asyncio.to_thread(video_decoder.analyze_video, temp_path)
        
        return JSONResponse(analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.get("/info")
async def get_api_info():
    """Get API information."""
    return {
        "name": "Agentic Commands Steganography API",
        "version": "1.0.0",
        "description": "API for embedding and decoding encrypted commands in audio/video files",
        "supported_formats": {
            "audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
            "video": [".mp4", ".avi", ".mov", ".mkv"]
        },
        "endpoints": {
            "embed": ["/embed/audio", "/embed/video"],
            "decode": ["/decode/audio", "/decode/video"],
            "analyze": ["/analyze/audio", "/analyze/video"]
        },
        "encryption": "AES-256-GCM",
        "steganography": "Ultrasonic FSK"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Steganography service is running"}


@app.post("/config/frequencies")
async def configure_frequencies(
    freq_0: float = Form(...),
    freq_1: float = Form(...)
):
    """Configure ultrasonic frequencies."""
    try:
        audio_embedder.set_frequencies(freq_0, freq_1)
        video_embedder.set_frequencies(freq_0, freq_1)
        audio_decoder.set_frequencies(freq_0, freq_1)
        video_decoder.set_frequencies(freq_0, freq_1)
        
        return {
            "success": True,
            "message": f"Frequencies updated to {freq_0} Hz and {freq_1} Hz",
            "freq_0": freq_0,
            "freq_1": freq_1
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid frequencies: {str(e)}")


@app.post("/config/key")
async def configure_key(key_base64: str = Form(...)):
    """Configure encryption key from base64 string."""
    try:
        cipher = CipherService()
        cipher.set_key_from_base64(key_base64)
        new_key = cipher.get_key()
        
        # Update all services
        audio_embedder.set_cipher_key(new_key)
        video_embedder.set_cipher_key(new_key)
        audio_decoder.set_cipher_key(new_key)
        video_decoder.set_cipher_key(new_key)
        
        return {
            "success": True,
            "message": "Encryption key updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid key: {str(e)}")


def main():
    """Main entry point for the API server."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()