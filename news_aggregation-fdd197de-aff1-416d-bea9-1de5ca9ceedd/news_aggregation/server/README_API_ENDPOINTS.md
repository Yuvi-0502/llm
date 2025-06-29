# News Aggregation API Documentation

This document provides comprehensive documentation for all REST API endpoints in the News Aggregation system.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### 1. News Management

#### Fetch News from External APIs
```http
POST /news/fetch
```
**Description:** Manually trigger news fetching from external APIs
**Response:**
```json
{
  "message": "25 articles stored and categorized from external APIs",
  "sources": "Multiple external APIs"
}
```

#### Get News System Status
```http
GET /news/status
```
**Description:** Get status of news fetching and database
**Response:**
```json
{
  "status": "operational",
  "total_articles": 1250,
  "categories": [
    {"category_id": 1, "category_name": "Business"},
    {"category_id": 2, "category_name": "Technology"}
  ],
  "message": "News aggregation system is running"
}
```

#### Get All Articles
```http
GET /news/articles?page=1&limit=50&category=Technology&sort_by=published_at
```
**Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)
- `category` (string, optional): Filter by category
- `sort_by` (string, optional): Sort by "likes", "dislikes", or "published_at"

#### Get Article by ID
```http
GET /news/articles/{article_id}
```
**Parameters:**
- `article_id` (int, required): Article ID

#### Get Categories
```http
GET /news/categories
```
**Response:**
```json
{
  "categories": [
    {"category_id": 1, "category_name": "Business"},
    {"category_id": 2, "category_name": "Technology"},
    {"category_id": 3, "category_name": "Sports"}
  ]
}
```

#### Get Articles by Category
```http
GET /news/categories/{category}/articles?page=1&limit=50
```
**Parameters:**
- `category` (string, required): Category name
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Search Articles
```http
GET /news/search?query=tesla&page=1&limit=50&category=Business&sort_by=published_at
```
**Parameters:**
- `query` (string, required): Search query
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)
- `category` (string, optional): Filter by category
- `sort_by` (string, optional): Sort by "likes", "dislikes", or "published_at"

#### Get Today's Articles
```http
GET /news/today?page=1&limit=50&category=Technology
```
**Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)
- `category` (string, optional): Filter by category

#### Get Articles by Date Range
```http
GET /news/date-range?start_date=2024-01-01&end_date=2024-01-15&page=1&limit=50&category=Business
```
**Parameters:**
- `start_date` (string, required): Start date (YYYY-MM-DD)
- `end_date` (string, required): End date (YYYY-MM-DD)
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)
- `category` (string, optional): Filter by category

### 2. User-Specific Endpoints (Requires Authentication)

#### Get Today's Headlines
```http
GET /user/headlines/today?category=Technology&page=1&limit=50
```
**Parameters:**
- `category` (string, optional): Filter by category
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Get Headlines by Date Range
```http
GET /user/headlines/date-range?start_date=2024-01-01&end_date=2024-01-15&category=Business&page=1&limit=50
```
**Parameters:**
- `start_date` (string, required): Start date (YYYY-MM-DD)
- `end_date` (string, required): End date (YYYY-MM-DD)
- `category` (string, optional): Filter by category
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Get Article by ID
```http
GET /user/articles/{article_id}
```
**Parameters:**
- `article_id` (int, required): Article ID

#### Get Categories
```http
GET /user/categories
```

#### Get Articles by Category
```http
GET /user/categories/{category}/articles?page=1&limit=50
```
**Parameters:**
- `category` (string, required): Category name
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Get Saved Articles
```http
GET /user/saved-articles?page=1&limit=50
```
**Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Save Article
```http
POST /user/saved-articles?article_id=123
```
**Parameters:**
- `article_id` (int, required): Article ID to save

#### Delete Saved Article
```http
DELETE /user/saved-articles/{article_id}
```
**Parameters:**
- `article_id` (int, required): Article ID to remove

#### Search Articles
```http
GET /user/search?query=tesla&start_date=2024-01-01&end_date=2024-01-15&sort_by=published_at&page=1&limit=50
```
**Parameters:**
- `query` (string, required): Search query
- `start_date` (string, optional): Start date filter (YYYY-MM-DD)
- `end_date` (string, optional): End date filter (YYYY-MM-DD)
- `sort_by` (string, optional): Sort by "likes", "dislikes", or "published_at"
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Articles per page (default: 50, max: 100)

#### Get Notifications
```http
GET /user/notifications?page=1&limit=50
```
**Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Notifications per page (default: 50, max: 100)

#### Logout
```http
POST /user/logout
```

### 3. Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}
```

### 4. External Server Management (Admin Only)

#### Get All External Servers
```http
GET /external-servers
```

#### Update External Server
```http
PUT /external-servers/{server_id}
Content-Type: application/json

{
  "api_key": "new_api_key_here"
}
```

### 5. Category Management (Admin Only)

#### Create Category
```http
POST /categories
Content-Type: application/json

{
  "category_name": "Science"
}
```

## Response Formats

### Success Response
```json
{
  "articles": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1250,
    "pages": 25
  },
  "category": "Technology"
}
```

### Error Response
```json
{
  "error": "Failed to fetch articles: Database connection error"
}
```

### Article Object Structure
```json
{
  "article_id": 123,
  "title": "Tesla Stock Surges After Strong Q4 Earnings",
  "description": "Tesla reported better-than-expected earnings...",
  "content": "Tesla's quarterly earnings exceeded...",
  "source": "Financial Times",
  "url": "https://example.com/article",
  "published_at": "2024-01-15T10:30:00",
  "likes": 45,
  "dislikes": 2,
  "categories": "Business,Technology"
}
```

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (starts from 1)
- `limit`: Number of items per page (1-100)

The response includes pagination metadata:
```json
{
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1250,
    "pages": 25
  }
}
```

## Filtering and Sorting

### Categories
Available categories: Business, Technology, Sports, Entertainment, Politics, Health, Environment, Cryptocurrency, Science, Education

### Sorting Options
- `published_at`: Sort by publication date (newest first)
- `likes`: Sort by number of likes (highest first)
- `dislikes`: Sort by number of dislikes (highest first)

### Date Format
All dates should be in `YYYY-MM-DD` format.

## Rate Limiting

- **Public endpoints**: 100 requests per minute
- **Authenticated endpoints**: 1000 requests per minute
- **Admin endpoints**: 500 requests per minute

## Error Codes

- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Missing or invalid authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `422`: Validation Error - Invalid request data
- `500`: Internal Server Error - Server error

## Examples

### Get Today's Technology News
```bash
curl -X GET "http://localhost:8000/user/headlines/today?category=Technology&page=1&limit=20" \
  -H "Authorization: Bearer your_jwt_token"
```

### Search for Tesla Articles
```bash
curl -X GET "http://localhost:8000/user/search?query=tesla&category=Business&sort_by=published_at" \
  -H "Authorization: Bearer your_jwt_token"
```

### Save an Article
```bash
curl -X POST "http://localhost:8000/user/saved-articles?article_id=123" \
  -H "Authorization: Bearer your_jwt_token"
```

### Manual News Fetch
```bash
curl -X POST "http://localhost:8000/news/fetch"
``` 