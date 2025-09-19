"""
Grammar correction using Gramformer for real-time text enhancement
"""

import time
from typing import Optional


class GrammarCorrector:
    def __init__(self, enable_correction=True):
        self.enable_correction = enable_correction
        self.gramformer = None
        self.is_initialized = False
        
        if enable_correction:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gramformer model (lazy loading)"""
        try:
            print("🔧 Loading Gramformer model...")
            start_time = time.time()
            
            from gramformer import Gramformer
            # Initialize with grammar correction model only (models=1)
            self.gramformer = Gramformer(models=1, use_gpu=False)
            
            load_time = time.time() - start_time
            print(f"✅ Gramformer loaded in {load_time:.2f}s")
            self.is_initialized = True
            
        except Exception as e:
            print(f"❌ Failed to load Gramformer: {e}")
            print("📝 Falling back to no grammar correction")
            self.enable_correction = False
            self.is_initialized = False
    
    def correct_grammar(self, text: str) -> str:
        """Apply grammar correction to text"""
        if not self.enable_correction or not text.strip():
            return text
        
        if not self.is_initialized:
            print("⚠️ Gramformer not initialized, returning original text")
            return text
        
        # Skip grammar correction for long text to prevent truncation
        word_count = len(text.split())
        if word_count > 50:
            print(f"⚠️ Skipping grammar correction for long text ({word_count} words > 50 word limit)")
            return text
        
        try:
            start_time = time.time()
            
            # Gramformer returns a set of corrections, take the first one
            corrections = self.gramformer.correct(text)
            corrected_text = list(corrections)[0] if corrections else text
            
            correction_time = time.time() - start_time
            
            # Only log if there was an actual change
            if corrected_text != text:
                print(f"📝 Grammar correction ({correction_time:.0f}ms): '{text}' → '{corrected_text}'")
            else:
                print(f"✅ No grammar changes needed ({correction_time:.0f}ms)")
            
            return corrected_text
            
        except Exception as e:
            print(f"❌ Grammar correction failed: {e}")
            return text
    
    def is_enabled(self) -> bool:
        """Check if grammar correction is enabled and working"""
        return self.enable_correction and self.is_initialized
    
    def get_stats(self) -> dict:
        """Get correction statistics"""
        return {
            "enabled": self.enable_correction,
            "initialized": self.is_initialized,
            "model_loaded": self.gramformer is not None
        }
