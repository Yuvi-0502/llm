from typing import Dict, List, Tuple
from app.models.article import ArticleCategory
from .tfidf_calculator import TFIDFCalculator

class CategoryScorer:
    """Handles category scoring and matching."""
    
    def __init__(self, category_keywords: Dict[ArticleCategory, List[str]]):
        self.category_keywords = category_keywords
    
    def calculate_category_score(
        self,
        text: str,
        category: ArticleCategory,
        tf_idf_scores: Dict[str, float]
    ) -> float:
        """Calculate score for a specific category."""
        score = 0
        category_keywords = self.category_keywords[category]
        
        for keyword in category_keywords:
            if keyword in tf_idf_scores:
                score += tf_idf_scores[keyword] * 2  # Give more weight to exact matches
            else:
                # Check for partial matches
                for word, score_value in tf_idf_scores.items():
                    if keyword in word or word in keyword:
                        score += score_value
                        
        return score
    
    def get_category_confidence(
        self,
        text: str,
        tf_idf_calculator: TFIDFCalculator
    ) -> Tuple[ArticleCategory, float]:
        """Get the predicted category and confidence score."""
        tf_idf_scores = tf_idf_calculator.calculate_tf_idf(text)
        
        category_scores = {
            category: self.calculate_category_score(text, category, tf_idf_scores)
            for category in self.category_keywords.keys()
        }
        
        max_score = max(category_scores.values())
        if max_score == 0:
            return ArticleCategory.GENERAL, 0.0
            
        total_score = sum(category_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return max(category_scores.items(), key=lambda x: x[1])[0], confidence
    
    def update_category_keywords(self, category: ArticleCategory, keywords: List[str]):
        """Update keywords for a specific category."""
        if category in self.category_keywords:
            self.category_keywords[category].extend(keywords)
            # Remove duplicates
            self.category_keywords[category] = list(set(self.category_keywords[category])) 