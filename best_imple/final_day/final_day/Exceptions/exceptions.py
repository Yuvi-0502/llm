class UserAlreadyExistsException(Exception):
    """Raised when trying to create a user that already exists"""
    pass

class UserNotFoundException(Exception):
    """Raised when a user is not found"""
    pass

class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid"""
    pass

class ArticleNotFoundException(Exception):
    """Raised when an article is not found"""
    pass

class ExternalServerNotFoundException(Exception):
    """Raised when an external server is not found"""
    pass

class CategoryNotFoundException(Exception):
    """Raised when a category is not found"""
    pass

class NotificationException(Exception):
    """Raised when there's an error with notifications"""
    pass 