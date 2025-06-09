import { useCallback, useMemo } from 'react'
import { useAudioStore, useEncodingStore } from '@/stores'

/**
 * Hook that combines audio and encoding stores for complex operations
 */
export function useAudioEncoding() {
  const audioStore = useAudioStore()
  const encodingStore = useEncodingStore()
  
  const encodeCurrentAudio = useCallback(async () => {
    const audioBuffer = audioStore.currentAudio.buffer
    if (!audioBuffer) {
      throw new Error('No audio loaded')
    }
    
    if (!encodingStore.message) {
      throw new Error('No message to encode')
    }
    
    // Convert AudioBuffer to File for API
    // This is a simplified approach - in production you'd want to use a proper encoder
    const blob = new Blob([audioBuffer.getChannelData(0)], { type: 'audio/wav' })
    const file = new File([blob], audioStore.currentAudio.metadata?.fileName || 'audio.wav', { type: 'audio/wav' })
    
    return encodingStore.encode(file)
  }, [audioStore.currentAudio.buffer, audioStore.currentAudio.metadata?.fileName, encodingStore])
  
  const isReady = useMemo(() => {
    return !!audioStore.currentAudio.buffer && !!encodingStore.message
  }, [audioStore.currentAudio.buffer, encodingStore.message])
  
  const encodingCapacity = useMemo(() => {
    const duration = audioStore.playbackState.duration
    if (!duration) return 0
    
    const bitsPerSecond = 1000 / encodingStore.settings.bitDuration
    const totalBits = bitsPerSecond * duration
    const overheadFactor = encodingStore.settings.errorCorrection === 'advanced' ? 0.5 : 
                          encodingStore.settings.errorCorrection === 'basic' ? 0.7 : 0.9
    
    return Math.floor((totalBits * overheadFactor) / 8) // bytes
  }, [audioStore.playbackState.duration, encodingStore.settings])
  
  return {
    // State
    isReady,
    isEncoding: encodingStore.isEncoding,
    progress: encodingStore.progress,
    encodingCapacity,
    messageFitsCapacity: encodingStore.message.length <= encodingCapacity,
    
    // Audio info
    audioLoaded: !!audioStore.currentAudio.buffer,
    audioDuration: audioStore.playbackState.duration,
    audioMetadata: audioStore.currentAudio.metadata,
    
    // Encoding info
    message: encodingStore.message,
    messageLength: encodingStore.message.length,
    settings: encodingStore.settings,
    
    // Actions
    encode: encodeCurrentAudio,
    loadAudio: audioStore.loadAudio,
    setMessage: encodingStore.setMessage,
    updateSettings: encodingStore.updateSettings
  }
}