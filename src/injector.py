"""
Text injection - ultra-fast typing, minimal delays
"""

from pynput.keyboard import Controller, Key
import subprocess
import time
import os
import pyperclip


class TextInjector:
    def __init__(self):
        self.keyboard = Controller()
        # Set ultra-fast typing speed (50x faster than default)
        self.keyboard._delay = 0.001  # 1ms delay instead of default ~50ms
    
    def type_text(self, text):
        """Instant text injection via clipboard paste"""
        if not text.strip():
            return
        
        try:
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            
            # Copy text to clipboard
            pyperclip.copy(text + ' ')
            
            # Paste instantly with Cmd+V
            self.keyboard.press(Key.cmd)
            self.keyboard.press('v')
            self.keyboard.release('v')
            self.keyboard.release(Key.cmd)
            
            # Restore original clipboard after a short delay
            time.sleep(0.1)
            pyperclip.copy(original_clipboard)
            
            print(f"✅ Text injected instantly: {text}")
        except Exception as e:
            print(f"❌ Injection failed: {e}")
            # Fallback to typing if clipboard fails
            try:
                self.keyboard.type(text + ' ')
                print(f"✅ Text injected via fallback typing: {text}")
            except Exception as e2:
                print(f"❌ Both injection methods failed: {e2}") 