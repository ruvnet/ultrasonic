# Audio Controls Component Development

## Overview
Audio control components for playing, recording, and manipulating audio in the Ultrasonic-Agentics UI.

## Component Specifications

### AudioPlayer Component
**Status**: 🔴 PRIORITY 1 - Core Functionality
**Purpose**: Play audio files with ultrasonic-encoded messages
**Dependencies**: None - foundational component

#### Props Interface
```typescript
interface AudioPlayerProps {
  audioUrl?: string
  audioBuffer?: AudioBuffer
  onPlaybackComplete?: () => void
  onError?: (error: Error) => void
  showWaveform?: boolean
  className?: string
}
```

#### Features
- [ ] Play/pause/stop controls
- [ ] Playback progress bar
- [ ] Volume control
- [ ] Playback speed control
- [ ] Waveform visualization integration
- [ ] Time display (current/total)

### AudioRecorder Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Record audio from microphone for real-time encoding
**Dependencies**: AudioPlayer must be complete

#### Props Interface
```typescript
interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void
  onRecordingStart?: () => void
  onError?: (error: Error) => void
  maxDuration?: number // in seconds
  showLevelMeter?: boolean
  className?: string
}
```

#### Features
- [ ] Start/stop recording
- [ ] Recording time display
- [ ] Audio level meter
- [ ] Device selection
- [ ] Recording format options
- [ ] Real-time visualization

### AudioDeviceSelector Component
**Status**: 🟢 PRIORITY 3 - Nice to Have
**Purpose**: Select audio input/output devices
**Dependencies**: AudioRecorder must be complete

#### Props Interface
```typescript
interface AudioDeviceSelectorProps {
  type: 'input' | 'output'
  onDeviceChange: (deviceId: string) => void
  currentDeviceId?: string
  className?: string
}
```

## Development Tasks

### Phase 1: Basic Audio Controls (Week 1)
1. [ ] Implement AudioPlayer with basic controls - **START HERE**
2. [ ] Add waveform visualization support
3. [ ] Create AudioRecorder with permission handling
4. [ ] Add device enumeration and selection

**Critical Path**: AudioPlayer → AudioRecorder → AudioDeviceSelector

### Phase 2: Advanced Features
1. [ ] Add real-time audio level monitoring
2. [ ] Implement recording format options
3. [ ] Add advanced playback controls (loop, markers)
4. [ ] Create audio preprocessing options

### Phase 3: Integration
1. [ ] Connect to Zustand store
2. [ ] Implement error boundaries
3. [ ] Add loading states
4. [ ] Create comprehensive tests

## Testing Requirements
- [ ] Unit tests for audio utilities
- [ ] Component interaction tests
- [ ] Cross-browser audio API compatibility
- [ ] Permission handling tests
- [ ] Error state testing

## Accessibility Considerations
- Keyboard navigation for all controls
- Screen reader announcements for state changes
- Visual feedback for audio levels
- Alternative text for waveform data

## Dependencies
- Web Audio API
- MediaRecorder API
- React hooks for audio context
- Waveform visualization library (TBD)

## Notes
- Consider using a library like WaveSurfer.js for waveform visualization
- Ensure proper cleanup of audio contexts and streams
- Handle browser compatibility issues gracefully
- Consider WebRTC for future real-time features