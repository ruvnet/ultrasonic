import { http, HttpResponse } from 'msw'
import type {
  EmbedResponse,
  DecodeResponse,
  AnalyzeResponse,
  ConfigResponse,
  HealthResponse,
  InfoResponse,
} from '@/types/api'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const handlers = [
  // Health endpoint
  http.get(`${API_URL}/health`, () => {
    return HttpResponse.json<HealthResponse>({
      status: 'healthy',
      message: 'Steganography service is running',
    })
  }),

  // Info endpoint
  http.get(`${API_URL}/info`, () => {
    return HttpResponse.json<InfoResponse>({
      name: 'Agentic Commands Steganography API',
      version: '1.0.0',
      description: 'API for embedding and decoding encrypted commands in audio/video files',
      supportedFormats: {
        audio: ['.mp3', '.wav', '.flac', '.ogg', '.m4a'],
        video: ['.mp4', '.avi', '.mov', '.mkv'],
      },
      endpoints: {
        embed: ['/embed/audio', '/embed/video'],
        decode: ['/decode/audio', '/decode/video'],
        analyze: ['/analyze/audio', '/analyze/video'],
      },
      encryption: 'AES-256-GCM',
      steganography: 'Ultrasonic FSK',
    })
  }),

  // Embed audio endpoint
  http.post(`${API_URL}/embed/audio`, async ({ request }) => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const formData = await request.formData()
    const command = formData.get('command') as string

    return HttpResponse.json<EmbedResponse>({
      success: true,
      message: 'Command successfully embedded',
      outputFile: `encoded_${Date.now()}.wav`,
      fileSizeBytes: 2456789,
      processingTimeMs: 234.5,
      ultrasonicFreq: 19500,
      amplitude: 0.1,
    })
  }),

  // Decode audio endpoint
  http.post(`${API_URL}/decode/audio`, async () => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Randomly return success or no command found
    const hasCommand = Math.random() > 0.3

    if (hasCommand) {
      return HttpResponse.json<DecodeResponse>({
        success: true,
        message: 'Command decoded successfully',
        command: 'execute:status_check',
        processingTimeMs: 156.2,
        confidenceScore: 0.95,
        encryptionDetected: true,
        detectedFrequencies: [18500, 19500],
      })
    } else {
      return HttpResponse.json<DecodeResponse>({
        success: false,
        message: 'No command found in audio file',
        processingTimeMs: 156.2,
      })
    }
  }),

  // Analyze audio endpoint
  http.post(`${API_URL}/analyze/audio`, async () => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    return HttpResponse.json<AnalyzeResponse>({
      success: true,
      message: 'Analysis complete',
      signalDetected: true,
      signalStrength: 0.85,
      frequencyRange: [18500, 19500],
      duration: 2.5,
      sampleRate: 44100,
      estimatedPayloadSize: 32,
    })
  }),

  // Embed video endpoint
  http.post(`${API_URL}/embed/video`, async ({ request }) => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 3000))

    const formData = await request.formData()
    const command = formData.get('command') as string

    return HttpResponse.json<EmbedResponse>({
      success: true,
      message: 'Command successfully embedded in video',
      outputFile: `encoded_video_${Date.now()}.mp4`,
      fileSizeBytes: 15678901,
      processingTimeMs: 1234.5,
      ultrasonicFreq: 19500,
      amplitude: 0.1,
    })
  }),

  // Decode video endpoint
  http.post(`${API_URL}/decode/video`, async () => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 2500))

    return HttpResponse.json<DecodeResponse>({
      success: true,
      message: 'Command decoded from video',
      command: 'configure:mode=stealth',
      processingTimeMs: 256.2,
      confidenceScore: 0.92,
      encryptionDetected: true,
      detectedFrequencies: [18500, 19500],
    })
  }),

  // Analyze video endpoint
  http.post(`${API_URL}/analyze/video`, async () => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    return HttpResponse.json<AnalyzeResponse>({
      success: true,
      message: 'Video analysis complete',
      signalDetected: true,
      signalStrength: 0.78,
      frequencyRange: [18500, 19500],
      duration: 5.2,
      sampleRate: 48000,
      estimatedPayloadSize: 48,
    })
  }),

  // Configure frequencies endpoint
  http.post(`${API_URL}/config/frequencies`, async ({ request }) => {
    const formData = await request.formData()
    const freq0 = Number(formData.get('freq_0'))
    const freq1 = Number(formData.get('freq_1'))

    return HttpResponse.json<ConfigResponse>({
      success: true,
      message: `Frequencies updated to ${freq0} Hz and ${freq1} Hz`,
      freq0,
      freq1,
    })
  }),

  // Configure key endpoint
  http.post(`${API_URL}/config/key`, async () => {
    return HttpResponse.json<ConfigResponse>({
      success: true,
      message: 'Encryption key updated successfully',
    })
  }),
]