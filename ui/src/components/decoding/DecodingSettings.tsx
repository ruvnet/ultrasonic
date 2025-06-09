import React from 'react'
import { Settings, Zap, Shield, Cpu } from 'lucide-react'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Slider } from '@/components/ui/slider'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { cn } from '@/lib/utils'

export interface DecodingSettings {
  detectionSensitivity: 'low' | 'medium' | 'high'
  errorTolerance: number // 0-1
  decryption: boolean
  parallelProcessing: boolean
}

export interface DecodingSettingsProps {
  settings: DecodingSettings
  onChange: (settings: DecodingSettings) => void
  mode?: 'auto' | 'manual'
  className?: string
}

const DEFAULT_SETTINGS: DecodingSettings = {
  detectionSensitivity: 'medium',
  errorTolerance: 0.7,
  decryption: true,
  parallelProcessing: true
}

export function DecodingSettings({
  settings = DEFAULT_SETTINGS,
  onChange,
  mode = 'manual',
  className
}: DecodingSettingsProps) {
  const handleChange = <K extends keyof DecodingSettings>(
    key: K,
    value: DecodingSettings[K]
  ) => {
    onChange({
      ...settings,
      [key]: value
    })
  }

  return (
    <div className={cn('space-y-6', className)}>
      <div className="flex items-center gap-2">
        <Settings className="h-5 w-5 text-muted-foreground" />
        <h3 className="font-semibold">Decoding Settings</h3>
        {mode === 'auto' && (
          <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
            Auto Mode
          </span>
        )}
      </div>

      {mode === 'manual' && (
        <>
          {/* Detection Sensitivity */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-muted-foreground" />
              <Label htmlFor="detection-sensitivity">Detection Sensitivity</Label>
            </div>
            <Select
              value={settings.detectionSensitivity}
              onValueChange={(value) => 
                handleChange('detectionSensitivity', value as 'low' | 'medium' | 'high')
              }
            >
              <SelectTrigger id="detection-sensitivity">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low">
                  <div className="flex items-center gap-2">
                    <span>Low</span>
                    <span className="text-xs text-muted-foreground">
                      Faster, may miss weak signals
                    </span>
                  </div>
                </SelectItem>
                <SelectItem value="medium">
                  <div className="flex items-center gap-2">
                    <span>Medium</span>
                    <span className="text-xs text-muted-foreground">
                      Balanced performance
                    </span>
                  </div>
                </SelectItem>
                <SelectItem value="high">
                  <div className="flex items-center gap-2">
                    <span>High</span>
                    <span className="text-xs text-muted-foreground">
                      Thorough, slower processing
                    </span>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Error Tolerance */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="error-tolerance">Error Tolerance</Label>
              <span className="text-sm text-muted-foreground">
                {Math.round(settings.errorTolerance * 100)}%
              </span>
            </div>
            <Slider
              id="error-tolerance"
              value={[settings.errorTolerance]}
              onValueChange={([value]) => handleChange('errorTolerance', value)}
              max={1}
              step={0.05}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground">
              Higher tolerance allows decoding of degraded signals
            </p>
          </div>
        </>
      )}

      {/* Decryption */}
      <div className="flex items-center justify-between space-x-2">
        <div className="space-y-0.5">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-muted-foreground" />
            <Label htmlFor="decryption">Enable Decryption</Label>
          </div>
          <p className="text-xs text-muted-foreground">
            Attempt to decrypt encoded messages
          </p>
        </div>
        <Switch
          id="decryption"
          checked={settings.decryption}
          onCheckedChange={(checked) => handleChange('decryption', checked)}
        />
      </div>

      {/* Parallel Processing */}
      <div className="flex items-center justify-between space-x-2">
        <div className="space-y-0.5">
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4 text-muted-foreground" />
            <Label htmlFor="parallel">Parallel Processing</Label>
          </div>
          <p className="text-xs text-muted-foreground">
            Use multiple threads for faster decoding
          </p>
        </div>
        <Switch
          id="parallel"
          checked={settings.parallelProcessing}
          onCheckedChange={(checked) => handleChange('parallelProcessing', checked)}
        />
      </div>

      {mode === 'auto' && (
        <div className="bg-muted/50 rounded-lg p-4 text-sm">
          <p className="font-medium mb-1">Auto Mode Active</p>
          <p className="text-muted-foreground">
            Settings are automatically optimized based on the audio characteristics.
            Switch to manual mode for full control.
          </p>
        </div>
      )}
    </div>
  )
}

export { DEFAULT_SETTINGS }