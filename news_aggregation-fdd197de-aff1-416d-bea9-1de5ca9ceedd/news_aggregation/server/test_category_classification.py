#!/usr/bin/env python3
"""
Test script to verify category classification and mapping functionality
"""

from server.services.news_service-1 import NewsService
from server.schemas.news-1 import NewsArticleCreate
from server.utils.category_classifier import CategoryClassifier
from datetime import datetime

def test_category_classification():
    """Test the category classification and mapping functionality"""
    
    # Initialize the news service
    news_service = NewsService()
    
    # Create test articles with different scenarios
    test_articles = [
        NewsArticleCreate(
            server_id=1,
            title="Tesla Stock Surges After Strong Q4 Earnings",
            description="Tesla reported better-than-expected earnings, causing stock prices to jump significantly.",
            content="Tesla's quarterly earnings exceeded analyst expectations...",
            source="Financial Times",
            url="https://example.com/tesla-earnings",
            published_at=datetime.now(),
            categories=[]  # No categories - should be classified as Business
        ),
        NewsArticleCreate(
            server_id=1,
            title="New AI Breakthrough in Machine Learning",
            description="Researchers develop new algorithm that improves AI performance by 50%",
            content="A team of researchers has developed...",
            source="Tech News",
            url="https://example.com/ai-breakthrough",
            published_at=datetime.now(),
            categories=["Technology"]  # Has category - should use it
        ),
        NewsArticleCreate(
            server_id=1,
            title="Football Championship Final Draws Record Viewers",
            description="The championship match between top teams attracted millions of viewers worldwide",
            content="The highly anticipated football championship...",
            source="Sports Central",
            url="https://example.com/football-championship",
            published_at=datetime.now(),
            categories=[]  # No categories - should be classified as Sports
        ),
        NewsArticleCreate(
            server_id=1,
            title="Bitcoin Reaches New All-Time High",
            description="Cryptocurrency market sees unprecedented growth as Bitcoin breaks records",
            content="The cryptocurrency market experienced...",
            source="Crypto News",
            url="https://example.com/bitcoin-high",
            published_at=datetime.now(),
            categories=[]  # No categories - should be classified as Cryptocurrency
        )
    ]
    
    print("Testing category classification and mapping...")
    print("=" * 50)
    
    for i, article in enumerate(test_articles, 1):
        print(f"\nTest Article {i}: {article.title}")
        print(f"Original categories: {article.categories}")
        
        # Test classification directly
        classifier = CategoryClassifier()
        classified_category = classifier.classify(
            title=article.title,
            description=article.description,
            content=article.content
        )
        print(f"Classified as: {classified_category}")
        
        # Save the article
        article_id = news_service.news_repo.save(article)
        if article_id:
            print(f"Article saved with ID: {article_id}")
            
            # Classify and map the article
            news_service._classify_and_map_article(article, article_id)
        else:
            print("Failed to save article")
    
    print("\n" + "=" * 50)
    print("Category classification test completed!")

if __name__ == "__main__":
    test_category_classification() 