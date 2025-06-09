import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'
import { apiClient } from '@/lib/api/client'

export interface EncodingSettings {
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

export interface EncodingPreset {
  id: string
  name: string
  description: string
  settings: EncodingSettings
}

export interface EncodingResult {
  id: string
  outputUrl: string
  downloadUrl: string
  metadata: {
    originalFileName: string
    outputFileName: string
    fileSize: number
    duration: number
    messageLength: number
    encodingTime: number
    settings: EncodingSettings
  }
  timestamp: string
}

export interface EncodingHistoryItem extends EncodingResult {
  message: string
}

interface EncodingState {
  // Settings
  settings: EncodingSettings
  presets: EncodingPreset[]
  
  // Operation state
  message: string
  isEncoding: boolean
  progress: number
  
  // Results
  lastResult: EncodingResult | null
  history: EncodingHistoryItem[]
  
  // Actions
  setMessage: (message: string) => void
  updateSettings: (settings: Partial<EncodingSettings>) => void
  loadPreset: (presetId: string) => void
  encode: (audioFile: File) => Promise<EncodingResult>
  saveToHistory: (result: EncodingResult) => void
  clearHistory: () => void
  removeFromHistory: (id: string) => void
}

const defaultSettings: EncodingSettings = {
  baseFrequency: 19000,
  frequencyRange: 3000,
  bitDuration: 20,
  guardInterval: 10,
  amplitude: 0.8,
  fadeInDuration: 100,
  fadeOutDuration: 100,
  errorCorrection: 'basic',
  redundancy: 2,
  encryption: false,
  compressionLevel: 5,
  adaptiveBitrate: false
}

const defaultPresets: EncodingPreset[] = [
  {
    id: 'quick',
    name: 'Quick & Simple',
    description: 'Fast encoding with minimal error correction',
    settings: {
      ...defaultSettings,
      baseFrequency: 19000,
      frequencyRange: 2000,
      bitDuration: 15,
      amplitude: 0.9,
      errorCorrection: 'none',
      redundancy: 1,
      encryption: false,
      compressionLevel: 3
    }
  },
  {
    id: 'balanced',
    name: 'Balanced',
    description: 'Good balance between speed and reliability',
    settings: {
      ...defaultSettings,
      baseFrequency: 19000,
      frequencyRange: 3000,
      bitDuration: 20,
      amplitude: 0.8,
      errorCorrection: 'basic',
      redundancy: 2,
      encryption: false,
      compressionLevel: 5
    }
  },
  {
    id: 'robust',
    name: 'Robust',
    description: 'Maximum reliability with advanced error correction',
    settings: {
      ...defaultSettings,
      baseFrequency: 20000,
      frequencyRange: 4000,
      bitDuration: 30,
      amplitude: 0.7,
      errorCorrection: 'advanced',
      redundancy: 3,
      encryption: true,
      compressionLevel: 7
    }
  }
]

export const useEncodingStore = create<EncodingState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Default settings
        settings: defaultSettings,
        presets: defaultPresets,
        message: '',
        isEncoding: false,
        progress: 0,
        lastResult: null,
        history: [],
        
        // Actions
        setMessage: (message: string) => {
          set(state => {
            state.message = message
          })
        },
        
        updateSettings: (newSettings: Partial<EncodingSettings>) => {
          set(state => {
            state.settings = { ...state.settings, ...newSettings }
          })
        },
        
        loadPreset: (presetId: string) => {
          const preset = get().presets.find(p => p.id === presetId)
          if (preset) {
            set(state => {
              state.settings = { ...preset.settings }
            })
          }
        },
        
        encode: async (audioFile: File) => {
          const { message, settings } = get()
          
          if (!message) {
            throw new Error('No message to encode')
          }
          
          set(state => {
            state.isEncoding = true
            state.progress = 0
          })
          
          try {
            // Simulate progress updates
            const progressInterval = setInterval(() => {
              set(state => {
                if (state.progress < 90) {
                  state.progress = Math.min(state.progress + 10, 90)
                }
              })
            }, 200)
            
            // Call the API
            const response = await apiClient.embedAudio({
              audioFile,
              command: message,
              obfuscate: settings.encryption,
              bitrate: `${Math.round(1000 / settings.bitDuration)}k`,
              ultrasonicFreq: settings.baseFrequency,
              amplitude: settings.amplitude
            })
            
            clearInterval(progressInterval)
            
            // Create result object
            const result: EncodingResult = {
              id: Date.now().toString(),
              outputUrl: response.outputUrl || '',
              downloadUrl: response.downloadUrl || '',
              metadata: {
                originalFileName: audioFile.name,
                outputFileName: `encoded_${audioFile.name}`,
                fileSize: audioFile.size,
                duration: 0, // Would need to be calculated from audio
                messageLength: message.length,
                encodingTime: Date.now(),
                settings: { ...settings }
              },
              timestamp: new Date().toISOString()
            }
            
            set(state => {
              state.progress = 100
              state.lastResult = result
              state.isEncoding = false
            })
            
            // Save to history
            get().saveToHistory(result)
            
            return result
          } catch (error) {
            set(state => {
              state.isEncoding = false
              state.progress = 0
            })
            throw error
          }
        },
        
        saveToHistory: (result: EncodingResult) => {
          const message = get().message
          set(state => {
            state.history.unshift({
              ...result,
              message
            })
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
        name: 'encoding-store',
        partialize: (state) => ({
          settings: state.settings,
          history: state.history
        })
      }
    ),
    { name: 'encoding-store' }
  )
)