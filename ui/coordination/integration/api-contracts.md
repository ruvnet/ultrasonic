# API Contracts Documentation

## Overview
This document defines the API contracts between the Ultrasonic-Agentics UI and backend services, ensuring consistent data exchange and type safety.

## Base Configuration

### API Endpoints
```typescript
// config/api.ts
export const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000/api',
    wsURL: 'ws://localhost:8000/ws',
    timeout: 30000
  },
  staging: {
    baseURL: 'https://staging-api.ultrasonic-agentics.com/api',
    wsURL: 'wss://staging-api.ultrasonic-agentics.com/ws',
    timeout: 30000
  },
  production: {
    baseURL: 'https://api.ultrasonic-agentics.com/api',
    wsURL: 'wss://api.ultrasonic-agentics.com/ws',
    timeout: 30000
  }
}
```

## Authentication

### Authentication Flow
```typescript
// POST /auth/login
interface LoginRequest {
  email: string
  password: string
}

interface LoginResponse {
  user: User
  token: string
  refreshToken: string
  expiresIn: number
}

// POST /auth/refresh
interface RefreshRequest {
  refreshToken: string
}

interface RefreshResponse {
  token: string
  refreshToken: string
  expiresIn: number
}

// POST /auth/logout
interface LogoutRequest {
  refreshToken: string
}

// Response: 204 No Content
```

### User Types
```typescript
interface User {
  id: string
  email: string
  name: string
  role: 'user' | 'admin'
  createdAt: string
  updatedAt: string
  preferences?: UserPreferences
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  defaultEncodingSettings: EncodingSettings
  notifications: NotificationSettings
}
```

## Encoding API

### Encode Audio File
```typescript
// POST /encode/audio
// Content-Type: multipart/form-data

interface EncodeAudioRequest {
  audio: File // Form field: 'audio'
  message: string // Form field: 'message'
  settings: string // Form field: 'settings' (JSON stringified)
}

interface EncodeAudioResponse {
  id: string
  status: 'completed' | 'failed'
  result?: {
    outputUrl: string
    downloadUrl: string
    expiresAt: string
    metadata: EncodingMetadata
  }
  error?: {
    code: string
    message: string
    details?: any
  }
}

interface EncodingMetadata {
  originalFileName: string
  outputFileName: string
  fileSize: number
  duration: number
  messageLength: number
  encodingTime: number
  settings: EncodingSettings
}
```

### Real-time Encoding Session
```typescript
// POST /encode/realtime/start
interface StartRealtimeEncodingRequest {
  message: string
  settings: EncodingSettings
}

interface StartRealtimeEncodingResponse {
  sessionId: string
  wsEndpoint: string
  token: string
  expiresAt: string
}

// WebSocket messages for real-time encoding
interface RealtimeEncodingMessage {
  type: 'audio_chunk' | 'settings_update' | 'message_update' | 'end_session'
  payload: any
}

// Audio chunk message
interface AudioChunkMessage {
  type: 'audio_chunk'
  payload: {
    chunk: ArrayBuffer
    timestamp: number
    sequenceNumber: number
  }
}

// Server responses
interface EncodingProgressMessage {
  type: 'progress'
  payload: {
    bytesProcessed: number
    totalBytes: number
    currentTime: number
  }
}

interface EncodingCompleteMessage {
  type: 'complete'
  payload: {
    outputUrl: string
    metadata: EncodingMetadata
  }
}
```

### Encoding Settings
```typescript
interface EncodingSettings {
  // Frequency parameters
  baseFrequency: number      // Hz (18000-22050)
  frequencyRange: number     // Hz (500-5000)
  
  // Timing parameters
  bitDuration: number        // milliseconds (10-100)
  guardInterval: number      // milliseconds (5-50)
  
  // Signal parameters
  amplitude: number          // 0-1
  fadeInDuration: number     // milliseconds
  fadeOutDuration: number    // milliseconds
  
  // Error correction
  errorCorrection: 'none' | 'basic' | 'advanced'
  redundancy: number         // 1-5
  
  // Security
  encryption: boolean
  encryptionKey?: string     // Base64 encoded
  
  // Optimization
  compressionLevel: number   // 0-9
  adaptiveBitrate: boolean
}
```

## Decoding API

### Decode Audio File
```typescript
// POST /decode/audio
// Content-Type: multipart/form-data

interface DecodeAudioRequest {
  audio: File // Form field: 'audio'
  settings?: string // Form field: 'settings' (JSON stringified, optional)
}

interface DecodeAudioResponse {
  id: string
  status: 'completed' | 'failed' | 'partial'
  results?: DecodingResult[]
  error?: {
    code: string
    message: string
    details?: any
  }
}

interface DecodingResult {
  message: string
  confidence: number // 0-1
  metadata: {
    detectedAt: number     // Timestamp in audio (seconds)
    endAt: number         // End timestamp
    frequency: number     // Detected base frequency
    bitRate: number       // Detected bit rate
    errorsCorrected: number
    encrypted: boolean
    signalQuality: 'excellent' | 'good' | 'fair' | 'poor'
  }
  warnings?: string[]
}
```

### Real-time Decoding
```typescript
// POST /decode/realtime/start
interface StartRealtimeDecodingRequest {
  settings?: DecodingSettings
}

interface StartRealtimeDecodingResponse {
  sessionId: string
  wsEndpoint: string
  token: string
  expiresAt: string
}

// WebSocket messages
interface DecodingDetectionMessage {
  type: 'detection'
  payload: {
    timestamp: number
    frequency: number
    strength: number
  }
}

interface DecodingResultMessage {
  type: 'result'
  payload: DecodingResult
}
```

### Decoding Settings
```typescript
interface DecodingSettings {
  // Detection parameters
  frequencyRange?: [number, number]  // Auto-detect if not specified
  detectionSensitivity: 'low' | 'medium' | 'high'
  minSignalStrength: number          // 0-1
  
  // Processing parameters
  windowSize: number                 // FFT window size
  hopSize: number                    // Window hop size
  smoothing: number                  // 0-1
  
  // Error handling
  errorTolerance: number             // 0-1
  maxRetries: number
  
  // Security
  decryption: boolean
  decryptionKey?: string             // Base64 encoded
  
  // Performance
  parallelProcessing: boolean
  gpuAcceleration: boolean
}
```

## Configuration API

### Get Default Settings
```typescript
// GET /config/defaults

interface DefaultSettingsResponse {
  encoding: {
    quick: EncodingSettings
    balanced: EncodingSettings
    robust: EncodingSettings
  }
  decoding: {
    sensitive: DecodingSettings
    balanced: DecodingSettings
    fast: DecodingSettings
  }
}
```

### Validate Settings
```typescript
// POST /config/validate

interface ValidateSettingsRequest {
  type: 'encoding' | 'decoding'
  settings: EncodingSettings | DecodingSettings
}

interface ValidateSettingsResponse {
  valid: boolean
  errors?: ValidationError[]
  warnings?: ValidationWarning[]
  suggestions?: SettingSuggestion[]
}

interface ValidationError {
  field: string
  value: any
  message: string
  code: string
}

interface ValidationWarning {
  field: string
  message: string
  impact: 'low' | 'medium' | 'high'
}

interface SettingSuggestion {
  field: string
  currentValue: any
  suggestedValue: any
  reason: string
}
```

## Analytics API

### Track Usage
```typescript
// POST /analytics/track

interface TrackEventRequest {
  event: string
  properties: Record<string, any>
  timestamp: string
  sessionId: string
}

// Response: 204 No Content
```

### Get Statistics
```typescript
// GET /analytics/stats

interface StatsResponse {
  usage: {
    totalEncodings: number
    totalDecodings: number
    totalDataProcessed: number // bytes
    averageProcessingTime: number // milliseconds
  }
  performance: {
    encodingSuccessRate: number // percentage
    decodingSuccessRate: number // percentage
    averageConfidence: number // 0-1
  }
  popular: {
    settings: {
      encoding: EncodingSettings
      decoding: DecodingSettings
    }
    frequencies: number[]
    messageLengths: number[]
  }
}
```

## Error Response Format

All error responses follow this structure:

```typescript
interface ErrorResponse {
  error: {
    code: string           // Machine-readable error code
    message: string        // Human-readable error message
    details?: any         // Additional error details
    timestamp: string     // ISO 8601 timestamp
    requestId?: string    // Request tracking ID
  }
}

// Common error codes
enum ErrorCode {
  // Client errors (4xx)
  INVALID_REQUEST = 'INVALID_REQUEST',
  INVALID_FILE_FORMAT = 'INVALID_FILE_FORMAT',
  FILE_TOO_LARGE = 'FILE_TOO_LARGE',
  MESSAGE_TOO_LONG = 'MESSAGE_TOO_LONG',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  RATE_LIMITED = 'RATE_LIMITED',
  
  // Server errors (5xx)
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  PROCESSING_FAILED = 'PROCESSING_FAILED',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  TIMEOUT = 'TIMEOUT'
}
```

## Rate Limiting

### Rate Limit Headers
```typescript
interface RateLimitHeaders {
  'X-RateLimit-Limit': string      // Request limit per window
  'X-RateLimit-Remaining': string  // Remaining requests
  'X-RateLimit-Reset': string      // Unix timestamp when limit resets
  'X-RateLimit-Window': string     // Time window in seconds
}
```

### Rate Limit Response
```typescript
// 429 Too Many Requests
interface RateLimitResponse {
  error: {
    code: 'RATE_LIMITED'
    message: string
    retryAfter: number // seconds
  }
}
```

## Pagination

### Paginated Request
```typescript
interface PaginationParams {
  page?: number      // Default: 1
  limit?: number     // Default: 20, Max: 100
  sort?: string      // Field to sort by
  order?: 'asc' | 'desc'
}
```

### Paginated Response
```typescript
interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNext: boolean
    hasPrevious: boolean
  }
}
```

## File Upload Constraints

```typescript
interface FileConstraints {
  encoding: {
    maxFileSize: 100 * 1024 * 1024  // 100MB
    allowedFormats: ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4']
    allowedExtensions: ['.wav', '.mp3', '.ogg', '.m4a']
  }
  decoding: {
    maxFileSize: 100 * 1024 * 1024  // 100MB
    allowedFormats: ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4']
    allowedExtensions: ['.wav', '.mp3', '.ogg', '.m4a']
  }
}
```

## WebSocket Protocol

### Connection Handshake
```typescript
// WebSocket connection URL format
// ws://localhost:8000/ws/{endpoint}?token={token}&sessionId={sessionId}

interface WebSocketHandshake {
  type: 'handshake'
  payload: {
    version: string
    capabilities: string[]
    sessionId: string
  }
}

interface WebSocketAck {
  type: 'ack'
  payload: {
    connected: boolean
    sessionId: string
  }
}
```

### Keep-Alive
```typescript
interface WebSocketPing {
  type: 'ping'
  payload: {
    timestamp: number
  }
}

interface WebSocketPong {
  type: 'pong'
  payload: {
    timestamp: number
    serverTime: number
  }
}
```

## API Versioning

### Version Header
```typescript
// Request header
'X-API-Version': '1.0'

// Response header
'X-API-Version': '1.0'
'X-API-Deprecated': 'true' // If using deprecated version
```

### Version Negotiation
```typescript
// GET /api/versions

interface VersionsResponse {
  current: string
  supported: string[]
  deprecated: string[]
  sunset: Record<string, string> // version -> sunset date
}
```