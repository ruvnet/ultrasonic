import React, { useState, useEffect } from 'react'
import { AudioPlayer } from '@/components/audio/AudioPlayer'
import { AudioRecorder } from '@/components/audio/AudioRecorder'
import { AudioDeviceSelector } from '@/components/audio/AudioDeviceSelector'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAudioStore } from '@/stores'

/**
 * Demo page showcasing all audio components with integration to audioStore
 */
export function AudioComponentsDemo() {
  const [recordings, setRecordings] = useState<Array<{ blob: Blob; url: string; timestamp: Date }>>([])
  const [selectedRecording, setSelectedRecording] = useState<string | null>(null)
  
  const { 
    initializeAudio, 
    audioContext,
    playbackState,
    recordingState,
    devices
  } = useAudioStore()

  // Initialize audio context on mount
  useEffect(() => {
    initializeAudio()
  }, [initializeAudio])

  const handleRecordingComplete = (blob: Blob) => {
    const url = URL.createObjectURL(blob)
    const newRecording = {
      blob,
      url,
      timestamp: new Date()
    }
    setRecordings(prev => [...prev, newRecording])
    setSelectedRecording(url)
  }

  const handleDeleteRecording = (index: number) => {
    const recording = recordings[index]
    URL.revokeObjectURL(recording.url)
    setRecordings(prev => prev.filter((_, i) => i !== index))
    if (selectedRecording === recording.url) {
      setSelectedRecording(null)
    }
  }

  return (
    <div className="container mx-auto p-8 space-y-8">
      <h1 className="text-3xl font-bold">Audio Components Demo</h1>
      
      {/* Audio Context Status */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Audio Context Status</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium">State:</span> {audioContext?.state || 'Not initialized'}
          </div>
          <div>
            <span className="font-medium">Sample Rate:</span> {audioContext?.sampleRate || 'N/A'} Hz
          </div>
          <div>
            <span className="font-medium">Current Time:</span> {audioContext?.currentTime?.toFixed(2) || '0.00'}s
          </div>
          <div>
            <span className="font-medium">Base Latency:</span> {audioContext?.baseLatency?.toFixed(3) || 'N/A'}s
          </div>
        </div>
      </Card>

      {/* Device Selection */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Audio Devices</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AudioDeviceSelector 
            type="input" 
            onDeviceChange={(device) => console.log('Input device changed:', device)}
          />
          <AudioDeviceSelector 
            type="output"
            onDeviceChange={(device) => console.log('Output device changed:', device)}
          />
        </div>
        {devices.inputDeviceId && (
          <p className="mt-4 text-sm text-muted-foreground">
            Selected input device: {devices.inputDeviceId}
          </p>
        )}
      </Card>

      {/* Recording Section */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Audio Recording</h2>
        <AudioRecorder
          onRecordingComplete={handleRecordingComplete}
          onRecordingStart={() => console.log('Recording started')}
          onError={(error) => console.error('Recording error:', error)}
          maxDuration={60}
          showLevelMeter={true}
        />
        
        {/* Recording State Info */}
        {recordingState.isRecording && (
          <div className="mt-4 p-3 bg-muted rounded-lg text-sm">
            <p>Recording in progress...</p>
            <p>Chunks collected: {recordingState.chunks.length}</p>
          </div>
        )}
      </Card>

      {/* Recordings List */}
      {recordings.length > 0 && (
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Recordings</h2>
          <div className="space-y-2">
            {recordings.map((recording, index) => (
              <div 
                key={index} 
                className="flex items-center justify-between p-3 bg-muted rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <Button
                    size="sm"
                    variant={selectedRecording === recording.url ? "default" : "outline"}
                    onClick={() => setSelectedRecording(recording.url)}
                  >
                    {selectedRecording === recording.url ? "Selected" : "Select"}
                  </Button>
                  <span className="text-sm">
                    Recording {index + 1} - {recording.timestamp.toLocaleTimeString()}
                  </span>
                </div>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDeleteRecording(index)}
                >
                  Delete
                </Button>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Playback Section */}
      {selectedRecording && (
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Audio Playback</h2>
          <AudioPlayer
            audioUrl={selectedRecording}
            onPlaybackComplete={() => console.log('Playback complete')}
            onError={(error) => console.error('Playback error:', error)}
            showWaveform={true}
          />
          
          {/* Playback State Info */}
          <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium">Playing:</span> {playbackState.isPlaying ? 'Yes' : 'No'}
            </div>
            <div>
              <span className="font-medium">Volume:</span> {Math.round(playbackState.volume * 100)}%
            </div>
            <div>
              <span className="font-medium">Playback Rate:</span> {playbackState.playbackRate}x
            </div>
            <div>
              <span className="font-medium">Duration:</span> {playbackState.duration.toFixed(2)}s
            </div>
          </div>
        </Card>
      )}

      {/* Test Audio File */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Test with Sample Audio</h2>
        <p className="text-sm text-muted-foreground mb-4">
          You can also test the player with a sample audio file URL
        </p>
        <AudioPlayer
          audioUrl="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
          onPlaybackComplete={() => console.log('Sample playback complete')}
          onError={(error) => console.error('Sample playback error:', error)}
          showWaveform={false}
        />
      </Card>
    </div>
  )
}