# Decoding Panel Component Development

## Overview
The decoding panel provides the interface for extracting hidden messages from audio files using ultrasonic steganography detection.

## Component Specifications

### DecodingPanel Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Main container for all decoding-related controls and results
**Dependencies**: AudioUploader, DecodingSettings, DecodingResults

#### Props Interface
```typescript
interface DecodingPanelProps {
  onDecode: (params: DecodingParams) => Promise<void>
  isProcessing?: boolean
  className?: string
}

interface DecodingParams {
  audioFile?: File
  audioBuffer?: AudioBuffer
  settings?: DecodingSettings
}
```

### AudioUploader Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Upload and preview audio files for decoding
**Dependencies**: AudioPlayer for preview functionality

#### Props Interface
```typescript
interface AudioUploaderProps {
  onFileSelect: (file: File) => void
  acceptedFormats?: string[]
  maxFileSize?: number // in MB
  showPreview?: boolean
  className?: string
}
```

#### Features
- [ ] Drag and drop support
- [ ] File validation
- [ ] Audio preview player
- [ ] File info display
- [ ] Multiple file queue
- [ ] URL input option

### DecodingSettings Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Configure decoding parameters
**Dependencies**: None - can be developed independently

#### Props Interface
```typescript
interface DecodingSettingsProps {
  settings: DecodingSettings
  onChange: (settings: DecodingSettings) => void
  mode?: 'auto' | 'manual'
  className?: string
}

interface DecodingSettings {
  frequencyRange?: [number, number] // Auto-detect if not specified
  detectionSensitivity: 'low' | 'medium' | 'high'
  errorTolerance: number // 0-1
  decryption: boolean
  parallelProcessing: boolean
}
```

### DecodingProgress Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Show real-time decoding progress and analysis
**Dependencies**: None - can be developed independently

#### Props Interface
```typescript
interface DecodingProgressProps {
  progress: DecodingProgress
  onCancel?: () => void
  className?: string
}

interface DecodingProgress {
  percentage: number // 0-100
  stage: 'analyzing' | 'detecting' | 'decoding' | 'verifying'
  currentFrequency?: number
  signalStrength?: number
  estimatedTime?: number // seconds remaining
}
```

### DecodingResults Component
**Status**: 🟡 PRIORITY 2 - Enhanced Features
**Purpose**: Display decoded messages and metadata
**Dependencies**: None - can be developed independently

#### Props Interface
```typescript
interface DecodingResultsProps {
  results: DecodingResult[]
  onExport?: (format: 'json' | 'txt' | 'csv') => void
  onCopyMessage?: (message: string) => void
  className?: string
}

interface DecodingResult {
  message: string
  confidence: number // 0-100
  metadata: {
    detectedAt: number // timestamp in audio
    frequency: number
    bitRate: number
    errorsCorrected: number
    encrypted: boolean
  }
  warnings?: string[]
}
```

### SignalAnalysis Component
**Status**: 🟢 PRIORITY 3 - Nice to Have
**Purpose**: Visual analysis of detected ultrasonic signals
**Dependencies**: WaveformVisualizer, FrequencyAnalyzer

#### Props Interface
```typescript
interface SignalAnalysisProps {
  audioBuffer: AudioBuffer
  detectedRegions: DetectedRegion[]
  onRegionClick?: (region: DetectedRegion) => void
  className?: string
}

interface DetectedRegion {
  start: number
  end: number
  frequency: number
  strength: number
  decoded: boolean
}
```

## Development Tasks

### Phase 1: Basic Decoding (Week 2-3)
1. [ ] Implement AudioUploader with validation - **AFTER ENCODING**
2. [ ] Create basic DecodingSettings
3. [ ] Add progress tracking
4. [ ] Display simple results

**Critical Path**: Complete encoding functionality first → AudioUploader → DecodingPanel

### Phase 2: Advanced Analysis
1. [ ] Add signal visualization
2. [ ] Implement auto-detection mode
3. [ ] Add batch processing
4. [ ] Create detailed analysis view

### Phase 3: Enhanced Features
1. [ ] Add real-time decoding from microphone
2. [ ] Implement confidence scoring
3. [ ] Add export functionality
4. [ ] Create comparison mode

## State Management
```typescript
// Zustand slice for decoding
interface DecodingSlice {
  // State
  audioFile: File | null
  settings: DecodingSettings
  isDecoding: boolean
  progress: DecodingProgress | null
  results: DecodingResult[]
  analysisData: AnalysisData | null
  
  // Actions
  setAudioFile: (file: File) => void
  updateSettings: (settings: Partial<DecodingSettings>) => void
  startDecoding: () => Promise<void>
  cancelDecoding: () => void
  clearResults: () => void
  exportResults: (format: string) => void
}
```

## Decoding Workflow
1. **Upload**: User uploads audio file
2. **Analyze**: System scans for ultrasonic frequencies
3. **Detect**: Identify potential encoded regions
4. **Decode**: Extract and verify messages
5. **Present**: Display results with confidence scores

## Performance Optimizations
- Use Web Workers for decoding operations
- Implement chunked processing for large files
- Cache frequency analysis results
- Progressive rendering of results
- Optimize FFT window size based on file

## Testing Requirements
- [ ] Various audio format support
- [ ] Large file handling
- [ ] Weak signal detection
- [ ] Error recovery testing
- [ ] Performance benchmarks

## Error Scenarios
- No message found
- Corrupted message data
- Insufficient signal strength
- Unsupported encoding format
- Partial message recovery

## UI/UX Considerations
- Clear empty states
- Helpful error messages
- Visual signal indicators
- Progress estimation
- Result confidence visualization

## Accessibility Features
- Screen reader support for results
- Keyboard navigation
- Audio descriptions of visual data
- High contrast mode
- Alternative text for graphs

## Advanced Features (Future)
- Machine learning signal detection
- Multi-channel audio support
- Real-time streaming decode
- Comparative analysis mode
- Historical decoding database

## Notes
- Consider TensorFlow.js for advanced signal detection
- Implement speculative decoding for faster results
- Add support for custom decoding algorithms
- Consider privacy implications of cloud processing