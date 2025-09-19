"""
Speech recognition using faster-whisper (OpenAI Whisper)
"""

import whisper
import numpy as np
import torch
from pathlib import Path
import sys

# Add the training directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent / "training"))
from data_logger import DataLogger
from dictionary_corrector import DictionaryCorrector


class ASREngine:
    def __init__(self, model_size="base", enable_logging=True, enable_dictionary=True):
        """
        Initialize Whisper model
        Model sizes: tiny, base, small, medium, large
        base = good balance of speed/accuracy
        """
        try:
            print(f"Loading Whisper model ({model_size})...")
            self.model = whisper.load_model(model_size)
            self.sample_rate = 16000
            print(f"Loaded Whisper model ({model_size})")
            
            # Initialize data logger
            self.logger = DataLogger() if enable_logging else None
            if self.logger:
                print("📝 Data logging enabled - saving audio/transcriptions for training")
            
            # Initialize dictionary corrector
            self.dictionary = DictionaryCorrector() if enable_dictionary else None
            if self.dictionary:
                print("📚 Dictionary correction enabled - real-time vocabulary fixes")
                
        except Exception as e:
            print(f"Could not load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_data):
        """Convert audio data to text using Whisper"""
        if not audio_data:
            return "", None
        
        try:
            # Convert audio bytes to numpy array
            audio_np = self._bytes_to_numpy(audio_data)
            
            # Transcribe with Whisper
            result = self.model.transcribe(audio_np, language="en")
            raw_text = result["text"].strip()
            
            # Apply real-time dictionary corrections
            corrected_text = raw_text
            if self.dictionary:
                corrected_text = self.dictionary.apply_real_time_corrections(raw_text)
                
                # If corrections were made, suggest adding to dictionary
                if corrected_text != raw_text:
                    suggestions = self.dictionary.suggest_corrections(raw_text, corrected_text)
                    for wrong, correct in suggestions:
                        print(f"💡 Dictionary suggestion: '{wrong}' → '{correct}'")
            
            # Return text and audio data for logging after injection
            return corrected_text, (audio_data, raw_text, self.sample_rate) if self.logger else None
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return "", None
    
    def _bytes_to_numpy(self, audio_data):
        """Convert audio bytes to numpy array for Whisper"""
        # Convert bytes to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        # Convert to float32 and normalize to [-1, 1]
        audio_np = audio_np.astype(np.float32) / 32768.0
        
        return audio_np 