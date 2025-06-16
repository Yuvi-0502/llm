from abc import ABC, abstractmethod
from typing import List
from collections import Counter

class ITextProcessor(ABC):
    """Interface for text processing operations."""
    
    @abstractmethod
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into words."""
        pass
    
    @abstractmethod
    def calculate_word_frequency(self, words: List[str]) -> Counter:
        """Calculate word frequency in text."""
        pass
    
    @abstractmethod
    def normalize_text(self, text: str) -> str:
        """Normalize text by converting to lowercase and removing extra whitespace."""
        pass
    
    @abstractmethod
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful keywords from text."""
        pass 