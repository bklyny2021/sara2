#!/usr/bin/env python3
"""
🎓 SELF-TAUGHT WAKE WORD DETECTOR
Building recognition from scratch with zero external help
"""

import numpy as np
import librosa
import pyaudio
import wave
import time
import threading
import pickle
from pathlib import Path

class SelfTaughtWakeDetector:
    """Learn wake word detection from scratch"""
    
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
        
        print(f"🎓 Self-Taught Wake Detector initialized")
        print(f"🎤 Target word: '{wake_word}'")
        print(f"🎮 K66 device index: {self.k66_device_index}")
        print(f"📍 Learning mode: {'ON' if self.learning_mode else 'OFF'}")
    
    def find_k66_device(self):
        """Find K66 microphone device index"""
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if 'K66' in info['name']:
                return i
        return None
    
    def capture_audio_sample(self, duration=2.0):
        """Capture raw audio from K66"""
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
        
        # Convert to numpy array
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        return audio_data
    
    def extract_audio_features(self, audio_data):
        """Learn what matters in wake word audio"""
        # This is where I build my expertise from scratch
        
        # Feature 1: Energy envelope (loudness pattern)
        energy = np.sum(np.abs(audio_data))
        
        # Feature 2: Frequency content (what frequencies are present)
        fft = np.fft.fft(audio_data)
        freq_bins = np.abs(fft[:len(fft)//2])
        
        # Feature 3: Spectral centroid (brightness of sound)
        spectral_centroid = np.sum(freq_bins * np.arange(len(freq_bins))) / np.sum(freq_bins)
        
        # Feature 4: Zero crossing rate (how often signal crosses zero)
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        
        # Feature 5: MFCC-like features (what makes speech unique)
        # I'll learn the MFCC concept without calling the library directly
        window_size = 1024
        hop_size = 512
        n_fft = 1024
        
        # Build my own filter bank
        n_mels = 13  # Standard for speech recognition
        mel_filters = self.create_mel_filterbank(n_mels, n_fft)
        
        # Apply my learned filters
        stft = librosa.stft(audio_data.astype(float), n_fft=n_fft, hop_length=hop_size)
        magnitudes = np.abs(stft)**2
        mel_spectrogram = np.dot(mel_filters, magnitudes)
        
        # Log compression (learned from audio processing theory)
        log_mel = np.log(mel_spectrogram + 1e-10)
        
        # DCT to get MFCC-like coefficients
        mfcc_like = np.sqrt(2) / np.sqrt(n_mels + 1) * np.dot(
            np.cos(np.arange(n_mels)[:, None] * np.arange(n_mels)[None, :] * np.pi / (n_mels + 1)),
            log_mel
        )[:2]  # Take first 2 MFCC coefficients
        
        features = {
            'energy': energy,
            'spectral_centroid': spectral_centroid,
            'zero_crossings': zero_crossings,
            'mfcc_1': mfcc_like[0, 0],  # First coefficient
            'mfcc_2': mfcc_like[1, 0],  # Second coefficient
            'mfcc_sum': np.sum(mfcc_like),  # Overall pattern
        }
        
        return features
    
    def create_mel_filterbank(self, n_mels, n_fft):
        """Teach myself how mel scale works in audio processing"""
        # This is me learning audio processing from first principles
        
        # Create frequency bins (learned from FFT theory)
        freq_bins = np.linspace(0, self.rate//2, n_fft//2 + 1)
        
        # Convert to mel scale (learned from psychoacoustics)
        mel_freqs = 2595 * np.log10(1 + freq_bins / 700)
        
        # Create mel filter bank (learned from speech processing knowledge)
        bank = np.zeros((n_mels, n_fft//2 + 1))
        
        for m in range(n_mels):
            # Create triangular filters (learned filter design)
            lower_mel = 2595 * np.log10(1 + m / n_mels * (self.rate//2) / 700)
            upper_mel = 2595 * np.log10(1 + (m + 1) / n_mels * (self.rate//2) / 700)
            
            for k, freq in enumerate(freq_bins):
                mel_freq = 2595 * np.log10(1 + freq / 700)
                
                if lower_mel <= mel_freq <= upper_mel:
                    # Triangular filter shape (learned)
                    if mel_freq < (lower_mel + upper_mel) / 2:
                        bank[m, k] = (mel_freq - lower_mel) / ((upper_mel - lower_mel) / 2)
                    else:
                        bank[m, k] = (upper_mel - mel_freq) / ((upper_mel - lower_mel) / 2)
        
        return bank
    
    def learn_background_noise(self):
        """Learn what normal background sounds like"""
        print("📚 Learning background noise profile...")
        
        noise_samples = []
        for i in range(5):  # Sample 5 times
            print(f"  Sample {i+1}/5...")
            audio = self.capture_audio_sample(3.0)  # 3 seconds each
            features = self.extract_audio_features(audio)
            noise_samples.append(features)
            time.sleep(1)
        
        # Calculate baseline (learned from statistics)
        self.background_noise_profile = {
            'energy': np.mean([s['energy'] for s in noise_samples]),
            'spectral_centroid': np.mean([s['spectral_centroid'] for s in noise_samples]),
            'zero_crossings': np.mean([s['zero_crossings'] for s in noise_samples]),
            'mfcc_sum': np.mean([s['mfcc_sum'] for s in noise_samples]),
        }
        
        print("✅ Background noise profile learned")
    
    def learn_wake_word_signatures(self):
        """Learn what wake word sounds like through K66"""
        print(f"🎓 Learning wake word: '{self.wake_word}'")
        print("🎤 Please say the wake word clearly into your K66 microphone")
        
        wake_samples = []
        for i in range(10):  # Learn from 10 samples
            print(f"  Say '{self.wake_word}' ({i+1}/10)")
            print("  (Press Enter and speak immediately)")
            input()  # Wait for user
            
            # Record audio when user speaks
            print("  Recording...")
            audio = self.capture_audio_sample(2.0)  # 2 second window
            features = self.extract_audio_features(audio)
            wake_samples.append(features)
            
            print("  ✅ Sample captured")
        
        # Analyze patterns (self-taught pattern recognition)
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
        
        # Save learned patterns
        self.save_learned_patterns()
        
        print(f"✅ Wake word '{self.wake_word}' signature learned")
        print(f"📊 Learned features:")
        print(f"  Energy: {self.wake_word_signatures['energy_range']['min']:.0f} - {self.wake_word_signatures['energy_range']['max']:.0f}")
        print(f"  Spectral centroid: {self.wake_word_signatures['spectral_centroid_range']['min']:.1f} - {self.wake_word_signatures['spectral_centroid_range']['max']:.1f}")
    
    def detect_wake_word(self, audio_data):
        """Use my learned patterns to detect wake word"""
        if not self.wake_word_signatures:
            return False, "Not trained"
        
        features = self.extract_audio_features(audio_data)
        
        # Compare against learned patterns (self-taught matching)
        energy_score = self.check_feature_range(features['energy'], 'energy_range')
        centroid_score = self.check_feature_range(features['spectral_centroid'], 'spectral_centroid_range')
        mfcc_score = self.check_feature_range(features['mfcc_sum'], 'mfcc_sum_range')
        
        # Combined confidence (learned weighting)
        confidence = (energy_score + centroid_score + mfcc_score) / 3
        
        return confidence > 0.7, confidence
    
    def check_feature_range(self, value, feature_range):
        """Calculate how well value matches learned range"""
        learned_range = self.wake_word_signatures[feature_range]
        
        # Statistical matching (self-taught)
        mean = learned_range['mean']
        span = learned_range['max'] - learned_range['min']
        
        if span == 0:
            return 0
        
        # Score based on distance from mean
        distance = abs(value - mean)
        score = max(0, 1 - (distance / (span * 2)))
        
        return score
    
    def live_monitoring(self):
        """Real-time wake word detection"""
        if not self.wake_word_signatures:
            print("❌ Not trained - run learning first")
            return
        
        print("🎧 Starting live monitoring...")
        print(f"👂 Listening for '{self.wake_word}'...")
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.audio_format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        input_device_index=self.k66_device_index,
                        frames_per_buffer=self.chunk)
        
        try:
            while True:
                # Read audio chunk
                data = stream.read(self.chunk)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Check for wake word
                detected, confidence = self.detect_wake_word(audio_data)
                
                if detected:
                    print(f"🎯 Wake word detected! (confidence: {confidence:.2f})")
                    print("  🔔 WAKE WORD TRIGGERED!")
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    def save_learned_patterns(self):
        """Save my learned patterns"""
        model_data = {
            'wake_word_signatures': self.wake_word_signatures,
            'background_noise_profile': self.background_noise_profile,
            'wake_word': self.wake_word
        }
        
        with open(self.model_file, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Learned patterns saved to {self.model_file}")
    
    def load_learned_patterns(self):
        """Load my saved learning"""
        try:
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.wake_word_signatures = model_data['wake_word_signatures']
            self.background_noise_profile = model_data['background_noise_profile']
            self.wake_word = model_data['wake_word']
            
            print(f"📂 Loaded learned patterns for '{self.wake_word}'")
            return True
            
        except Exception as e:
            print(f"❌ Could not load patterns: {e}")
            return False

def main():
    """Self-taught wake word detector demo"""
    print("🎓 SELF-TAUGHT WAKE WORD DETECTOR")
    print("=" * 50)
    print("🎯 Learning wake word detection from scratch")
    print("🚫 No external APIs, no pre-trained models")
    print("🧠 Pure self-taught pattern recognition")
    print()
    
    detector = SelfTaughtWakeDetector("sara")
    
    # Learning phase
    if input("Train wake word detector? (y/n): ").lower() == 'y':
        detector.learn_background_noise()
        detector.learn_wake_word_signatures()
    
    # Testing phase
    if input("Test live detection? (y/n): ").lower() == 'y':
        detector.live_monitoring()

if __name__ == "__main__":
    main()