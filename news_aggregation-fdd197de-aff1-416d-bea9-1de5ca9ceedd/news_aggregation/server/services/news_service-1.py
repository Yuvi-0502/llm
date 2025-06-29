import requests
from server.schemas.news-1 import NewsArticleCreate
from server.repos.news_repository import NewsRepository
from server.repos.category_repo import CategoryRepo
from server.repos.external_api_repo import ExternalAPIRepository
from server.config.constants import API_URL
from server.utils.category_classifier import CategoryClassifier
from server.services.api_manager import APIManager

class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.api_manager = APIManager()
        self.category_repo = CategoryRepo()
        self.classifier = CategoryClassifier()
        # Ensure default categories exist when service is initialized
        self.category_repo.ensure_default_categories_exist()

    def get_active_api(self):
        active_apis = self.api_manager.get_active_apis()
        return active_apis[0] if active_apis else None

    def fetch_news(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
        return None

    def _classify_and_map_article(self, article, article_id):
        """Classify article and map it to categories in the database"""
        categories_to_map = []
        
        # If article has categories from the API, use them
        if article.categories and len(article.categories) > 0:
            categories_to_map = article.categories
        else:
            # Use category classifier to determine category
            classified_category = self.classifier.classify(
                title=article.title or "",
                description=article.description or "",
                content=article.content or ""
            )
            categories_to_map = [classified_category]
            print(f"Classified article '{article.title}' as: {classified_category}")
        
        # Map each category to the article
        for category_name in categories_to_map:
            if category_name:
                # Get or create category
                category = self.category_repo.get_by_name(category_name)
                if not category:
                    print(f"Creating new category: {category_name}")
                    category = self.category_repo.create_category(category_name)
                
                category_id = category["category_id"]
                
                # Insert mapping
                try:
                    self.category_repo.insert_article_category(category_id, article_id)
                    print(f"Mapped Article {article_id} to Category '{category_name}' (ID: {category_id})")
                except Exception as e:
                    print(f"Error mapping article {article_id} to category {category_name}: {e}")

    def fetch_news_from_api(self):
        print("Starting sync from external APIs...")

        articles = self.api_manager.fetch_news_from_all_active_servers()
        if not articles:
            return {"error": "No articles fetched from any external APIs"}

        saved_count = 0
        print(f"Fetched {len(articles)} articles from external APIs")
        
        for article in articles:
            print(f"Processing article: {article.title}")
            
            # Save article to database
            article_id = self.news_repo.save(article)
            if not article_id:
                print(f"Failed to save article: {article.title}")
                continue
            
            # Classify and map article to categories
            self._classify_and_map_article(article, article_id)
            saved_count += 1

        print(f"{saved_count} articles stored and categorized from external APIs")
        return {
            "message": f"{saved_count} articles stored and categorized from external APIs",
            "sources": "Multiple external APIs"
        }
