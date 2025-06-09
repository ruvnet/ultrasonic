# Error Handling Strategies

## Overview
This document defines comprehensive error handling strategies for the Ultrasonic-Agentics UI, ensuring graceful error recovery and user-friendly error messages.

## Error Classification

### Error Categories
```typescript
// types/errors.types.ts

export enum ErrorCategory {
  // Network errors
  NETWORK = 'NETWORK',
  
  // API errors
  API = 'API',
  
  // Audio processing errors
  AUDIO = 'AUDIO',
  
  // Encoding/Decoding errors
  ENCODING = 'ENCODING',
  DECODING = 'DECODING',
  
  // File handling errors
  FILE = 'FILE',
  
  // Browser/Permission errors
  BROWSER = 'BROWSER',
  
  // Validation errors
  VALIDATION = 'VALIDATION',
  
  // System errors
  SYSTEM = 'SYSTEM'
}

export interface AppError extends Error {
  category: ErrorCategory
  code: string
  userMessage: string
  technicalDetails?: any
  recoverable: boolean
  retry?: () => Promise<any>
  timestamp: number
  requestId?: string
}
```

## Error Handlers

### Global Error Boundary
```typescript
// components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react'
import { logError } from '@/services/errorLogging'

interface Props {
  children: ReactNode
  fallback?: (error: Error, reset: () => void) => ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to monitoring service
    logError({
      error,
      errorInfo,
      context: 'ErrorBoundary',
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    })
  }

  reset = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.reset)
      }

      return <DefaultErrorFallback error={this.state.error} reset={this.reset} />
    }

    return this.props.children
  }
}

function DefaultErrorFallback({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <XCircle className="h-12 w-12 text-red-500" />
          </div>
          <div className="ml-4">
            <h3 className="text-lg font-medium text-gray-900">
              Something went wrong
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {error.message || 'An unexpected error occurred'}
            </p>
          </div>
        </div>
        
        <div className="mt-6 flex space-x-3">
          <Button onClick={reset} variant="primary">
            Try Again
          </Button>
          <Button onClick={() => window.location.href = '/'} variant="secondary">
            Go Home
          </Button>
        </div>
        
        {process.env.NODE_ENV === 'development' && (
          <details className="mt-6">
            <summary className="cursor-pointer text-sm text-gray-500">
              Error Details
            </summary>
            <pre className="mt-2 text-xs bg-gray-100 p-2 rounded overflow-auto">
              {error.stack}
            </pre>
          </details>
        )}
      </div>
    </div>
  )
}
```

### API Error Handler
```typescript
// services/errorHandlers/apiErrorHandler.ts

export class ApiErrorHandler {
  static handle(error: AxiosError): AppError {
    const baseError: Partial<AppError> = {
      category: ErrorCategory.API,
      timestamp: Date.now(),
      recoverable: true
    }

    if (!error.response) {
      // Network error
      return {
        ...baseError,
        name: 'NetworkError',
        code: 'NETWORK_ERROR',
        message: error.message,
        userMessage: 'Unable to connect to the server. Please check your internet connection.',
        category: ErrorCategory.NETWORK
      } as AppError
    }

    const { status, data } = error.response
    
    switch (status) {
      case 400:
        return this.handleBadRequest(data, baseError)
      case 401:
        return this.handleUnauthorized(data, baseError)
      case 403:
        return this.handleForbidden(data, baseError)
      case 404:
        return this.handleNotFound(data, baseError)
      case 422:
        return this.handleValidationError(data, baseError)
      case 429:
        return this.handleRateLimit(data, baseError)
      case 500:
      case 502:
      case 503:
        return this.handleServerError(data, baseError)
      default:
        return this.handleUnknownError(error, baseError)
    }
  }

  private static handleBadRequest(data: any, baseError: Partial<AppError>): AppError {
    return {
      ...baseError,
      name: 'BadRequestError',
      code: data.error?.code || 'BAD_REQUEST',
      message: data.error?.message || 'Invalid request',
      userMessage: 'The request could not be processed. Please check your input and try again.',
      technicalDetails: data.error?.details
    } as AppError
  }

  private static handleValidationError(data: any, baseError: Partial<AppError>): AppError {
    const errors = data.errors || []
    const userMessage = errors.length > 0
      ? `Please fix the following errors: ${errors.map((e: any) => e.message).join(', ')}`
      : 'Please check your input and try again.'

    return {
      ...baseError,
      name: 'ValidationError',
      code: 'VALIDATION_ERROR',
      message: 'Validation failed',
      userMessage,
      category: ErrorCategory.VALIDATION,
      technicalDetails: { errors }
    } as AppError
  }

  private static handleRateLimit(data: any, baseError: Partial<AppError>): AppError {
    const retryAfter = data.retryAfter || 60
    
    return {
      ...baseError,
      name: 'RateLimitError',
      code: 'RATE_LIMITED',
      message: 'Rate limit exceeded',
      userMessage: `Too many requests. Please try again in ${retryAfter} seconds.`,
      recoverable: true,
      technicalDetails: { retryAfter }
    } as AppError
  }

  private static handleServerError(data: any, baseError: Partial<AppError>): AppError {
    return {
      ...baseError,
      name: 'ServerError',
      code: data.error?.code || 'SERVER_ERROR',
      message: data.error?.message || 'Internal server error',
      userMessage: 'The server encountered an error. Our team has been notified. Please try again later.',
      recoverable: false,
      category: ErrorCategory.SYSTEM
    } as AppError
  }
}
```

### Audio Error Handler
```typescript
// services/errorHandlers/audioErrorHandler.ts

export class AudioErrorHandler {
  static handle(error: Error, context: AudioErrorContext): AppError {
    const baseError: Partial<AppError> = {
      category: ErrorCategory.AUDIO,
      timestamp: Date.now(),
      technicalDetails: { context }
    }

    if (error.name === 'NotAllowedError') {
      return this.handlePermissionError(error, baseError)
    }

    if (error.name === 'NotFoundError') {
      return this.handleDeviceNotFound(error, baseError)
    }

    if (error.message.includes('AudioContext')) {
      return this.handleAudioContextError(error, baseError)
    }

    if (error.message.includes('decode')) {
      return this.handleDecodeError(error, baseError)
    }

    return this.handleGenericAudioError(error, baseError)
  }

  private static handlePermissionError(error: Error, baseError: Partial<AppError>): AppError {
    return {
      ...baseError,
      name: 'AudioPermissionError',
      code: 'AUDIO_PERMISSION_DENIED',
      message: error.message,
      userMessage: 'Microphone access is required. Please grant permission and try again.',
      category: ErrorCategory.BROWSER,
      recoverable: true,
      retry: async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        return stream
      }
    } as AppError
  }

  private static handleDecodeError(error: Error, baseError: Partial<AppError>): AppError {
    return {
      ...baseError,
      name: 'AudioDecodeError',
      code: 'AUDIO_DECODE_FAILED',
      message: error.message,
      userMessage: 'Unable to process the audio file. Please ensure it\'s a valid audio format.',
      recoverable: false
    } as AppError
  }

  private static handleAudioContextError(error: Error, baseError: Partial<AppError>): AppError {
    return {
      ...baseError,
      name: 'AudioContextError',
      code: 'AUDIO_CONTEXT_ERROR',
      message: error.message,
      userMessage: 'Audio system initialization failed. Please refresh the page and try again.',
      recoverable: true,
      retry: async () => {
        const audioContext = new AudioContext()
        await audioContext.resume()
        return audioContext
      }
    } as AppError
  }
}

interface AudioErrorContext {
  operation: 'record' | 'play' | 'process' | 'analyze'
  phase?: string
  audioFile?: string
  settings?: any
}
```

### File Error Handler
```typescript
// services/errorHandlers/fileErrorHandler.ts

export class FileErrorHandler {
  static handle(error: Error, file?: File): AppError {
    const baseError: Partial<AppError> = {
      category: ErrorCategory.FILE,
      timestamp: Date.now(),
      technicalDetails: { 
        fileName: file?.name,
        fileSize: file?.size,
        fileType: file?.type
      }
    }

    if (error.message.includes('size')) {
      return this.handleFileSizeError(file, baseError)
    }

    if (error.message.includes('type') || error.message.includes('format')) {
      return this.handleFileTypeError(file, baseError)
    }

    if (error.name === 'NotReadableError') {
      return this.handleFileReadError(error, baseError)
    }

    return this.handleGenericFileError(error, baseError)
  }

  private static handleFileSizeError(file: File | undefined, baseError: Partial<AppError>): AppError {
    const maxSize = 100 * 1024 * 1024 // 100MB
    const fileSize = file?.size || 0
    
    return {
      ...baseError,
      name: 'FileSizeError',
      code: 'FILE_TOO_LARGE',
      message: `File size (${formatBytes(fileSize)}) exceeds maximum allowed size`,
      userMessage: `The file is too large. Maximum size is ${formatBytes(maxSize)}.`,
      recoverable: false
    } as AppError
  }

  private static handleFileTypeError(file: File | undefined, baseError: Partial<AppError>): AppError {
    const allowedTypes = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4']
    
    return {
      ...baseError,
      name: 'FileTypeError',
      code: 'INVALID_FILE_TYPE',
      message: `Invalid file type: ${file?.type}`,
      userMessage: `Please upload a valid audio file. Supported formats: ${allowedTypes.join(', ')}`,
      recoverable: false
    } as AppError
  }
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
```

## Error Recovery Strategies

### Retry Logic
```typescript
// utils/retryLogic.ts

interface RetryOptions {
  maxAttempts?: number
  delay?: number
  backoff?: 'linear' | 'exponential'
  shouldRetry?: (error: Error, attempt: number) => boolean
  onRetry?: (error: Error, attempt: number) => void
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    delay = 1000,
    backoff = 'exponential',
    shouldRetry = () => true,
    onRetry
  } = options

  let lastError: Error

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (attempt === maxAttempts || !shouldRetry(lastError, attempt)) {
        throw lastError
      }

      onRetry?.(lastError, attempt)

      const retryDelay = backoff === 'exponential' 
        ? delay * Math.pow(2, attempt - 1)
        : delay * attempt

      await sleep(retryDelay)
    }
  }

  throw lastError!
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

// Usage example
const fetchData = () => withRetry(
  async () => {
    const response = await api.get('/data')
    return response.data
  },
  {
    maxAttempts: 3,
    delay: 1000,
    backoff: 'exponential',
    shouldRetry: (error, attempt) => {
      // Don't retry on 4xx errors (except 429)
      if (error instanceof ApiError) {
        const status = error.technicalDetails?.status
        return status === 429 || status >= 500
      }
      return true
    },
    onRetry: (error, attempt) => {
      console.log(`Retry attempt ${attempt} after error:`, error.message)
    }
  }
)
```

### Circuit Breaker Pattern
```typescript
// utils/circuitBreaker.ts

enum CircuitState {
  CLOSED = 'CLOSED',
  OPEN = 'OPEN',
  HALF_OPEN = 'HALF_OPEN'
}

export class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED
  private failureCount = 0
  private lastFailureTime: number | null = null
  private successCount = 0

  constructor(
    private readonly threshold: number = 5,
    private readonly timeout: number = 60000, // 1 minute
    private readonly successThreshold: number = 2
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (this.shouldAttemptReset()) {
        this.state = CircuitState.HALF_OPEN
      } else {
        throw new Error('Circuit breaker is OPEN')
      }
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  private onSuccess(): void {
    this.failureCount = 0
    
    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++
      if (this.successCount >= this.successThreshold) {
        this.state = CircuitState.CLOSED
        this.successCount = 0
      }
    }
  }

  private onFailure(): void {
    this.failureCount++
    this.lastFailureTime = Date.now()
    
    if (this.state === CircuitState.HALF_OPEN) {
      this.state = CircuitState.OPEN
      this.successCount = 0
    } else if (this.failureCount >= this.threshold) {
      this.state = CircuitState.OPEN
    }
  }

  private shouldAttemptReset(): boolean {
    return (
      this.lastFailureTime !== null &&
      Date.now() - this.lastFailureTime >= this.timeout
    )
  }

  getState(): CircuitState {
    return this.state
  }
}

// Usage
const apiCircuitBreaker = new CircuitBreaker(5, 60000, 2)

export async function protectedApiCall<T>(
  apiCall: () => Promise<T>
): Promise<T> {
  return apiCircuitBreaker.execute(apiCall)
}
```

## User-Friendly Error Messages

### Error Message Generator
```typescript
// utils/errorMessages.ts

export class ErrorMessageGenerator {
  private static readonly messages: Record<string, (error: AppError) => string> = {
    // Network errors
    NETWORK_ERROR: () => 
      'Unable to connect to the server. Please check your internet connection and try again.',
    TIMEOUT: () => 
      'The request took too long. Please try again.',
    
    // File errors
    FILE_TOO_LARGE: (error) => {
      const maxSize = error.technicalDetails?.maxSize || 100 * 1024 * 1024
      return `The file is too large. Maximum size is ${formatBytes(maxSize)}.`
    },
    INVALID_FILE_TYPE: (error) => {
      const allowedTypes = error.technicalDetails?.allowedTypes || []
      return `Invalid file type. Please upload one of: ${allowedTypes.join(', ')}`
    },
    
    // Audio errors
    AUDIO_PERMISSION_DENIED: () => 
      'Microphone access is required for this feature. Please grant permission in your browser settings.',
    AUDIO_DECODE_FAILED: () => 
      'Unable to process the audio file. Please ensure it\'s a valid, uncorrupted audio file.',
    
    // Encoding/Decoding errors
    ENCODING_FAILED: () => 
      'Failed to encode the message. Please try with different settings or a different audio file.',
    DECODING_FAILED: () => 
      'No message found in the audio file. Please ensure the file contains an encoded message.',
    MESSAGE_TOO_LONG: (error) => {
      const maxLength = error.technicalDetails?.maxLength || 1000
      return `Message is too long. Maximum length is ${maxLength} characters.`
    },
    
    // Validation errors
    VALIDATION_ERROR: (error) => {
      const errors = error.technicalDetails?.errors || []
      if (errors.length === 1) {
        return errors[0].message
      }
      return 'Please fix the following errors:\n' + errors.map((e: any) => `• ${e.message}`).join('\n')
    }
  }

  static generate(error: AppError): string {
    const generator = this.messages[error.code]
    if (generator) {
      return generator(error)
    }
    
    // Fallback to user message or generic message
    return error.userMessage || 'An unexpected error occurred. Please try again.'
  }

  static generateWithContext(error: AppError, context: ErrorContext): string {
    let message = this.generate(error)
    
    // Add context-specific information
    if (context.operation) {
      message = `Error during ${context.operation}: ${message}`
    }
    
    // Add recovery suggestions
    if (error.recoverable && context.showRecoverySuggestions) {
      message += '\n\nSuggestions:'
      message += '\n• Try refreshing the page'
      message += '\n• Check your internet connection'
      message += '\n• Try again in a few moments'
    }
    
    return message
  }
}

interface ErrorContext {
  operation?: string
  showRecoverySuggestions?: boolean
  showTechnicalDetails?: boolean
}
```

### Error Display Components
```typescript
// components/ErrorDisplay.tsx

interface ErrorDisplayProps {
  error: AppError
  onRetry?: () => void
  onDismiss?: () => void
  variant?: 'inline' | 'toast' | 'modal'
}

export function ErrorDisplay({ 
  error, 
  onRetry, 
  onDismiss, 
  variant = 'inline' 
}: ErrorDisplayProps) {
  const message = ErrorMessageGenerator.generate(error)
  
  if (variant === 'toast') {
    return (
      <Toast
        type="error"
        title="Error"
        message={message}
        onDismiss={onDismiss}
        action={error.recoverable && onRetry ? {
          label: 'Retry',
          onClick: onRetry
        } : undefined}
      />
    )
  }
  
  if (variant === 'modal') {
    return (
      <Modal isOpen onClose={onDismiss || (() => {})} title="Error">
        <div className="space-y-4">
          <div className="flex items-start">
            <XCircle className="h-6 w-6 text-red-500 mt-0.5" />
            <p className="ml-3 text-gray-700">{message}</p>
          </div>
          
          {error.recoverable && onRetry && (
            <div className="flex justify-end space-x-3">
              <Button variant="secondary" onClick={onDismiss}>
                Cancel
              </Button>
              <Button variant="primary" onClick={onRetry}>
                Try Again
              </Button>
            </div>
          )}
        </div>
      </Modal>
    )
  }
  
  // Inline variant
  return (
    <div className="rounded-md bg-red-50 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <XCircle className="h-5 w-5 text-red-400" />
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-red-800">
            {error.name || 'Error'}
          </h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{message}</p>
          </div>
          {error.recoverable && onRetry && (
            <div className="mt-4">
              <button
                type="button"
                onClick={onRetry}
                className="text-sm font-medium text-red-600 hover:text-red-500"
              >
                Try again
              </button>
            </div>
          )}
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <button
              onClick={onDismiss}
              className="inline-flex rounded-md bg-red-50 p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 focus:ring-offset-red-50"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
```

## Error Logging and Monitoring

### Error Logger
```typescript
// services/errorLogging.ts

interface ErrorLog {
  error: Error | AppError
  context?: any
  userAgent: string
  timestamp: string
  sessionId: string
  userId?: string
  severity: 'low' | 'medium' | 'high' | 'critical'
}

export class ErrorLogger {
  private static queue: ErrorLog[] = []
  private static batchSize = 10
  private static flushInterval = 5000 // 5 seconds

  static {
    // Start batch processing
    setInterval(() => this.flush(), this.flushInterval)
    
    // Flush on page unload
    if (typeof window !== 'undefined') {
      window.addEventListener('beforeunload', () => this.flush())
    }
  }

  static log(error: Error | AppError, context?: any): void {
    const errorLog: ErrorLog = {
      error: this.sanitizeError(error),
      context,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      sessionId: this.getSessionId(),
      userId: this.getUserId(),
      severity: this.calculateSeverity(error)
    }
    
    this.queue.push(errorLog)
    
    // Immediate flush for critical errors
    if (errorLog.severity === 'critical') {
      this.flush()
    }
    
    // Console log in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[Error Logger]', errorLog)
    }
  }

  private static async flush(): Promise<void> {
    if (this.queue.length === 0) return
    
    const errors = [...this.queue]
    this.queue = []
    
    try {
      await this.sendToMonitoring(errors)
    } catch (error) {
      // Put errors back in queue if sending fails
      this.queue.unshift(...errors)
      console.error('Failed to send error logs:', error)
    }
  }

  private static async sendToMonitoring(errors: ErrorLog[]): Promise<void> {
    // Send to your monitoring service (e.g., Sentry, LogRocket, etc.)
    const response = await fetch('/api/errors/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ errors })
    })
    
    if (!response.ok) {
      throw new Error(`Failed to log errors: ${response.statusText}`)
    }
  }

  private static sanitizeError(error: Error | AppError): any {
    return {
      name: error.name,
      message: error.message,
      stack: error.stack,
      ...(this.isAppError(error) && {
        category: error.category,
        code: error.code,
        userMessage: error.userMessage,
        recoverable: error.recoverable
      })
    }
  }

  private static isAppError(error: any): error is AppError {
    return 'category' in error && 'code' in error
  }

  private static calculateSeverity(error: Error | AppError): ErrorLog['severity'] {
    if (this.isAppError(error)) {
      if (error.category === ErrorCategory.SYSTEM) return 'critical'
      if (error.category === ErrorCategory.API && !error.recoverable) return 'high'
      if (error.category === ErrorCategory.VALIDATION) return 'low'
    }
    
    return 'medium'
  }

  private static getSessionId(): string {
    // Implement session ID retrieval
    return sessionStorage.getItem('sessionId') || 'unknown'
  }

  private static getUserId(): string | undefined {
    // Implement user ID retrieval
    return localStorage.getItem('userId') || undefined
  }
}

// Global error handler
if (typeof window !== 'undefined') {
  window.addEventListener('error', (event) => {
    ErrorLogger.log(event.error || new Error(event.message), {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno
    })
  })
  
  window.addEventListener('unhandledrejection', (event) => {
    ErrorLogger.log(
      new Error(`Unhandled Promise Rejection: ${event.reason}`),
      { reason: event.reason }
    )
  })
}
```

## Error Prevention

### Input Validation
```typescript
// utils/validation.ts

export class ValidationError extends Error {
  constructor(
    public field: string,
    public value: any,
    public rule: string,
    message: string
  ) {
    super(message)
    this.name = 'ValidationError'
  }
}

export class Validator {
  static validateAudioFile(file: File): void {
    const maxSize = 100 * 1024 * 1024 // 100MB
    const allowedTypes = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4']
    
    if (file.size > maxSize) {
      throw new ValidationError(
        'file',
        file,
        'maxSize',
        `File size must be less than ${formatBytes(maxSize)}`
      )
    }
    
    if (!allowedTypes.includes(file.type)) {
      throw new ValidationError(
        'file',
        file,
        'fileType',
        `File type must be one of: ${allowedTypes.join(', ')}`
      )
    }
  }

  static validateEncodingSettings(settings: EncodingSettings): void {
    const errors: ValidationError[] = []
    
    if (settings.baseFrequency < 18000 || settings.baseFrequency > 22050) {
      errors.push(new ValidationError(
        'baseFrequency',
        settings.baseFrequency,
        'range',
        'Base frequency must be between 18000 and 22050 Hz'
      ))
    }
    
    if (settings.amplitude < 0 || settings.amplitude > 1) {
      errors.push(new ValidationError(
        'amplitude',
        settings.amplitude,
        'range',
        'Amplitude must be between 0 and 1'
      ))
    }
    
    if (errors.length > 0) {
      throw new AggregateValidationError(errors)
    }
  }
}

export class AggregateValidationError extends Error {
  constructor(public errors: ValidationError[]) {
    super(`Validation failed: ${errors.length} errors`)
    this.name = 'AggregateValidationError'
  }
}
```

### Defensive Programming
```typescript
// utils/defensive.ts

export function assertDefined<T>(
  value: T | null | undefined,
  message: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message)
  }
}

export function assertType<T>(
  value: any,
  type: string,
  message?: string
): asserts value is T {
  if (typeof value !== type) {
    throw new TypeError(
      message || `Expected ${type} but got ${typeof value}`
    )
  }
}

export function safeExecute<T>(
  fn: () => T,
  fallback: T,
  onError?: (error: Error) => void
): T {
  try {
    return fn()
  } catch (error) {
    onError?.(error as Error)
    return fallback
  }
}

export async function safeExecuteAsync<T>(
  fn: () => Promise<T>,
  fallback: T,
  onError?: (error: Error) => void
): Promise<T> {
  try {
    return await fn()
  } catch (error) {
    onError?.(error as Error)
    return fallback
  }
}
```