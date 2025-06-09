import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { AudioPlayer } from '../AudioPlayer'
import { useAudioStore } from '@/stores'

// Mock the audio store
vi.mock('@/stores', () => ({
  useAudioStore: vi.fn()
}))

// Mock Web Audio API
const mockAudioContext = {
  createBufferSource: vi.fn(() => ({
    buffer: null,
    connect: vi.fn(),
    start: vi.fn(),
    stop: vi.fn(),
    onended: null
  })),
  createGain: vi.fn(() => ({
    gain: { value: 1 },
    connect: vi.fn()
  })),
  currentTime: 0,
  destination: {}
}

describe('AudioPlayer', () => {
  const mockStore = {
    audioContext: mockAudioContext,
    initializeAudio: vi.fn(),
    loadAudio: vi.fn(),
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
    }
  }

  beforeEach(() => {
    vi.clearAllMocks()
    ;(useAudioStore as any).mockReturnValue(mockStore)
  })

  it('renders without crashing', () => {
    render(<AudioPlayer />)
    expect(screen.getByRole('button', { name: /play/i })).toBeInTheDocument()
  })

  it('displays time information correctly', () => {
    render(<AudioPlayer />)
    expect(screen.getByText('0:00 / 0:00')).toBeInTheDocument()
  })

  it('disables controls when no audio is loaded', () => {
    render(<AudioPlayer />)
    const playButton = screen.getByRole('button', { name: /play/i })
    expect(playButton).toBeDisabled()
  })

  it('loads audio from URL prop', async () => {
    const audioUrl = 'https://example.com/audio.mp3'
    render(<AudioPlayer audioUrl={audioUrl} />)
    
    await waitFor(() => {
      expect(mockStore.loadAudio).toHaveBeenCalledWith(audioUrl)
    })
  })

  it('initializes audio context if not already initialized', async () => {
    const storeWithoutContext = {
      ...mockStore,
      audioContext: null
    }
    ;(useAudioStore as any).mockReturnValue(storeWithoutContext)
    
    render(<AudioPlayer audioUrl="test.mp3" />)
    
    await waitFor(() => {
      expect(storeWithoutContext.initializeAudio).toHaveBeenCalled()
    })
  })

  it('enables controls when audio buffer is available', () => {
    const storeWithBuffer = {
      ...mockStore,
      currentAudio: {
        buffer: { duration: 10 } as AudioBuffer,
        url: 'test.mp3',
        metadata: null
      }
    }
    ;(useAudioStore as any).mockReturnValue(storeWithBuffer)
    
    render(<AudioPlayer />)
    const playButton = screen.getByRole('button', { name: /play/i })
    expect(playButton).not.toBeDisabled()
  })

  it('shows volume control with correct initial value', () => {
    render(<AudioPlayer />)
    expect(screen.getByText('100%')).toBeInTheDocument()
  })

  it('shows waveform placeholder when showWaveform is true', () => {
    render(<AudioPlayer showWaveform={true} />)
    expect(screen.getByText('Waveform visualization')).toBeInTheDocument()
  })

  it('does not show waveform when showWaveform is false', () => {
    render(<AudioPlayer showWaveform={false} />)
    expect(screen.queryByText('Waveform visualization')).not.toBeInTheDocument()
  })

  it('calls onError when audio loading fails', async () => {
    const onError = vi.fn()
    const error = new Error('Failed to load audio')
    mockStore.loadAudio.mockRejectedValueOnce(error)
    
    render(<AudioPlayer audioUrl="test.mp3" onError={onError} />)
    
    await waitFor(() => {
      expect(onError).toHaveBeenCalledWith(error)
    })
  })

  it('formats time correctly', () => {
    const storeWithDuration = {
      ...mockStore,
      currentAudio: {
        buffer: { duration: 125.5 } as AudioBuffer,
        url: 'test.mp3',
        metadata: null
      }
    }
    ;(useAudioStore as any).mockReturnValue(storeWithDuration)
    
    render(<AudioPlayer />)
    expect(screen.getByText('0:00 / 2:05')).toBeInTheDocument()
  })
})