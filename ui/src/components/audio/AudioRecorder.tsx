import React, { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Square, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { useAudioStore } from '@/stores'

export interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void
  onRecordingStart?: () => void
  onError?: (error: Error) => void
  maxDuration?: number // in seconds
  showLevelMeter?: boolean
  className?: string
}

export function AudioRecorder({
  onRecordingComplete,
  onRecordingStart,
  onError,
  maxDuration = 300, // 5 minutes default
  showLevelMeter = true,
  className
}: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioLevel, setAudioLevel] = useState(0)
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)
  
  const analyserRef = useRef<AnalyserNode | null>(null)
  const animationFrameRef = useRef<number | null>(null)
  const startTimeRef = useRef<number>(0)
  
  const { 
    audioContext, 
    initializeAudio, 
    startRecording: storeStartRecording, 
    stopRecording: storeStopRecording 
  } = useAudioStore()
  
  // Check microphone permissions
  useEffect(() => {
    const checkPermission = async () => {
      try {
        const result = await navigator.permissions.query({ name: 'microphone' as PermissionName })
        setHasPermission(result.state === 'granted')
        
        result.addEventListener('change', () => {
          setHasPermission(result.state === 'granted')
        })
      } catch (err) {
        // Permissions API might not be available
        console.log('Permissions API not available')
      }
    }
    
    checkPermission()
  }, [])
  
  // Update recording time
  useEffect(() => {
    if (!isRecording) return
    
    const interval = setInterval(() => {
      const elapsed = (Date.now() - startTimeRef.current) / 1000
      setRecordingTime(elapsed)
      
      if (maxDuration && elapsed >= maxDuration) {
        handleStopRecording()
      }
    }, 100)
    
    return () => clearInterval(interval)
  }, [isRecording, maxDuration])
  
  const handleStartRecording = async () => {
    try {
      if (!audioContext) {
        await initializeAudio()
      }
      
      await storeStartRecording()
      
      // Set up audio level monitoring
      if (showLevelMeter && audioContext) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const source = audioContext.createMediaStreamSource(stream)
        const analyser = audioContext.createAnalyser()
        analyser.fftSize = 256
        source.connect(analyser)
        analyserRef.current = analyser
        
        // Start monitoring audio levels
        monitorAudioLevel()
      }
      
      startTimeRef.current = Date.now()
      setIsRecording(true)
      setRecordingTime(0)
      onRecordingStart?.()
      setHasPermission(true)
    } catch (err) {
      const error = err as Error
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        setHasPermission(false)
      }
      onError?.(error)
    }
  }
  
  const handleStopRecording = async () => {
    try {
      const blob = await storeStopRecording()
      
      // Clean up audio level monitoring
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = null
      }
      analyserRef.current = null
      
      setIsRecording(false)
      setRecordingTime(0)
      setAudioLevel(0)
      onRecordingComplete(blob)
    } catch (err) {
      onError?.(err as Error)
    }
  }
  
  const monitorAudioLevel = () => {
    if (!analyserRef.current || !isRecording) return
    
    const analyser = analyserRef.current
    const dataArray = new Uint8Array(analyser.frequencyBinCount)
    analyser.getByteFrequencyData(dataArray)
    
    // Calculate average level
    const average = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length
    const normalizedLevel = average / 255
    setAudioLevel(normalizedLevel)
    
    animationFrameRef.current = requestAnimationFrame(monitorAudioLevel)
  }
  
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }
  
  return (
    <div className={cn('space-y-4', className)}>
      {/* Permission warning */}
      {hasPermission === false && (
        <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-lg">
          <AlertCircle className="h-4 w-4" />
          <span className="text-sm">Microphone permission denied. Please enable it in your browser settings.</span>
        </div>
      )}
      
      {/* Level meter */}
      {showLevelMeter && isRecording && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>Audio Level</span>
            <span>{Math.round(audioLevel * 100)}%</span>
          </div>
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div 
              className="h-full bg-primary transition-all duration-100 ease-out"
              style={{ width: `${audioLevel * 100}%` }}
            />
          </div>
        </div>
      )}
      
      {/* Recording controls */}
      <div className="flex items-center gap-4">
        {!isRecording ? (
          <Button
            onClick={handleStartRecording}
            variant="default"
            className="gap-2"
          >
            <Mic className="h-4 w-4" />
            Start Recording
          </Button>
        ) : (
          <>
            <Button
              onClick={handleStopRecording}
              variant="destructive"
              className="gap-2"
            >
              <Square className="h-4 w-4" />
              Stop Recording
            </Button>
            
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 bg-destructive rounded-full animate-pulse" />
              <span className="font-mono">{formatTime(recordingTime)}</span>
              {maxDuration && (
                <span className="text-muted-foreground">
                  / {formatTime(maxDuration)}
                </span>
              )}
            </div>
          </>
        )}
      </div>
      
      {/* Recording indicator */}
      {isRecording && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <MicOff className="h-4 w-4" />
          <span>Recording in progress...</span>
        </div>
      )}
    </div>
  )
}