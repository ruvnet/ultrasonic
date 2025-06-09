# Encoding Panel Component Development

## Overview
The encoding panel provides the interface for users to embed hidden messages into audio files using ultrasonic steganography.

## Component Specifications

### EncodingPanel Component
**Status**: 🔴 PRIORITY 1 - Core Functionality
**Purpose**: Main container for all encoding-related controls and feedback
**Dependencies**: AudioPlayer, MessageInput, EncodingSettings

#### Props Interface
```typescript
interface EncodingPanelProps {
  onEncode: (params: EncodingParams) => Promise<void>
  isProcessing?: boolean
  className?: string
}

interface EncodingParams {
  message: string
  audioFile?: File
  audioBuffer?: AudioBuffer
  settings: EncodingSettings
}
```

### MessageInput Component
**Status**: 🔴 PRIORITY 1 - Core Functionality
**Purpose**: Input and validation for messages to be encoded
**Dependencies**: None - foundational component

#### Props Interface
```typescript
interface MessageInputProps {
  value: string
  onChange: (value: string) => void
  maxLength?: number
  onValidationChange?: (isValid: boolean) => void
  className?: string
}
```

#### Features
- [ ] Character count display
- [ ] Real-time validation
- [ ] Encryption option toggle
- [ ] Message preview
- [ ] Multi-line support
- [ ] Special character handling

### EncodingSettings Component
**Status**: 🔴 PRIORITY 1 - Core Functionality
**Purpose**: Configure encoding parameters
**Dependencies**: None - foundational component

#### Props Interface
```typescript
interface EncodingSettingsProps {
  settings: EncodingSettings
  onChange: (settings: EncodingSettings) => void
  presets?: EncodingPreset[]
  showAdvanced?: boolean
  className?: string
}

interface EncodingSettings {
  baseFrequency: number      // e.g., 19000 Hz
  frequencyRange: number     // e.g., 3000 Hz
  bitDuration: number        // milliseconds
  amplitude: number          // 0-1
  errorCorrection: 'none' | 'basic' | 'advanced'
  encryption: boolean
  compressionLevel: number   // 0-9
}
```

#### Features
- [ ] Preset selection (Quick, Balanced, Robust)
- [ ] Advanced settings toggle
- [ ] Real-time parameter validation
- [ ] Visual frequency range indicator
- [ ] Estimated capacity display

### AudioSourceSelector Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Choose audio source for encoding
**Dependencies**: AudioPlayer, AudioRecorder

#### Props Interface
```typescript
interface AudioSourceSelectorProps {
  onSourceSelect: (source: AudioSource) => void
  currentSource?: AudioSource
  className?: string
}

type AudioSource = 
  | { type: 'file'; file: File }
  | { type: 'recording'; duration: number }
  | { type: 'generated'; waveform: 'sine' | 'noise' }
```

### EncodingProgress Component
**Status**: 🔴 PRIORITY 1 - Core Functionality
**Purpose**: Show encoding progress and results
**Dependencies**: None - foundational component

#### Props Interface
```typescript
interface EncodingProgressProps {
  progress: number // 0-100
  stage?: 'preparing' | 'encoding' | 'finalizing'
  result?: EncodingResult
  onDownload?: () => void
  onReset?: () => void
  className?: string
}

interface EncodingResult {
  outputFile: Blob
  duration: number
  messageSize: number
  capacity: number
  settings: EncodingSettings
}
```

## Development Tasks

### Phase 1: Core Components (Week 1-2)
1. [ ] Create MessageInput with validation - **START HERE**
2. [ ] Implement basic EncodingSettings - **PARALLEL WORK**
3. [ ] Create simple progress display - **PARALLEL WORK**
4. [ ] Add file upload for AudioSourceSelector

**Critical Path**: MessageInput + EncodingSettings → EncodingPanel → AudioSourceSelector

### Phase 2: Advanced Features
1. [ ] Add encoding presets system
2. [ ] Implement real-time capacity calculation
3. [ ] Add audio generation options
4. [ ] Create advanced settings panel

### Phase 3: User Experience
1. [ ] Add drag-and-drop for audio files
2. [ ] Implement settings persistence
3. [ ] Add encoding history
4. [ ] Create batch encoding support

## State Management
```typescript
// Zustand slice for encoding
interface EncodingSlice {
  // State
  message: string
  audioSource: AudioSource | null
  settings: EncodingSettings
  isEncoding: boolean
  progress: number
  result: EncodingResult | null
  
  // Actions
  setMessage: (message: string) => void
  setAudioSource: (source: AudioSource) => void
  updateSettings: (settings: Partial<EncodingSettings>) => void
  startEncoding: () => Promise<void>
  resetEncoding: () => void
}
```

## Validation Rules
- Message length: 1-1000 characters
- Base frequency: 18000-22050 Hz
- Frequency range: 500-5000 Hz
- Bit duration: 10-100 ms
- File formats: MP3, WAV, OGG, M4A

## Testing Requirements
- [ ] Form validation tests
- [ ] File upload handling
- [ ] Settings persistence
- [ ] Error state handling
- [ ] Progress tracking accuracy

## Accessibility Requirements
- Form labels and descriptions
- Error announcements
- Progress updates for screen readers
- Keyboard navigation for all controls
- Focus management in multi-step process

## Error Handling
- Invalid file format
- Message too long for audio capacity
- Unsupported browser features
- Network errors during processing
- Invalid parameter combinations

## UI/UX Considerations
- Clear visual hierarchy
- Immediate feedback on actions
- Helpful tooltips for settings
- Mobile-responsive layout
- Graceful degradation for unsupported features

## Notes
- Consider WebAssembly for heavy encoding operations
- Implement client-side encoding for privacy
- Add option to save/load encoding profiles
- Consider batch operations for multiple files