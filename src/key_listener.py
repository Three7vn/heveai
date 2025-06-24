"""
Key listener for Right Option key with debounce protection
"""

import time
from pynput import keyboard


class KeyListener:
    def __init__(self, trigger_key=None, on_press=None, on_release=None):
        self.on_press_callback = on_press
        self.on_release_callback = on_release
        self.listener = None
        self.is_pressed = False
        self.is_processing = False  # Prevent overlapping dictation
        self.last_release_time = 0  # Debounce protection
        self.debounce_delay = 0.5  # 500ms minimum between dictations
    
    def start(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
    
    def stop(self):
        if self.listener:
            self.listener.stop()
    
    def _on_press(self, key):
        if key == keyboard.Key.alt_r and not self.is_pressed and not self.is_processing:
            current_time = time.time()
            # Check debounce - prevent rapid successive presses  
            if current_time - self.last_release_time < self.debounce_delay:
                return
                
            self.is_pressed = True
            if self.on_press_callback:
                self.on_press_callback()
    
    def _on_release(self, key):
        if key == keyboard.Key.alt_r and self.is_pressed:
            current_time = time.time()
            self.is_pressed = False
            self.is_processing = True  # Block new presses during processing
            
            if self.on_release_callback:
                self.on_release_callback()
            
            self.is_processing = False
            self.last_release_time = current_time 