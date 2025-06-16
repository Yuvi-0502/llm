from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from app.models.article import ArticleCategory
from .tfidf_calculator import ITFIDFCalculator

class ICategoryScorer(ABC):
    """Interface for category scoring operations."""
    
    @abstractmethod
    def calculate_category_score(
        self,
        text: str,
        category: ArticleCategory,
        tf_idf_scores: Dict[str, float]
    ) -> float:
        """Calculate score for a specific category."""
        pass
    
    @abstractmethod
    def get_category_confidence(
        self,
        text: str,
        tf_idf_calculator: ITFIDFCalculator
    ) -> Tuple[ArticleCategory, float]:
        """Get the predicted category and confidence score."""
        pass
    
    @abstractmethod
    def update_category_keywords(self, category: ArticleCategory, keywords: List[str]):
        """Update keywords for a specific category."""
        pass 