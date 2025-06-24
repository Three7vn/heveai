"""
Key listener for Right Option key
"""

from pynput import keyboard


class KeyListener:
    def __init__(self, trigger_key=None, on_press=None, on_release=None):
        self.on_press_callback = on_press
        self.on_release_callback = on_release
        self.listener = None
        self.is_pressed = False
    
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
        if key == keyboard.Key.alt_r and not self.is_pressed:
            self.is_pressed = True
            if self.on_press_callback:
                self.on_press_callback()
    
    def _on_release(self, key):
        if key == keyboard.Key.alt_r and self.is_pressed:
            self.is_pressed = False
            if self.on_release_callback:
                self.on_release_callback() 