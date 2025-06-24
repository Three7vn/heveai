"""
Enhanced punctuation and capitalization with local rules
"""

import re


class Punctuator:
    def __init__(self):
        # Common greetings that should always have commas after them
        self.greetings = [
            'hey there', 'hello there', 'hi there', 'hey everyone', 'hello everyone',
            'good morning', 'good afternoon', 'good evening', 'hey guys', 'hello folks'
        ]
        
        # Common words that should trigger commas before them (but not always)
        self.comma_triggers = [
            'and', 'but', 'or', 'so', 'yet', 
            'however', 'therefore', 'meanwhile', 'furthermore'
        ]
        
        # Phrases that often need commas before them (independent clauses)
        self.independent_clause_starters = [
            'i think', 'i believe', 'i feel', 'i know', 'i suppose',
            'i guess', 'i assume', 'i would love', 'i will', 'i can',
            'i should', 'i could', 'we should', 'we could', 'we can'
        ]
        
        # Words that often start new sentences
        self.sentence_starters = [
            'i look forward', 'i would love to', 'i will',
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
        formatted = re.sub(r'\bwhat you done\b', 'what you did', formatted)
        
        # Add commas after greetings at the start of sentences
        for greeting in self.greetings:
            pattern = r'^(' + re.escape(greeting) + r')\s+([^,])'
            formatted = re.sub(pattern, r'\1, \2', formatted, flags=re.IGNORECASE)
        
        # Add commas before independent clauses (only after substantial content)
        for starter in self.independent_clause_starters:
            # Only add comma if there's substantial content before (15+ chars)
            pattern = r'([^,]{15,})\s+(' + re.escape(starter) + r')\s+'
            formatted = re.sub(pattern, r'\1, \2 ', formatted, flags=re.IGNORECASE)
        
        # Add commas before some conjunctions (but be selective)
        selective_triggers = ['but', 'so', 'yet', 'however', 'therefore']
        for trigger in selective_triggers:
            pattern = r'([^,]{10,})\s+(' + re.escape(trigger) + r')\s+'
            formatted = re.sub(pattern, r'\1, \2 ', formatted, flags=re.IGNORECASE)
        
        # Handle sentence breaks for specific patterns
        formatted = re.sub(r'\s+(on a separate note)\s+', r'. \1, ', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'([^.!?]{30,})\s+(i would love to)\s+', r'\1. \2 ', formatted, flags=re.IGNORECASE)
        
        # Add commas after long introductory phrases (25+ chars)
        formatted = re.sub(r'^([^,]{25,})\s+(i\s)', r'\1, \2', formatted, flags=re.IGNORECASE)
        
        # Capitalize 'I' throughout the text
        formatted = re.sub(r'\bi\b', 'I', formatted)
        
        # Capitalize first letter of sentences
        formatted = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), formatted)
        
        # Ensure first letter of entire text is capitalized
        if formatted:
            formatted = formatted[0].upper() + formatted[1:] if len(formatted) > 1 else formatted.upper()
        
        # Add final punctuation if missing
        if not formatted.endswith(('.', '!', '?')):
            formatted += '.'
        
        # Clean up punctuation issues
        formatted = re.sub(r',\s*\.', '.', formatted)  # Remove comma before period
        formatted = re.sub(r',\s*,', ',', formatted)   # Remove double commas
        formatted = re.sub(r'\s+([,.!?])', r'\1', formatted)  # Remove space before punctuation
        formatted = re.sub(r'([,.!?])\s+', r'\1 ', formatted)  # Ensure space after punctuation
        formatted = re.sub(r'\s+', ' ', formatted)     # Remove extra spaces
        
        return formatted.strip() 