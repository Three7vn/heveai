"""
Text injection - ultra-fast typing, minimal delays
"""

from pynput.keyboard import Controller, Key
import subprocess
import time
import os


class TextInjector:
    def __init__(self):
        self.keyboard = Controller()
        # Set ultra-fast typing speed (50x faster than default)
        self.keyboard._delay = 0.001  # 1ms delay instead of default ~50ms
    
    def type_text(self, text):
        """Type text directly - simple and reliable"""
        if not text.strip():
            return
        
        try:
            # Simple direct typing - this works
            self.keyboard.type(text + ' ')
            print(f"✅ Text injected: {text}")
        except Exception as e:
            print(f"❌ Injection failed: {e}") 