from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from app.models.models import Category

# Define category keywords
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Business": [
        "business", "economy", "market", "stock", "finance", "investment",
        "trading", "company", "corporate", "startup", "entrepreneur"
    ],
    "Technology": [
        "technology", "tech", "software", "hardware", "computer", "digital",
        "internet", "ai", "artificial intelligence", "machine learning",
        "blockchain", "cybersecurity"
    ],
    "Sports": [
        "sports", "football", "basketball", "baseball", "soccer", "tennis",
        "olympics", "championship", "tournament", "game", "match"
    ],
    "Entertainment": [
        "entertainment", "movie", "film", "music", "celebrity", "actor",
        "actress", "director", "concert", "show", "television", "tv"
    ]
}


async def categorize_article(text: str, db: Session) -> Optional[Category]:
    """
    Categorize an article based on its content using keyword matching.
    Returns the most relevant category or None if no match is found.
    """
    text = text.lower()
    category_scores: Dict[str, int] = {}

    # Score each category based on keyword matches
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score > 0:
            category_scores[category] = score

    if not category_scores:
        return None

    # Get the category with the highest score
    best_category = max(category_scores.items(), key=lambda x: x[1])[0]
    
    # Get or create the category in the database
    category = db.query(Category).filter(Category.name == best_category).first()
    if not category:
        category = Category(name=best_category)
        db.add(category)
        db.commit()
        db.refresh(category)

    return category 