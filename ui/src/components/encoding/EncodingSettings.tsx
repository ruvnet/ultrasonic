import React, { useState, useCallback } from 'react';
import { Settings, Info, ChevronDown, ChevronUp } from 'lucide-react';

export interface EncodingSettings {
  baseFrequency: number;
  frequencyRange: number;
  bitDuration: number;
  amplitude: number;
  errorCorrection: 'none' | 'basic' | 'advanced';
  encryption: boolean;
  compressionLevel: number;
}

export interface EncodingPreset {
  name: string;
  description: string;
  settings: EncodingSettings;
}

interface EncodingSettingsProps {
  settings: EncodingSettings;
  onChange: (settings: EncodingSettings) => void;
  presets?: EncodingPreset[];
  showAdvanced?: boolean;
  className?: string;
}

const defaultPresets: EncodingPreset[] = [
  {
    name: 'Quick',
    description: 'Fast encoding with basic error correction',
    settings: {
      baseFrequency: 19000,
      frequencyRange: 2000,
      bitDuration: 50,
      amplitude: 0.5,
      errorCorrection: 'basic',
      encryption: true,
      compressionLevel: 5
    }
  },
  {
    name: 'Balanced',
    description: 'Good balance of speed and reliability',
    settings: {
      baseFrequency: 19500,
      frequencyRange: 3000,
      bitDuration: 75,
      amplitude: 0.7,
      errorCorrection: 'advanced',
      encryption: true,
      compressionLevel: 6
    }
  },
  {
    name: 'Robust',
    description: 'Maximum reliability for noisy environments',
    settings: {
      baseFrequency: 20000,
      frequencyRange: 4000,
      bitDuration: 100,
      amplitude: 0.9,
      errorCorrection: 'advanced',
      encryption: true,
      compressionLevel: 7
    }
  }
];

export const EncodingSettings: React.FC<EncodingSettingsProps> = ({
  settings,
  onChange,
  presets = defaultPresets,
  showAdvanced: initialShowAdvanced = false,
  className = ''
}) => {
  const [showAdvanced, setShowAdvanced] = useState(initialShowAdvanced);
  const [selectedPreset, setSelectedPreset] = useState<string | null>(null);
  
  const handlePresetChange = useCallback((presetName: string) => {
    const preset = presets.find(p => p.name === presetName);
    if (preset) {
      onChange(preset.settings);
      setSelectedPreset(presetName);
    }
  }, [presets, onChange]);
  
  const handleSettingChange = useCallback(<K extends keyof EncodingSettings>(
    key: K,
    value: EncodingSettings[K]
  ) => {
    onChange({ ...settings, [key]: value });
    setSelectedPreset(null); // Clear preset selection on manual change
  }, [settings, onChange]);
  
  const toggleAdvanced = useCallback(() => {
    setShowAdvanced(prev => !prev);
  }, []);
  
  // Calculate estimated capacity
  const estimatedCapacity = Math.floor(
    (1000 / settings.bitDuration) * 
    (settings.errorCorrection === 'advanced' ? 0.5 : 
     settings.errorCorrection === 'basic' ? 0.75 : 1)
  );
  
  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center gap-2">
        <Settings className="w-5 h-5 text-gray-600" />
        <h3 className="text-lg font-medium text-gray-800">Encoding Settings</h3>
      </div>
      
      {/* Presets */}
      <div>
        <label className="text-sm font-medium text-gray-700 mb-2 block">
          Preset Configuration
        </label>
        <div className="grid grid-cols-3 gap-2">
          {presets.map(preset => (
            <button
              key={preset.name}
              onClick={() => handlePresetChange(preset.name)}
              className={`
                px-3 py-2 rounded-md border transition-all
                ${selectedPreset === preset.name
                  ? 'bg-blue-50 border-blue-500 text-blue-700'
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                }
              `}
              aria-pressed={selectedPreset === preset.name}
            >
              <div className="font-medium text-sm">{preset.name}</div>
              <div className="text-xs opacity-75 mt-0.5">{preset.description}</div>
            </button>
          ))}
        </div>
      </div>
      
      {/* Basic Settings */}
      <div className="space-y-3">
        {/* Frequency */}
        <div>
          <label htmlFor="base-frequency" className="text-sm font-medium text-gray-700 flex items-center gap-1">
            Base Frequency
            <Info className="w-3 h-3 text-gray-400" title="Center frequency for encoding" />
          </label>
          <div className="mt-1 flex items-center gap-2">
            <input
              id="base-frequency"
              type="range"
              min="18000"
              max="22050"
              step="100"
              value={settings.baseFrequency}
              onChange={(e) => handleSettingChange('baseFrequency', Number(e.target.value))}
              className="flex-1"
            />
            <span className="text-sm text-gray-600 w-16 text-right">
              {(settings.baseFrequency / 1000).toFixed(1)} kHz
            </span>
          </div>
        </div>
        
        {/* Amplitude */}
        <div>
          <label htmlFor="amplitude" className="text-sm font-medium text-gray-700 flex items-center gap-1">
            Signal Strength
            <Info className="w-3 h-3 text-gray-400" title="Volume of the ultrasonic signal" />
          </label>
          <div className="mt-1 flex items-center gap-2">
            <input
              id="amplitude"
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={settings.amplitude}
              onChange={(e) => handleSettingChange('amplitude', Number(e.target.value))}
              className="flex-1"
            />
            <span className="text-sm text-gray-600 w-16 text-right">
              {(settings.amplitude * 100).toFixed(0)}%
            </span>
          </div>
        </div>
        
        {/* Error Correction */}
        <div>
          <label htmlFor="error-correction" className="text-sm font-medium text-gray-700">
            Error Correction
          </label>
          <select
            id="error-correction"
            value={settings.errorCorrection}
            onChange={(e) => handleSettingChange('errorCorrection', e.target.value as any)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="none">None (Fastest)</option>
            <option value="basic">Basic (Recommended)</option>
            <option value="advanced">Advanced (Most Reliable)</option>
          </select>
        </div>
      </div>
      
      {/* Advanced Settings Toggle */}
      <button
        onClick={toggleAdvanced}
        className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
      >
        {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        Advanced Settings
      </button>
      
      {/* Advanced Settings */}
      {showAdvanced && (
        <div className="space-y-3 pt-2 border-t border-gray-200">
          {/* Frequency Range */}
          <div>
            <label htmlFor="frequency-range" className="text-sm font-medium text-gray-700">
              Frequency Range
            </label>
            <div className="mt-1 flex items-center gap-2">
              <input
                id="frequency-range"
                type="range"
                min="500"
                max="5000"
                step="100"
                value={settings.frequencyRange}
                onChange={(e) => handleSettingChange('frequencyRange', Number(e.target.value))}
                className="flex-1"
              />
              <span className="text-sm text-gray-600 w-16 text-right">
                {settings.frequencyRange} Hz
              </span>
            </div>
          </div>
          
          {/* Bit Duration */}
          <div>
            <label htmlFor="bit-duration" className="text-sm font-medium text-gray-700">
              Bit Duration
            </label>
            <div className="mt-1 flex items-center gap-2">
              <input
                id="bit-duration"
                type="range"
                min="10"
                max="100"
                step="5"
                value={settings.bitDuration}
                onChange={(e) => handleSettingChange('bitDuration', Number(e.target.value))}
                className="flex-1"
              />
              <span className="text-sm text-gray-600 w-16 text-right">
                {settings.bitDuration} ms
              </span>
            </div>
          </div>
          
          {/* Compression Level */}
          <div>
            <label htmlFor="compression" className="text-sm font-medium text-gray-700">
              Compression Level
            </label>
            <div className="mt-1 flex items-center gap-2">
              <input
                id="compression"
                type="range"
                min="0"
                max="9"
                step="1"
                value={settings.compressionLevel}
                onChange={(e) => handleSettingChange('compressionLevel', Number(e.target.value))}
                className="flex-1"
              />
              <span className="text-sm text-gray-600 w-16 text-right">
                {settings.compressionLevel}
              </span>
            </div>
          </div>
        </div>
      )}
      
      {/* Capacity Indicator */}
      <div className="bg-gray-50 rounded-md p-3">
        <div className="text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Estimated Capacity:</span>
            <span className="font-medium">{estimatedCapacity} chars/sec</span>
          </div>
          <div className="flex justify-between mt-1">
            <span>Frequency Range:</span>
            <span className="font-medium">
              {(settings.baseFrequency / 1000).toFixed(1)} - 
              {((settings.baseFrequency + settings.frequencyRange) / 1000).toFixed(1)} kHz
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EncodingSettings;