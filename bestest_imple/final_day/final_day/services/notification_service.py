from Repositories.notification_repo import NotificationRepository
from Repositories.user_preference_repo import UserPreferenceRepository
from Repositories.user_repo import UserRepository
from Utils.email_utils import send_email
from config.constants import DEFAULT_CATEGORIES
from config.database import DbConnection

class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()
        self.user_pref_repo = UserPreferenceRepository()
        self.user_repo = UserRepository()

    def notify_users_for_articles(self, articles: list):
        # Get all users
        users = self.get_all_users()
        for user in users:
            pref = self.user_pref_repo.get_preferences(user['user_id'])
            if not pref:
                continue
            # Check category match
            for article in articles:
                match = False
                if pref['category_id']:
                    # If user has a preferred category
                    if article.get('category_id') == pref['category_id']:
                        match = True
                # Check keyword match
                if pref['keywords']:
                    keywords = [k.strip().lower() for k in pref['keywords'].split(',') if k.strip()]
                    article_text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
                    if any(kw in article_text for kw in keywords):
                        match = True
                if match:
                    # Store notification
                    title = f"New Article: {article.get('title', 'No title')}"
                    message = f"A new article matching your preferences is available.\nTitle: {article.get('title')}\nURL: {article.get('url')}"
                    self.notification_repo.add_notification(user['user_id'], title, message)
                    # Send email if enabled
                    if pref.get('email_notifications', True):
                        send_email(user['email'], title, message)

    def get_all_users(self):
        # Get all users from DB
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users 