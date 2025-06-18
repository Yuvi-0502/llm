# API URLs for external news sources
API_URL = {
    "NewsAPI": "https://newsapi.org/v2/top-headlines?country=us&apiKey=",
    "The News API": "https://api.thenewsapi.com/v1/news/top?api_token=",
    "Firebase API": "https://us-central1-symbolic-gift98004.cloudfunctions.net/newsapi?country=us&category=business"
}

# HTTP Status Codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500

# JWT Configuration
JWT_SECRET_KEY = "your-secret-key-here"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"

# News Categories
DEFAULT_CATEGORIES = [
    "business",
    "entertainment", 
    "sports",
    "technology",
    "general"
]

# Pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100 