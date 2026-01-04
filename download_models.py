#!/usr/bin/env python3
"""
Download missing models for Project VICTUS
Downloads Piper TTS models (ONNX format) to the models/ directory
"""

import sys
from pathlib import Path
import urllib.request
from urllib.error import URLError, HTTPError
import importlib.util  # noqa: F401

# Model directory
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# Piper TTS model - English US, Amy voice, Medium quality
# Using direct Hugging Face CDN links
PIPER_MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx"
PIPER_CONFIG_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json"

def download_file(url: str, filepath: Path, description: str = ""):
    """Download a file with progress indication."""
    try:
        print(f"📥 Downloading: {description or filepath.name}")
        print(f"   From: {url}")
        
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100) if total_size > 0 else 0
            size_mb = total_size / (1024 * 1024) if total_size > 0 else 0
            downloaded_mb = downloaded / (1024 * 1024)
            print(f"\r   Progress: {percent:.1f}% ({downloaded_mb:.1f}/{size_mb:.1f} MB)", end='', flush=True)
        
        urllib.request.urlretrieve(url, filepath, reporthook=show_progress)
        print()  # New line after progress
        
        file_size = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ Downloaded: {filepath.name} ({file_size:.1f} MB)")
        return True
    except HTTPError as e:
        print(f"\n❌ HTTP Error {e.code}: {e.reason}")
        return False
    except URLError as e:
        print(f"\n❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def download_piper_models():
    """Download Piper TTS models."""
    print("\n" + "="*70)
    print("🎤 Downloading Piper TTS Models")
    print("="*70)
    
    model_file = MODELS_DIR / "en_US-amy-medium.onnx"
    config_file = MODELS_DIR / "en_US-amy-medium.onnx.json"
    
    success_count = 0
    
    # Download model file
    if model_file.exists():
        print(f"⏭️  Skipping {model_file.name} (already exists)")
    else:
        if download_file(PIPER_MODEL_URL, model_file, "Piper TTS Model (ONNX)"):
            success_count += 1
    
    # Download config file
    if config_file.exists():
        print(f"⏭️  Skipping {config_file.name} (already exists)")
    else:
        if download_file(PIPER_CONFIG_URL, config_file, "Piper TTS Config"):
            success_count += 1
    
    return success_count

def verify_faster_whisper():
    """Verify faster-whisper setup."""
    print("\n" + "="*70)
    print("🎙️  Verifying Faster-Whisper Setup")
    print("="*70)
    
    try:
        import faster_whisper  # noqa: F401
        print("✅ faster-whisper package is installed")
        
        # Try to load the model (will auto-download on first use)
        print("📥 Testing model load (will auto-download 'base.en' if needed)...")
        from faster_whisper import WhisperModel
        # model = WhisperModel("base.en", device="cpu", compute_type="int8") # Remove unused assign
        WhisperModel("base.en", device="cpu", compute_type="int8")
        print("✅ Faster-Whisper model is ready")
        return True
    except ImportError:
        print("⚠️  faster-whisper is not installed")
        print("   Install with: pip install faster-whisper")
        print("   Or: pip3 install faster-whisper")
        return False
    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("   The model will download automatically on first use")
        return False

def main():
    """Main function."""
    print("\n" + "="*70)
    print("🚀 Project VICTUS - Model Downloader")
    print("="*70)
    
    # Ensure models directory exists
    if not MODELS_DIR.exists():
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {MODELS_DIR.absolute()}")
    
    # Download Piper models
    download_piper_models()
    
    # Verify faster-whisper
    whisper_ready = verify_faster_whisper()
    
    # Summary
    print("\n" + "="*70)
    print("📊 Download Summary")
    print("="*70)
    
    onnx_files = list(MODELS_DIR.glob("*.onnx"))
    if onnx_files:
        print(f"\n📦 Models in {MODELS_DIR}:")
        for f in sorted(onnx_files):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"   ✅ {f.name} ({size_mb:.1f} MB)")
    else:
        print(f"\n⚠️  No .onnx files found in {MODELS_DIR}")
    
    print(f"\nPiper TTS: {'✅ Ready' if onnx_files else '❌ Not found'}")
    print(f"Faster-Whisper: {'✅ Ready' if whisper_ready else '⚠️  Will download on first use'}")
    
    print("\n✅ Model download process complete!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
