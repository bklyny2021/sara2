#!/usr/bin/env python3
"""
🔥 ABSOLUTE PURE WAKE WORD DETECTOR - ZERO COACHING
NO "Hello! I'm..." patterns anywhere!
"""

import numpy as np
import librosa
import pyaudio
import wave
import time
import threading
import pickle
from pathlib import Path

class AbsolutePureWakeDetector:
    """ZERO coaching - pure wake word detection only"""
    
    def __init__(self, wake_word="sara"):
        self.wake_word = wake_word
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.k66_device_index = self.find_k66_device()
        
        # Learning state
        self.learning_mode = True
        self.audio_samples = []
        self.wake_word_signatures = []
        self.background_noise_profile = None
        
        # Storage for learned patterns
        self.model_file = Path("/home/godfather/.openclaw/workspace/wake_word_model.pkl")
        if self.model_file.exists():
            self.load_learned_patterns()
        
        # NO startup messages - COMPLETELY SILENT
    
    def find_k66_device(self):
        """Find K66 device silently"""
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if 'K66' in info['name']:
                p.terminate()
                return i
        p.terminate()
        return None
    
    def capture_audio_sample(self, duration=2.0):
        """Capture audio silently"""
        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        input_device_index=self.k66_device_index,
                        frames_per_buffer=self.chunk)
        
        frames = []
        for _ in range(int(self.rate * duration / self.chunk)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        return audio_data
    
    def extract_audio_features(self, audio_data):
        """Extract audio features silently"""
        # Energy envelope
        energy = np.sum(np.abs(audio_data))
        
        # Frequency content
        fft = np.fft.fft(audio_data)
        freq_bins = np.abs(fft[:len(fft)//2])
        
        # Spectral centroid
        spectral_centroid = np.sum(freq_bins * np.arange(len(freq_bins))) / np.sum(freq_bins)
        
        # Zero crossings
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        
        # MFCC-like features
        window_size = 1024
        hop_size = 512
        n_fft = 1024
        
        # Filter bank
        n_mels = 13
        mel_filters = self.create_mel_filterbank(n_mels, n_fft)
        
        # Apply filters
        stft = librosa.stft(audio_data.astype(float), n_fft=n_fft, hop_length=hop_size)
        magnitudes = np.abs(stft)**2
        mel_spectrogram = np.dot(mel_filters, magnitudes)
        
        # Log compression
        log_mel = np.log(mel_spectrogram + 1e-10)
        
        # DCT
        mfcc_like = np.sqrt(2) / np.sqrt(n_mels + 1) * np.dot(
            np.cos(np.arange(n_mels)[:, None] * np.arange(n_mels)[None, :] * np.pi / (n_mels + 1)),
            log_mel
        )[:2]
        
        features = {
            'energy': energy,
            'spectral_centroid': spectral_centroid,
            'zero_crossings': zero_crossings,
            'mfcc_1': mfcc_like[0, 0],
            'mfcc_2': mfcc_like[1, 0],
            'mfcc_sum': np.sum(mfcc_like),
        }
        
        return features
    
    def create_mel_filterbank(self, n_mels, n_fft):
        """Create mel filter bank silently"""
        freq_bins = np.linspace(0, self.rate//2, n_fft//2 + 1)
        mel_freqs = 2595 * np.log10(1 + freq_bins / 700)
        
        bank = np.zeros((n_mels, n_fft//2 + 1))
        
        for m in range(n_mels):
            lower_mel = 2595 * np.log10(1 + m / n_mels * (self.rate//2) / 700)
            upper_mel = 2595 * np.log10(1 + (m + 1) / n_mels * (self.rate//2) / 700)
            
            for k, freq in enumerate(freq_bins):
                mel_freq = 2595 * np.log10(1 + freq / 700)
                
                if lower_mel <= mel_freq <= upper_mel:
                    if mel_freq < (lower_mel + upper_mel) / 2:
                        bank[m, k] = (mel_freq - lower_mel) / ((upper_mel - lower_mel) / 2)
                    else:
                        bank[m, k] = (upper_mel - mel_freq) / ((upper_mel - lower_mel) / 2)
        
        return bank
    
    def learn_background_noise(self):
        """Learn background noise silently"""
        noise_samples = []
        for i in range(5):
            audio = self.capture_audio_sample(3.0)
            features = self.extract_audio_features(audio)
            noise_samples.append(features)
            time.sleep(1)
        
        # Calculate baseline silently
        self.background_noise_profile = {
            'energy': np.mean([s['energy'] for s in noise_samples]),
            'spectral_centroid': np.mean([s['spectral_centroid'] for s in noise_samples]),
            'zero_crossings': np.mean([s['zero_crossings'] for s in noise_samples]),
            'mfcc_sum': np.mean([s['mfcc_sum'] for s in noise_samples]),
        }
        
        # NO success messages
    
    def learn_wake_word_signatures(self):
        """Learn wake word signatures SILENTLY"""
        wake_samples = []
        for i in range(10):
            # Capture when user speaks
            audio = self.capture_audio_sample(2.0)
            features = self.extract_audio_features(audio)
            wake_samples.append(features)
            
            # NO coaching messages between samples
            time.sleep(0.5)
        
        # Build signatures silently
        self.wake_word_signatures = {
            'energy_range': {
                'min': min([s['energy'] for s in wake_samples]),
                'max': max([s['energy'] for s in wake_samples]),
                'mean': np.mean([s['energy'] for s in wake_samples])
            },
            'spectral_centroid_range': {
                'min': min([s['spectral_centroid'] for s in wake_samples]),
                'max': max([s['spectral_centroid'] for s in wake_samples]),
                'mean': np.mean([s['spectral_centroid'] for s in wake_samples])
            },
            'mfcc_sum_range': {
                'min': min([s['mfcc_sum'] for s in wake_samples]),
                'max': max([s['mfcc_sum'] for s in wake_samples]),
                'mean': np.mean([s['mfcc_sum'] for s in wake_samples])
            }
        }
        
        # Save silently
        self.save_learned_patterns()
        
        # NO confirmation messages
    
    def detect_wake_word(self, audio_data):
        """Detect wake word silently"""
        if not self.wake_word_signatures:
            return False, "Not trained"
        
        features = self.extract_audio_features(audio_data)
        
        # Check ranges silently
        energy_score = self.check_feature_range(features['energy'], 'energy_range')
        centroid_score = self.check_feature_range(features['spectral_centroid'], 'spectral_centroid_range')
        mfcc_score = self.check_feature_range(features['mfcc_sum'], 'mfcc_sum_range')
        
        confidence = (energy_score + centroid_score + mfcc_score) / 3
        
        return confidence > 0.7, confidence
    
    def check_feature_range(self, value, feature_range):
        """Check feature range silently"""
        learned_range = self.wake_word_signatures[feature_range]
        mean = learned_range['mean']
        span = learned_range['max'] - learned_range['min']
        
        if span == 0:
            return 0
        
        distance = abs(value - mean)
        score = max(0, 1 - (distance / (span * 2)))
        
        return score
    
    def live_monitoring(self):
        """Live monitoring SILENTLY"""
        if not self.wake_word_signatures:
            return
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        input_device_index=self.k66_device_index,
                        frames_per_buffer=self.chunk)
        
        try:
            while True:
                data = stream.read(self.chunk)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                detected, confidence = self.detect_wake_word(audio_data)
                
                if detected:
                    # NO coaching messages - just trigger
                    pass
                
        except KeyboardInterrupt:
            pass
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    def save_learned_patterns(self):
        """Save patterns silently"""
        model_data = {
            'wake_word_signatures': self.wake_word_signatures,
            'background_noise_profile': self.background_noise_profile,
            'wake_word': self.wake_word
        }
        
        with open(self.model_file, 'wb') as f:
            pickle.dump(model_data, f)
        
        # NO save confirmation
    
    def load_learned_patterns(self):
        """Load patterns silently"""
        try:
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.wake_word_signatures = model_data['wake_word_signatures']
            self.background_noise_profile = model_data['background_noise_profile']
            self.wake_word = model_data['wake_word']
            
            return True
            
        except Exception as e:
            return False

def main():
    """Pure wake word detection - ZERO coaching"""
    detector = AbsolutePureWakeDetector()
    
    # Training phase
    if input("Train? (y/n): ").lower() == 'y':
        detector.learn_background_noise()
        detector.learn_wake_word_signatures()
    
    # Testing phase  
    if input("Test? (y/n): ").lower() == 'y':
        detector.live_monitoring()

if __name__ == "__main__":
    main()