import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import librosa
import soundfile as sf
import numpy as np

class DictionaryCorrector:
    def __init__(self, dict_file="training/vocabulary_dictionary.json"):
        self.dict_file = Path(dict_file)
        self.dictionary = self.load_dictionary()
        self.audio_snippets_dir = Path("training/data/audio_snippets")
        self.audio_snippets_dir.mkdir(parents=True, exist_ok=True)
        
    def load_dictionary(self) -> Dict:
        """Load vocabulary dictionary from JSON file"""
        if self.dict_file.exists():
            with open(self.dict_file, 'r') as f:
                return json.load(f)
        return {
            "replacements": {},
            "technical_terms": [],
            "context_mappings": {},
            "audio_snippets": {"enabled": True, "snippet_duration": 2.0, "context_padding": 0.5}
        }
    
    def save_dictionary(self):
        """Save dictionary back to JSON file"""
        with open(self.dict_file, 'w') as f:
            json.dump(self.dictionary, f, indent=2)
    
    def apply_real_time_corrections(self, text: str) -> str:
        """Apply real-time corrections using dictionary mappings"""
        corrected_text = text
        
        # Sort replacements by length (longest first) to avoid partial replacements
        replacements = sorted(self.dictionary["replacements"].items(), key=lambda x: len(x[0]), reverse=True)
        
        # Apply simple replacements (case-insensitive)
        for wrong, correct in replacements:
            # Use regex with word boundaries for partial matches in longer text
            pattern = r'\b' + re.escape(wrong) + r'\b'
            corrected_text = re.sub(pattern, correct, corrected_text, flags=re.IGNORECASE)
        
        # Apply context-aware corrections
        corrected_text = self._apply_context_corrections(corrected_text)
        
        return corrected_text
    
    def _apply_context_corrections(self, text: str) -> str:
        """Apply context-aware corrections based on surrounding words"""
        for word, contexts in self.dictionary["context_mappings"].items():
            # Simple context detection - can be enhanced
            if word in text.lower():
                # Check for coding context keywords
                coding_keywords = ["python", "code", "script", "programming", "jupyter", "github"]
                if any(keyword in text.lower() for keyword in coding_keywords):
                    if "coding_context" in contexts:
                        text = re.sub(r'\b' + word + r'\b', contexts["coding_context"], text, flags=re.IGNORECASE)
                else:
                    if "default" in contexts:
                        text = re.sub(r'\b' + word + r'\b', contexts["default"], text, flags=re.IGNORECASE)
        
        return text
    
    def extract_audio_snippet(self, audio_data: np.ndarray, sample_rate: int, 
                            word_position: float, word: str, correct_word: str) -> str:
        """Extract audio snippet around a specific word for dictionary training"""
        if not self.dictionary["audio_snippets"]["enabled"]:
            return None
            
        snippet_duration = self.dictionary["audio_snippets"]["snippet_duration"]
        context_padding = self.dictionary["audio_snippets"]["context_padding"]
        
        # Calculate snippet boundaries
        start_time = max(0, word_position - context_padding)
        end_time = min(len(audio_data) / sample_rate, word_position + snippet_duration + context_padding)
        
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        # Extract snippet
        snippet = audio_data[start_sample:end_sample]
        
        # Generate filename
        timestamp = int(word_position * 1000)  # milliseconds
        snippet_filename = f"snippet_{word}_{correct_word}_{timestamp}.wav"
        snippet_path = self.audio_snippets_dir / snippet_filename
        
        # Save snippet
        sf.write(snippet_path, snippet, sample_rate)
        
        return str(snippet_path)
    
    def add_replacement(self, wrong_word: str, correct_word: str):
        """Add new replacement to dictionary"""
        self.dictionary["replacements"][wrong_word.lower()] = correct_word
        self.save_dictionary()
    
    def add_technical_term(self, term: str):
        """Add technical term to dictionary"""
        if term not in self.dictionary["technical_terms"]:
            self.dictionary["technical_terms"].append(term)
            self.save_dictionary()
    
    def suggest_corrections(self, original: str, corrected: str) -> List[Tuple[str, str]]:
        """Analyze differences between original and corrected text to suggest dictionary entries"""
        suggestions = []
        
        # Simple word-level comparison
        original_words = original.lower().split()
        corrected_words = corrected.split()
        
        # Find potential replacements (this is a simple heuristic)
        if len(original_words) == len(corrected_words):
            for orig, corr in zip(original_words, corrected_words):
                if orig != corr.lower() and len(orig) > 2:  # Avoid single letters
                    suggestions.append((orig, corr))
        
        return suggestions
    
    def get_correction_stats(self) -> Dict:
        """Get statistics about corrections made"""
        return {
            "total_replacements": len(self.dictionary["replacements"]),
            "technical_terms": len(self.dictionary["technical_terms"]),
            "context_mappings": len(self.dictionary["context_mappings"])
        }
