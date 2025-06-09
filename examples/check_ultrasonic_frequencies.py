#!/usr/bin/env python3
"""
Diagnostic tool to check if ultrasonic frequencies are preserved in an audio file.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import signal
from pydub import AudioSegment
import matplotlib.pyplot as plt

def analyze_frequency_content(audio_file, plot=False):
    """
    Analyze the frequency content of an audio file.
    
    Args:
        audio_file: Path to audio file
        plot: Whether to display a frequency plot
        
    Returns:
        Dictionary with frequency analysis results
    """
    print(f"\nAnalyzing frequency content of: {audio_file}")
    print("-" * 60)
    
    try:
        # Load audio file
        audio = AudioSegment.from_file(audio_file)
        
        # Get audio properties
        sample_rate = audio.frame_rate
        nyquist = sample_rate / 2
        
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Nyquist frequency: {nyquist} Hz")
        print(f"Duration: {len(audio) / 1000:.2f} seconds")
        print(f"Channels: {audio.channels}")
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # If stereo, use first channel
        if audio.channels == 2:
            samples = samples[0::2]
        
        # Compute frequency spectrum using FFT
        freqs, psd = signal.periodogram(samples, sample_rate)
        
        # Find frequencies with significant energy
        # Normalize PSD
        psd_normalized = psd / np.max(psd)
        
        # Find frequencies above certain thresholds
        threshold_levels = [0.1, 0.01, 0.001]
        
        print("\nFrequency content analysis:")
        for threshold in threshold_levels:
            significant_freqs = freqs[psd_normalized > threshold]
            if len(significant_freqs) > 0:
                max_freq = np.max(significant_freqs)
                print(f"  Max frequency > {threshold*100}% power: {max_freq:.0f} Hz")
            else:
                print(f"  No frequencies > {threshold*100}% power")
        
        # Check ultrasonic range (> 15 kHz)
        ultrasonic_mask = freqs > 15000
        ultrasonic_psd = psd[ultrasonic_mask]
        ultrasonic_freqs = freqs[ultrasonic_mask]
        
        if len(ultrasonic_psd) > 0 and np.max(ultrasonic_psd) > 0:
            ultrasonic_power_ratio = np.sum(ultrasonic_psd) / np.sum(psd)
            peak_ultrasonic_freq = ultrasonic_freqs[np.argmax(ultrasonic_psd)]
            
            print(f"\nUltrasonic analysis (>15 kHz):")
            print(f"  Power ratio: {ultrasonic_power_ratio:.6f} ({ultrasonic_power_ratio*100:.4f}%)")
            print(f"  Peak frequency: {peak_ultrasonic_freq:.0f} Hz")
            
            # Check specific ultrasonic embedding range (18-20 kHz)
            embedding_mask = (freqs >= 18000) & (freqs <= 20000)
            embedding_psd = psd[embedding_mask]
            if len(embedding_psd) > 0 and np.max(embedding_psd) > 0:
                embedding_power = np.sum(embedding_psd) / np.sum(psd)
                print(f"  18-20 kHz power ratio: {embedding_power:.6f} ({embedding_power*100:.4f}%)")
        else:
            print(f"\nNo significant ultrasonic content detected (>15 kHz)")
        
        # Plot if requested
        if plot:
            plt.figure(figsize=(12, 6))
            
            # Full spectrum
            plt.subplot(1, 2, 1)
            plt.semilogy(freqs, psd)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power Spectral Density')
            plt.title('Full Frequency Spectrum')
            plt.grid(True)
            plt.xlim(0, nyquist)
            
            # Ultrasonic range zoom
            plt.subplot(1, 2, 2)
            ultrasonic_range = (freqs >= 15000) & (freqs <= nyquist)
            plt.semilogy(freqs[ultrasonic_range], psd[ultrasonic_range])
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power Spectral Density')
            plt.title('Ultrasonic Range (15+ kHz)')
            plt.grid(True)
            plt.xlim(15000, min(25000, nyquist))
            
            plt.tight_layout()
            plt.show()
        
        # Return analysis results
        return {
            'sample_rate': sample_rate,
            'nyquist': nyquist,
            'has_ultrasonic': ultrasonic_power_ratio > 0.0001 if 'ultrasonic_power_ratio' in locals() else False,
            'ultrasonic_power_ratio': ultrasonic_power_ratio if 'ultrasonic_power_ratio' in locals() else 0,
            'peak_ultrasonic_freq': peak_ultrasonic_freq if 'peak_ultrasonic_freq' in locals() else None,
            'format': os.path.splitext(audio_file)[1][1:].upper()
        }
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None


def compare_files(original_file, embedded_file):
    """Compare frequency content between original and embedded files."""
    print("\n" + "=" * 70)
    print("FREQUENCY CONTENT COMPARISON")
    print("=" * 70)
    
    # Analyze both files
    original_analysis = analyze_frequency_content(original_file)
    embedded_analysis = analyze_frequency_content(embedded_file)
    
    if original_analysis and embedded_analysis:
        print("\n" + "=" * 70)
        print("COMPARISON SUMMARY")
        print("=" * 70)
        
        print(f"\nOriginal file ({original_analysis['format']}):")
        print(f"  Sample rate: {original_analysis['sample_rate']} Hz")
        print(f"  Has ultrasonic: {original_analysis['has_ultrasonic']}")
        if original_analysis['has_ultrasonic']:
            print(f"  Ultrasonic power: {original_analysis['ultrasonic_power_ratio']*100:.4f}%")
        
        print(f"\nEmbedded file ({embedded_analysis['format']}):")
        print(f"  Sample rate: {embedded_analysis['sample_rate']} Hz")
        print(f"  Has ultrasonic: {embedded_analysis['has_ultrasonic']}")
        if embedded_analysis['has_ultrasonic']:
            print(f"  Ultrasonic power: {embedded_analysis['ultrasonic_power_ratio']*100:.4f}%")
            print(f"  Peak ultrasonic: {embedded_analysis['peak_ultrasonic_freq']:.0f} Hz")
        
        # Verdict
        print("\nVERDICT:")
        if embedded_analysis['has_ultrasonic'] and embedded_analysis['ultrasonic_power_ratio'] > 0.0001:
            print("✓ Ultrasonic frequencies are preserved!")
            print("  The embedded signal should be decodable.")
        else:
            print("✗ Ultrasonic frequencies are NOT well preserved.")
            print("  The embedded signal may not be decodable.")
            print(f"  Consider using WAV or FLAC format instead of {embedded_analysis['format']}.")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python check_ultrasonic_frequencies.py <audio_file> [compare_with_file]")
        print("\nExamples:")
        print("  python check_ultrasonic_frequencies.py embedded_audio.wav")
        print("  python check_ultrasonic_frequencies.py original.mp3 embedded.mp3")
        return
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found")
        return
    
    if len(sys.argv) >= 3:
        # Compare mode
        compare_file = sys.argv[2]
        if not os.path.exists(compare_file):
            print(f"Error: File '{compare_file}' not found")
            return
        compare_files(audio_file, compare_file)
    else:
        # Single file analysis
        analyze_frequency_content(audio_file, plot=False)
        
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS:")
        print("=" * 70)
        print("For best ultrasonic embedding results:")
        print("- Use WAV format (uncompressed)")
        print("- Use FLAC format (lossless compression)")
        print("- Ensure sample rate is at least 44.1 kHz (48 kHz preferred)")
        print("- Avoid MP3, AAC, or OGG formats for ultrasonic frequencies")


if __name__ == "__main__":
    main()