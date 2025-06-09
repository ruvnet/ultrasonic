import { useEffect, useCallback, useRef, useState } from 'react'
import { WebSocketManager, WebSocketState, getWebSocketManager } from '@/lib/api/websocket'
import { useAuthStore } from '@/stores/auth-store'

export interface UseWebSocketOptions {
  autoConnect?: boolean
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: Error) => void
  onReconnect?: (attempt: number) => void
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const { autoConnect = true, onConnect, onDisconnect, onError, onReconnect } = options
  const [state, setState] = useState<WebSocketState>(WebSocketState.DISCONNECTED)
  const [isConnected, setIsConnected] = useState(false)
  const wsManager = useRef<WebSocketManager>(getWebSocketManager())
  const token = useAuthStore(state => state.token)

  useEffect(() => {
    const ws = wsManager.current

    const handleStateChange = ({ newState }: { oldState: WebSocketState, newState: WebSocketState }) => {
      setState(newState)
      setIsConnected(newState === WebSocketState.CONNECTED)
    }

    const handleConnect = () => {
      onConnect?.()
    }

    const handleDisconnect = () => {
      onDisconnect?.()
    }

    const handleError = (error: Error) => {
      onError?.(error)
    }

    const handleReconnect = ({ attempt }: { attempt: number }) => {
      onReconnect?.(attempt)
    }

    // Subscribe to events
    ws.on('stateChange', handleStateChange)
    ws.on('connected', handleConnect)
    ws.on('disconnected', handleDisconnect)
    ws.on('error', handleError)
    ws.on('reconnecting', handleReconnect)

    // Set initial state
    setState(ws.getState())
    setIsConnected(ws.isConnected())

    // Auto-connect if enabled
    if (autoConnect && !ws.isConnected() && token) {
      ws.connect(token).catch(console.error)
    }

    return () => {
      ws.off('stateChange', handleStateChange)
      ws.off('connected', handleConnect)
      ws.off('disconnected', handleDisconnect)
      ws.off('error', handleError)
      ws.off('reconnecting', handleReconnect)
    }
  }, [autoConnect, token, onConnect, onDisconnect, onError, onReconnect])

  const connect = useCallback(async () => {
    try {
      await wsManager.current.connect(token)
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      throw error
    }
  }, [token])

  const disconnect = useCallback(() => {
    wsManager.current.disconnect()
  }, [])

  const send = useCallback((event: string, data: any) => {
    wsManager.current.send(event, data)
  }, [])

  const sendBinary = useCallback((data: ArrayBuffer | Blob) => {
    wsManager.current.sendBinary(data)
  }, [])

  return {
    state,
    isConnected,
    connect,
    disconnect,
    send,
    sendBinary,
    wsManager: wsManager.current
  }
}

// Hook for subscribing to specific WebSocket events
export function useWebSocketEvent<T = any>(
  event: string,
  handler: (data: T) => void,
  deps: React.DependencyList = []
) {
  const wsManager = useRef<WebSocketManager>(getWebSocketManager())

  useEffect(() => {
    const ws = wsManager.current
    
    const eventHandler = (data: T) => {
      handler(data)
    }

    ws.on(event, eventHandler)

    return () => {
      ws.off(event, eventHandler)
    }
  }, [event, ...deps])
}

// Hook for real-time encoding progress
export function useEncodingProgress() {
  const [progress, setProgress] = useState<{
    percentage: number
    stage: string
    estimatedTime?: number
  } | null>(null)

  useWebSocketEvent('encoding:progress', (data) => {
    setProgress(data)
  })

  useWebSocketEvent('encoding:complete', () => {
    setProgress(null)
  })

  useWebSocketEvent('encoding:error', () => {
    setProgress(null)
  })

  return progress
}

// Hook for real-time decoding progress
export function useDecodingProgress() {
  const [progress, setProgress] = useState<{
    percentage: number
    stage: string
    frequency?: number
    signalStrength?: number
  } | null>(null)

  useWebSocketEvent('decoding:progress', (data) => {
    setProgress(data)
  })

  useWebSocketEvent('decoding:complete', () => {
    setProgress(null)
  })

  useWebSocketEvent('decoding:error', () => {
    setProgress(null)
  })

  return progress
}

// Hook for real-time signal analysis
export function useSignalAnalysis() {
  const [analysis, setAnalysis] = useState<{
    frequencies: number[]
    amplitudes: number[]
    ultrasonic: {
      detected: boolean
      frequency: number
      strength: number
    }
  } | null>(null)

  useWebSocketEvent('signal:analysis', (data) => {
    setAnalysis(data)
  })

  return analysis
}

// Hook for system performance metrics
export function useSystemMetrics() {
  const [metrics, setMetrics] = useState<{
    cpu: number
    memory: number
    activeConnections: number
    processingQueue: number
  } | null>(null)

  useWebSocketEvent('system:metrics', (data) => {
    setMetrics(data)
  })

  return metrics
}