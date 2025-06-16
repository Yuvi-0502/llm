from abc import ABC, abstractmethod
from typing import Dict

class ITFIDFCalculator(ABC):
    """Interface for TF-IDF calculations."""
    
    @abstractmethod
    def calculate_tf_idf(self, text: str) -> Dict[str, float]:
        """Calculate TF-IDF scores for words in the text."""
        pass
    
    @abstractmethod
    def update_document_frequency(self, new_doc_freq: Dict[str, int]):
        """Update document frequency with new data."""
        pass 