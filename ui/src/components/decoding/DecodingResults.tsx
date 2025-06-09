import React, { useState } from 'react'
import { 
  Copy, 
  Download, 
  MessageSquare, 
  Clock, 
  Shield, 
  AlertTriangle,
  FileJson,
  FileText,
  Table
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { cn } from '@/lib/utils'
import { formatDate, formatDuration } from '@/lib/utils'

export interface DecodingResult {
  message: string
  confidence: number
  timestamp: Date
  position: number // seconds into audio
  metadata?: {
    frequency: number
    bitrate: number
    errorsCorrected: number
    encrypted: boolean
  }
  warnings?: string[]
}

export interface DecodingResultsProps {
  results: DecodingResult[]
  onExport?: (format: 'json' | 'txt' | 'csv') => void
  onCopyMessage?: (message: string) => void
  className?: string
}

export function DecodingResults({
  results,
  onExport,
  onCopyMessage,
  className
}: DecodingResultsProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const handleCopy = async (message: string, index: number) => {
    try {
      await navigator.clipboard.writeText(message)
      setCopiedIndex(index)
      onCopyMessage?.(message)
      
      setTimeout(() => {
        setCopiedIndex(null)
      }, 2000)
    } catch (error) {
      console.error('Failed to copy message:', error)
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600 bg-green-50'
    if (confidence >= 0.7) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const exportIcons = {
    json: FileJson,
    txt: FileText,
    csv: Table
  }

  if (results.length === 0) {
    return (
      <div className={cn('text-center py-8', className)}>
        <MessageSquare className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
        <p className="text-muted-foreground">No messages decoded yet</p>
      </div>
    )
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Export Button */}
      {onExport && results.length > 0 && (
        <div className="flex justify-end">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export Results
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {(['json', 'txt', 'csv'] as const).map((format) => {
                const Icon = exportIcons[format]
                return (
                  <DropdownMenuItem
                    key={format}
                    onClick={() => onExport(format)}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    Export as {format.toUpperCase()}
                  </DropdownMenuItem>
                )
              })}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      )}

      {/* Results List */}
      <div className="space-y-3">
        {results.map((result, index) => (
          <Card key={index}>
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <CardTitle className="text-base">
                    Message {index + 1}
                  </CardTitle>
                  <Badge
                    variant="secondary"
                    className={cn('text-xs', getConfidenceColor(result.confidence))}
                  >
                    {Math.round(result.confidence * 100)}% confidence
                  </Badge>
                  {result.metadata?.encrypted && (
                    <Badge variant="outline" className="text-xs">
                      <Shield className="h-3 w-3 mr-1" />
                      Encrypted
                    </Badge>
                  )}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleCopy(result.message, index)}
                >
                  {copiedIndex === index ? (
                    <>
                      <span className="text-green-600">Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                    </>
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {/* Message Content */}
              <div className="bg-muted/50 rounded-lg p-4 mb-3 font-mono text-sm break-all">
                {result.message}
              </div>

              {/* Metadata */}
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>Position: {formatDuration(result.position)}</span>
                </div>
                <div className="flex items-center gap-2 text-muted-foreground">
                  <span>Decoded: {formatDate(result.timestamp, {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                  })}</span>
                </div>
                {result.metadata && (
                  <>
                    <div className="text-muted-foreground">
                      Frequency: {(result.metadata.frequency / 1000).toFixed(1)} kHz
                    </div>
                    <div className="text-muted-foreground">
                      Errors corrected: {result.metadata.errorsCorrected}
                    </div>
                  </>
                )}
              </div>

              {/* Warnings */}
              {result.warnings && result.warnings.length > 0 && (
                <div className="mt-3 space-y-1">
                  {result.warnings.map((warning, i) => (
                    <div
                      key={i}
                      className="flex items-start gap-2 text-xs text-yellow-600 bg-yellow-50 rounded p-2"
                    >
                      <AlertTriangle className="h-3 w-3 mt-0.5 shrink-0" />
                      <span>{warning}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}