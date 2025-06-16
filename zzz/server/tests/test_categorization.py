import pytest
from app.services.categorization import ArticleCategorizer
from app.models.article import ArticleCategory

@pytest.fixture
def categorizer():
    return ArticleCategorizer()

def test_categorize_business_article(categorizer):
    title = "Stock Market Reaches New Highs"
    description = "The Dow Jones Industrial Average surged to record levels"
    content = "Investors are optimistic about the economy's recovery"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.BUSINESS
    assert confidence > 0.5  # High confidence for clear business article

def test_categorize_entertainment_article(categorizer):
    title = "New Movie Release: The Last Adventure"
    description = "Starring famous actors in a blockbuster film"
    content = "The movie premiered at the Cannes Film Festival"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.ENTERTAINMENT
    assert confidence > 0.5  # High confidence for clear entertainment article

def test_categorize_sports_article(categorizer):
    title = "Championship Game Ends in Overtime"
    description = "Team wins the tournament in a thrilling match"
    content = "The players showed exceptional skill throughout the game"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.SPORTS
    assert confidence > 0.5  # High confidence for clear sports article

def test_categorize_technology_article(categorizer):
    title = "New AI Technology Revolutionizes Industry"
    description = "Machine learning algorithms improve efficiency"
    content = "The software uses advanced programming techniques"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.TECHNOLOGY
    assert confidence > 0.5  # High confidence for clear technology article

def test_categorize_general_article(categorizer):
    title = "Local Community Event"
    description = "Residents gather for annual celebration"
    content = "The event featured various activities and performances"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.GENERAL
    assert confidence < 0.3  # Low confidence for general article

def test_categorize_ambiguous_article(categorizer):
    title = "Tech Startup Raises Millions in Funding"
    description = "The company plans to revolutionize the market"
    content = "Investors are excited about the innovative technology"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    # Could be either BUSINESS or TECHNOLOGY
    assert category in [ArticleCategory.BUSINESS, ArticleCategory.TECHNOLOGY]
    assert confidence < 0.7  # Lower confidence for ambiguous article

def test_update_category_keywords(categorizer):
    new_keywords = ["startup", "venture capital", "entrepreneurship"]
    categorizer.update_category_keywords(ArticleCategory.BUSINESS, new_keywords)
    
    # Test categorization with new keywords
    title = "Startup Secures Venture Capital Funding"
    description = "Entrepreneurship is on the rise"
    content = "The company plans to expand its operations"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.BUSINESS
    assert confidence > 0.5  # High confidence after adding relevant keywords

def test_partial_keyword_matching(categorizer):
    title = "Tech Companies Face Market Challenges"
    description = "Innovation in the industry continues"
    content = "Developers are working on new solutions"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    assert category == ArticleCategory.TECHNOLOGY
    assert confidence > 0.3  # Moderate confidence for partial matches

def test_multiple_category_keywords(categorizer):
    title = "Sports Tech Startup Raises Funding"
    description = "Innovative technology for athletes"
    content = "The company plans to revolutionize sports training"
    
    category, confidence = categorizer.get_category_confidence(title, description, content)
    # Should pick the category with the strongest signal
    assert category in [ArticleCategory.TECHNOLOGY, ArticleCategory.SPORTS]
    assert confidence > 0.3  # Moderate confidence due to mixed signals 