# News Aggregation System

A comprehensive news aggregation system built with FastAPI, following SOLID principles, MVC architecture, and OOP concepts.

## Features

- User Authentication (Admin/User roles)
- News aggregation from multiple sources
- Article saving and management
- Email notifications
- Category-based news filtering
- Search functionality
- Real-time news updates

## Project Structure

```
news_aggregation/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── news.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   └── news.py
│   │   ├── services/
│   │   │   ├── news_service.py
│   │   │   └── email_service.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── .env
│   └── requirements.txt
└── main.py
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file
5. Run the application:
   ```bash
   uvicorn main:app --reload
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

This project uses PostgreSQL as the database system because:
1. Strong data consistency requirements
2. Complex relationships between entities
3. Need for ACID compliance
4. Robust transaction support
5. Excellent support for JSON data types

## External APIs Used

1. NewsAPI (https://newsapi.org/)
2. The News API (https://www.thenewsapi.com/documentation)

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation
- Rate limiting
- CORS protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 