import React from 'react'
import { Loader2, Radio, Search, Shield, CheckCircle } from 'lucide-react'
import { Progress } from '@/components/ui/progress'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

export interface DecodingProgressData {
  percentage: number
  stage: 'analyzing' | 'detecting' | 'decoding' | 'verifying'
  currentFrequency?: number
  signalStrength?: number
  estimatedTime?: number // seconds remaining
}

export interface DecodingProgressProps {
  progress: DecodingProgressData
  onCancel?: () => void
  className?: string
}

const stageInfo = {
  analyzing: {
    icon: Search,
    label: 'Analyzing Audio',
    description: 'Scanning audio file for ultrasonic signals...'
  },
  detecting: {
    icon: Radio,
    label: 'Detecting Signals',
    description: 'Identifying ultrasonic frequency patterns...'
  },
  decoding: {
    icon: Loader2,
    label: 'Decoding Message',
    description: 'Extracting embedded data from signal...'
  },
  verifying: {
    icon: Shield,
    label: 'Verifying Integrity',
    description: 'Checking message integrity and decryption...'
  }
}

export function DecodingProgress({
  progress,
  onCancel,
  className
}: DecodingProgressProps) {
  const { percentage, stage, currentFrequency, signalStrength, estimatedTime } = progress
  const { icon: Icon, label, description } = stageInfo[stage]

  const formatTime = (seconds: number) => {
    if (seconds < 60) {
      return `${Math.round(seconds)}s`
    }
    const minutes = Math.floor(seconds / 60)
    const secs = Math.round(seconds % 60)
    return `${minutes}m ${secs}s`
  }

  const formatFrequency = (freq: number) => {
    if (freq >= 1000) {
      return `${(freq / 1000).toFixed(1)} kHz`
    }
    return `${freq} Hz`
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Stage Info */}
      <div className="flex items-start gap-3">
        <div className="mt-0.5">
          {stage === 'decoding' ? (
            <Icon className="h-5 w-5 text-primary animate-spin" />
          ) : stage === 'verifying' && percentage === 100 ? (
            <CheckCircle className="h-5 w-5 text-green-500" />
          ) : (
            <Icon className="h-5 w-5 text-primary" />
          )}
        </div>
        <div className="flex-1 space-y-1">
          <div className="flex items-center justify-between">
            <h4 className="font-medium">{label}</h4>
            {estimatedTime && estimatedTime > 0 && (
              <span className="text-sm text-muted-foreground">
                {formatTime(estimatedTime)} remaining
              </span>
            )}
          </div>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <Progress value={percentage} className="h-2" />
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{Math.round(percentage)}%</span>
          {onCancel && percentage < 100 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onCancel}
              className="h-auto p-0 text-xs"
            >
              Cancel
            </Button>
          )}
        </div>
      </div>

      {/* Signal Info */}
      {(currentFrequency || signalStrength !== undefined) && (
        <div className="grid grid-cols-2 gap-4 pt-2">
          {currentFrequency && (
            <div className="bg-muted/50 rounded-lg p-3">
              <p className="text-xs text-muted-foreground mb-1">Current Frequency</p>
              <p className="font-mono font-medium">{formatFrequency(currentFrequency)}</p>
            </div>
          )}
          {signalStrength !== undefined && (
            <div className="bg-muted/50 rounded-lg p-3">
              <p className="text-xs text-muted-foreground mb-1">Signal Strength</p>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                  <div
                    className={cn(
                      'h-full transition-all duration-300',
                      signalStrength > 0.7
                        ? 'bg-green-500'
                        : signalStrength > 0.4
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    )}
                    style={{ width: `${signalStrength * 100}%` }}
                  />
                </div>
                <span className="text-sm font-medium">
                  {Math.round(signalStrength * 100)}%
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Stage-specific Info */}
      {stage === 'analyzing' && (
        <div className="text-xs text-muted-foreground bg-muted/30 rounded p-2">
          Tip: Higher quality audio files yield better decoding results
        </div>
      )}
      
      {stage === 'detecting' && currentFrequency && currentFrequency > 18000 && (
        <div className="text-xs text-muted-foreground bg-muted/30 rounded p-2">
          Ultrasonic signal detected at {formatFrequency(currentFrequency)}
        </div>
      )}
    </div>
  )
}