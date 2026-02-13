#!/usr/bin/env python3
"""
🎓 Install self-taught dependencies
Building voice skills from scratch
"""

import subprocess
import sys

def install_dependencies():
    """Install what I need to self-teach"""
    packages = [
        'numpy',      # For numerical computing
        'librosa',    # For audio processing
        'pyaudio',    # For microphone access
        'scipy',      # For signal processing
    ]
    
    print("🎓 Installing self-taught voice recognition dependencies...")
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                          check=True, capture_output=True)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            print(f"   May need user intervention")
    
    print("🎓 Dependencies installation complete!")

if __name__ == "__main__":
    install_dependencies()