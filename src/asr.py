"""
Speech recognition using faster-whisper (OpenAI Whisper)
Much better accuracy than Vosk while still running locally
"""

import numpy as np
import io
import wave
from faster_whisper import WhisperModel


class ASREngine:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper model
        Model sizes: tiny, base, small, medium, large
        base = good balance of speed/accuracy
        """
        try:
            print(f"Loading Whisper model ({model_size})...")
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
            self.sample_rate = 16000
            print(f"Loaded Whisper model ({model_size})")
        except Exception as e:
            print(f"Could not load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_data):
        """Convert audio data to text using Whisper"""
        if not audio_data:
            return ""
        
        try:
            # Convert audio bytes to numpy array
            audio_np = self._bytes_to_numpy(audio_data)
            
            # Transcribe with Whisper
            segments, info = self.model.transcribe(
                audio_np,
                language="en",
                beam_size=5,
                best_of=5,
                temperature=0.0,
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(min_silence_duration_ms=1000)
            )
            
            # Combine all segments
            text = " ".join([segment.text for segment in segments])
            
            return text.strip()
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return ""
    
    def _bytes_to_numpy(self, audio_data):
        """Convert audio bytes to numpy array for Whisper"""
        # Convert bytes to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        # Convert to float32 and normalize to [-1, 1]
        audio_np = audio_np.astype(np.float32) / 32768.0
        
        return audio_np 