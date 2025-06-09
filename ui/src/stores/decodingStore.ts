import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'
import { apiClient } from '@/lib/api/client'

export interface DecodingSettings {
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

export interface DecodingResult {
  id: string
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
  timestamp: string
}

export interface DecodingHistoryItem extends DecodingResult {
  fileName: string
  fileSize: number
}

interface DecodingState {
  // Settings
  settings: DecodingSettings
  
  // Operation state
  isDecoding: boolean
  progress: number
  currentFile: File | null
  
  // Results
  lastResults: DecodingResult[]
  history: DecodingHistoryItem[]
  
  // Analysis
  signalAnalysis: {
    hasSignal: boolean
    frequencies: number[]
    strength: number
    quality: string
  } | null
  
  // Actions
  updateSettings: (settings: Partial<DecodingSettings>) => void
  decode: (audioFile: File) => Promise<DecodingResult[]>
  analyze: (audioFile: File) => Promise<void>
  saveToHistory: (results: DecodingResult[], file: File) => void
  clearHistory: () => void
  removeFromHistory: (id: string) => void
}

const defaultSettings: DecodingSettings = {
  detectionSensitivity: 'medium',
  minSignalStrength: 0.3,
  windowSize: 2048,
  hopSize: 512,
  smoothing: 0.5,
  errorTolerance: 0.3,
  maxRetries: 3,
  decryption: false,
  parallelProcessing: true,
  gpuAcceleration: false
}

export const useDecodingStore = create<DecodingState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Initial state
        settings: defaultSettings,
        isDecoding: false,
        progress: 0,
        currentFile: null,
        lastResults: [],
        history: [],
        signalAnalysis: null,
        
        // Actions
        updateSettings: (newSettings: Partial<DecodingSettings>) => {
          set(state => {
            state.settings = { ...state.settings, ...newSettings }
          })
        },
        
        decode: async (audioFile: File) => {
          set(state => {
            state.isDecoding = true
            state.progress = 0
            state.currentFile = audioFile
            state.lastResults = []
          })
          
          try {
            // Simulate progress updates
            const progressInterval = setInterval(() => {
              set(state => {
                if (state.progress < 90) {
                  state.progress = Math.min(state.progress + 15, 90)
                }
              })
            }, 300)
            
            // Call the API
            const response = await apiClient.decodeAudio({
              file: audioFile,
              detailedAnalysis: true
            })
            
            clearInterval(progressInterval)
            
            // Process the response
            let results: DecodingResult[] = []
            
            if (response.command) {
              const result: DecodingResult = {
                id: Date.now().toString(),
                message: response.command,
                confidence: response.analysis?.confidence || 0.9,
                metadata: {
                  detectedAt: 0,
                  endAt: response.analysis?.duration || 0,
                  frequency: response.analysis?.detected_frequency || 19000,
                  bitRate: 50,
                  errorsCorrected: 0,
                  encrypted: false,
                  signalQuality: response.analysis?.signal_quality || 'good'
                },
                warnings: response.analysis?.warnings,
                timestamp: new Date().toISOString()
              }
              results = [result]
            }
            
            set(state => {
              state.progress = 100
              state.lastResults = results
              state.isDecoding = false
              
              // Update signal analysis if available
              if (response.analysis) {
                state.signalAnalysis = {
                  hasSignal: response.success || false,
                  frequencies: response.analysis.frequency_analysis?.peaks || [],
                  strength: response.analysis.signal_strength || 0,
                  quality: response.analysis.signal_quality || 'unknown'
                }
              }
            })
            
            // Save to history if we found messages
            if (results.length > 0) {
              get().saveToHistory(results, audioFile)
            }
            
            return results
          } catch (error) {
            set(state => {
              state.isDecoding = false
              state.progress = 0
              state.currentFile = null
            })
            throw error
          }
        },
        
        analyze: async (audioFile: File) => {
          set(state => {
            state.isDecoding = true
            state.progress = 0
            state.currentFile = audioFile
          })
          
          try {
            const response = await apiClient.analyzeAudio({
              file: audioFile
            })
            
            set(state => {
              state.progress = 100
              state.isDecoding = false
              state.signalAnalysis = {
                hasSignal: response.has_ultrasonic_content || false,
                frequencies: response.frequency_analysis?.peaks || [],
                strength: response.signal_strength || 0,
                quality: response.signal_quality || 'unknown'
              }
            })
          } catch (error) {
            set(state => {
              state.isDecoding = false
              state.progress = 0
              state.currentFile = null
            })
            throw error
          }
        },
        
        saveToHistory: (results: DecodingResult[], file: File) => {
          set(state => {
            const historyItems: DecodingHistoryItem[] = results.map(result => ({
              ...result,
              fileName: file.name,
              fileSize: file.size
            }))
            
            state.history.unshift(...historyItems)
            
            // Keep only last 50 items
            if (state.history.length > 50) {
              state.history = state.history.slice(0, 50)
            }
          })
        },
        
        clearHistory: () => {
          set(state => {
            state.history = []
          })
        },
        
        removeFromHistory: (id: string) => {
          set(state => {
            state.history = state.history.filter(item => item.id !== id)
          })
        }
      })),
      {
        name: 'decoding-store',
        partialize: (state) => ({
          settings: state.settings,
          history: state.history
        })
      }
    ),
    { name: 'decoding-store' }
  )
)