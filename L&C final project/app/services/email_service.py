import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from app.core.config import settings
from app.models.news import NewsArticle
from app.models.user import User

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_news_notification(self, user: User, articles: List[NewsArticle]) -> bool:
        if not articles:
            return True

        subject = "Your News Update"
        
        # Create HTML content
        html_content = f"""
        <html>
            <body>
                <h2>Hello {user.username},</h2>
                <p>Here are your latest news updates:</p>
                <ul>
        """
        
        for article in articles:
            html_content += f"""
                <li>
                    <h3>{article.title}</h3>
                    <p>{article.description}</p>
                    <p>Category: {article.category.value}</p>
                    <p>Source: {article.source}</p>
                    <p><a href="{article.url}">Read more</a></p>
                </li>
            """
        
        html_content += """
                </ul>
                <p>Thank you for using our News Aggregation service!</p>
            </body>
        </html>
        """
        
        return self.send_email(user.email, subject, html_content)

    def send_keyword_notification(self, user: User, articles: List[NewsArticle], keyword: str) -> bool:
        if not articles:
            return True

        subject = f"News Updates for Keyword: {keyword}"
        
        html_content = f"""
        <html>
            <body>
                <h2>Hello {user.username},</h2>
                <p>Here are the latest news articles matching your keyword "{keyword}":</p>
                <ul>
        """
        
        for article in articles:
            html_content += f"""
                <li>
                    <h3>{article.title}</h3>
                    <p>{article.description}</p>
                    <p>Category: {article.category.value}</p>
                    <p>Source: {article.source}</p>
                    <p><a href="{article.url}">Read more</a></p>
                </li>
            """
        
        html_content += """
                </ul>
                <p>Thank you for using our News Aggregation service!</p>
            </body>
        </html>
        """
        
        return self.send_email(user.email, subject, html_content) 