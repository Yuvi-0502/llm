# News Aggregation System

A comprehensive news aggregation system built with Python, FastAPI, and MySQL.

## Features

- User Authentication (Admin/User roles)
- News aggregation from multiple sources
- Article saving and management
- Email notifications
- Category-based news filtering
- Search functionality
- Admin dashboard for external API management

## Project Structure

```
news_aggregation/
├── server/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   └── main.py
├── client/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── views/
│   │   └── utils/
│   ├── tests/
│   └── main.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the server directory with:
```
DATABASE_URL=mysql+pymysql://user:password@localhost/news_aggregation
SECRET_KEY=your-secret-key
NEWS_API_KEY=your-news-api-key
THENEWS_API_KEY=your-thenews-api-key
```

4. Initialize the database:
```bash
cd server
python -m app.db.init_db
```

5. Run the server:
```bash
cd server
uvicorn main:app --reload
```

6. Run the client:
```bash
cd client
python main.py
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests using pytest:
```bash
pytest
```

## Database Choice

This project uses MySQL as the database because:
1. Structured data with clear relationships between entities
2. ACID compliance for data integrity
3. Strong support for complex queries and joins
4. Mature ecosystem and tooling
5. Excellent performance for read-heavy operations 