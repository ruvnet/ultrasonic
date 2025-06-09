# Task 003: Algorithm Optimization

## Objective
Optimize ultrasonic signal detection algorithms for better performance and accuracy.

## Current Performance Issues
- FFT operations potentially inefficient
- Demodulation algorithm may miss weak signals
- Processing time for large audio files
- Memory usage during signal processing

## Subtasks

### 1. Performance Profiling ⚪ TODO
- [ ] Profile current encoder performance
- [ ] Profile current decoder performance
- [ ] Identify bottlenecks (CPU vs memory)
- [ ] Measure processing time per audio second

### 2. FFT Optimization ⚪ TODO
- [ ] Evaluate current FFT window size (1024)
- [ ] Test overlap-add method efficiency
- [ ] Consider using scipy.fft vs numpy.fft
- [ ] Implement sliding window optimization
- [ ] Test with power-of-2 window sizes

### 3. Demodulation Enhancement ⚪ TODO
- [ ] Implement adaptive thresholding
- [ ] Add pre-filtering for noise reduction
- [ ] Optimize frequency detection algorithm
- [ ] Consider phase-locked loop (PLL) approach
- [ ] Add confidence scoring for detections

### 4. Memory Optimization ⚪ TODO
- [ ] Implement streaming processing for large files
- [ ] Optimize array allocations
- [ ] Use memory-mapped files for large audio
- [ ] Reduce intermediate array copies

### 5. Algorithm Alternatives ⚪ TODO
- [ ] Research Goertzel algorithm for specific frequency detection
- [ ] Evaluate correlation-based detection
- [ ] Test matched filter approach
- [ ] Consider machine learning-based detection

## Optimization Targets

```python
# Current Performance (estimated)
Processing Speed: ~10x realtime
Memory Usage: ~100MB per minute of audio
Detection Accuracy: ~78% (based on tests)

# Target Performance
Processing Speed: >50x realtime
Memory Usage: <50MB per minute of audio
Detection Accuracy: >95%
```

## Code Areas to Optimize

1. **ultrasonic_encoder.py**
   - `_modulate_fsk()` - Signal generation
   - Array concatenation in loops

2. **ultrasonic_decoder.py**
   - `_band_pass_filter()` - Filter design
   - `_extract_ultrasonic()` - FFT operations
   - `_demodulate_fsk()` - Peak detection

## Success Criteria
- 5x improvement in processing speed
- 50% reduction in memory usage
- >95% test pass rate
- Maintains accuracy on noisy signals

## Dependencies
- Calibration task (Task 001) should be complete
- Need baseline performance metrics first

## Notes for Other Agents
- Document performance improvements in `memory_bank/calibration_values.md`
- Consider creating benchmark suite for consistent testing
- Ensure optimizations don't break existing functionality