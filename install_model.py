#!/usr/bin/env python3
"""
Simple script to download Vosk model
"""

import os
import urllib.request
import zipfile
from pathlib import Path

# Using larger, more accurate model (~1GB vs ~40MB)
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
MODEL_NAME = "vosk-model-en-us-0.22"

def download_model():
    models_dir = Path("models")
    model_path = models_dir / MODEL_NAME
    
    if model_path.exists():
        print(f"Model already exists: {MODEL_NAME}")
        return
    
    print(f"Downloading {MODEL_NAME} (~1GB - better accuracy)...")
    
    # Create models directory
    models_dir.mkdir(exist_ok=True)
    
    # Download
    zip_path = models_dir / f"{MODEL_NAME}.zip"
    urllib.request.urlretrieve(MODEL_URL, zip_path)
    
    # Extract
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(models_dir)
    
    # Cleanup
    zip_path.unlink()
    
    print("Model installed successfully!")

if __name__ == "__main__":
    download_model() 