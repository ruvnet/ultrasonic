import React, { useState, useCallback, useEffect } from 'react';
import { AlertCircle, Lock, Unlock, Info } from 'lucide-react';
import { useEncodingStore } from '@/stores';
import { useAudioEncoding } from '@/hooks/useAudioEncoding';

interface MessageInputProps {
  value?: string;
  onChange?: (value: string) => void;
  maxLength?: number;
  onValidationChange?: (isValid: boolean) => void;
  className?: string;
  useStore?: boolean; // Whether to use the store directly
}

export const MessageInput: React.FC<MessageInputProps> = ({
  value: propValue,
  onChange: propOnChange,
  maxLength = 1000,
  onValidationChange,
  className = '',
  useStore = true
}) => {
  // Use store or props
  const { message: storeMessage, setMessage: storeSetMessage, settings, updateSettings } = useEncodingStore();
  const { encodingCapacity, messageFitsCapacity } = useAudioEncoding();
  
  const value = useStore ? storeMessage : (propValue || '');
  const onChange = useStore ? storeSetMessage : (propOnChange || (() => {}));
  
  const [validationError, setValidationError] = useState<string | null>(null);
  
  // Character count
  const charCount = value.length;
  const charPercentage = (charCount / maxLength) * 100;
  
  // Use effective max length based on encoding capacity
  const effectiveMaxLength = encodingCapacity > 0 ? Math.min(maxLength, encodingCapacity) : maxLength;
  
  // Validation
  useEffect(() => {
    let error: string | null = null;
    
    if (charCount === 0) {
      error = 'Message cannot be empty';
    } else if (charCount > maxLength) {
      error = `Message exceeds maximum length of ${maxLength} characters`;
    } else if (encodingCapacity > 0 && !messageFitsCapacity) {
      error = `Message too long for audio capacity (max ${encodingCapacity} bytes)`;
    }
    
    setValidationError(error);
    onValidationChange?.(error === null);
  }, [value, charCount, maxLength, encodingCapacity, messageFitsCapacity, onValidationChange]);
  
  const handleChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= maxLength) {
      onChange(newValue);
    }
  }, [onChange, maxLength]);
  
  const toggleEncryption = useCallback(() => {
    if (useStore) {
      updateSettings({ encryption: !settings.encryption });
    }
  }, [useStore, settings.encryption, updateSettings]);
  
  // Determine character count color
  const getCharCountColor = () => {
    if (charPercentage > 90) return 'text-red-500';
    if (charPercentage > 75) return 'text-yellow-500';
    return 'text-gray-500';
  };
  
  return (
    <div className={`space-y-2 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <label htmlFor="message-input" className="text-sm font-medium text-gray-700">
          Secret Message
        </label>
        <button
          onClick={toggleEncryption}
          className="flex items-center gap-1 text-xs text-gray-600 hover:text-gray-800 transition-colors"
          aria-label={settings.encryption ? 'Disable encryption' : 'Enable encryption'}
        >
          {settings.encryption ? (
            <>
              <Lock className="w-3 h-3" />
              <span>Encrypted</span>
            </>
          ) : (
            <>
              <Unlock className="w-3 h-3" />
              <span>Not Encrypted</span>
            </>
          )}
        </button>
      </div>
      
      {/* Textarea */}
      <div className="relative">
        <textarea
          id="message-input"
          value={value}
          onChange={handleChange}
          placeholder="Enter your secret message here..."
          className={`
            w-full px-3 py-2 border rounded-md shadow-sm
            focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            resize-vertical min-h-[100px] max-h-[300px]
            ${validationError ? 'border-red-300' : 'border-gray-300'}
          `}
          aria-invalid={!!validationError}
          aria-describedby={validationError ? 'message-error' : undefined}
        />
        
        {/* Character count indicator */}
        <div className="absolute bottom-2 right-2 text-xs">
          <span className={getCharCountColor()}>
            {charCount} / {maxLength}
          </span>
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full transition-all duration-300 ${
            charPercentage > 90 ? 'bg-red-500' :
            charPercentage > 75 ? 'bg-yellow-500' :
            'bg-blue-500'
          }`}
          style={{ width: `${Math.min(charPercentage, 100)}%` }}
        />
      </div>
      
      {/* Error message */}
      {validationError && (
        <div
          id="message-error"
          className="flex items-center gap-1 text-sm text-red-600"
          role="alert"
        >
          <AlertCircle className="w-4 h-4" />
          <span>{validationError}</span>
        </div>
      )}
      
      {/* Helper text */}
      {!validationError && (
        <div className="space-y-1">
          <p className="text-xs text-gray-500">
            Your message will be {settings.encryption ? 'encrypted and ' : ''}embedded in the audio using ultrasonic frequencies.
          </p>
          {encodingCapacity > 0 && (
            <p className="text-xs text-gray-500 flex items-center gap-1">
              <Info className="w-3 h-3" />
              Audio capacity: {encodingCapacity} bytes available
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default MessageInput;