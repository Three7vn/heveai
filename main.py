#!/usr/bin/env python3
"""
Heve AI - Lean speech-to-text dictation
Hold Right Option key and speak to dictate text
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from key_listener import KeyListener
from audio_capture import AudioCapture
from asr import ASREngine
from injector import TextInjector
from advanced_punctuator import AdvancedPunctuator


def main():
    print("Heve AI - Hold RIGHT OPTION key (⌥) and speak to dictate")
    
    # Initialize components
    audio = AudioCapture()
    asr = ASREngine()
    injector = TextInjector()
    punctuator = AdvancedPunctuator()
    
    def start_dictation():
        print("Recording...")
        audio.start()
    
    def stop_dictation():
        print("Processing...")
        audio_data = audio.stop()
        text = asr.transcribe(audio_data)
        if text.strip():
            # Add advanced punctuation and capitalization
            formatted_text = punctuator.add_punctuation(text)
            injector.type_text(formatted_text)
            print(f"Typed: {formatted_text}")
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
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        listener.stop()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 