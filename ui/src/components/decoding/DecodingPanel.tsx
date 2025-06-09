import React, { useState, useCallback } from 'react'
import { Headphones, Settings as SettingsIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { AudioUploader } from './AudioUploader'
import { DecodingSettings, DEFAULT_SETTINGS } from './DecodingSettings'
import { DecodingProgress, DecodingProgressData } from './DecodingProgress'
import { DecodingResults, DecodingResult } from './DecodingResults'
import { useDecodingStore } from '@/stores/decodingStore'
import { cn } from '@/lib/utils'

export interface DecodingParams {
  audioFile?: File
  audioBuffer?: AudioBuffer
  settings?: DecodingSettings
}

export interface DecodingPanelProps {
  onDecode?: (params: DecodingParams) => Promise<void>
  isProcessing?: boolean
  className?: string
}

export function DecodingPanel({
  onDecode,
  isProcessing: externalProcessing,
  className
}: DecodingPanelProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [settings, setSettings] = useState<DecodingSettings>(DEFAULT_SETTINGS)
  const [mode, setMode] = useState<'auto' | 'manual'>('auto')
  const [activeTab, setActiveTab] = useState<'upload' | 'results'>('upload')

  // Store integration
  const {
    isDecoding,
    progress,
    results,
    decode,
    cancelDecoding,
    exportResults,
    clearResults
  } = useDecodingStore()

  const isProcessing = externalProcessing || isDecoding

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file)
  }, [])

  const handleDecode = useCallback(async () => {
    if (!selectedFile) return

    const params: DecodingParams = {
      audioFile: selectedFile,
      settings: mode === 'manual' ? settings : undefined
    }

    try {
      if (onDecode) {
        await onDecode(params)
      } else {
        // Use store's decode function
        await decode(selectedFile, mode === 'manual' ? settings : undefined)
      }
      
      // Switch to results tab after successful decoding
      setActiveTab('results')
    } catch (error) {
      console.error('Decoding failed:', error)
    }
  }, [selectedFile, settings, mode, onDecode, decode])

  const handleExport = useCallback((format: 'json' | 'txt' | 'csv') => {
    exportResults(format)
  }, [exportResults])

  const handleCopyMessage = useCallback((message: string) => {
    // Additional handling if needed
    console.log('Message copied:', message)
  }, [])

  const progressData: DecodingProgressData | null = progress ? {
    percentage: progress.percentage,
    stage: progress.stage as DecodingProgressData['stage'],
    currentFrequency: undefined,
    signalStrength: undefined,
    estimatedTime: undefined
  } : null

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Headphones className="h-6 w-6 text-primary" />
          <h2 className="text-2xl font-bold">Decode Audio</h2>
        </div>
        {results.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={clearResults}
          >
            Clear Results
          </Button>
        )}
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as 'upload' | 'results')}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="upload">Upload & Decode</TabsTrigger>
          <TabsTrigger value="results" disabled={results.length === 0}>
            Results ({results.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          {/* File Upload */}
          <Card className="p-6">
            <h3 className="font-semibold mb-4">Select Audio File</h3>
            <AudioUploader
              onFileSelect={handleFileSelect}
              showPreview={true}
            />
          </Card>

          {/* Settings */}
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold flex items-center gap-2">
                <SettingsIcon className="h-4 w-4" />
                Decoding Mode
              </h3>
              <div className="flex gap-2">
                <Button
                  variant={mode === 'auto' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setMode('auto')}
                >
                  Auto
                </Button>
                <Button
                  variant={mode === 'manual' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setMode('manual')}
                >
                  Manual
                </Button>
              </div>
            </div>
            
            <DecodingSettings
              settings={settings}
              onChange={setSettings}
              mode={mode}
            />
          </Card>

          {/* Decode Button */}
          <Button
            className="w-full"
            size="lg"
            onClick={handleDecode}
            disabled={!selectedFile || isProcessing}
          >
            {isProcessing ? 'Decoding...' : 'Start Decoding'}
          </Button>
        </TabsContent>

        <TabsContent value="results" className="space-y-6">
          <DecodingResults
            results={results}
            onExport={handleExport}
            onCopyMessage={handleCopyMessage}
          />
        </TabsContent>
      </Tabs>

      {/* Progress Overlay */}
      {isProcessing && progressData && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md p-6">
            <DecodingProgress
              progress={progressData}
              onCancel={cancelDecoding}
            />
          </Card>
        </div>
      )}
    </div>
  )
}