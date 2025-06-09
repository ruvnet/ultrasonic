import { create } from 'zustand'
import { devtools, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

interface AudioMetadata {
  fileName: string
  fileSize: number
  duration: number
  sampleRate: number
  channels: number
  format: string
}

interface AudioState {
  // State
  audioContext: AudioContext | null
  currentAudio: {
    buffer: AudioBuffer | null
    url: string | null
    metadata: AudioMetadata | null
  }
  playbackState: {
    isPlaying: boolean
    currentTime: number
    duration: number
    volume: number
    playbackRate: number
  }
  recordingState: {
    isRecording: boolean
    stream: MediaStream | null
    recorder: MediaRecorder | null
    chunks: Blob[]
  }
  devices: {
    inputDeviceId: string | null
    outputDeviceId: string | null
  }
  
  // Actions
  initializeAudio: () => Promise<void>
  loadAudio: (source: string | File) => Promise<void>
  play: () => void
  pause: () => void
  seek: (time: number) => void
  setVolume: (volume: number) => void
  setPlaybackRate: (rate: number) => void
  startRecording: () => Promise<void>
  stopRecording: () => Promise<Blob>
  setAudioInputDevice: (deviceId: string) => void
  setAudioOutputDevice: (deviceId: string) => void
  cleanup: () => void
}

export const useAudioStore = create<AudioState>()(
  devtools(
    subscribeWithSelector(
      immer((set, get) => ({
        // Initial state
        audioContext: null,
        currentAudio: {
          buffer: null,
          url: null,
          metadata: null
        },
        playbackState: {
          isPlaying: false,
          currentTime: 0,
          duration: 0,
          volume: 1,
          playbackRate: 1
        },
        recordingState: {
          isRecording: false,
          stream: null,
          recorder: null,
          chunks: []
        },
        devices: {
          inputDeviceId: null,
          outputDeviceId: null
        },
        
        // Actions
        initializeAudio: async () => {
          if (get().audioContext) return
          
          const context = new (window.AudioContext || (window as any).webkitAudioContext)()
          set(state => {
            state.audioContext = context
          })
        },
        
        loadAudio: async (source) => {
          const context = get().audioContext
          if (!context) {
            await get().initializeAudio()
          }
          
          const audioContext = get().audioContext!
          let arrayBuffer: ArrayBuffer
          let url: string
          
          if (source instanceof File) {
            arrayBuffer = await source.arrayBuffer()
            url = URL.createObjectURL(source)
          } else {
            const response = await fetch(source)
            arrayBuffer = await response.arrayBuffer()
            url = source
          }
          
          const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
          
          set(state => {
            // Clean up previous URL if it was a blob
            if (state.currentAudio.url && state.currentAudio.url.startsWith('blob:')) {
              URL.revokeObjectURL(state.currentAudio.url)
            }
            
            state.currentAudio.buffer = audioBuffer
            state.currentAudio.url = url
            state.currentAudio.metadata = {
              fileName: source instanceof File ? source.name : url.split('/').pop() || 'unknown',
              fileSize: arrayBuffer.byteLength,
              duration: audioBuffer.duration,
              sampleRate: audioBuffer.sampleRate,
              channels: audioBuffer.numberOfChannels,
              format: source instanceof File ? source.type : 'unknown'
            }
            state.playbackState.duration = audioBuffer.duration
            state.playbackState.currentTime = 0
          })
        },
        
        play: () => {
          const { audioContext, currentAudio } = get()
          if (!audioContext || !currentAudio.buffer || get().playbackState.isPlaying) return
          
          set(state => {
            state.playbackState.isPlaying = true
          })
        },
        
        pause: () => {
          set(state => {
            state.playbackState.isPlaying = false
          })
        },
        
        seek: (time: number) => {
          const duration = get().playbackState.duration
          const clampedTime = Math.max(0, Math.min(time, duration))
          
          set(state => {
            state.playbackState.currentTime = clampedTime
          })
        },
        
        setVolume: (volume: number) => {
          const clampedVolume = Math.max(0, Math.min(1, volume))
          
          set(state => {
            state.playbackState.volume = clampedVolume
          })
        },
        
        setPlaybackRate: (rate: number) => {
          const clampedRate = Math.max(0.25, Math.min(4, rate))
          
          set(state => {
            state.playbackState.playbackRate = clampedRate
          })
        },
        
        startRecording: async () => {
          if (get().recordingState.isRecording) return
          
          try {
            const { inputDeviceId } = get().devices
            const constraints: MediaStreamConstraints = {
              audio: inputDeviceId ? { deviceId: inputDeviceId } : true
            }
            
            const stream = await navigator.mediaDevices.getUserMedia(constraints)
            const recorder = new MediaRecorder(stream, {
              mimeType: 'audio/webm;codecs=opus'
            })
            
            const chunks: Blob[] = []
            
            recorder.ondataavailable = (event) => {
              if (event.data.size > 0) {
                chunks.push(event.data)
                set(state => {
                  state.recordingState.chunks = [...chunks]
                })
              }
            }
            
            set(state => {
              state.recordingState.isRecording = true
              state.recordingState.stream = stream
              state.recordingState.recorder = recorder
              state.recordingState.chunks = []
            })
            
            recorder.start(100) // Collect data every 100ms
          } catch (error) {
            console.error('Error starting recording:', error)
            throw error
          }
        },
        
        stopRecording: async () => {
          const { recorder, stream, chunks } = get().recordingState
          
          if (!recorder || !stream) {
            throw new Error('No active recording')
          }
          
          return new Promise<Blob>((resolve) => {
            recorder.onstop = () => {
              const blob = new Blob(chunks, { type: 'audio/webm;codecs=opus' })
              
              // Stop all tracks
              stream.getTracks().forEach(track => track.stop())
              
              set(state => {
                state.recordingState.isRecording = false
                state.recordingState.stream = null
                state.recordingState.recorder = null
                state.recordingState.chunks = []
              })
              
              resolve(blob)
            }
            
            recorder.stop()
          })
        },
        
        setAudioInputDevice: (deviceId: string) => {
          set(state => {
            state.devices.inputDeviceId = deviceId
          })
        },
        
        setAudioOutputDevice: (deviceId: string) => {
          set(state => {
            state.devices.outputDeviceId = deviceId
          })
          
          // Note: Setting output device requires setSinkId API which may not be available
          // This is primarily for tracking the selected device
        },
        
        cleanup: () => {
          const state = get()
          
          // Stop any active recording
          if (state.recordingState.isRecording && state.recordingState.recorder) {
            state.recordingState.recorder.stop()
            state.recordingState.stream?.getTracks().forEach(track => track.stop())
          }
          
          // Clean up audio context
          if (state.audioContext) {
            state.audioContext.close()
          }
          
          // Clean up blob URLs
          if (state.currentAudio.url && state.currentAudio.url.startsWith('blob:')) {
            URL.revokeObjectURL(state.currentAudio.url)
          }
          
          set(state => {
            state.audioContext = null
            state.currentAudio = {
              buffer: null,
              url: null,
              metadata: null
            }
            state.playbackState = {
              isPlaying: false,
              currentTime: 0,
              duration: 0,
              volume: 1,
              playbackRate: 1
            }
            state.recordingState = {
              isRecording: false,
              stream: null,
              recorder: null,
              chunks: []
            }
            state.devices = {
              inputDeviceId: null,
              outputDeviceId: null
            }
          })
        }
      }))
    ),
    { name: 'audio-store' }
  )
)