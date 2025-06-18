import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DbConnection:
    @staticmethod
    def get_db_connection():
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'news_aggregator'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                port=int(os.getenv('DB_PORT', 3306))
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return None

    @staticmethod
    def create_tables():
        """Create all necessary tables if they don't exist"""
        connection = DbConnection.get_db_connection()
        if connection is None:
            return False
        
        cursor = connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'user') DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # External servers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS external_servers (
                server_id INT AUTO_INCREMENT PRIMARY KEY,
                server_name VARCHAR(100) NOT NULL,
                api_key VARCHAR(255) NOT NULL,
                base_url VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                article_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                description TEXT,
                content TEXT,
                url VARCHAR(500),
                source VARCHAR(100),
                published_at TIMESTAMP,
                category_id INT,
                server_id INT,
                likes INT DEFAULT 0,
                dislikes INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id),
                FOREIGN KEY (server_id) REFERENCES external_servers(server_id)
            )
        """)
        
        # Saved articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_articles (
                saved_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                article_id INT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_article (user_id, article_id)
            )
        """)
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                preference_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                category_id INT,
                keywords TEXT,
                email_notifications BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        """)
        
        # Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                title VARCHAR(200) NOT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Insert default categories
        cursor.execute("""
            INSERT IGNORE INTO categories (name, description) VALUES 
            ('business', 'Business and financial news'),
            ('entertainment', 'Entertainment and celebrity news'),
            ('sports', 'Sports news and updates'),
            ('technology', 'Technology and innovation news'),
            ('general', 'General news and current events')
        """)
        
        # Insert default admin user if not exists
        cursor.execute("""
            INSERT IGNORE INTO users (user_name, email, password, role) VALUES 
            ('admin', 'admin@newsaggregator.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G', 'admin')
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True 