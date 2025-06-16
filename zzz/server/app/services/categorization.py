from typing import Dict, List, Tuple
from collections import Counter
from app.models.article import ArticleCategory
from .text_processor import TextProcessor
from .tfidf_calculator import TFIDFCalculator
from .category_scorer import CategoryScorer

class ArticleCategorizer:
    """Main article categorization service that coordinates between different components."""
    
    def __init__(self):
        self.category_keywords: Dict[ArticleCategory, List[str]] = {
            ArticleCategory.BUSINESS: [
                "stock", "market", "economy", "business", "finance", "trade",
                "investment", "banking", "currency", "stock market", "dow jones",
                "nasdaq", "s&p 500", "federal reserve", "inflation", "recession",
                "startup", "venture capital", "entrepreneurship", "profit", "revenue",
                "earnings", "quarterly", "annual", "dividend", "shareholder", "ipo",
                "merger", "acquisition", "market cap", "valuation", "funding"
            ],
            ArticleCategory.ENTERTAINMENT: [
                "movie", "film", "actor", "actress", "celebrity", "music",
                "concert", "album", "song", "artist", "entertainment", "show",
                "television", "tv", "netflix", "hulu", "amazon prime", "streaming",
                "box office", "premiere", "red carpet", "award", "oscar", "grammy",
                "director", "producer", "studio", "release", "trailer", "review",
                "performance", "tour", "concert", "festival", "premiere"
            ],
            ArticleCategory.SPORTS: [
                "sport", "football", "basketball", "baseball", "soccer",
                "tennis", "golf", "olympics", "championship", "tournament",
                "player", "team", "coach", "game", "match", "score", "league",
                "season", "playoff", "final", "victory", "defeat", "champion",
                "athlete", "competition", "stadium", "arena", "fans", "ticket",
                "broadcast", "live", "highlights", "statistics", "ranking"
            ],
            ArticleCategory.TECHNOLOGY: [
                "tech", "technology", "computer", "software", "hardware",
                "internet", "digital", "artificial intelligence", "ai", "machine learning",
                "blockchain", "cryptocurrency", "bitcoin", "programming", "coding",
                "startup", "innovation", "gadget", "device", "app", "cloud",
                "data", "security", "privacy", "cybersecurity", "algorithm",
                "platform", "interface", "user experience", "mobile", "web",
                "development", "engineer", "developer", "code", "system"
            ]
        }
        
        # Initialize components
        self.text_processor = TextProcessor()
        self.tfidf_calculator = TFIDFCalculator(
            self._calculate_document_frequency(),
            len(self.category_keywords)
        )
        self.category_scorer = CategoryScorer(self.category_keywords)
        
    def _calculate_document_frequency(self) -> Dict[str, int]:
        """Calculate initial document frequency for each keyword."""
        doc_freq = Counter()
        for keywords in self.category_keywords.values():
            for keyword in keywords:
                doc_freq[keyword] += 1
        return doc_freq
        
    def categorize_article(self, title: str, description: str, content: str) -> ArticleCategory:
        """Categorize an article based on its content."""
        text = f"{title} {description} {content}"
        category, _ = self.category_scorer.get_category_confidence(text, self.tfidf_calculator)
        return category
        
    def get_category_confidence(
        self,
        title: str,
        description: str,
        content: str
    ) -> Tuple[ArticleCategory, float]:
        """Get the predicted category and confidence score."""
        text = f"{title} {description} {content}"
        return self.category_scorer.get_category_confidence(text, self.tfidf_calculator)
        
    def update_category_keywords(self, category: ArticleCategory, keywords: List[str]):
        """Update keywords for a specific category."""
        self.category_scorer.update_category_keywords(category, keywords)
        # Update document frequency
        self.tfidf_calculator.update_document_frequency(
            {keyword: 1 for keyword in keywords}
        ) 