import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { AudioDeviceSelector } from '../AudioDeviceSelector'
import { useAudioStore } from '@/stores'

// Mock the audio store
vi.mock('@/stores', () => ({
  useAudioStore: vi.fn()
}))

// Mock MediaDevices API
const mockDevices = [
  {
    deviceId: 'default',
    kind: 'audioinput',
    label: 'Default Microphone',
    groupId: 'group1'
  },
  {
    deviceId: 'mic1',
    kind: 'audioinput',
    label: 'USB Microphone',
    groupId: 'group2'
  },
  {
    deviceId: 'speaker1',
    kind: 'audiooutput',
    label: 'Default Speaker',
    groupId: 'group3'
  }
]

global.navigator.mediaDevices = {
  getUserMedia: vi.fn(() => Promise.resolve({} as MediaStream)),
  enumerateDevices: vi.fn(() => Promise.resolve(mockDevices)),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn()
} as any

// Mock permissions API
global.navigator.permissions = {
  query: vi.fn(() => Promise.resolve({ 
    state: 'granted',
    addEventListener: vi.fn()
  }))
} as any

describe('AudioDeviceSelector', () => {
  const mockStore = {
    setAudioInputDevice: vi.fn(),
    setAudioOutputDevice: vi.fn()
  }

  const defaultProps = {
    type: 'input' as const,
    onDeviceChange: vi.fn()
  }

  beforeEach(() => {
    vi.clearAllMocks()
    ;(useAudioStore as any).mockReturnValue(mockStore)
  })

  it('renders without crashing', () => {
    render(<AudioDeviceSelector {...defaultProps} />)
    expect(screen.getByText('Microphone')).toBeInTheDocument()
  })

  it('shows correct label for input type', () => {
    render(<AudioDeviceSelector {...defaultProps} type="input" />)
    expect(screen.getByText('Microphone')).toBeInTheDocument()
  })

  it('shows correct label for output type', () => {
    render(<AudioDeviceSelector {...defaultProps} type="output" />)
    expect(screen.getByText('Speaker')).toBeInTheDocument()
  })

  it('loads and displays audio devices', async () => {
    render(<AudioDeviceSelector {...defaultProps} />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.enumerateDevices).toHaveBeenCalled()
    })
    
    // Open the select dropdown
    const trigger = screen.getByRole('combobox')
    fireEvent.click(trigger)
    
    await waitFor(() => {
      expect(screen.getByText('System Default')).toBeInTheDocument()
      expect(screen.getByText('Default Microphone')).toBeInTheDocument()
      expect(screen.getByText('USB Microphone')).toBeInTheDocument()
    })
  })

  it('filters devices by type', async () => {
    render(<AudioDeviceSelector {...defaultProps} type="output" />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.enumerateDevices).toHaveBeenCalled()
    })
    
    const trigger = screen.getByRole('combobox')
    fireEvent.click(trigger)
    
    await waitFor(() => {
      expect(screen.getByText('Default Speaker')).toBeInTheDocument()
      expect(screen.queryByText('USB Microphone')).not.toBeInTheDocument()
    })
  })

  it('requests microphone permission for input devices', async () => {
    render(<AudioDeviceSelector {...defaultProps} type="input" />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ audio: true })
    })
  })

  it('does not request permission for output devices', async () => {
    render(<AudioDeviceSelector {...defaultProps} type="output" />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.getUserMedia).not.toHaveBeenCalled()
    })
  })

  it('handles permission denied error', async () => {
    const error = new Error('Permission denied')
    error.name = 'NotAllowedError'
    global.navigator.mediaDevices.getUserMedia = vi.fn(() => Promise.reject(error))
    
    render(<AudioDeviceSelector {...defaultProps} type="input" />)
    
    await waitFor(() => {
      expect(screen.getByText(/permission denied/i)).toBeInTheDocument()
    })
  })

  it('calls onDeviceChange when device is selected', async () => {
    render(<AudioDeviceSelector {...defaultProps} />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.enumerateDevices).toHaveBeenCalled()
    })
    
    const trigger = screen.getByRole('combobox')
    fireEvent.click(trigger)
    
    await waitFor(() => {
      const usbMic = screen.getByText('USB Microphone')
      fireEvent.click(usbMic)
    })
    
    expect(defaultProps.onDeviceChange).toHaveBeenCalledWith({
      deviceId: 'mic1',
      kind: 'audioinput',
      label: 'USB Microphone',
      groupId: 'group2'
    })
  })

  it('updates store when input device is selected', async () => {
    render(<AudioDeviceSelector {...defaultProps} type="input" />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.enumerateDevices).toHaveBeenCalled()
    })
    
    const trigger = screen.getByRole('combobox')
    fireEvent.click(trigger)
    
    await waitFor(() => {
      const usbMic = screen.getByText('USB Microphone')
      fireEvent.click(usbMic)
    })
    
    expect(mockStore.setAudioInputDevice).toHaveBeenCalledWith('mic1')
  })

  it('updates store when output device is selected', async () => {
    render(<AudioDeviceSelector {...defaultProps} type="output" />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.enumerateDevices).toHaveBeenCalled()
    })
    
    const trigger = screen.getByRole('combobox')
    fireEvent.click(trigger)
    
    await waitFor(() => {
      const speaker = screen.getByText('Default Speaker')
      fireEvent.click(speaker)
    })
    
    expect(mockStore.setAudioOutputDevice).toHaveBeenCalledWith('speaker1')
  })

  it('handles devices with no label', async () => {
    const devicesWithNoLabel = [
      {
        deviceId: 'device1',
        kind: 'audioinput',
        label: '',
        groupId: 'group1'
      }
    ]
    global.navigator.mediaDevices.enumerateDevices = vi.fn(() => Promise.resolve(devicesWithNoLabel))
    
    render(<AudioDeviceSelector {...defaultProps} />)
    
    await waitFor(() => {
      const trigger = screen.getByRole('combobox')
      fireEvent.click(trigger)
    })
    
    await waitFor(() => {
      expect(screen.getByText(/Microphone devi/)).toBeInTheDocument()
    })
  })

  it('listens for device changes', async () => {
    render(<AudioDeviceSelector {...defaultProps} />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.addEventListener).toHaveBeenCalledWith('devicechange', expect.any(Function))
    })
  })

  it('removes device change listener on unmount', async () => {
    const { unmount } = render(<AudioDeviceSelector {...defaultProps} />)
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.addEventListener).toHaveBeenCalled()
    })
    
    unmount()
    
    expect(global.navigator.mediaDevices.removeEventListener).toHaveBeenCalledWith('devicechange', expect.any(Function))
  })

  it('sets default device ID when provided', async () => {
    render(<AudioDeviceSelector {...defaultProps} defaultDeviceId="mic1" />)
    
    await waitFor(() => {
      const trigger = screen.getByRole('combobox')
      expect(trigger).toHaveValue('mic1')
    })
  })
})