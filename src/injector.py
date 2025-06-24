"""
Text injection - ultra-fast typing, minimal delays
"""

from pynput.keyboard import Controller
import time


class TextInjector:
    def __init__(self):
        self.keyboard = Controller()
        # Set ultra-fast typing speed (50x faster than default)
        self.keyboard._delay = 0.001  # 1ms delay instead of default ~50ms
    
    def type_text(self, text):
        """Type text with ultra-fast speed"""
        if not text.strip():
            return
        
        # Type with minimal delays for maximum speed
        for char in text:
            self.keyboard.press(char)
            self.keyboard.release(char)
            # Minimal delay for reliability but maximum speed
            time.sleep(0.001)  # 1ms between characters = 1000 chars/second
        
        # Add space at the end
        self.keyboard.press(' ')
        self.keyboard.release(' ') 