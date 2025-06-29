from typing import Dict

class CategoryClassifier:

    CATEGORY_KEYWORDS: Dict[str, list] = {
        "Business": ["business", "economy", "finance", "market", "stock", "investors", "ipo", "startup"],
        "Entertainment": ["movie", "film", "tv", "netflix", "actor", "music", "entertainment"],
        "Sports": ["football", "cricket", "nba", "fifa", "match", "tournament", "player"],
        "Technology": ["technology", "ai", "artificial intelligence", "data", "machine learning", "cloud", "robotics"],
        "Cryptocurrency": ["bitcoin", "crypto", "ethereum", "blockchain", "web3", "token", "wallet"],
        "Politics": ["trump", "biden", "election", "government", "law", "policy", "senate", "president"],
        "Health": ["health", "vaccine", "doctor", "hospital", "covid", "fitness", "medicine"],
        "Environment": ["climate", "carbon", "sustainability", "pollution", "green", "earthquake", "disaster"],
    }

    DEFAULT_CATEGORY = "All"

    def classify(self, title: str, description: str, content: str = ""):
        text = f"{title} {description} {content}".lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return category

        return self.DEFAULT_CATEGORY