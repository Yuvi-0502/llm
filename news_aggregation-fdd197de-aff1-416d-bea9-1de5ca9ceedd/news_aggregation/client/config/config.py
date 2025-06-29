"""
Configuration settings for the News Aggregation Client
"""

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

# Authentication
AUTH_ENDPOINTS = {
    "login": "/auth/login",
    "register": "/auth/register"
}

# News Endpoints
NEWS_ENDPOINTS = {
    "status": "/news/status",
    "fetch": "/news/fetch",
    "today": "/news/today",
    "categories": "/news/categories"
}

# User Endpoints
USER_ENDPOINTS = {
    "headlines_today": "/user/headlines/today",
    "headlines_range": "/user/headlines/date-range",
    "saved_articles": "/user/saved-articles",
    "search": "/user/search",
    "categories": "/user/categories",
    "article": "/user/articles/{article_id}",
    "logout": "/user/logout"
}

# Admin Endpoints
ADMIN_ENDPOINTS = {
    "external_servers": "/external-servers",
    "update_server": "/external-servers/{server_id}",
    "create_category": "/categories"
}

# Display Settings
DISPLAY_SETTINGS = {
    "articles_per_page": 10,
    "max_title_length": 80,
    "max_description_length": 150,
    "date_format": "%Y-%m-%d %H:%M"
}

# Colors for console output (ANSI escape codes)
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m"
}

# Menu Options
MENU_OPTIONS = {
    "user": {
        "1": "View Today's Headlines",
        "2": "Search Articles",
        "3": "View Saved Articles",
        "4": "Save Article",
        "5": "View Categories",
        "6": "View Articles by Category",
        "7": "View Date Range Headlines",
        "8": "Logout",
        "0": "Exit"
    },
    "admin": {
        "1": "View Today's Headlines",
        "2": "Search Articles",
        "3": "View Saved Articles",
        "4": "Save Article",
        "5": "View Categories",
        "6": "View Articles by Category",
        "7": "View Date Range Headlines",
        "8": "Manage External Servers",
        "9": "Create Category",
        "10": "Fetch News from APIs",
        "11": "Logout",
        "0": "Exit"
    }
}

# Available Categories
CATEGORIES = [
    "Business", "Technology", "Sports", "Entertainment",
    "Politics", "Health", "Environment", "Cryptocurrency",
    "Science", "Education"
]

# Sort Options
SORT_OPTIONS = {
    "published_at": "Publication Date",
    "likes": "Likes",
    "dislikes": "Dislikes"
} 