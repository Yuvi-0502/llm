# News Aggregation System

A comprehensive news aggregation system with server and client applications.

## Project Structure

```
news_aggregator/
├── server/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
├── client/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
└── README.md
```

## Features

### Server Application
- News feed collection from multiple sources
- RESTful API endpoints
- User authentication and management
- News data processing and categorization
- Email notification system
- Database management

### Client Application
- User authentication (Admin/User roles)
- News browsing and searching
- Article saving functionality
- Notification configuration
- Keyword-based news filtering

## Setup Instructions

1. Clone the repository
2. Set up virtual environments for both server and client
3. Install dependencies:
   ```bash
   # Server
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Client
   cd ../client
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create `.env` files in both server and client directories
   - Add necessary API keys and configuration

5. Run the applications:
   ```bash
   # Server
   cd server
   python run.py

   # Client
   cd client
   python run.py
   ```

## API Documentation

The API documentation is available at `/api/docs` when running the server.

## Testing

Run tests using pytest:
```bash
# Server tests
cd server
pytest

# Client tests
cd client
pytest
```

## Technologies Used

- Python 3.8+
- FastAPI (Server)
- SQLAlchemy (Database ORM)
- PostgreSQL (Database)
- Pydantic (Data validation)
- pytest (Testing)
- requests (HTTP client)
- python-dotenv (Environment management) 