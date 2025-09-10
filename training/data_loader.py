"""
Data loader that integrates dictionary corrections with fine-tuning pipeline
"""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Tuple
import librosa
import numpy as np

class DataLoader:
    def __init__(self, data_dir="training/data", dict_file="training/vocabulary_dictionary.json"):
        self.data_dir = Path(data_dir)
        self.dict_file = Path(dict_file)
        self.audio_dir = self.data_dir / "audio"
        self.snippets_dir = self.data_dir / "audio_snippets"
        self.csv_file = self.data_dir / "transcriptions.csv"
        
    def load_dictionary(self) -> Dict:
        """Load vocabulary dictionary"""
        if self.dict_file.exists():
            with open(self.dict_file, 'r') as f:
                return json.load(f)
        return {}
    
    def create_dual_training_dataset(self) -> Tuple[List[str], List[str]]:
        """
        Create dual training dataset that includes:
        1. CSV transcriptions (corrected)
        2. Dictionary audio snippets
        """
        # Load main transcriptions
        df = pd.read_csv(self.csv_file)
        corrected_df = df[df['corrected_transcription'].notna() & (df['corrected_transcription'] != '')]
        
        audio_paths = []
        transcriptions = []
        
        # Add main corrected examples
        for _, row in corrected_df.iterrows():
            audio_path = self.audio_dir / row['audio_file']
            if audio_path.exists():
                audio_paths.append(str(audio_path))
                transcriptions.append(row['corrected_transcription'])
        
        # Add audio snippet examples for dictionary vocabulary training
        snippet_examples = self._load_snippet_examples()
        for audio_path, transcription in snippet_examples:
            audio_paths.append(audio_path)
            transcriptions.append(transcription)
        
        return audio_paths, transcriptions
    
    def _generate_dictionary_examples(self, df: pd.DataFrame, dictionary: Dict) -> List[Tuple[str, str]]:
        """
        Generate synthetic training examples by applying dictionary corrections
        to create contextual learning examples
        """
        examples = []
        replacements = dictionary.get("replacements", {})
        
        for _, row in df.iterrows():
            original = row['transcription']
            corrected = row['corrected_transcription']
            audio_path = str(self.audio_dir / row['audio_file'])
            
            # Create variations with different dictionary corrections
            for wrong, correct in replacements.items():
                if wrong.lower() in original.lower() and correct in corrected:
                    # This audio contains a word that was dictionary-corrected
                    # Use this as a positive example for contextual learning
                    examples.append((audio_path, corrected))
                    break
        
        return examples
    
    def _load_snippet_examples(self) -> List[Tuple[str, str]]:
        """Load audio snippet examples for specific vocabulary training"""
        examples = []
        
        if not self.snippets_dir.exists():
            return examples
        
        # Load snippet files and create targeted vocabulary examples
        for snippet_file in self.snippets_dir.glob("*.wav"):
            # Parse filename: snippet_{wrong_word}_{correct_word}_{timestamp}.wav
            parts = snippet_file.stem.split('_')
            if len(parts) >= 4 and parts[0] == "snippet":
                correct_word = parts[2]
                # Create a simple transcription for the snippet
                transcription = correct_word
                examples.append((str(snippet_file), transcription))
        
        return examples
    
    def create_contextual_training_pairs(self) -> List[Tuple[str, str, str]]:
        """
        Create training pairs that teach contextual understanding:
        (audio_path, wrong_context, correct_context)
        """
        df = pd.read_csv(self.csv_file)
        dictionary = self.load_dictionary()
        context_mappings = dictionary.get("context_mappings", {})
        
        pairs = []
        
        for _, row in df.iterrows():
            original = row['transcription']
            corrected = row['corrected_transcription']
            audio_path = str(self.audio_dir / row['audio_file'])
            
            # Find context-dependent corrections
            for word, contexts in context_mappings.items():
                if word in original.lower():
                    # Check if this was corrected based on context
                    coding_context = contexts.get("coding_context", "")
                    if coding_context in corrected:
                        # This is a context-dependent correction
                        wrong_context = original
                        correct_context = corrected
                        pairs.append((audio_path, wrong_context, correct_context))
        
        return pairs
    
    def get_training_statistics(self) -> Dict:
        """Get statistics about the enhanced training dataset"""
        audio_paths, transcriptions = self.create_enhanced_training_dataset()
        contextual_pairs = self.create_contextual_training_pairs()
        
        return {
            "total_examples": len(audio_paths),
            "main_transcriptions": len(pd.read_csv(self.csv_file)),
            "corrected_transcriptions": len([t for t in transcriptions if t]),
            "contextual_pairs": len(contextual_pairs),
            "snippet_examples": len(list(self.snippets_dir.glob("*.wav"))) if self.snippets_dir.exists() else 0
        }
