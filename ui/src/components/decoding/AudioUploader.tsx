import React, { useState, useRef, useCallback } from 'react'
import { Upload, File, X, Play, Pause, Link } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { cn } from '@/lib/utils'
import { AudioPlayer } from '@/components/audio'
import { formatFileSize } from '@/lib/utils'

export interface AudioUploaderProps {
  onFileSelect: (file: File) => void
  onUrlSubmit?: (url: string) => void
  acceptedFormats?: string[]
  maxFileSize?: number // in MB
  showPreview?: boolean
  className?: string
}

const DEFAULT_ACCEPTED_FORMATS = ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
const DEFAULT_MAX_FILE_SIZE = 50 // 50MB

export function AudioUploader({
  onFileSelect,
  onUrlSubmit,
  acceptedFormats = DEFAULT_ACCEPTED_FORMATS,
  maxFileSize = DEFAULT_MAX_FILE_SIZE,
  showPreview = true,
  className
}: AudioUploaderProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [fileUrl, setFileUrl] = useState<string | null>(null)
  const [urlInput, setUrlInput] = useState('')
  const [showUrlInput, setShowUrlInput] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = useCallback((file: File): string | null => {
    // Check file size
    const maxSizeBytes = maxFileSize * 1024 * 1024
    if (file.size > maxSizeBytes) {
      return `File size exceeds ${maxFileSize}MB limit`
    }

    // Check file format
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!acceptedFormats.includes(fileExtension)) {
      return `File format not supported. Accepted formats: ${acceptedFormats.join(', ')}`
    }

    return null
  }, [maxFileSize, acceptedFormats])

  const handleFileSelect = useCallback((file: File) => {
    const validationError = validateFile(file)
    if (validationError) {
      setError(validationError)
      return
    }

    setError(null)
    setSelectedFile(file)
    
    // Create object URL for preview
    if (fileUrl) {
      URL.revokeObjectURL(fileUrl)
    }
    const url = URL.createObjectURL(file)
    setFileUrl(url)
    
    onFileSelect(file)
  }, [validateFile, fileUrl, onFileSelect])

  const [isDragActive, setIsDragActive] = useState(false)

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)

    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0 && files[0].type.startsWith('audio/')) {
      handleFileSelect(files[0])
    }
  }, [handleFileSelect])

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFileSelect(files[0])
    }
  }, [handleFileSelect])

  const handleUrlSubmit = useCallback(() => {
    if (!urlInput.trim()) {
      setError('Please enter a valid URL')
      return
    }

    try {
      new URL(urlInput)
      setError(null)
      setShowUrlInput(false)
      onUrlSubmit?.(urlInput)
    } catch {
      setError('Invalid URL format')
    }
  }, [urlInput, onUrlSubmit])

  const handleClear = useCallback(() => {
    setSelectedFile(null)
    if (fileUrl) {
      URL.revokeObjectURL(fileUrl)
      setFileUrl(null)
    }
    setError(null)
    setUrlInput('')
  }, [fileUrl])

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      if (fileUrl) {
        URL.revokeObjectURL(fileUrl)
      }
    }
  }, [fileUrl])

  return (
    <div className={cn('space-y-4', className)}>
      {/* File Upload Area */}
      {!selectedFile && !showUrlInput && (
        <div
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={cn(
            'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
            isDragActive
              ? 'border-primary bg-primary/10'
              : 'border-muted-foreground/25 hover:border-primary/50'
          )}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={acceptedFormats.join(',')}
            onChange={handleFileInputChange}
            className="hidden"
          />
          <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
          <p className="text-sm font-medium mb-2">
            {isDragActive ? 'Drop the audio file here' : 'Drag & drop an audio file here'}
          </p>
          <p className="text-xs text-muted-foreground mb-4">
            or click to browse your files
          </p>
          <div className="flex items-center justify-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                setShowUrlInput(true)
              }}
            >
              <Link className="h-4 w-4 mr-2" />
              Use URL
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-4">
            Supported formats: {acceptedFormats.join(', ')} (Max {maxFileSize}MB)
          </p>
        </div>
      )}

      {/* URL Input */}
      {showUrlInput && (
        <div className="space-y-2">
          <Label htmlFor="audio-url">Audio URL</Label>
          <div className="flex gap-2">
            <Input
              id="audio-url"
              type="url"
              placeholder="https://example.com/audio.mp3"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleUrlSubmit()
                }
              }}
            />
            <Button onClick={handleUrlSubmit}>
              Load
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => {
                setShowUrlInput(false)
                setUrlInput('')
                setError(null)
              }}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Selected File Info */}
      {selectedFile && (
        <div className="bg-muted rounded-lg p-4">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <File className="h-8 w-8 text-muted-foreground mt-0.5" />
              <div>
                <p className="font-medium text-sm">{selectedFile.name}</p>
                <p className="text-xs text-muted-foreground">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleClear}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Audio Preview */}
      {showPreview && fileUrl && (
        <div className="border rounded-lg p-4">
          <Label className="text-sm font-medium mb-2 block">Preview</Label>
          <AudioPlayer
            audioUrl={fileUrl}
            className="w-full"
          />
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-lg">
          {error}
        </div>
      )}
    </div>
  )
}