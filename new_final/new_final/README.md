# News Aggregation Project

This project is a News Aggregation system built with FastAPI and MySQL. It collects news from external APIs, processes and stores them, and provides a RESTful API for client applications. The system supports user authentication, article saving, notifications, and admin management features.

## Features
- User and Admin roles
- News fetching from multiple external APIs
- Article saving and feedback
- Notification and keyword management
- RESTful API (FastAPI)
- MySQL database (SQLAlchemy ORM)
- SOLID, MVC, and OOP principles
- Background tasks for periodic news fetching and email notifications
- API documentation (Swagger UI)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your MySQL database in `app/core/config.py`.
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing
Run tests with:
```bash
pytest
``` 