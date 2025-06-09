import React, { useState, useCallback, useMemo } from 'react';
import { Send, Download, AlertCircle } from 'lucide-react';
import MessageInput from './MessageInput';
import EncodingSettings, { EncodingSettings as Settings } from './EncodingSettings';
import AudioSourceSelector, { AudioSource } from './AudioSourceSelector';
import EncodingProgress from './EncodingProgress';

interface EncodingPanelProps {
  onEncode?: (params: EncodingParams) => Promise<EncodingResult>;
  className?: string;
}

export interface EncodingParams {
  message: string;
  audioSource: AudioSource;
  settings: Settings;
}

export interface EncodingResult {
  success: boolean;
  outputUrl?: string;
  downloadUrl?: string;
  error?: string;
  metadata?: {
    duration: number;
    fileSize: number;
    encodingTime: number;
  };
}

const defaultSettings: Settings = {
  baseFrequency: 19500,
  frequencyRange: 3000,
  bitDuration: 75,
  amplitude: 0.7,
  errorCorrection: 'advanced',
  encryption: true,
  compressionLevel: 6
};

export const EncodingPanel: React.FC<EncodingPanelProps> = ({
  onEncode,
  className = ''
}) => {
  // State
  const [message, setMessage] = useState('');
  const [audioSource, setAudioSource] = useState<AudioSource | null>(null);
  const [settings, setSettings] = useState<Settings>(defaultSettings);
  const [isMessageValid, setIsMessageValid] = useState(false);
  const [isEncoding, setIsEncoding] = useState(false);
  const [encodingResult, setEncodingResult] = useState<EncodingResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Validation
  const canEncode = useMemo(() => {
    return isMessageValid && audioSource !== null && !isEncoding;
  }, [isMessageValid, audioSource, isEncoding]);

  // Handlers
  const handleEncode = useCallback(async () => {
    if (!canEncode || !audioSource || !onEncode) return;

    setIsEncoding(true);
    setError(null);
    setEncodingResult(null);

    try {
      const result = await onEncode({
        message,
        audioSource,
        settings
      });

      setEncodingResult(result);
      
      if (!result.success) {
        setError(result.error || 'Encoding failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsEncoding(false);
    }
  }, [canEncode, audioSource, message, settings, onEncode]);

  const handleDownload = useCallback(() => {
    if (encodingResult?.downloadUrl) {
      const link = document.createElement('a');
      link.href = encodingResult.downloadUrl;
      link.download = 'encoded_audio.wav';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }, [encodingResult]);

  const handleReset = useCallback(() => {
    setMessage('');
    setAudioSource(null);
    setEncodingResult(null);
    setError(null);
  }, []);

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Encode Message</h2>
        <p className="mt-1 text-sm text-gray-600">
          Embed your secret message into audio using ultrasonic frequencies
        </p>
      </div>

      {/* Main encoding interface */}
      {!encodingResult && (
        <>
          {/* Message Input */}
          <MessageInput
            value={message}
            onChange={setMessage}
            onValidationChange={setIsMessageValid}
            className="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
          />

          {/* Audio Source Selection */}
          <AudioSourceSelector
            onSourceSelect={setAudioSource}
            currentSource={audioSource}
            className="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
          />

          {/* Encoding Settings */}
          <EncodingSettings
            settings={settings}
            onChange={setSettings}
            className="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
          />

          {/* Error Display */}
          {error && (
            <div className="flex items-start gap-2 p-4 bg-red-50 rounded-lg border border-red-200">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium text-red-800">Encoding Error</p>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleEncode}
              disabled={!canEncode}
              className={`
                flex-1 flex items-center justify-center gap-2 px-6 py-3
                rounded-lg font-medium transition-all
                ${canEncode
                  ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-sm'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                }
              `}
            >
              <Send className="w-5 h-5" />
              {isEncoding ? 'Encoding...' : 'Encode Message'}
            </button>
          </div>
        </>
      )}

      {/* Encoding Progress */}
      {isEncoding && (
        <EncodingProgress
          isActive={true}
          progress={-1} // Indeterminate progress
          status="Encoding your message..."
        />
      )}

      {/* Encoding Result */}
      {encodingResult && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          {encodingResult.success ? (
            <>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Encoding Successful</h3>
                  <p className="text-sm text-gray-600">Your message has been embedded in the audio</p>
                </div>
              </div>

              {/* Metadata */}
              {encodingResult.metadata && (
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-gray-900">
                      {encodingResult.metadata.duration.toFixed(1)}s
                    </p>
                    <p className="text-sm text-gray-600">Duration</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-gray-900">
                      {(encodingResult.metadata.fileSize / (1024 * 1024)).toFixed(1)}MB
                    </p>
                    <p className="text-sm text-gray-600">File Size</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-gray-900">
                      {encodingResult.metadata.encodingTime.toFixed(1)}s
                    </p>
                    <p className="text-sm text-gray-600">Processing Time</p>
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={handleDownload}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  Download Encoded Audio
                </button>
                <button
                  onClick={handleReset}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
                >
                  Encode Another
                </button>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                  <AlertCircle className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Encoding Failed</h3>
                  <p className="text-sm text-gray-600">{encodingResult.error || 'An error occurred during encoding'}</p>
                </div>
              </div>
              <button
                onClick={handleReset}
                className="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Try Again
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default EncodingPanel;