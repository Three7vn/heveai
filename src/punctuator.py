"""
Basic punctuation and capitalization
"""


class Punctuator:
    def __init__(self):
        pass
    
    def add_punctuation(self, text):
        """Add basic punctuation and capitalization"""
        if not text.strip():
            return text
        
        # Clean and format text
        formatted = text.strip()
        
        if formatted:
            # Capitalize first letter
            formatted = formatted[0].upper() + formatted[1:] if len(formatted) > 1 else formatted.upper()
            
            # Add period if no ending punctuation
            if not formatted.endswith(('.', '!', '?', ':')):
                formatted += '.'
        
        return formatted 