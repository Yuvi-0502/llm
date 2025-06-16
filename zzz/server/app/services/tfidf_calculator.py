from typing import Dict, List
from math import log
from collections import Counter
from .text_processor import TextProcessor

class TFIDFCalculator:
    """Handles TF-IDF calculations."""
    
    def __init__(self, document_frequency: Dict[str, int], total_documents: int):
        self.doc_freq = document_frequency
        self.total_docs = total_documents
    
    def calculate_tf_idf(self, text: str) -> Dict[str, float]:
        """Calculate TF-IDF scores for words in the text."""
        words = TextProcessor.tokenize_text(text)
        word_freq = TextProcessor.calculate_word_frequency(words)
        
        tf_idf = {}
        for word, freq in word_freq.items():
            # Calculate TF (term frequency)
            tf = freq / len(words)
            
            # Calculate IDF (inverse document frequency)
            if word in self.doc_freq:
                idf = log(self.total_docs / self.doc_freq[word])
            else:
                idf = 0
                
            tf_idf[word] = tf * idf
            
        return tf_idf
    
    def update_document_frequency(self, new_doc_freq: Dict[str, int]):
        """Update document frequency with new data."""
        for word, freq in new_doc_freq.items():
            self.doc_freq[word] = self.doc_freq.get(word, 0) + freq
        self.total_docs += 1 