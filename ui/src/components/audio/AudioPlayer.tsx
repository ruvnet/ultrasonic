import React, { useEffect, useRef, useState } from 'react'
import { Play, Pause, SkipBack, Volume2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { cn } from '@/lib/utils'
import { useAudioStore } from '@/stores'

export interface AudioPlayerProps {
  audioUrl?: string
  audioBuffer?: AudioBuffer
  onPlaybackComplete?: () => void
  onError?: (error: Error) => void
  showWaveform?: boolean
  className?: string
}

export function AudioPlayer({
  audioUrl,
  audioBuffer,
  onPlaybackComplete,
  onError,
  showWaveform = false,
  className
}: AudioPlayerProps) {
  const audioContextRef = useRef<AudioContext | null>(null)
  const sourceNodeRef = useRef<AudioBufferSourceNode | null>(null)
  const gainNodeRef = useRef<GainNode | null>(null)
  const startTimeRef = useRef<number>(0)
  const pauseTimeRef = useRef<number>(0)
  
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  
  const {
    audioContext,
    initializeAudio,
    loadAudio,
    currentAudio,
    playbackState
  } = useAudioStore()
  
  // Initialize audio context and load audio
  useEffect(() => {
    const init = async () => {
      try {
        if (!audioContext) {
          await initializeAudio()
        }
        
        if (audioUrl) {
          await loadAudio(audioUrl)
        }
      } catch (err) {
        onError?.(err as Error)
      }
    }
    
    init()
  }, [audioUrl, audioContext, initializeAudio, loadAudio, onError])
  
  // Update duration when audio is loaded
  useEffect(() => {
    if (audioBuffer) {
      setDuration(audioBuffer.duration)
    } else if (currentAudio.buffer) {
      setDuration(currentAudio.buffer.duration)
    }
  }, [audioBuffer, currentAudio.buffer])
  
  // Update current time periodically when playing
  useEffect(() => {
    if (!isPlaying) return
    
    const interval = setInterval(() => {
      if (audioContext && sourceNodeRef.current) {
        const elapsed = audioContext.currentTime - startTimeRef.current + pauseTimeRef.current
        setCurrentTime(Math.min(elapsed, duration))
        
        if (elapsed >= duration) {
          handleStop()
          onPlaybackComplete?.()
        }
      }
    }, 100)
    
    return () => clearInterval(interval)
  }, [isPlaying, duration, audioContext, onPlaybackComplete])
  
  const handlePlay = async () => {
    if (!audioContext) return
    
    const buffer = audioBuffer || currentAudio.buffer
    if (!buffer) return
    
    try {
      // Create nodes
      const source = audioContext.createBufferSource()
      const gainNode = audioContext.createGain()
      
      source.buffer = buffer
      gainNode.gain.value = volume
      
      // Connect nodes
      source.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      // Start playback
      source.start(0, pauseTimeRef.current)
      startTimeRef.current = audioContext.currentTime
      
      sourceNodeRef.current = source
      gainNodeRef.current = gainNode
      
      source.onended = () => {
        if (isPlaying) {
          handleStop()
          onPlaybackComplete?.()
        }
      }
      
      setIsPlaying(true)
    } catch (err) {
      onError?.(err as Error)
    }
  }
  
  const handlePause = () => {
    if (sourceNodeRef.current) {
      sourceNodeRef.current.stop()
      sourceNodeRef.current = null
      pauseTimeRef.current = currentTime
      setIsPlaying(false)
    }
  }
  
  const handleStop = () => {
    if (sourceNodeRef.current) {
      sourceNodeRef.current.stop()
      sourceNodeRef.current = null
    }
    pauseTimeRef.current = 0
    setCurrentTime(0)
    setIsPlaying(false)
  }
  
  const handleSeek = (value: number[]) => {
    const newTime = value[0]
    const wasPlaying = isPlaying
    
    if (isPlaying) {
      handlePause()
    }
    
    pauseTimeRef.current = newTime
    setCurrentTime(newTime)
    
    if (wasPlaying) {
      handlePlay()
    }
  }
  
  const handleVolumeChange = (value: number[]) => {
    const newVolume = value[0]
    setVolume(newVolume)
    
    if (gainNodeRef.current) {
      gainNodeRef.current.gain.value = newVolume
    }
  }
  
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }
  
  const hasAudio = !!(audioBuffer || currentAudio.buffer)
  
  return (
    <div className={cn('space-y-4', className)}>
      {/* Waveform visualization placeholder */}
      {showWaveform && (
        <div className="h-32 bg-muted rounded-lg flex items-center justify-center text-muted-foreground">
          Waveform visualization
        </div>
      )}
      
      {/* Controls */}
      <div className="flex items-center gap-2">
        <Button
          size="icon"
          variant="ghost"
          onClick={handleStop}
          disabled={!hasAudio || currentTime === 0}
        >
          <SkipBack className="h-4 w-4" />
        </Button>
        
        <Button
          size="icon"
          onClick={isPlaying ? handlePause : handlePlay}
          disabled={!hasAudio}
        >
          {isPlaying ? (
            <Pause className="h-4 w-4" />
          ) : (
            <Play className="h-4 w-4" />
          )}
        </Button>
        
        {/* Time display */}
        <div className="text-sm text-muted-foreground ml-2">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
      </div>
      
      {/* Progress bar */}
      <Slider
        value={[currentTime]}
        max={duration}
        step={0.1}
        onValueChange={handleSeek}
        disabled={!hasAudio}
        className="w-full"
      />
      
      {/* Volume control */}
      <div className="flex items-center gap-2">
        <Volume2 className="h-4 w-4 text-muted-foreground" />
        <Slider
          value={[volume]}
          max={1}
          step={0.01}
          onValueChange={handleVolumeChange}
          className="w-24"
        />
        <span className="text-sm text-muted-foreground w-10">
          {Math.round(volume * 100)}%
        </span>
      </div>
    </div>
  )
}