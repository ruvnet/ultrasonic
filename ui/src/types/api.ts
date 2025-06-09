// API Request/Response Types

export interface EmbedAudioRequest {
  audioFile: File
  command: string
  obfuscate?: boolean
  bitrate?: string
  ultrasonicFreq?: number
  amplitude?: number
}

export interface EmbedVideoRequest {
  videoFile: File
  command: string
  obfuscate?: boolean
  audioBitrate?: string
  ultrasonicFreq?: number
  amplitude?: number
}

export interface DecodeRequest {
  file: File
  detailedAnalysis?: boolean
}

export interface AnalyzeRequest {
  file: File
}

export interface ConfigFrequenciesRequest {
  freq0: number
  freq1: number
}

export interface ConfigKeyRequest {
  keyBase64?: string
  keyFilePath?: string
  generateNew?: boolean
}

// Response types
export interface BaseResponse {
  success: boolean
  message: string
}

export interface EmbedResponse extends BaseResponse {
  outputFile?: string
  fileSizeBytes?: number
  processingTimeMs?: number
  ultrasonicFreq?: number
  amplitude?: number
}

export interface DecodeResponse extends BaseResponse {
  command?: string
  processingTimeMs?: number
  confidenceScore?: number
  analysis?: string
  encryptionDetected?: boolean
  detectedFrequencies?: number[]
}

export interface AnalyzeResponse extends BaseResponse {
  signalDetected: boolean
  signalStrength: number
  frequencyRange: [number, number]
  duration: number
  sampleRate: number
  estimatedPayloadSize: number
}

export interface ConfigResponse extends BaseResponse {
  freq0?: number
  freq1?: number
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy'
  message: string
}

export interface InfoResponse {
  name: string
  version: string
  description: string
  supportedFormats: {
    audio: string[]
    video: string[]
  }
  endpoints: {
    embed: string[]
    decode: string[]
    analyze: string[]
  }
  encryption: string
  steganography: string
}