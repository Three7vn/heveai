"""
Data logging system to save audio and transcriptions for model improvement
"""

import csv
import os
import wave
import time
from datetime import datetime
from pathlib import Path


class DataLogger:
    def __init__(self, base_dir="training/data"):
        self.base_dir = Path(base_dir)
        self.audio_dir = self.base_dir / "audio"
        self.csv_file = self.base_dir / "transcriptions.csv"
        
        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize CSV if it doesn't exist
        if not self.csv_file.exists():
            self._init_csv()
    
    def _init_csv(self):
        """Initialize CSV with headers"""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'audio_file', 'transcription', 'corrected_transcription', 'audio_duration'])
    
    def save_transcription(self, audio_data, transcription, sample_rate=16000):
        """Save audio file and transcription to CSV"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # millisecond precision
            audio_filename = f"audio_{timestamp}.wav"
            audio_path = self.audio_dir / audio_filename
            
            # Save audio as WAV file
            with wave.open(str(audio_path), 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            
            # Calculate audio duration
            duration = len(audio_data) / (sample_rate * 2)  # 2 bytes per sample
            
            # Append to CSV
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    audio_filename,
                    transcription,
                    "",  # corrected_transcription (empty for now)
                    f"{duration:.2f}"
                ])
            
            print(f"📝 Logged: {audio_filename} -> '{transcription}' (saved to {self.csv_file})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to log data: {e}")
            return False
    
    def get_training_data(self):
        """Load all training data from CSV"""
        training_data = []
        if self.csv_file.exists():
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    training_data.append({
                        'audio_path': str(self.audio_dir / row['audio_file']),
                        'transcription': row['transcription'],
                        'corrected': row['corrected_transcription'],
                        'duration': float(row['audio_duration'])
                    })
        return training_data
    
    def update_correction(self, audio_filename, corrected_text):
        """Update a transcription with corrected text"""
        # Read current CSV
        rows = []
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Update the specific row
        for row in rows:
            if row['audio_file'] == audio_filename:
                row['corrected_transcription'] = corrected_text
                break
        
        # Write back to CSV
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
