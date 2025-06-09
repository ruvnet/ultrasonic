import React, { useEffect, ReactNode } from 'react'
import { useWebSocket, useWebSocketEvent } from '@/hooks/useWebSocket'
import { useWebSocketStore } from '@/stores/websocketStore'
import { useAuthStore } from '@/stores/auth-store'
import { useEncodingStore } from '@/stores/encodingStore'
import { useDecodingStore } from '@/stores/decodingStore'
import { useUIStore } from '@/stores/uiStore'

interface WebSocketProviderProps {
  children: ReactNode
}

export function WebSocketProvider({ children }: WebSocketProviderProps) {
  const { isConnected, connect, disconnect } = useWebSocket({
    autoConnect: false,
    onConnect: () => {
      console.log('WebSocket connected')
      useUIStore.getState().addNotification({
        type: 'success',
        title: 'Connected',
        message: 'Real-time connection established'
      })
    },
    onDisconnect: () => {
      console.log('WebSocket disconnected')
    },
    onError: (error) => {
      console.error('WebSocket error:', error)
      useUIStore.getState().addNotification({
        type: 'error',
        title: 'Connection Error',
        message: error.message
      })
    },
    onReconnect: (attempt) => {
      console.log(`WebSocket reconnecting... Attempt ${attempt}`)
    }
  })

  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  const autoReconnect = useWebSocketStore(state => state.autoReconnect)

  // Connect when authenticated
  useEffect(() => {
    if (isAuthenticated && autoReconnect && !isConnected) {
      connect().catch(console.error)
    } else if (!isAuthenticated && isConnected) {
      disconnect()
    }
  }, [isAuthenticated, autoReconnect, isConnected, connect, disconnect])

  // Handle encoding events
  useWebSocketEvent('encoding:progress', (data: {
    taskId: string
    percentage: number
    stage: string
    estimatedTime?: number
  }) => {
    useEncodingStore.getState().updateProgress(data.percentage, data.stage)
  })

  useWebSocketEvent('encoding:complete', (data: {
    taskId: string
    result: {
      outputUrl: string
      messageSize: number
      capacity: number
      settings: any
    }
  }) => {
    const { result } = data
    useEncodingStore.getState().setResult({
      audioUrl: result.outputUrl,
      messageSize: result.messageSize,
      capacity: result.capacity,
      settings: result.settings
    })
    
    useUIStore.getState().addNotification({
      type: 'success',
      title: 'Encoding Complete',
      message: 'Your message has been successfully embedded'
    })
  })

  useWebSocketEvent('encoding:error', (data: {
    taskId: string
    error: string
    code?: string
  }) => {
    useEncodingStore.getState().setError(new Error(data.error))
    
    useUIStore.getState().addNotification({
      type: 'error',
      title: 'Encoding Failed',
      message: data.error
    })
  })

  // Handle decoding events
  useWebSocketEvent('decoding:progress', (data: {
    taskId: string
    percentage: number
    stage: string
    frequency?: number
    signalStrength?: number
  }) => {
    useDecodingStore.getState().updateProgress(data.percentage, data.stage)
    
    if (data.frequency && data.signalStrength) {
      useDecodingStore.getState().updateSignalAnalysis({
        frequency: data.frequency,
        strength: data.signalStrength,
        detected: true
      })
    }
  })

  useWebSocketEvent('decoding:complete', (data: {
    taskId: string
    results: Array<{
      message: string
      confidence: number
      position: number
      metadata: any
    }>
  }) => {
    const { results } = data
    results.forEach(result => {
      useDecodingStore.getState().addResult({
        message: result.message,
        confidence: result.confidence,
        timestamp: new Date(),
        position: result.position,
        metadata: result.metadata
      })
    })
    
    useUIStore.getState().addNotification({
      type: 'success',
      title: 'Decoding Complete',
      message: `Found ${results.length} message(s)`
    })
  })

  useWebSocketEvent('decoding:error', (data: {
    taskId: string
    error: string
    code?: string
  }) => {
    useDecodingStore.getState().setError(new Error(data.error))
    
    useUIStore.getState().addNotification({
      type: 'error',
      title: 'Decoding Failed',
      message: data.error
    })
  })

  // Handle real-time audio streaming
  useWebSocketEvent('audio:chunk', (data: {
    taskId: string
    chunk: ArrayBuffer
    timestamp: number
  }) => {
    // Handle audio chunk for real-time processing
    console.log('Received audio chunk:', data.timestamp)
  })

  // Handle system events
  useWebSocketEvent('system:broadcast', (data: {
    type: string
    message: string
    severity: 'info' | 'warning' | 'error'
  }) => {
    useUIStore.getState().addNotification({
      type: data.severity === 'error' ? 'error' : data.severity === 'warning' ? 'warning' : 'info',
      title: 'System Message',
      message: data.message
    })
  })

  return <>{children}</>
}