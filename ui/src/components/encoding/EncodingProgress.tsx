import React, { useEffect, useState } from 'react';
import { Loader2, CheckCircle, AlertCircle, Volume2 } from 'lucide-react';

interface EncodingProgressProps {
  isActive: boolean;
  progress?: number; // 0-100, or -1 for indeterminate
  status?: string;
  stage?: 'preparing' | 'encoding' | 'finalizing' | 'complete' | 'error';
  error?: string;
  className?: string;
}

export const EncodingProgress: React.FC<EncodingProgressProps> = ({
  isActive,
  progress = -1,
  status = 'Processing...',
  stage = 'encoding',
  error,
  className = ''
}) => {
  const [animatedProgress, setAnimatedProgress] = useState(0);

  // Animate progress changes
  useEffect(() => {
    if (progress >= 0) {
      const timer = setTimeout(() => {
        setAnimatedProgress(progress);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [progress]);

  // Stage icons and colors
  const getStageIcon = () => {
    switch (stage) {
      case 'preparing':
        return <Loader2 className="w-5 h-5 animate-spin" />;
      case 'encoding':
        return <Volume2 className="w-5 h-5" />;
      case 'finalizing':
        return <Loader2 className="w-5 h-5 animate-spin" />;
      case 'complete':
        return <CheckCircle className="w-5 h-5" />;
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      default:
        return <Loader2 className="w-5 h-5 animate-spin" />;
    }
  };

  const getStageColor = () => {
    switch (stage) {
      case 'complete':
        return 'text-green-600 bg-green-50';
      case 'error':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-blue-600 bg-blue-50';
    }
  };

  const getProgressBarColor = () => {
    switch (stage) {
      case 'complete':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-blue-500';
    }
  };

  if (!isActive && stage !== 'complete' && stage !== 'error') {
    return null;
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getStageColor()}`}>
          {getStageIcon()}
        </div>
        <div className="flex-1">
          <p className="font-medium text-gray-900">
            {stage === 'complete' ? 'Encoding Complete' : 
             stage === 'error' ? 'Encoding Failed' : 
             'Encoding in Progress'}
          </p>
          <p className="text-sm text-gray-600">{error || status}</p>
        </div>
        {progress >= 0 && stage === 'encoding' && (
          <div className="text-2xl font-bold text-gray-900">
            {Math.round(progress)}%
          </div>
        )}
      </div>

      {/* Progress Bar */}
      {(progress >= 0 || stage === 'encoding') && stage !== 'complete' && stage !== 'error' && (
        <div className="relative">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            {progress >= 0 ? (
              <div
                className={`h-full transition-all duration-500 ease-out ${getProgressBarColor()}`}
                style={{ width: `${animatedProgress}%` }}
              />
            ) : (
              <div className={`h-full ${getProgressBarColor()} indeterminate-progress`} />
            )}
          </div>
        </div>
      )}

      {/* Stage indicators */}
      {stage === 'encoding' && (
        <div className="mt-4 grid grid-cols-3 gap-2">
          <StageIndicator
            label="Preparing"
            isActive={stage === 'preparing'}
            isComplete={true}
          />
          <StageIndicator
            label="Encoding"
            isActive={stage === 'encoding'}
            isComplete={false}
          />
          <StageIndicator
            label="Finalizing"
            isActive={stage === 'finalizing'}
            isComplete={false}
          />
        </div>
      )}

      {/* Additional info for encoding stage */}
      {stage === 'encoding' && progress >= 0 && (
        <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Time elapsed</p>
            <p className="font-medium text-gray-900">
              {formatTime(Math.floor((Date.now() - startTime) / 1000))}
            </p>
          </div>
          <div>
            <p className="text-gray-500">Time remaining</p>
            <p className="font-medium text-gray-900">
              {progress > 0 ? formatTime(estimateTimeRemaining(progress)) : '--:--'}
            </p>
          </div>
        </div>
      )}

      <style jsx>{`
        .indeterminate-progress {
          animation: indeterminate 1.5s infinite ease-in-out;
          width: 40%;
        }

        @keyframes indeterminate {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(250%);
          }
        }
      `}</style>
    </div>
  );
};

// Helper component for stage indicators
interface StageIndicatorProps {
  label: string;
  isActive: boolean;
  isComplete: boolean;
}

const StageIndicator: React.FC<StageIndicatorProps> = ({ label, isActive, isComplete }) => {
  return (
    <div className={`text-center ${isActive ? 'opacity-100' : 'opacity-50'}`}>
      <div className={`
        w-2 h-2 mx-auto rounded-full mb-1
        ${isComplete ? 'bg-green-500' : isActive ? 'bg-blue-500' : 'bg-gray-300'}
      `} />
      <p className="text-xs text-gray-600">{label}</p>
    </div>
  );
};

// Helper functions
let startTime = Date.now();

const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

const estimateTimeRemaining = (progress: number): number => {
  if (progress === 0) return 0;
  const elapsed = (Date.now() - startTime) / 1000;
  const total = elapsed / (progress / 100);
  return Math.max(0, Math.floor(total - elapsed));
};

export default EncodingProgress;