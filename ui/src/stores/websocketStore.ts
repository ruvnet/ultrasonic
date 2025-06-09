import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'
import { WebSocketState } from '@/lib/api/websocket'

interface WebSocketStore {
  // State
  connectionState: WebSocketState
  reconnectAttempts: number
  lastError: Error | null
  lastConnected: Date | null
  messageHistory: Array<{
    event: string
    data: any
    timestamp: Date
    direction: 'sent' | 'received'
  }>
  
  // Settings
  autoReconnect: boolean
  maxHistorySize: number
  
  // Actions
  setConnectionState: (state: WebSocketState) => void
  setReconnectAttempts: (attempts: number) => void
  setLastError: (error: Error | null) => void
  setLastConnected: (date: Date | null) => void
  addMessage: (event: string, data: any, direction: 'sent' | 'received') => void
  clearMessageHistory: () => void
  setAutoReconnect: (enabled: boolean) => void
  
  // Computed
  isConnected: () => boolean
  isConnecting: () => boolean
  isReconnecting: () => boolean
  hasError: () => boolean
}

export const useWebSocketStore = create<WebSocketStore>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    connectionState: WebSocketState.DISCONNECTED,
    reconnectAttempts: 0,
    lastError: null,
    lastConnected: null,
    messageHistory: [],
    autoReconnect: true,
    maxHistorySize: 100,
    
    // Actions
    setConnectionState: (state) => set({ connectionState: state }),
    
    setReconnectAttempts: (attempts) => set({ reconnectAttempts: attempts }),
    
    setLastError: (error) => set({ lastError: error }),
    
    setLastConnected: (date) => set({ lastConnected: date }),
    
    addMessage: (event, data, direction) => set((state) => {
      const message = {
        event,
        data,
        timestamp: new Date(),
        direction
      }
      
      const history = [...state.messageHistory, message]
      
      // Limit history size
      if (history.length > state.maxHistorySize) {
        history.splice(0, history.length - state.maxHistorySize)
      }
      
      return { messageHistory: history }
    }),
    
    clearMessageHistory: () => set({ messageHistory: [] }),
    
    setAutoReconnect: (enabled) => set({ autoReconnect: enabled }),
    
    // Computed
    isConnected: () => get().connectionState === WebSocketState.CONNECTED,
    isConnecting: () => get().connectionState === WebSocketState.CONNECTING,
    isReconnecting: () => get().connectionState === WebSocketState.RECONNECTING,
    hasError: () => get().connectionState === WebSocketState.ERROR
  }))
)

// Selectors for common use cases
export const selectConnectionState = (state: WebSocketStore) => state.connectionState
export const selectIsConnected = (state: WebSocketStore) => state.isConnected()
export const selectReconnectInfo = (state: WebSocketStore) => ({
  attempts: state.reconnectAttempts,
  isReconnecting: state.isReconnecting()
})
export const selectLastError = (state: WebSocketStore) => state.lastError
export const selectMessageHistory = (state: WebSocketStore) => state.messageHistory

// Subscribe to WebSocket manager events and sync with store
import { getWebSocketManager } from '@/lib/api/websocket'

const wsManager = getWebSocketManager()

// Sync WebSocket events with store
wsManager.on('stateChange', ({ newState }: { newState: WebSocketState }) => {
  useWebSocketStore.getState().setConnectionState(newState)
})

wsManager.on('connected', () => {
  const state = useWebSocketStore.getState()
  state.setLastConnected(new Date())
  state.setReconnectAttempts(0)
  state.setLastError(null)
})

wsManager.on('error', (error: Error) => {
  useWebSocketStore.getState().setLastError(error)
})

wsManager.on('reconnecting', ({ attempt }: { attempt: number }) => {
  useWebSocketStore.getState().setReconnectAttempts(attempt)
})

wsManager.on('message', (message: { event: string; data: any }) => {
  useWebSocketStore.getState().addMessage(message.event, message.data, 'received')
})

wsManager.on('messageSent', (message: { event: string; data: any }) => {
  useWebSocketStore.getState().addMessage(message.event, message.data, 'sent')
})