# Test Failure Analysis

## Overview
This document tracks all test failures discovered during calibration and debugging.

## Test Failure Categories

### 1. Signal Detection Failures
- **Pattern**: Ultrasonic signals not detected in decoded audio
- **Affected Tests**: TBD after analysis
- **Likely Cause**: Threshold too high or frequency drift

### 2. Demodulation Errors
- **Pattern**: Signal detected but data corrupted
- **Affected Tests**: TBD after analysis
- **Likely Cause**: FSK demodulation parameters mismatched

### 3. Format Conversion Issues
- **Pattern**: Failures specific to certain audio formats
- **Affected Tests**: TBD after analysis
- **Likely Cause**: FFmpeg not available

## Detailed Failure Log

### Integration Test Failures (11/14 tests failing)

1. **test_audio_embed_and_decode_roundtrip**
   - Pattern: `decoded_command = None` instead of expected command
   - Issue: Decoder cannot find embedded signal in audio
   - Key parameters: amplitude=0.3, detection_threshold=0.05

2. **test_audio_file_embed_and_decode_roundtrip**
   - Pattern: FFmpeg not found, file export fails
   - Issue: Missing FFmpeg dependency
   - Error: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

3. **test_signal_strength_measurement**
   - Pattern: Signal strength below threshold
   - Issue: Amplitude or detection parameters mismatched

4. **test_obfuscation_roundtrip**
   - Pattern: Decoding returns None
   - Issue: Obfuscation may be interfering with signal detection

5. **test_different_frequencies_work**
   - Pattern: Alternative frequencies not detected
   - Issue: Frequency detection algorithm needs calibration

6. **test_unicode_commands**
   - Pattern: Unicode encoding/decoding fails
   - Issue: Signal corruption or detection failure

7. **test_empty_and_long_commands**
   - Pattern: Edge cases not handled
   - Issue: Empty or very long payloads fail

8. **test_audio_format_compatibility**
   - Pattern: FFmpeg required for non-WAV formats
   - Issue: Missing FFmpeg dependency

9. **test_analyzer_provides_accurate_information**
   - Pattern: Analyzer cannot detect embedded signals
   - Issue: Detection threshold too high

10. **test_video_embed_and_decode_roundtrip**
    - Pattern: MoviePy import error
    - Issue: Optional dependency not available

11. **test_performance_characteristics**
    - Pattern: Decoding returns None
    - Issue: Same as basic roundtrip test

## Common Failure Modes

1. **Silent Failures**: Function returns None instead of decoded data
2. **Threshold Misses**: Signal present but below detection threshold
3. **Frequency Interference**: Adjacent frequency bins causing false positives
4. **Edge Cases**: Short messages or messages at audio boundaries

## Debugging Strategies

1. Add verbose logging to signal processing steps
2. Visualize FFT output for failing cases
3. Compare synthetic vs real-world audio behavior
4. Test with gradually increasing noise levels