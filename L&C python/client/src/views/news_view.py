from .base_view import BaseView
from ..models.article import Article

class NewsView(BaseView):
    def show_news_menu(self, is_admin: bool):
        self.clear_screen()
        menu_items = [
            "1. View All News",
            "2. View by Category",
            "3. Search News",
            "4. View Saved Articles"
        ]
        if is_admin:
            menu_items.append("5. Admin Panel")
        menu_items.extend(["6. Logout", "7. Exit"])
        
        self.show_panel("News Menu", "\n".join(menu_items))
        return self.get_input("Select an option", choices=[str(i) for i in range(1, len(menu_items) + 1)])

    def show_categories(self, categories: list):
        self.clear_screen()
        self.show_panel("Categories", "\n".join(f"{i+1}. {cat}" for i, cat in enumerate(categories)))
        return self.get_input("Select a category", choices=[str(i) for i in range(1, len(categories) + 2)])

    def show_articles(self, articles: list[Article]):
        if not articles:
            self.show_warning("No articles found")
            return

        headers = ["Title", "Source", "Category", "Published"]
        rows = [
            [article.title, article.source, article.category, article.published_at]
            for article in articles
        ]
        self.show_table("Articles", headers, rows)

    def get_search_query(self):
        self.clear_screen()
        self.show_panel("Search News", "Enter your search query")
        return self.get_input("Search") 