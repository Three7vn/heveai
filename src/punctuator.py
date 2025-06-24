"""
Enhanced punctuation and capitalization with local rules
"""

import re


class Punctuator:
    def __init__(self):
        # Common words that should trigger commas before them
        self.comma_triggers = [
            'and', 'but', 'or', 'so', 'yet', 'for', 'nor',
            'however', 'therefore', 'meanwhile', 'furthermore',
            'on a separate note', 'separately', 'also', 'additionally'
        ]
        
        # Phrases that often need commas before them (independent clauses)
        self.independent_clause_starters = [
            'i think', 'i believe', 'i feel', 'i know', 'i suppose',
            'i guess', 'i assume', 'i would', 'i will', 'i can',
            'i should', 'i could', 'we should', 'we could', 'we can',
            'you should', 'you could', 'you can', 'it would', 'it will'
        ]
        
        # Words that often start new sentences
        self.sentence_starters = [
            'i look forward', 'i would', 'i will', 'i think',
            'on a separate note', 'separately', 'also', 'additionally',
            'furthermore', 'however', 'meanwhile', 'therefore'
        ]
    
    def add_punctuation(self, text):
        """Add enhanced punctuation and capitalization"""
        if not text.strip():
            return text
        
        # Clean and normalize text
        formatted = text.strip().lower()
        
        # Fix common grammar issues
        formatted = re.sub(r'\bseparate notes\b', 'separate note', formatted)
        formatted = re.sub(r'\bas well\b', 'as well', formatted)
        formatted = re.sub(r'\bwhat you done\b', 'what you did', formatted)
        
        # Add commas before independent clauses (compound sentences)
        for starter in self.independent_clause_starters:
            # Look for pattern: [some words] + [independent clause starter]
            pattern = r'(\w+(?:\s+\w+){3,})\s+(' + re.escape(starter) + r')\s+'
            formatted = re.sub(pattern, r'\1, \2 ', formatted, flags=re.IGNORECASE)
        
        # Add commas before common conjunctions and transitions
        for trigger in self.comma_triggers:
            pattern = r'\s+(' + re.escape(trigger) + r')\s+'
            formatted = re.sub(pattern, r', \1 ', formatted, flags=re.IGNORECASE)
        
        # Handle sentence breaks for common patterns
        formatted = re.sub(r'\s+(on a separate note)\s+', r'. \1, ', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'\s+(i look forward)\s+', r'. \1 ', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'\s+(i would love)\s+', r'. \1 ', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'\s+(i really like)\s+', r'. \1 ', formatted, flags=re.IGNORECASE)
        
        # Add commas after introductory phrases (longer than 4 words)
        formatted = re.sub(r'^([^,]{20,?})\s+(i\s)', r'\1, \2', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'(thank you for [^.]*?)\s+(i\s)', r'\1, \2', formatted, flags=re.IGNORECASE)
        
        # Capitalize 'I' throughout the text
        formatted = re.sub(r'\bi\b', 'I', formatted)
        
        # Capitalize first letter of sentences
        formatted = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), formatted)
        
        # Ensure first letter of entire text is capitalized
        if formatted:
            formatted = formatted[0].upper() + formatted[1:] if len(formatted) > 1 else formatted.upper()
        
        # Add final punctuation if missing
        if not formatted.endswith(('.', '!', '?', ':')):
            formatted += '.'
        
        # Clean up extra spaces around punctuation
        formatted = re.sub(r'\s+([,.!?])', r'\1', formatted)
        formatted = re.sub(r'([,.!?])\s+', r'\1 ', formatted)
        formatted = re.sub(r'\s+', ' ', formatted)  # Remove extra spaces
        
        return formatted.strip() 