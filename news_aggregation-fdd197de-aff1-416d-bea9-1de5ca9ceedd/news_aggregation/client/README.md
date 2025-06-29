# News Aggregation Client

A console-based Python client for the News Aggregation System.

## Features

- **User Authentication**: Login and registration with role-based access
- **News Browsing**: View today's headlines, search articles, browse by category
- **Article Management**: Save and manage favorite articles
- **Admin Features**: Manage external servers, create categories, fetch news from APIs
- **Interactive Interface**: Colorful console interface with easy navigation

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Server**:
   - Ensure the News Aggregation Server is running on `http://localhost:8000`
   - Update `client/config/config.py` if your server runs on a different URL

## Usage

### Running the Client

```bash
python client/main.py
```

### User Features

1. **Authentication**:
   - Register a new account
   - Login with existing credentials
   - Automatic role detection (user/admin)

2. **News Browsing**:
   - View today's headlines with category filtering
   - Search articles with advanced filters
   - Browse articles by specific categories
   - View headlines for custom date ranges

3. **Article Management**:
   - Save interesting articles to reading list
   - View and manage saved articles
   - Delete articles from saved list

### Admin Features

1. **External Server Management**:
   - View all configured external news servers
   - Update API keys for news sources

2. **Category Management**:
   - Create new article categories

3. **News Fetching**:
   - Manually trigger news fetching from external APIs

## Client Structure

```
client/
├── config/
│   ├── __init__.py
│   └── config.py          # Configuration settings
├── controllers/
│   ├── __init__.py
│   ├── auth_controller.py # Authentication handling
│   ├── news_controller.py # News operations
│   └── admin_controller.py # Admin operations
├── utils/
│   ├── __init__.py
│   ├── api_client.py      # API communication
│   └── display.py         # Console display utilities
├── __init__.py
├── main.py               # Main application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

Edit `client/config/config.py` to customize:

- **API Settings**: Server URL, timeout values
- **Display Settings**: Colors, text lengths, date formats
- **Menu Options**: Available menu choices for users and admins

## Error Handling

The client includes comprehensive error handling:

- **Connection Errors**: Clear messages when server is unreachable
- **Authentication Errors**: Helpful feedback for login/registration issues
- **API Errors**: Detailed error messages from server responses
- **Input Validation**: User-friendly validation for all inputs

## Keyboard Shortcuts

- **Ctrl+C**: Exit the application
- **Enter**: Continue after viewing content
- **y/n**: Confirm or cancel actions

## Examples

### User Workflow

1. **Login**:
   ```
   Email: user@example.com
   Password: password123
   ```

2. **View Headlines**:
   ```
   Select option: 1
   Enter category to filter (or press Enter for all): Technology
   ```

3. **Save Article**:
   ```
   Select option: 4
   Enter article ID to save: 123
   ```

### Admin Workflow

1. **Manage Servers**:
   ```
   Select option: 8
   Enter action: update 1
   Enter new API key: your_new_api_key_here
   ```

2. **Create Category**:
   ```
   Select option: 9
   Enter category name: Science
   ```

## Troubleshooting

### Common Issues

1. **Connection Failed**:
   - Ensure the server is running on `http://localhost:8000`
   - Check firewall settings
   - Verify network connectivity

2. **Authentication Errors**:
   - Verify email and password
   - Check if account exists
   - Ensure proper email format

3. **Display Issues**:
   - Ensure terminal supports ANSI color codes
   - Check terminal size for proper formatting

### Debug Mode

For debugging, you can modify the API client to show detailed request/response information.

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include input validation
4. Update documentation for new features

## License

This client is part of the News Aggregation System. 