# WebSocket Events Documentation

## Overview
This document defines the WebSocket event protocols for real-time communication between the Ultrasonic-Agentics UI and backend services.

## WebSocket Connection Management

### Connection Lifecycle
```typescript
// Connection states
enum WebSocketState {
  CONNECTING = 'CONNECTING',
  CONNECTED = 'CONNECTED',
  RECONNECTING = 'RECONNECTING',
  DISCONNECTED = 'DISCONNECTED',
  ERROR = 'ERROR'
}

// Connection manager
class WebSocketManager {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  
  connect(url: string, token: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const wsUrl = `${url}?token=${encodeURIComponent(token)}`
      this.ws = new WebSocket(wsUrl)
      
      this.ws.onopen = () => {
        this.reconnectAttempts = 0
        this.sendHandshake()
        resolve()
      }
      
      this.ws.onerror = (error) => {
        reject(error)
      }
      
      this.ws.onclose = this.handleClose.bind(this)
      this.ws.onmessage = this.handleMessage.bind(this)
    })
  }
  
  private handleClose(event: CloseEvent) {
    if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnect()
    }
  }
  
  private reconnect() {
    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
    
    setTimeout(() => {
      this.connect(this.lastUrl, this.lastToken)
    }, delay)
  }
}
```

## Event Message Format

### Base Message Structure
```typescript
interface WebSocketMessage<T = any> {
  id: string           // Unique message ID
  type: string         // Event type
  timestamp: number    // Unix timestamp
  payload: T          // Event-specific payload
  metadata?: {
    version: string
    clientId?: string
    sessionId?: string
  }
}

// Message factory
function createMessage<T>(type: string, payload: T): WebSocketMessage<T> {
  return {
    id: generateUUID(),
    type,
    timestamp: Date.now(),
    payload,
    metadata: {
      version: '1.0',
      clientId: getClientId(),
      sessionId: getSessionId()
    }
  }
}
```

## Real-Time Encoding Events

### Client → Server Events

#### Start Encoding Session
```typescript
interface StartEncodingEvent {
  type: 'encoding:start'
  payload: {
    message: string
    settings: EncodingSettings
    streamConfig: {
      sampleRate: number
      channels: number
      bitDepth: number
    }
  }
}
```

#### Audio Stream Chunk
```typescript
interface AudioStreamChunkEvent {
  type: 'encoding:audio_chunk'
  payload: {
    chunk: ArrayBuffer
    sequenceNumber: number
    timestamp: number
    isLastChunk?: boolean
  }
}
```

#### Update Encoding Parameters
```typescript
interface UpdateEncodingEvent {
  type: 'encoding:update'
  payload: {
    settings?: Partial<EncodingSettings>
    message?: string
  }
}
```

#### Pause/Resume Encoding
```typescript
interface PauseEncodingEvent {
  type: 'encoding:pause'
  payload: {
    timestamp: number
  }
}

interface ResumeEncodingEvent {
  type: 'encoding:resume'
  payload: {
    timestamp: number
  }
}
```

#### End Encoding Session
```typescript
interface EndEncodingEvent {
  type: 'encoding:end'
  payload: {
    reason: 'complete' | 'cancel' | 'error'
    finalSequenceNumber: number
  }
}
```

### Server → Client Events

#### Encoding Progress
```typescript
interface EncodingProgressEvent {
  type: 'encoding:progress'
  payload: {
    processedSamples: number
    totalSamples: number
    processedDuration: number // seconds
    estimatedTimeRemaining: number // seconds
    currentFrequency: number
    signalStrength: number
  }
}
```

#### Encoding Chunk Processed
```typescript
interface ChunkProcessedEvent {
  type: 'encoding:chunk_processed'
  payload: {
    sequenceNumber: number
    processedAt: number
    outputSize: number
    quality: number // 0-1
  }
}
```

#### Encoding Complete
```typescript
interface EncodingCompleteEvent {
  type: 'encoding:complete'
  payload: {
    outputUrl: string
    downloadUrl: string
    metadata: {
      duration: number
      fileSize: number
      messageLength: number
      actualBitRate: number
      compressionRatio: number
      signalQuality: number
    }
  }
}
```

#### Encoding Error
```typescript
interface EncodingErrorEvent {
  type: 'encoding:error'
  payload: {
    code: string
    message: string
    details?: any
    recoverable: boolean
    sequenceNumber?: number
  }
}
```

## Real-Time Decoding Events

### Client → Server Events

#### Start Decoding Session
```typescript
interface StartDecodingEvent {
  type: 'decoding:start'
  payload: {
    settings?: DecodingSettings
    streamConfig: {
      sampleRate: number
      channels: number
      bitDepth: number
    }
  }
}
```

#### Audio Stream for Decoding
```typescript
interface DecodingAudioChunkEvent {
  type: 'decoding:audio_chunk'
  payload: {
    chunk: ArrayBuffer
    sequenceNumber: number
    timestamp: number
  }
}
```

### Server → Client Events

#### Signal Detection
```typescript
interface SignalDetectionEvent {
  type: 'decoding:signal_detected'
  payload: {
    timestamp: number        // When in the audio stream
    frequency: number        // Detected frequency
    strength: number         // Signal strength 0-1
    confidence: number       // Detection confidence 0-1
    region: {
      start: number
      end: number
      duration: number
    }
  }
}
```

#### Partial Decoding Result
```typescript
interface PartialDecodingEvent {
  type: 'decoding:partial_result'
  payload: {
    message: string
    completeness: number     // 0-1 how much of message decoded
    confidence: number       // 0-1 confidence in result
    position: {
      start: number
      current: number
      estimated_end: number
    }
  }
}
```

#### Final Decoding Result
```typescript
interface FinalDecodingEvent {
  type: 'decoding:final_result'
  payload: {
    results: Array<{
      message: string
      confidence: number
      metadata: {
        startTime: number
        endTime: number
        frequency: number
        bitRate: number
        errorsCorrected: number
        encrypted: boolean
      }
    }>
    summary: {
      totalMessages: number
      averageConfidence: number
      processingTime: number
    }
  }
}
```

## Analysis Events

### Frequency Analysis
```typescript
interface FrequencyAnalysisEvent {
  type: 'analysis:frequency'
  payload: {
    timestamp: number
    spectrum: Array<{
      frequency: number
      magnitude: number
    }>
    peaks: Array<{
      frequency: number
      magnitude: number
      q: number
    }>
    ultrasonicActivity: {
      detected: boolean
      frequencies: number[]
      strength: number
    }
  }
}
```

### Quality Metrics
```typescript
interface QualityMetricsEvent {
  type: 'analysis:quality'
  payload: {
    timestamp: number
    snr: number              // Signal-to-noise ratio
    dynamicRange: number     // dB
    distortion: number       // THD percentage
    clarity: number          // 0-1 subjective clarity
    recommendation: 'excellent' | 'good' | 'fair' | 'poor'
  }
}
```

## System Events

### Performance Metrics
```typescript
interface PerformanceMetricsEvent {
  type: 'system:performance'
  payload: {
    cpu: number              // CPU usage percentage
    memory: number           // Memory usage MB
    latency: number          // Processing latency ms
    queueLength: number      // Processing queue length
    throughput: number       // Samples per second
  }
}
```

### Server Notifications
```typescript
interface ServerNotificationEvent {
  type: 'system:notification'
  payload: {
    level: 'info' | 'warning' | 'error'
    message: string
    action?: {
      type: string
      label: string
      data?: any
    }
  }
}
```

## Error Events

### Connection Errors
```typescript
interface ConnectionErrorEvent {
  type: 'error:connection'
  payload: {
    code: number
    reason: string
    willReconnect: boolean
    nextAttemptIn?: number   // milliseconds
  }
}
```

### Processing Errors
```typescript
interface ProcessingErrorEvent {
  type: 'error:processing'
  payload: {
    operation: 'encoding' | 'decoding' | 'analysis'
    code: string
    message: string
    details?: any
    timestamp: number
    recoverable: boolean
  }
}
```

## Event Handling Implementation

### Event Handler Registry
```typescript
class EventHandlerRegistry {
  private handlers: Map<string, Set<EventHandler>> = new Map()
  
  on(eventType: string, handler: EventHandler): () => void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set())
    }
    
    this.handlers.get(eventType)!.add(handler)
    
    // Return unsubscribe function
    return () => {
      this.handlers.get(eventType)?.delete(handler)
    }
  }
  
  emit(event: WebSocketMessage): void {
    const handlers = this.handlers.get(event.type)
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(event)
        } catch (error) {
          console.error(`Error in handler for ${event.type}:`, error)
        }
      })
    }
    
    // Also emit to wildcard handlers
    const wildcardHandlers = this.handlers.get('*')
    if (wildcardHandlers) {
      wildcardHandlers.forEach(handler => handler(event))
    }
  }
}
```

### React Hook for WebSocket Events
```typescript
// hooks/useWebSocketEvent.ts
export function useWebSocketEvent<T = any>(
  eventType: string,
  handler: (payload: T) => void,
  deps: DependencyList = []
) {
  const wsService = useWebSocketService()
  
  useEffect(() => {
    const unsubscribe = wsService.on(eventType, (event: WebSocketMessage<T>) => {
      handler(event.payload)
    })
    
    return unsubscribe
  }, [eventType, ...deps])
}

// Usage example
function EncodingProgress() {
  const [progress, setProgress] = useState(0)
  
  useWebSocketEvent<EncodingProgressEvent['payload']>(
    'encoding:progress',
    (payload) => {
      setProgress((payload.processedSamples / payload.totalSamples) * 100)
    }
  )
  
  return <ProgressBar value={progress} />
}
```

## Debugging and Monitoring

### Event Logger
```typescript
class WebSocketEventLogger {
  private events: WebSocketMessage[] = []
  private maxEvents = 1000
  
  log(event: WebSocketMessage): void {
    this.events.push({
      ...event,
      loggedAt: Date.now()
    })
    
    if (this.events.length > this.maxEvents) {
      this.events.shift()
    }
    
    if (process.env.NODE_ENV === 'development') {
      console.log(`[WS ${event.type}]`, event.payload)
    }
  }
  
  getEvents(filter?: {
    type?: string
    since?: number
    limit?: number
  }): WebSocketMessage[] {
    let filtered = this.events
    
    if (filter?.type) {
      filtered = filtered.filter(e => e.type === filter.type)
    }
    
    if (filter?.since) {
      filtered = filtered.filter(e => e.timestamp > filter.since)
    }
    
    if (filter?.limit) {
      filtered = filtered.slice(-filter.limit)
    }
    
    return filtered
  }
}
```

### Chrome DevTools Integration
```typescript
// Expose WebSocket events to DevTools
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  (window as any).__ULTRASONIC_WS_EVENTS__ = {
    logger: eventLogger,
    registry: eventRegistry,
    getStats: () => ({
      connected: wsManager.isConnected(),
      eventsReceived: eventLogger.getEvents().length,
      eventTypes: Array.from(eventRegistry.handlers.keys()),
      uptime: wsManager.getUptime()
    })
  }
}
```

## Best Practices

### Event Naming Convention
- Use namespace:action format (e.g., `encoding:start`)
- Keep event names consistent and descriptive
- Use present tense for actions, past tense for results

### Payload Design
- Keep payloads minimal but complete
- Use consistent property names across events
- Include timestamps for time-sensitive data
- Provide units for all measurements

### Error Handling
- Always include error details in error events
- Indicate if errors are recoverable
- Provide actionable error messages
- Include correlation IDs for debugging

### Performance Considerations
- Batch small updates when possible
- Use binary format for audio data
- Implement message compression for large payloads
- Throttle high-frequency events client-side