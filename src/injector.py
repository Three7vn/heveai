"""
Text injection - instant typing, no animation
"""

from pynput.keyboard import Controller


class TextInjector:
    def __init__(self):
        self.keyboard = Controller()
    
    def type_text(self, text):
        """Type text instantly - no delays or animation"""
        if not text.strip():
            return
        
        # Type entire text at once - no character-by-character delays
        self.keyboard.type(text + ' ') 