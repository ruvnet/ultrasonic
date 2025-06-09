import React, { useState, useEffect } from 'react'
import { Mic, Volume2, AlertCircle } from 'lucide-react'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { cn } from '@/lib/utils'
import { useAudioStore } from '@/stores'

export interface AudioDevice {
  deviceId: string
  kind: MediaDeviceKind
  label: string
  groupId: string
}

export interface AudioDeviceSelectorProps {
  type: 'input' | 'output'
  onDeviceChange?: (device: AudioDevice) => void
  defaultDeviceId?: string
  className?: string
}

export function AudioDeviceSelector({
  type,
  onDeviceChange,
  defaultDeviceId,
  className
}: AudioDeviceSelectorProps) {
  const [devices, setDevices] = useState<AudioDevice[]>([])
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>(defaultDeviceId || 'default')
  const [hasPermission, setHasPermission] = useState<boolean | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { setAudioInputDevice, setAudioOutputDevice } = useAudioStore()

  useEffect(() => {
    const loadDevices = async () => {
      try {
        // Request permissions if needed
        if (type === 'input') {
          await navigator.mediaDevices.getUserMedia({ audio: true })
        }

        const allDevices = await navigator.mediaDevices.enumerateDevices()
        const filteredDevices = allDevices.filter(device => 
          type === 'input' 
            ? device.kind === 'audioinput' 
            : device.kind === 'audiooutput'
        )

        setDevices(filteredDevices.map(device => ({
          deviceId: device.deviceId,
          kind: device.kind,
          label: device.label || `${type === 'input' ? 'Microphone' : 'Speaker'} ${device.deviceId.slice(0, 4)}`,
          groupId: device.groupId
        })))

        setHasPermission(true)
        setError(null)
      } catch (err) {
        const error = err as Error
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
          setHasPermission(false)
          setError('Permission denied. Please allow access to audio devices.')
        } else {
          setError('Failed to load audio devices.')
        }
        console.error('Error loading devices:', error)
      }
    }

    loadDevices()

    // Listen for device changes
    const handleDeviceChange = () => {
      loadDevices()
    }

    navigator.mediaDevices.addEventListener('devicechange', handleDeviceChange)
    return () => {
      navigator.mediaDevices.removeEventListener('devicechange', handleDeviceChange)
    }
  }, [type])

  const handleDeviceSelect = (deviceId: string) => {
    setSelectedDeviceId(deviceId)
    const device = devices.find(d => d.deviceId === deviceId)
    
    if (device) {
      if (type === 'input') {
        setAudioInputDevice(deviceId)
      } else {
        setAudioOutputDevice(deviceId)
      }
      onDeviceChange?.(device)
    }
  }

  const icon = type === 'input' ? Mic : Volume2
  const Icon = icon

  return (
    <div className={cn('space-y-2', className)}>
      <Label htmlFor={`${type}-device-select`} className="flex items-center gap-2">
        <Icon className="h-4 w-4" />
        {type === 'input' ? 'Microphone' : 'Speaker'}
      </Label>

      {error ? (
        <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-lg text-sm">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      ) : (
        <Select
          value={selectedDeviceId}
          onValueChange={handleDeviceSelect}
          disabled={devices.length === 0}
        >
          <SelectTrigger id={`${type}-device-select`}>
            <SelectValue placeholder={`Select ${type === 'input' ? 'microphone' : 'speaker'}`} />
          </SelectTrigger>
          <SelectContent>
            {devices.length === 0 ? (
              <SelectItem value="no-devices" disabled>
                No devices found
              </SelectItem>
            ) : (
              <>
                <SelectItem value="default">
                  System Default
                </SelectItem>
                {devices.map((device) => (
                  <SelectItem key={device.deviceId} value={device.deviceId}>
                    {device.label}
                  </SelectItem>
                ))}
              </>
            )}
          </SelectContent>
        </Select>
      )}
    </div>
  )
}