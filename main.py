#!/usr/bin/env python3
"""
Heve AI - Speech-to-text dictation
Hold Right Option key and speak to dictate text
"""

import sys
import time
import os
import atexit
import threading
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from key_listener import KeyListener
from audio_capture import AudioCapture
from asr import ASREngine
from injector import TextInjector
from advanced_punctuator import AdvancedPunctuator
from grammar_corrector import GrammarCorrector

# Lock file to prevent multiple instances
LOCK_FILE = Path("/tmp/heve_ai.lock")

def create_lock():
    """Create lock file to prevent multiple instances"""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Check if process is still running
            os.kill(pid, 0)  # This will raise OSError if process doesn't exist
            print("❌ Another instance of Heve AI is already running!")
            print(f"   PID: {pid}")
            print("   Kill it first with: pkill -f 'python.*main.py'")
            return False
        except (OSError, ValueError):
            # Process is dead, remove stale lock file
            LOCK_FILE.unlink()
    
    # Create new lock file
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    # Register cleanup function
    atexit.register(cleanup_lock)
    return True

def cleanup_lock():
    """Remove lock file on exit"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

def main():
    # Check for existing instance
    if not create_lock():
        return 1
    
    print("Heve AI - Hold RIGHT OPTION key (⌥) and speak to dictate")
    
    # Initialize components
    audio = AudioCapture()
    asr = ASREngine()
    injector = TextInjector()
    punctuator = AdvancedPunctuator()
    grammar_corrector = GrammarCorrector(enable_correction=True)
    
    def start_dictation():
        print("Recording...")
        audio.start()
    
    def stop_dictation():
        print("Processing...")
        audio_data = audio.stop()
        text, audio_log_data = asr.transcribe(audio_data)
        if text.strip():
            # Add advanced punctuation and capitalization
            formatted_text = punctuator.add_punctuation(text)
            
            # Apply grammar correction
            corrected_text = grammar_corrector.correct_grammar(formatted_text)
            
            # 🚀 INJECT TEXT FIRST - HIGHEST PRIORITY
            injector.type_text(corrected_text)
            print(f"Typed: {corrected_text}")
            
            # Log to CSV in background AFTER injection
            def log_to_csv():
                if audio_log_data and asr.logger:
                    audio_data_for_log, raw_text, sample_rate = audio_log_data
                    audio_filename = asr.logger.save_transcription(audio_data_for_log, raw_text, sample_rate)
                    if audio_filename:
                        asr.logger.update_correction(audio_filename, corrected_text)
                        if corrected_text != text:
                            print(f"📝 Grammar correction applied: '{text}' → '{corrected_text}'")
                        else:
                            print(f"📝 Final transcription logged: '{corrected_text}'")
            
            # Run CSV logging in background AFTER text injection
            threading.Thread(target=log_to_csv, daemon=True).start()
            
        else:
            print("No speech detected")
    
    # Start key listener for Right Option key
    listener = KeyListener(
        trigger_key='right_option',
        on_press=start_dictation,
        on_release=stop_dictation
    )
    
    try:
        listener.start()
        print("Ready! Hold RIGHT OPTION key (⌥) and speak...")
        print("The Right Option key is to the right of the spacebar")
        print("Also: Enable Terminal in System Settings > Privacy & Security > Accessibility")
        print("🔒 Single instance protection active")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        listener.stop()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 