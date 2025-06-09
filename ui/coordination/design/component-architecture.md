# Component Architecture Decisions

## Overview
This document outlines the architectural decisions and patterns for building components in the Ultrasonic-Agentics UI.

## Component Philosophy

### Design Principles
1. **Single Responsibility**: Each component has one clear purpose
2. **Composition over Inheritance**: Build complex UIs from simple parts
3. **Props over State**: Prefer controlled components
4. **Type Safety**: Full TypeScript coverage
5. **Accessibility First**: WCAG 2.1 AA compliance

## Component Categories

### 1. Atomic Components
Basic building blocks with no business logic.

```typescript
// components/atoms/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  children: React.ReactNode
  className?: string
}
```

### 2. Molecular Components
Combinations of atoms with minimal logic.

```typescript
// components/molecules/FormField.tsx
interface FormFieldProps {
  label: string
  error?: string
  required?: boolean
  children: React.ReactElement
  className?: string
}
```

### 3. Organism Components
Complex components with business logic.

```typescript
// components/organisms/AudioPlayer.tsx
interface AudioPlayerProps {
  src: string
  onTimeUpdate?: (time: number) => void
  onEnded?: () => void
  showControls?: boolean
  showWaveform?: boolean
}
```

### 4. Template Components
Page layouts and structure.

```typescript
// components/templates/DashboardLayout.tsx
interface DashboardLayoutProps {
  sidebar?: React.ReactNode
  header?: React.ReactNode
  children: React.ReactNode
}
```

## File Structure Pattern

```
ComponentName/
├── index.ts                 # Public exports
├── ComponentName.tsx        # Main component
├── ComponentName.types.ts   # TypeScript interfaces
├── ComponentName.styles.ts  # Styled components (if used)
├── ComponentName.test.tsx   # Component tests
├── ComponentName.stories.tsx # Storybook stories
└── hooks/                   # Component-specific hooks
    └── useComponentLogic.ts
```

## Component Patterns

### 1. Compound Components
For related components that work together.

```typescript
// Usage
<AudioControls>
  <AudioControls.Player />
  <AudioControls.VolumeSlider />
  <AudioControls.Timeline />
</AudioControls>

// Implementation
const AudioControls = ({ children }) => {
  const [state, setState] = useState(initialState)
  
  return (
    <AudioContext.Provider value={{ state, setState }}>
      <div className="audio-controls">{children}</div>
    </AudioContext.Provider>
  )
}

AudioControls.Player = () => {
  const { state, setState } = useAudioContext()
  // Player implementation
}
```

### 2. Render Props
For flexible component composition.

```typescript
interface WaveformVisualizerProps {
  audioBuffer: AudioBuffer
  render: (props: {
    peaks: number[]
    duration: number
    currentTime: number
  }) => React.ReactNode
}

// Usage
<WaveformVisualizer
  audioBuffer={buffer}
  render={({ peaks, duration, currentTime }) => (
    <CustomWaveform peaks={peaks} progress={currentTime / duration} />
  )}
/>
```

### 3. Higher-Order Components
For cross-cutting concerns.

```typescript
// withErrorBoundary.tsx
function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  fallback?: React.ComponentType<{ error: Error }>
) {
  return class WithErrorBoundary extends React.Component<P> {
    state = { hasError: false, error: null }
    
    static getDerivedStateFromError(error: Error) {
      return { hasError: true, error }
    }
    
    render() {
      if (this.state.hasError) {
        const Fallback = fallback || DefaultErrorFallback
        return <Fallback error={this.state.error} />
      }
      
      return <Component {...this.props} />
    }
  }
}
```

### 4. Custom Hooks
For reusable component logic.

```typescript
// hooks/useAudioPlayer.ts
export function useAudioPlayer(src: string) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const audioRef = useRef<HTMLAudioElement>(null)
  
  const play = useCallback(() => {
    audioRef.current?.play()
    setIsPlaying(true)
  }, [])
  
  const pause = useCallback(() => {
    audioRef.current?.pause()
    setIsPlaying(false)
  }, [])
  
  // ... more logic
  
  return {
    isPlaying,
    currentTime,
    duration,
    play,
    pause,
    audioRef
  }
}
```

## State Management Patterns

### Local State
For UI-only state that doesn't need sharing.

```typescript
function ToggleButton() {
  const [isOn, setIsOn] = useState(false)
  
  return (
    <button onClick={() => setIsOn(!isOn)}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )
}
```

### Lifted State
For state shared between siblings.

```typescript
function Parent() {
  const [sharedValue, setSharedValue] = useState('')
  
  return (
    <>
      <Input value={sharedValue} onChange={setSharedValue} />
      <Display value={sharedValue} />
    </>
  )
}
```

### Global State (Zustand)
For app-wide state and complex logic.

```typescript
// stores/audioStore.ts
interface AudioStore {
  currentTrack: Track | null
  isPlaying: boolean
  volume: number
  
  play: () => void
  pause: () => void
  setVolume: (volume: number) => void
}
```

## Performance Patterns

### Memoization
```typescript
// Memoize expensive computations
const expensiveValue = useMemo(
  () => computeExpensiveValue(deps),
  [deps]
)

// Memoize components
const MemoizedComponent = memo(Component, (prevProps, nextProps) => {
  return prevProps.id === nextProps.id
})
```

### Code Splitting
```typescript
// Lazy load heavy components
const SignalAnalyzer = lazy(() => import('./SignalAnalyzer'))

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <SignalAnalyzer />
    </Suspense>
  )
}
```

### Virtual Scrolling
```typescript
// For long lists
import { FixedSizeList } from 'react-window'

function FileList({ files }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={files.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <FileItem file={files[index]} style={style} />
      )}
    </FixedSizeList>
  )
}
```

## Testing Patterns

### Component Testing
```typescript
describe('Button', () => {
  it('should handle click events', async () => {
    const handleClick = jest.fn()
    const { getByRole } = render(
      <Button onClick={handleClick}>Click me</Button>
    )
    
    await userEvent.click(getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react'

describe('useAudioPlayer', () => {
  it('should update playing state', () => {
    const { result } = renderHook(() => useAudioPlayer('test.mp3'))
    
    act(() => {
      result.current.play()
    })
    
    expect(result.current.isPlaying).toBe(true)
  })
})
```

## Accessibility Patterns

### ARIA Labels
```typescript
<button
  aria-label="Play audio"
  aria-pressed={isPlaying}
  onClick={togglePlay}
>
  <PlayIcon />
</button>
```

### Keyboard Navigation
```typescript
function NavigableList({ items }) {
  const [focusedIndex, setFocusedIndex] = useState(0)
  
  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        setFocusedIndex(prev => Math.min(prev + 1, items.length - 1))
        break
      case 'ArrowUp':
        setFocusedIndex(prev => Math.max(prev - 1, 0))
        break
    }
  }
  
  return (
    <ul role="listbox" onKeyDown={handleKeyDown}>
      {items.map((item, index) => (
        <li
          key={item.id}
          role="option"
          tabIndex={focusedIndex === index ? 0 : -1}
          aria-selected={focusedIndex === index}
        >
          {item.name}
        </li>
      ))}
    </ul>
  )
}
```

## Documentation Standards

### Component Documentation
```typescript
/**
 * AudioPlayer component for playing audio files with waveform visualization.
 * 
 * @example
 * ```tsx
 * <AudioPlayer
 *   src="/audio/sample.mp3"
 *   onTimeUpdate={(time) => console.log('Current time:', time)}
 *   showWaveform
 * />
 * ```
 */
export function AudioPlayer(props: AudioPlayerProps) {
  // Implementation
}
```

### Props Documentation
```typescript
interface AudioPlayerProps {
  /** Audio file URL or blob URL */
  src: string
  
  /** Callback fired when playback time updates */
  onTimeUpdate?: (time: number) => void
  
  /** Whether to show waveform visualization */
  showWaveform?: boolean
  
  /** Custom CSS class name */
  className?: string
}
```

## Best Practices Checklist

- [ ] Component has single responsibility
- [ ] Props are properly typed
- [ ] Component is accessible
- [ ] Error boundaries implemented
- [ ] Loading states handled
- [ ] Tests written
- [ ] Documentation complete
- [ ] Performance optimized
- [ ] Responsive design implemented
- [ ] Cross-browser tested