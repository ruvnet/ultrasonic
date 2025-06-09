# Task 001: Signal Calibration

## Objective
Calibrate ultrasonic signal detection thresholds to fix failing tests in the steganography framework.

## Current Issues
- FSK demodulation failing to detect embedded signals
- Threshold values too strict or incorrect frequency detection
- Test failures primarily in `test_ultrasonic_decoder.py` and `test_ultrasonic_encoder.py`

## Subtasks

### 1. Analyze Current Parameters ⚪ TODO
- [ ] Document current frequency pairs (18-20 kHz range)
- [ ] Record current amplitude thresholds
- [ ] List bit duration settings
- [ ] Map SNR requirements

### 2. Identify Failing Test Patterns 🟡 IN_PROGRESS
- [ ] Run test suite and categorize failures
- [ ] Identify common failure modes
- [ ] Document which signal parameters cause failures
- [ ] Create minimal reproducible test cases

### 3. Experimental Calibration ⚪ TODO
- [ ] Create calibration test harness
- [ ] Test frequency pair separations (100Hz - 2000Hz)
- [ ] Test amplitude variations (0.1 - 1.0)
- [ ] Test bit durations (0.01s - 0.1s)
- [ ] Find optimal SNR thresholds

### 4. Update Implementation ⚪ TODO
- [ ] Update `UltrasonicEncoder` parameters
- [ ] Update `UltrasonicDecoder` thresholds
- [ ] Adjust FFT window sizes if needed
- [ ] Update band-pass filter parameters

### 5. Validate Changes ⚪ TODO
- [ ] Run full test suite
- [ ] Test with various audio formats
- [ ] Test with different noise levels
- [ ] Ensure backwards compatibility

## Key Parameters to Calibrate

```python
# Current values (may need adjustment)
FREQ_0 = 18000  # Hz for bit 0
FREQ_1 = 19000  # Hz for bit 1
BIT_DURATION = 0.05  # seconds
AMPLITUDE = 0.3
DETECTION_THRESHOLD = 0.1  # SNR threshold
FFT_WINDOW_SIZE = 1024
```

## Success Criteria
- All ultrasonic-related tests passing
- Reliable detection across different audio formats
- Robust to moderate background noise
- False positive rate < 1%

## Dependencies
- None - can proceed immediately

## Notes for Other Agents
- Document any discovered optimal values in `memory_bank/calibration_values.md`
- If you find parameters that work, update this file immediately
- Test with both synthetic and real audio files