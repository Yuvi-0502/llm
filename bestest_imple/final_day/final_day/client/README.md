# News Aggregator Client - Modular Structure

## Overview
The client application has been modularized into separate components for better maintainability, testability, and code organization.

## Module Structure

### `base_client.py`
- **BaseClient**: Core functionality shared across all client modules
- **Features**:
  - HTTP request handling
  - Screen management (clear, headers, menus)
  - Email validation
  - User session management (token, logout)

### `auth_client.py`
- **AuthClient**: User authentication and registration
- **Features**:
  - User registration with validation
  - User login with JWT token handling
  - Password confirmation and role selection

### `news_client.py`
- **NewsClient**: News browsing and management
- **Features**:
  - Display articles in formatted view
  - Headlines menu (today, date range)
  - Saved articles management
  - Search functionality with filters
  - Article actions (save, delete)

### `notification_client.py`
- **NotificationClient**: Notification management
- **Features**:
  - View notifications (read/unread)
  - Configure notification preferences
  - Email notification settings
  - Keyword and category preferences

### `admin_client.py`
- **AdminClient**: Administrative functions
- **Features**:
  - External server management
  - Server status monitoring
  - Category management
  - API key management

### `user_client.py`
- **UserClient**: Regular user functionality
- **Features**:
  - User menu orchestration
  - Integration with news and notification clients
  - Token synchronization across modules

### `main_client.py`
- **NewsAggregatorClient**: Main application orchestrator
- **Features**:
  - Inherits from all client modules
  - Main menu and application flow
  - Role-based routing (admin/user)
  - Session management

## Benefits of Modularization

1. **Separation of Concerns**: Each module handles a specific domain
2. **Maintainability**: Easier to modify individual features
3. **Testability**: Each module can be tested independently
4. **Reusability**: Modules can be reused in different contexts
5. **Scalability**: Easy to add new features or modify existing ones

## Usage

```python
from client.main_client import NewsAggregatorClient

# Start the application
client = NewsAggregatorClient()
client.main_menu()
```

## File Structure
```
client/
├── __init__.py
├── README.md
├── base_client.py
├── auth_client.py
├── news_client.py
├── notification_client.py
├── admin_client.py
├── user_client.py
└── main_client.py
```

## Design Patterns Used

1. **Inheritance**: Main client inherits from all functional modules
2. **Composition**: UserClient composes NewsClient and NotificationClient
3. **Single Responsibility**: Each module has one clear purpose
4. **Dependency Injection**: Base URL and configuration passed to modules 