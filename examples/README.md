# Example Media Files

This directory contains sample media files for testing the Ultrasonic Agentics steganography framework.

## Files

### sample_audio.mp3
- **Description**: Crowd cheering sound effect
- **Format**: MP3 (MPEG Audio Layer III)
- **Duration**: 27.74 seconds
- **Bit Rate**: 128 kbps
- **Sample Rate**: 44.1 kHz
- **Channels**: Joint Stereo
- **Size**: 434 KB
- **Source**: Sample-Videos.com
- **License**: Free for testing and development

### sample_video.mp4
- **Description**: Big Buck Bunny animated short film (clip)
- **Format**: MP4 (H.264 video + AAC audio)
- **Duration**: 5.31 seconds
- **Resolution**: 1280x720 (720p HD)
- **Video Codec**: H.264
- **Audio Codec**: AAC
- **Size**: 1.1 MB
- **Source**: Sample-Videos.com
- **License**: Creative Commons / Free for testing

## Usage

These files can be used with the Ultrasonic Agentics tools to test embedding and extracting encrypted commands:

```bash
# Embed a command in the audio file
python -m src.examples.basic_encoding

# Use the API to process files
python -m src.examples.audio_file_processing

# Test with the MCP CLI
ultrasonic-agentics embed -i sample_audio.mp3 -o output_with_command.mp3 -m "test command"
```

## Notes

- These files are suitable for testing but may not be optimal for production use
- The audio file has sufficient duration (27+ seconds) for embedding longer commands
- The video file includes both video and audio tracks, allowing for audio-based steganography
- Both files use common codecs that are widely supported

## Additional Test Files

You can download additional royalty-free test files from:
- [Pexels](https://www.pexels.com) - Free stock videos and music
- [Sample-Videos.com](https://www.sample-videos.com) - Various test media files
- [Pixabay](https://pixabay.com) - Royalty-free audio and video
- [Freesound](https://freesound.org) - Creative Commons audio samples