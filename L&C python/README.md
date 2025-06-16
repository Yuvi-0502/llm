# News Aggregation System

A comprehensive news aggregation system built with Python, following SOLID principles and MVC architecture.

## Project Structure

```
news_aggregation/
├── server/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── news_service.py
│   │   │   └── user_service.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_api/
│   ├── .env
│   └── main.py
├── client/
│   ├── src/
│   │   ├── services/
│   │   │   └── api_client.py
│   │   └── main.py
│   └── requirements.txt
└── README.md
```

## Server Setup

1. Create a virtual environment:
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env` file:
```
DATABASE_URL=mysql+pymysql://user:password@localhost/news_aggregation
SECRET_KEY=your-secret-key
NEWS_API_KEY=your-news-api-key
THENEWS_API_KEY=your-thenews-api-key
```

4. Run the server:
```bash
uvicorn main:app --reload
```

## Client Setup

1. Create a virtual environment:
```bash
cd client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the client:
```bash
python src/main.py
```

## Features

- User Authentication (Admin/User roles)
- News aggregation from multiple sources
- Article saving and management
- Category-based news filtering
- Search functionality
- Email notifications
- Notification preferences

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run server tests:
```bash
cd server
pytest
```

Run client tests:
```bash
cd client
pytest
```

## Database Schema

The application uses MySQL with the following main tables:
- users
- news_articles
- saved_articles
- categories
- notifications
- external_servers

## Architecture

The project follows:
- SOLID principles
- MVC architecture
- RESTful API design
- Layered architecture
- Clean code principles 