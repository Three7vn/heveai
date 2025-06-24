"""
Speech recognition using Vosk
"""

import json
import vosk
import wave
import io


class ASREngine:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        try:
            self.model = vosk.Model(model_path)
            self.sample_rate = 16000
        except:
            print(f"❌ Could not load Vosk model from {model_path}")
            print("💡 Download a model with: python scripts/install_models.py vosk-model-small-en-us-0.15")
            raise
    
    def transcribe(self, audio_data):
        """Convert audio data to text"""
        if not audio_data:
            return ""
        
        # Create recognizer
        rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
        
        # Process audio data
        rec.AcceptWaveform(audio_data)
        result = json.loads(rec.FinalResult())
        
        return result.get('text', '') 