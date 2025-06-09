import React, { useState, useCallback, useRef } from 'react';
import { Upload, Mic, Waveform, FileAudio, AlertCircle } from 'lucide-react';

export type AudioSource = 
  | { type: 'file'; file: File }
  | { type: 'recording'; duration: number }
  | { type: 'generated'; waveform: 'sine' | 'noise' };

interface AudioSourceSelectorProps {
  onSourceSelect: (source: AudioSource) => void;
  currentSource?: AudioSource;
  className?: string;
}

const ALLOWED_FILE_TYPES = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/mp4'];
const ALLOWED_EXTENSIONS = ['.wav', '.mp3', '.ogg', '.m4a'];
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB

export const AudioSourceSelector: React.FC<AudioSourceSelectorProps> = ({
  onSourceSelect,
  currentSource,
  className = ''
}) => {
  const [activeTab, setActiveTab] = useState<'file' | 'record' | 'generate'>('file');
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // File handling
  const validateFile = useCallback((file: File): string | null => {
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      const ext = file.name.slice(file.name.lastIndexOf('.'));
      if (!ALLOWED_EXTENSIONS.includes(ext.toLowerCase())) {
        return `Unsupported file type. Please upload ${ALLOWED_EXTENSIONS.join(', ')} files.`;
      }
    }
    
    if (file.size > MAX_FILE_SIZE) {
      return `File size exceeds 100MB limit. Current size: ${(file.size / (1024 * 1024)).toFixed(1)}MB`;
    }
    
    return null;
  }, []);
  
  const handleFileSelect = useCallback((file: File) => {
    const error = validateFile(file);
    if (error) {
      setError(error);
      return;
    }
    
    setError(null);
    onSourceSelect({ type: 'file', file });
  }, [validateFile, onSourceSelect]);
  
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);
  
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = Array.from(e.dataTransfer.files);
    const audioFile = files.find(file => 
      ALLOWED_FILE_TYPES.includes(file.type) || 
      ALLOWED_EXTENSIONS.includes(file.name.slice(file.name.lastIndexOf('.')).toLowerCase())
    );
    
    if (audioFile) {
      handleFileSelect(audioFile);
    } else {
      setError('No valid audio file found in dropped items.');
    }
  }, [handleFileSelect]);
  
  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  }, [handleFileSelect]);
  
  const handleGenerateSelect = useCallback((waveform: 'sine' | 'noise') => {
    setError(null);
    onSourceSelect({ type: 'generated', waveform });
  }, [onSourceSelect]);
  
  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <h3 className="text-lg font-medium text-gray-800">Audio Source</h3>
      
      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab('file')}
          className={`
            px-4 py-2 text-sm font-medium border-b-2 transition-colors
            ${activeTab === 'file'
              ? 'text-blue-600 border-blue-600'
              : 'text-gray-500 border-transparent hover:text-gray-700'
            }
          `}
        >
          <FileAudio className="w-4 h-4 inline-block mr-1" />
          File Upload
        </button>
        <button
          onClick={() => setActiveTab('record')}
          className={`
            px-4 py-2 text-sm font-medium border-b-2 transition-colors
            ${activeTab === 'record'
              ? 'text-blue-600 border-blue-600'
              : 'text-gray-500 border-transparent hover:text-gray-700'
            }
          `}
        >
          <Mic className="w-4 h-4 inline-block mr-1" />
          Record
        </button>
        <button
          onClick={() => setActiveTab('generate')}
          className={`
            px-4 py-2 text-sm font-medium border-b-2 transition-colors
            ${activeTab === 'generate'
              ? 'text-blue-600 border-blue-600'
              : 'text-gray-500 border-transparent hover:text-gray-700'
            }
          `}
        >
          <Waveform className="w-4 h-4 inline-block mr-1" />
          Generate
        </button>
      </div>
      
      {/* Tab Content */}
      <div className="min-h-[200px]">
        {/* File Upload Tab */}
        {activeTab === 'file' && (
          <div className="space-y-4">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`
                border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all
                ${dragActive
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
                }
              `}
            >
              <Upload className="w-12 h-12 mx-auto text-gray-400 mb-3" />
              <p className="text-sm text-gray-600">
                {dragActive
                  ? 'Drop your audio file here'
                  : 'Click to upload or drag and drop'
                }
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Supports {ALLOWED_EXTENSIONS.join(', ')} up to 100MB
              </p>
              <input
                ref={fileInputRef}
                type="file"
                accept={ALLOWED_EXTENSIONS.join(',')}
                onChange={handleFileInputChange}
                className="hidden"
              />
            </div>
            
            {/* Current file display */}
            {currentSource?.type === 'file' && (
              <div className="bg-gray-50 rounded-md p-3 flex items-center gap-3">
                <FileAudio className="w-5 h-5 text-gray-600" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">
                    {currentSource.file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {(currentSource.file.size / (1024 * 1024)).toFixed(1)} MB
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
        
        {/* Record Tab */}
        {activeTab === 'record' && (
          <div className="text-center py-8">
            <Mic className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 mb-4">Recording feature coming soon!</p>
            <p className="text-sm text-gray-500">
              You'll be able to record audio directly from your microphone.
            </p>
          </div>
        )}
        
        {/* Generate Tab */}
        {activeTab === 'generate' && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              Generate a test audio signal for encoding:
            </p>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => handleGenerateSelect('sine')}
                className={`
                  p-4 rounded-lg border-2 transition-all
                  ${currentSource?.type === 'generated' && currentSource.waveform === 'sine'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                <Waveform className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <p className="font-medium">Sine Wave</p>
                <p className="text-xs text-gray-500 mt-1">
                  Pure tone at 440Hz
                </p>
              </button>
              
              <button
                onClick={() => handleGenerateSelect('noise')}
                className={`
                  p-4 rounded-lg border-2 transition-all
                  ${currentSource?.type === 'generated' && currentSource.waveform === 'noise'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                <Waveform className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <p className="font-medium">White Noise</p>
                <p className="text-xs text-gray-500 mt-1">
                  Random noise signal
                </p>
              </button>
            </div>
          </div>
        )}
      </div>
      
      {/* Error Display */}
      {error && (
        <div className="flex items-start gap-2 p-3 bg-red-50 rounded-md">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}
    </div>
  );
};

export default AudioSourceSelector;