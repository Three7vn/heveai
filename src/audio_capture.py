"""
Audio capture using PyAudio
"""

import pyaudio
import wave
import io


class AudioCapture:
    def __init__(self, sample_rate=16000, channels=1, chunk=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
    
    def start(self):
        """Start recording audio"""
        self.frames = []
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._callback
        )
        self.stream.start_stream()
    
    def stop(self):
        """Stop recording and return audio data"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Convert frames to bytes
        audio_data = b''.join(self.frames)
        return audio_data
    
    def _callback(self, in_data, frame_count, time_info, status):
        """Audio stream callback"""
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def __del__(self):
        """Cleanup PyAudio"""
        if hasattr(self, 'audio'):
            self.audio.terminate() 