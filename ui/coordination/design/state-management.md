# State Management Architecture

## Overview
This document defines the state management approach using Zustand for the Ultrasonic-Agentics UI application.

## State Management Principles

1. **Single Source of Truth**: Each piece of state has one authoritative source
2. **Predictable Updates**: State changes are explicit and traceable
3. **Performance First**: Minimize re-renders through selective subscriptions
4. **Type Safety**: Full TypeScript support for all stores
5. **DevTools Integration**: Time-travel debugging and state inspection

## Store Architecture

### Store Organization
```
stores/
├── index.ts              # Store exports and composition
├── audioStore.ts         # Audio playback and recording state
├── encodingStore.ts      # Encoding operations and settings
├── decodingStore.ts      # Decoding operations and results
├── uiStore.ts           # UI state (modals, themes, etc.)
├── settingsStore.ts     # User preferences and configuration
└── types/               # Shared type definitions
    └── index.ts
```

## When to Use Global State vs Local State

### Use Global State (Zustand) When:
1. **Data is shared across multiple components**
   - Audio buffer used by player, encoder, and visualizer
   - User settings affecting multiple views
   - Authentication state

2. **State persists across route changes**
   - Current audio file
   - Encoding/decoding history
   - User preferences

3. **Complex state logic with multiple operations**
   - Audio playback with play/pause/seek/volume
   - Multi-step encoding process
   - Batch operations

4. **State needs to be synchronized**
   - Real-time progress updates
   - WebSocket connections
   - Background operations

### Use Local State (useState/useReducer) When:
1. **State is only used by one component**
   - Form input validation errors
   - Dropdown open/closed state
   - Hover states

2. **State is temporary and UI-specific**
   - Loading spinners for specific operations
   - Modal visibility
   - Animation states

3. **State resets when component unmounts**
   - Search filters
   - Temporary form data
   - UI toggle states

4. **Performance optimization**
   - High-frequency updates (mouse position, scroll)
   - Debounced input values
   - Intermediate calculation results

### Decision Tree
```
Does multiple components need this data?
  ├─ YES → Use Global State
  └─ NO → Does it need to persist?
          ├─ YES → Use Global State
          └─ NO → Is it simple UI state?
                  ├─ YES → Use Local State
                  └─ NO → Consider complexity
                         ├─ Complex → Use Global State
                         └─ Simple → Use Local State
```

### Examples

#### Global State Examples:
```typescript
// Audio buffer - shared by player, encoder, visualizer
const audioBuffer = useAudioStore(state => state.currentAudio.buffer)

// User settings - affects entire app
const theme = useSettingsStore(state => state.theme)

// Encoding progress - needs real-time updates
const progress = useEncodingStore(state => state.progress)
```

#### Local State Examples:
```typescript
// Form validation - only used in this component
const [errors, setErrors] = useState({})

// Dropdown state - resets when component unmounts
const [isOpen, setIsOpen] = useState(false)

// Debounced search - temporary UI state
const [searchTerm, setSearchTerm] = useState('')
const debouncedSearch = useDebounce(searchTerm, 300)
```

## Core Stores Implementation

### Audio Store
Manages audio context, playback, and recording state.

```typescript
// stores/audioStore.ts
import { create } from 'zustand'
import { devtools, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

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
  
  // Actions
  initializeAudio: () => Promise<void>
  loadAudio: (url: string | File) => Promise<void>
  play: () => void
  pause: () => void
  seek: (time: number) => void
  setVolume: (volume: number) => void
  startRecording: () => Promise<void>
  stopRecording: () => Promise<Blob>
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
        
        // Actions
        initializeAudio: async () => {
          if (get().audioContext) return
          
          const context = new AudioContext()
          set(state => {
            state.audioContext = context
          })
        },
        
        loadAudio: async (source) => {
          const context = get().audioContext
          if (!context) throw new Error('Audio context not initialized')
          
          let arrayBuffer: ArrayBuffer
          
          if (source instanceof File) {
            arrayBuffer = await source.arrayBuffer()
          } else {
            const response = await fetch(source)
            arrayBuffer = await response.arrayBuffer()
          }
          
          const audioBuffer = await context.decodeAudioData(arrayBuffer)
          
          set(state => {
            state.currentAudio.buffer = audioBuffer
            state.currentAudio.url = source instanceof File ? URL.createObjectURL(source) : source
            state.playbackState.duration = audioBuffer.duration
          })
        },
        
        // ... more actions
      }))
    ),
    { name: 'audio-store' }
  )
)
```

### Encoding Store
Manages message encoding operations and settings.

```typescript
// stores/encodingStore.ts
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
  encode: (audio: AudioBuffer) => Promise<EncodingResult>
  saveToHistory: (result: EncodingResult) => void
  clearHistory: () => void
}

export const useEncodingStore = create<EncodingState>()(
  persist(
    immer((set, get) => ({
      // Default settings
      settings: {
        baseFrequency: 19000,
        frequencyRange: 3000,
        bitDuration: 20,
        amplitude: 0.8,
        errorCorrection: 'basic',
        encryption: false,
        compressionLevel: 5
      },
      
      presets: [
        {
          id: 'quick',
          name: 'Quick & Simple',
          settings: {
            baseFrequency: 19000,
            frequencyRange: 2000,
            bitDuration: 15,
            amplitude: 0.9,
            errorCorrection: 'none',
            encryption: false,
            compressionLevel: 3
          }
        },
        // ... more presets
      ],
      
      message: '',
      isEncoding: false,
      progress: 0,
      lastResult: null,
      history: [],
      
      // Actions implementation
      encode: async (audio) => {
        set(state => {
          state.isEncoding = true
          state.progress = 0
        })
        
        try {
          // Simulate progress updates
          const progressInterval = setInterval(() => {
            set(state => {
              state.progress = Math.min(state.progress + 10, 90)
            })
          }, 100)
          
          const result = await encodingService.encode({
            audio,
            message: get().message,
            settings: get().settings
          })
          
          clearInterval(progressInterval)
          
          set(state => {
            state.progress = 100
            state.lastResult = result
            state.isEncoding = false
          })
          
          get().saveToHistory(result)
          
          return result
        } catch (error) {
          set(state => {
            state.isEncoding = false
            state.progress = 0
          })
          throw error
        }
      }
    })),
    {
      name: 'encoding-store',
      partialize: (state) => ({
        settings: state.settings,
        history: state.history
      })
    }
  )
)
```

### UI Store
Manages UI-specific state that doesn't belong to business logic.

```typescript
// stores/uiStore.ts
interface UIState {
  // Theme
  theme: 'light' | 'dark' | 'system'
  
  // Modals
  modals: {
    settings: boolean
    help: boolean
    about: boolean
  }
  
  // Layout
  sidebarCollapsed: boolean
  activeView: 'encode' | 'decode' | 'analyze'
  
  // Notifications
  notifications: Notification[]
  
  // Actions
  setTheme: (theme: UIState['theme']) => void
  toggleSidebar: () => void
  openModal: (modal: keyof UIState['modals']) => void
  closeModal: (modal: keyof UIState['modals']) => void
  showNotification: (notification: Omit<Notification, 'id'>) => void
  dismissNotification: (id: string) => void
}

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message?: string
  duration?: number
}
```

## Advanced Patterns

### Computed Values
Using selectors for derived state.

```typescript
// Selector for encoding capacity
export const useEncodingCapacity = () => {
  const settings = useEncodingStore(state => state.settings)
  const audioDuration = useAudioStore(state => state.playbackState.duration)
  
  return useMemo(() => {
    if (!audioDuration) return 0
    
    const bitsPerSecond = 1000 / settings.bitDuration
    const totalBits = bitsPerSecond * audioDuration
    const overheadFactor = settings.errorCorrection === 'advanced' ? 0.5 : 0.8
    
    return Math.floor((totalBits * overheadFactor) / 8) // bytes
  }, [settings, audioDuration])
}
```

### Store Composition
Combining multiple stores for complex operations.

```typescript
// Hook that combines audio and encoding
export function useAudioEncoding() {
  const audioStore = useAudioStore()
  const encodingStore = useEncodingStore()
  
  const encodeCurrentAudio = useCallback(async () => {
    const audioBuffer = audioStore.currentAudio.buffer
    if (!audioBuffer) {
      throw new Error('No audio loaded')
    }
    
    return encodingStore.encode(audioBuffer)
  }, [audioStore.currentAudio.buffer, encodingStore.encode])
  
  return {
    isReady: !!audioStore.currentAudio.buffer && !!encodingStore.message,
    encode: encodeCurrentAudio,
    progress: encodingStore.progress,
    isEncoding: encodingStore.isEncoding
  }
}
```

### Middleware Patterns

#### Persistence Middleware
```typescript
const persistConfig = {
  name: 'ultrasonic-storage',
  storage: createJSONStorage(() => localStorage),
  partialize: (state) => ({
    // Only persist specific fields
    settings: state.settings,
    theme: state.theme
  }),
  onRehydrateStorage: () => (state) => {
    console.log('Store rehydrated:', state)
  }
}
```

#### Logger Middleware
```typescript
const logger = (config) => (set, get, api) =>
  config(
    (...args) => {
      console.log('Previous state:', get())
      set(...args)
      console.log('New state:', get())
    },
    get,
    api
  )
```

### Performance Optimization

#### Selective Subscriptions
```typescript
// Only re-render when specific state changes
function AudioTimer() {
  const currentTime = useAudioStore(state => state.playbackState.currentTime)
  const duration = useAudioStore(state => state.playbackState.duration)
  
  return (
    <div>
      {formatTime(currentTime)} / {formatTime(duration)}
    </div>
  )
}
```

#### Shallow Equality Checks
```typescript
// Use shallow equality for object selections
const playbackState = useAudioStore(
  state => state.playbackState,
  shallow
)
```

## Testing Strategies

### Store Testing
```typescript
// tests/stores/encodingStore.test.ts
describe('EncodingStore', () => {
  beforeEach(() => {
    useEncodingStore.setState({
      message: '',
      settings: defaultSettings,
      isEncoding: false
    })
  })
  
  it('should update message', () => {
    const { setMessage } = useEncodingStore.getState()
    
    setMessage('Test message')
    
    expect(useEncodingStore.getState().message).toBe('Test message')
  })
  
  it('should handle encoding', async () => {
    const { encode, setMessage } = useEncodingStore.getState()
    const mockAudioBuffer = createMockAudioBuffer()
    
    setMessage('Secret message')
    
    const result = await encode(mockAudioBuffer)
    
    expect(result).toBeDefined()
    expect(useEncodingStore.getState().lastResult).toEqual(result)
  })
})
```

### Component Integration Testing
```typescript
// tests/integration/encoding.test.tsx
describe('Encoding Integration', () => {
  it('should encode message with current audio', async () => {
    const { getByRole, getByText } = render(<EncodingPanel />)
    
    // Load audio
    await act(async () => {
      useAudioStore.getState().loadAudio(testAudioFile)
    })
    
    // Set message
    const input = getByRole('textbox', { name: /message/i })
    await userEvent.type(input, 'Test message')
    
    // Start encoding
    const encodeButton = getByRole('button', { name: /encode/i })
    await userEvent.click(encodeButton)
    
    // Wait for completion
    await waitFor(() => {
      expect(getByText(/encoding complete/i)).toBeInTheDocument()
    })
  })
})
```

## DevTools Integration

### Zustand DevTools
```typescript
// Enable Redux DevTools
const useStore = create(devtools(store, {
  name: 'ultrasonic-app',
  trace: true,
  traceLimit: 25
}))
```

### Custom DevTools Panel
```typescript
// components/DevTools.tsx
export function DevTools() {
  const stores = {
    audio: useAudioStore(),
    encoding: useEncodingStore(),
    decoding: useDecodingStore(),
    ui: useUIStore()
  }
  
  return (
    <div className="devtools">
      <pre>{JSON.stringify(stores, null, 2)}</pre>
    </div>
  )
}
```

## Migration Guide

### From Redux
```typescript
// Redux action
dispatch({ type: 'SET_MESSAGE', payload: 'Hello' })

// Zustand equivalent
useEncodingStore.getState().setMessage('Hello')
```

### From Context API
```typescript
// Context pattern
const AudioContext = createContext()
<AudioContext.Provider value={state}>

// Zustand equivalent
const useAudioStore = create(...)
// No provider needed!
```

## Best Practices

1. **Keep Stores Focused**: One store per domain
2. **Avoid Nested State**: Use normalized data structures
3. **Use Immer for Complex Updates**: Simplifies immutable updates
4. **Memoize Selectors**: For expensive computations
5. **Test Store Logic**: Separate from components
6. **Document Actions**: Clear action names and purposes
7. **Type Everything**: Full TypeScript coverage
8. **Start with Local State**: Elevate to global only when needed
9. **Consider Colocation**: Keep state close to where it's used
10. **Avoid Premature Optimization**: Don't create stores for future "might need"

## State Migration Patterns

### Elevating Local to Global State
When local state needs to become global:

```typescript
// Before: Local state in component
function AudioPlayer() {
  const [volume, setVolume] = useState(1)
  // ... volume only used here
}

// After: Moved to global store when needed elsewhere
// audioStore.ts
interface AudioState {
  playbackState: {
    volume: number
    // ... other playback state
  }
}

// Component now uses store
function AudioPlayer() {
  const volume = useAudioStore(state => state.playbackState.volume)
  const setVolume = useAudioStore(state => state.setVolume)
}
```

### Extracting Global to Local State
When global state is only used in one place:

```typescript
// Before: Unnecessary global state
interface UIStore {
  dropdownStates: Record<string, boolean>
}

// After: Local state where used
function Dropdown({ id }) {
  const [isOpen, setIsOpen] = useState(false)
  // Simpler, more performant
}
```

## Performance Monitoring

```typescript
// Monitor store updates
if (process.env.NODE_ENV === 'development') {
  useEncodingStore.subscribe(
    state => state,
    (state, prevState) => {
      console.log('Store updated:', { prevState, state })
    }
  )
}
```