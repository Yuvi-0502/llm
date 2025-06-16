from typing import List, Dict
import re
from collections import Counter

class TextProcessor:
    """Handles text processing operations."""
    
    @staticmethod
    def tokenize_text(text: str) -> List[str]:
        """Tokenize text into words."""
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def calculate_word_frequency(words: List[str]) -> Counter:
        """Calculate word frequency in text."""
        return Counter(words)
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text by converting to lowercase and removing extra whitespace."""
        return ' '.join(text.lower().split())
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful keywords from text."""
        words = TextProcessor.tokenize_text(text)
        return [word for word in words if len(word) >= min_length] 