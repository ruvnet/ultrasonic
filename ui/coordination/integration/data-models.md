# Data Models and TypeScript Interfaces

## Overview
This document defines the TypeScript interfaces and data models used throughout the Ultrasonic-Agentics UI application, ensuring type safety and consistency.

## Core Domain Models

### Audio Models
```typescript
// types/audio.types.ts

export interface AudioFile {
  id: string
  name: string
  size: number                    // bytes
  duration: number                // seconds
  format: AudioFormat
  sampleRate: number              // Hz
  channels: number
  bitDepth: number
  createdAt: string
  metadata?: AudioMetadata
}

export enum AudioFormat {
  WAV = 'audio/wav',
  MP3 = 'audio/mpeg',
  OGG = 'audio/ogg',
  M4A = 'audio/mp4',
  WEBM = 'audio/webm'
}

export interface AudioMetadata {
  title?: string
  artist?: string
  album?: string
  year?: number
  genre?: string
  comment?: string
  [key: string]: any
}

export interface AudioBuffer {
  sampleRate: number
  length: number
  duration: number
  numberOfChannels: number
  getChannelData(channel: number): Float32Array
}

export interface AudioSegment {
  startTime: number
  endTime: number
  data: Float32Array
  metadata?: SegmentMetadata
}

export interface SegmentMetadata {
  frequency?: number
  amplitude?: number
  phase?: number
  quality?: number
}
```

### Encoding Models
```typescript
// types/encoding.types.ts

export interface EncodingJob {
  id: string
  status: EncodingStatus
  input: {
    audioFile: AudioFile
    message: string
  }
  settings: EncodingSettings
  output?: EncodingOutput
  progress: EncodingProgress
  createdAt: string
  updatedAt: string
  error?: EncodingError
}

export enum EncodingStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export interface EncodingSettings {
  // Frequency parameters
  baseFrequency: number           // Hz (18000-22050)
  frequencyRange: number          // Hz (500-5000)
  frequencyHopping: boolean
  hoppingPattern?: number[]
  
  // Timing parameters
  bitDuration: number             // milliseconds (10-100)
  guardInterval: number           // milliseconds (5-50)
  preambleDuration: number        // milliseconds
  
  // Signal parameters
  amplitude: number               // 0-1
  fadeInDuration: number          // milliseconds
  fadeOutDuration: number         // milliseconds
  modulationType: ModulationType
  
  // Error correction
  errorCorrection: ErrorCorrectionLevel
  redundancy: number              // 1-5
  interleaving: boolean
  
  // Security
  encryption: boolean
  encryptionAlgorithm?: EncryptionAlgorithm
  encryptionKey?: string          // Base64 encoded
  
  // Optimization
  compressionLevel: number        // 0-9
  adaptiveBitrate: boolean
  noiseShaping: boolean
}

export enum ModulationType {
  FSK = 'FSK',
  PSK = 'PSK',
  QAM = 'QAM',
  OFDM = 'OFDM'
}

export enum ErrorCorrectionLevel {
  NONE = 'none',
  BASIC = 'basic',
  ADVANCED = 'advanced'
}

export enum EncryptionAlgorithm {
  AES_128 = 'AES-128',
  AES_256 = 'AES-256',
  CHACHA20 = 'ChaCha20'
}

export interface EncodingOutput {
  audioFile: AudioFile
  encodedRegions: EncodedRegion[]
  statistics: EncodingStatistics
}

export interface EncodedRegion {
  startTime: number
  endTime: number
  frequency: number
  bitCount: number
  quality: number
}

export interface EncodingStatistics {
  totalBits: number
  effectiveBitRate: number        // bits per second
  compressionRatio: number
  signalQuality: number           // 0-1
  peakFrequency: number
  averageSNR: number              // dB
}

export interface EncodingProgress {
  percentage: number              // 0-100
  phase: EncodingPhase
  currentSample: number
  totalSamples: number
  estimatedTimeRemaining: number  // seconds
  speed: number                   // samples per second
}

export enum EncodingPhase {
  INITIALIZING = 'initializing',
  ANALYZING = 'analyzing',
  ENCODING = 'encoding',
  APPLYING = 'applying',
  FINALIZING = 'finalizing'
}

export interface EncodingError {
  code: string
  message: string
  details?: any
  phase?: EncodingPhase
  recoverable: boolean
}
```

### Decoding Models
```typescript
// types/decoding.types.ts

export interface DecodingJob {
  id: string
  status: DecodingStatus
  input: {
    audioFile: AudioFile
  }
  settings?: DecodingSettings
  results: DecodingResult[]
  progress: DecodingProgress
  createdAt: string
  updatedAt: string
  error?: DecodingError
}

export enum DecodingStatus {
  PENDING = 'pending',
  ANALYZING = 'analyzing',
  DECODING = 'decoding',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export interface DecodingSettings {
  // Detection parameters
  frequencyRange?: [number, number]     // Auto-detect if not specified
  detectionSensitivity: DetectionSensitivity
  minSignalStrength: number             // 0-1
  adaptiveThreshold: boolean
  
  // Processing parameters
  windowSize: number                    // FFT window size
  windowOverlap: number                 // 0-1
  windowFunction: WindowFunction
  smoothing: number                     // 0-1
  
  // Analysis parameters
  multipassAnalysis: boolean
  correlationThreshold: number          // 0-1
  patternMatching: boolean
  
  // Error handling
  errorTolerance: number                // 0-1
  maxRetries: number
  useErrorCorrection: boolean
  
  // Security
  decryption: boolean
  decryptionKey?: string                // Base64 encoded
  bruteForceDecryption: boolean
  
  // Performance
  parallelProcessing: boolean
  gpuAcceleration: boolean
  maxThreads?: number
}

export enum DetectionSensitivity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  ULTRA = 'ultra'
}

export enum WindowFunction {
  HANN = 'hann',
  HAMMING = 'hamming',
  BLACKMAN = 'blackman',
  KAISER = 'kaiser'
}

export interface DecodingResult {
  id: string
  message: string
  confidence: number                    // 0-1
  metadata: DecodingMetadata
  quality: DecodingQuality
  warnings: string[]
  raw?: DecodingRawData
}

export interface DecodingMetadata {
  detectedAt: number                    // Timestamp in audio (seconds)
  endAt: number                         // End timestamp
  duration: number                      // Message duration
  frequency: number                     // Detected base frequency
  frequencyVariation: number            // Hz
  bitRate: number                       // Detected bit rate
  modulationType: ModulationType
  errorsCorrected: number
  parityErrors: number
  encrypted: boolean
  compressionDetected: boolean
}

export interface DecodingQuality {
  overall: QualityLevel
  signalStrength: number                // 0-1
  noiseLevel: number                    // 0-1
  snr: number                          // dB
  distortion: number                    // 0-1
  clarity: number                       // 0-1
}

export enum QualityLevel {
  EXCELLENT = 'excellent',
  GOOD = 'good',
  FAIR = 'fair',
  POOR = 'poor'
}

export interface DecodingRawData {
  bits: string
  frequencies: number[]
  amplitudes: number[]
  phases: number[]
  timestamps: number[]
}

export interface DecodingProgress {
  percentage: number                    // 0-100
  phase: DecodingPhase
  currentPosition: number               // seconds
  totalDuration: number                 // seconds
  detectedSignals: number
  decodedMessages: number
}

export enum DecodingPhase {
  INITIALIZING = 'initializing',
  SCANNING = 'scanning',
  DETECTING = 'detecting',
  DECODING = 'decoding',
  VERIFYING = 'verifying',
  FINALIZING = 'finalizing'
}

export interface DecodingError {
  code: string
  message: string
  details?: any
  phase?: DecodingPhase
  position?: number                     // Audio position where error occurred
}
```

### Analysis Models
```typescript
// types/analysis.types.ts

export interface AnalysisResult {
  id: string
  audioFile: AudioFile
  timestamp: string
  spectrum: SpectrumAnalysis
  ultrasonic: UltrasonicAnalysis
  quality: QualityAnalysis
  patterns: PatternAnalysis
}

export interface SpectrumAnalysis {
  fftSize: number
  sampleRate: number
  frequencyBins: FrequencyBin[]
  peaks: FrequencyPeak[]
  powerSpectrum: number[]
  spectralCentroid: number
  spectralRolloff: number
}

export interface FrequencyBin {
  frequency: number
  magnitude: number
  phase: number
}

export interface FrequencyPeak {
  frequency: number
  magnitude: number
  q: number                            // Quality factor
  prominence: number
  harmonics: number[]
}

export interface UltrasonicAnalysis {
  detected: boolean
  regions: UltrasonicRegion[]
  dominantFrequency: number
  bandwidth: number
  modulation: ModulationAnalysis
  encoding: EncodingAnalysis
}

export interface UltrasonicRegion {
  startTime: number
  endTime: number
  centerFrequency: number
  bandwidth: number
  averagePower: number
  peakPower: number
  confidence: number
}

export interface ModulationAnalysis {
  type: ModulationType
  parameters: Record<string, number>
  confidence: number
}

export interface EncodingAnalysis {
  detected: boolean
  type: string
  bitRate: number
  symbolRate: number
  confidence: number
}

export interface QualityAnalysis {
  overall: QualityLevel
  metrics: QualityMetrics
  issues: QualityIssue[]
  recommendations: string[]
}

export interface QualityMetrics {
  snr: number                          // Signal-to-noise ratio (dB)
  thd: number                          // Total harmonic distortion (%)
  dynamicRange: number                 // dB
  peakLevel: number                    // dBFS
  rmsLevel: number                     // dBFS
  crestFactor: number
  clarity: number                      // 0-1
}

export interface QualityIssue {
  type: IssueType
  severity: IssueSeverity
  description: string
  location?: {
    startTime: number
    endTime: number
  }
  impact: string
}

export enum IssueType {
  CLIPPING = 'clipping',
  DISTORTION = 'distortion',
  NOISE = 'noise',
  DROPOUT = 'dropout',
  INTERFERENCE = 'interference'
}

export enum IssueSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export interface PatternAnalysis {
  patterns: DetectedPattern[]
  periodicity: PeriodicityAnalysis
  similarity: SimilarityAnalysis
}

export interface DetectedPattern {
  type: string
  confidence: number
  locations: PatternLocation[]
  characteristics: Record<string, any>
}

export interface PatternLocation {
  startTime: number
  endTime: number
  strength: number
}

export interface PeriodicityAnalysis {
  detected: boolean
  period: number                       // seconds
  confidence: number
  harmonics: number[]
}

export interface SimilarityAnalysis {
  segments: SimilarSegment[]
  overallSimilarity: number
}

export interface SimilarSegment {
  segment1: AudioSegment
  segment2: AudioSegment
  similarity: number
}
```

### User Interface Models
```typescript
// types/ui.types.ts

export interface UIState {
  theme: Theme
  layout: LayoutConfig
  notifications: Notification[]
  modals: ModalState
  tooltips: TooltipConfig
}

export interface Theme {
  mode: 'light' | 'dark' | 'system'
  primary: string
  secondary: string
  accent: string
  customColors?: Record<string, string>
}

export interface LayoutConfig {
  sidebarCollapsed: boolean
  headerHeight: number
  contentPadding: number
  responsiveBreakpoint: string
}

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message?: string
  duration?: number
  actions?: NotificationAction[]
  timestamp: string
}

export enum NotificationType {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error'
}

export interface NotificationAction {
  label: string
  action: () => void
  style?: 'primary' | 'secondary'
}

export interface ModalState {
  [key: string]: {
    isOpen: boolean
    data?: any
  }
}

export interface TooltipConfig {
  delay: number
  placement: 'top' | 'bottom' | 'left' | 'right'
  showOnHover: boolean
  showOnFocus: boolean
}

export interface FormState<T = any> {
  values: T
  errors: Partial<Record<keyof T, string>>
  touched: Partial<Record<keyof T, boolean>>
  isSubmitting: boolean
  isValid: boolean
}

export interface TableState<T = any> {
  data: T[]
  sorting: SortConfig
  filtering: FilterConfig
  pagination: PaginationConfig
  selection: SelectionConfig
}

export interface SortConfig {
  field: string
  direction: 'asc' | 'desc'
}

export interface FilterConfig {
  filters: Record<string, any>
  globalFilter?: string
}

export interface PaginationConfig {
  page: number
  pageSize: number
  total: number
}

export interface SelectionConfig {
  mode: 'single' | 'multiple'
  selected: string[]
}
```

### Application State Models
```typescript
// types/app.types.ts

export interface AppState {
  user: User | null
  session: Session | null
  preferences: UserPreferences
  features: FeatureFlags
  performance: PerformanceMetrics
}

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  role: UserRole
  permissions: Permission[]
  createdAt: string
  updatedAt: string
}

export enum UserRole {
  USER = 'user',
  PRO = 'pro',
  ADMIN = 'admin'
}

export interface Permission {
  resource: string
  actions: string[]
}

export interface Session {
  id: string
  token: string
  refreshToken: string
  expiresAt: string
  device: DeviceInfo
}

export interface DeviceInfo {
  id: string
  name: string
  type: 'desktop' | 'mobile' | 'tablet'
  os: string
  browser: string
}

export interface UserPreferences {
  theme: Theme
  language: string
  timezone: string
  notifications: NotificationPreferences
  privacy: PrivacyPreferences
  encoding: EncodingPreferences
  decoding: DecodingPreferences
}

export interface NotificationPreferences {
  email: boolean
  push: boolean
  inApp: boolean
  types: {
    [key in NotificationType]: boolean
  }
}

export interface PrivacyPreferences {
  analytics: boolean
  crashReports: boolean
  usageData: boolean
}

export interface EncodingPreferences {
  defaultSettings: EncodingSettings
  favoritePresets: string[]
  autoSave: boolean
  confirmBeforeEncode: boolean
}

export interface DecodingPreferences {
  defaultSettings: DecodingSettings
  autoAnalyze: boolean
  saveResults: boolean
}

export interface FeatureFlags {
  [key: string]: boolean | string | number
}

export interface PerformanceMetrics {
  fps: number
  latency: number
  memoryUsage: number
  cpuUsage: number
  networkLatency: number
}
```

### Utility Types
```typescript
// types/utility.types.ts

export type Nullable<T> = T | null
export type Optional<T> = T | undefined
export type ValueOf<T> = T[keyof T]

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P]
}

export type Mutable<T> = {
  -readonly [P in keyof T]: T[P]
}

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> =
  Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
  }[Keys]

export type RequireOnlyOne<T, Keys extends keyof T = keyof T> =
  Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Record<Exclude<Keys, K>, undefined>>
  }[Keys]

export type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

export interface PaginatedData<T> {
  items: T[]
  pagination: {
    page: number
    pageSize: number
    total: number
    totalPages: number
    hasNext: boolean
    hasPrevious: boolean
  }
}

export interface ApiResponse<T> {
  data: T
  status: number
  headers: Record<string, string>
  timestamp: string
}

export interface ApiError {
  code: string
  message: string
  details?: any
  timestamp: string
  requestId?: string
}
```

## Type Guards and Validators

```typescript
// utils/typeGuards.ts

export function isAudioFile(file: File): boolean {
  return file.type.startsWith('audio/')
}

export function isEncodingJob(job: any): job is EncodingJob {
  return job && 
    typeof job.id === 'string' &&
    job.status in EncodingStatus &&
    job.input && 
    job.settings
}

export function isDecodingResult(result: any): result is DecodingResult {
  return result &&
    typeof result.message === 'string' &&
    typeof result.confidence === 'number' &&
    result.metadata
}

export function hasUltrasonicContent(analysis: AnalysisResult): boolean {
  return analysis.ultrasonic.detected && analysis.ultrasonic.regions.length > 0
}

export function isValidFrequency(freq: number): boolean {
  return freq >= 20 && freq <= 22050
}

export function isValidEncodingSettings(settings: any): settings is EncodingSettings {
  return settings &&
    isValidFrequency(settings.baseFrequency) &&
    settings.frequencyRange > 0 &&
    settings.bitDuration > 0 &&
    settings.amplitude >= 0 && settings.amplitude <= 1
}
```

## Constants and Enums

```typescript
// constants/audio.constants.ts

export const AUDIO_CONSTRAINTS = {
  MIN_FREQUENCY: 20,
  MAX_FREQUENCY: 22050,
  ULTRASONIC_MIN: 18000,
  ULTRASONIC_MAX: 22050,
  MIN_SAMPLE_RATE: 44100,
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  SUPPORTED_FORMATS: [AudioFormat.WAV, AudioFormat.MP3, AudioFormat.OGG, AudioFormat.M4A]
} as const

export const ENCODING_LIMITS = {
  MIN_BIT_DURATION: 10,
  MAX_BIT_DURATION: 100,
  MIN_MESSAGE_LENGTH: 1,
  MAX_MESSAGE_LENGTH: 1000,
  MIN_AMPLITUDE: 0.1,
  MAX_AMPLITUDE: 1.0
} as const

export const QUALITY_THRESHOLDS = {
  EXCELLENT: { snr: 40, confidence: 0.95 },
  GOOD: { snr: 30, confidence: 0.85 },
  FAIR: { snr: 20, confidence: 0.70 },
  POOR: { snr: 10, confidence: 0.50 }
} as const
```