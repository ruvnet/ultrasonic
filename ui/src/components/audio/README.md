# Audio Components

This directory contains React components for audio recording and playback functionality, integrated with the Zustand audio store.

## Components

### AudioPlayer

A full-featured audio player component with playback controls, progress bar, and volume control.

```tsx
import { AudioPlayer } from '@/components/audio'

<AudioPlayer
  audioUrl="https://example.com/audio.mp3"  // URL or blob URL
  audioBuffer={audioBuffer}                  // Optional: Direct AudioBuffer
  onPlaybackComplete={() => {}}              // Called when playback ends
  onError={(error) => {}}                    // Error handler
  showWaveform={true}                        // Show waveform visualization
  className="custom-class"                   // Additional CSS classes
/>
```

**Features:**
- Play/pause/stop controls
- Seek functionality with progress bar
- Volume control with slider
- Time display (current/total)
- Web Audio API integration
- Waveform visualization placeholder

### AudioRecorder

Component for recording audio from the user's microphone.

```tsx
import { AudioRecorder } from '@/components/audio'

<AudioRecorder
  onRecordingComplete={(blob) => {}}         // Called with audio blob
  onRecordingStart={() => {}}                // Called when recording starts
  onError={(error) => {}}                    // Error handler
  maxDuration={300}                          // Max recording time in seconds
  showLevelMeter={true}                      // Show audio level visualization
  className="custom-class"                   // Additional CSS classes
/>
```

**Features:**
- Start/stop recording controls
- Recording time display
- Audio level meter
- Permission handling
- Maximum duration limit
- MediaRecorder API integration

### AudioDeviceSelector

Dropdown selector for choosing audio input/output devices.

```tsx
import { AudioDeviceSelector } from '@/components/audio'

<AudioDeviceSelector
  type="input"                               // "input" or "output"
  onDeviceChange={(device) => {}}            // Called when device changes
  defaultDeviceId="device-id"                // Initial device selection
  className="custom-class"                   // Additional CSS classes
/>
```

**Features:**
- Lists available audio devices
- Handles permission requests
- Updates on device changes
- Integrates with audio store

## Audio Store Integration

All components integrate with the Zustand audio store (`useAudioStore`) which manages:

- Audio context initialization
- Audio buffer management
- Playback state (playing, time, volume, rate)
- Recording state (recording, stream, chunks)
- Device selection
- Cleanup on unmount

### Store Actions

```typescript
const {
  // State
  audioContext,
  currentAudio,
  playbackState,
  recordingState,
  devices,
  
  // Actions
  initializeAudio,
  loadAudio,
  play,
  pause,
  seek,
  setVolume,
  setPlaybackRate,
  startRecording,
  stopRecording,
  setAudioInputDevice,
  setAudioOutputDevice,
  cleanup
} = useAudioStore()
```

## Usage Example

```tsx
import { AudioPlayer, AudioRecorder, AudioDeviceSelector } from '@/components/audio'
import { useAudioStore } from '@/stores'

function AudioDemo() {
  const [recordedUrl, setRecordedUrl] = useState<string | null>(null)
  const { initializeAudio } = useAudioStore()
  
  useEffect(() => {
    initializeAudio()
  }, [])
  
  const handleRecordingComplete = (blob: Blob) => {
    const url = URL.createObjectURL(blob)
    setRecordedUrl(url)
  }
  
  return (
    <div>
      <AudioDeviceSelector type="input" />
      <AudioRecorder onRecordingComplete={handleRecordingComplete} />
      {recordedUrl && <AudioPlayer audioUrl={recordedUrl} />}
    </div>
  )
}
```

## Testing

Each component has comprehensive test coverage:
- `__tests__/AudioPlayer.test.tsx`
- `__tests__/AudioRecorder.test.tsx`
- `__tests__/AudioDeviceSelector.test.tsx`

Run tests with:
```bash
npm test
```

## Browser Compatibility

- Modern browsers with Web Audio API support
- MediaRecorder API for recording (Chrome, Firefox, Edge, Safari 14.1+)
- Permissions API for device access
- setSinkId API for output device selection (limited support)

## Dependencies

- React 19+
- Zustand for state management
- Radix UI for accessible components
- Lucide React for icons
- Tailwind CSS for styling