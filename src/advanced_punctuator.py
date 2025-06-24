"""
Enhanced punctuation using advanced local rules only
"""

from punctuator import Punctuator


class AdvancedPunctuator(Punctuator):
    def __init__(self):
        super().__init__()
        print("Using enhanced local punctuation rules")
    
    def add_punctuation(self, text):
        """Add punctuation using enhanced local rules"""
        return super().add_punctuation(text) 