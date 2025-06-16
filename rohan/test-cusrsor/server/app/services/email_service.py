import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import get_settings
from app.models.models import Article, User

settings = get_settings()


def send_email(
    email_to: str,
    subject: str,
    html_content: str,
) -> None:
    """
    Send an email using the configured SMTP settings.
    """
    if not all([
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        settings.SMTP_USER,
        settings.SMTP_PASSWORD,
        settings.EMAILS_FROM_EMAIL
    ]):
        print("Email settings not configured")
        return

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = email_to

    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_TLS:
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(message)


def send_article_notification(
    user: User,
    articles: List[Article],
    category: Optional[str] = None
) -> None:
    """
    Send a notification email to a user about new articles.
    """
    subject = f"New Articles for You"
    if category:
        subject += f" in {category}"

    html_content = f"""
    <html>
        <body>
            <h2>Hello {user.username},</h2>
            <p>Here are some new articles that might interest you:</p>
            <ul>
    """

    for article in articles:
        html_content += f"""
            <li>
                <h3>{article.title}</h3>
                <p>{article.description}</p>
                <a href="{article.url}">Read more</a>
            </li>
        """

    html_content += """
            </ul>
            <p>Best regards,<br>News Aggregator Team</p>
        </body>
    </html>
    """

    send_email(user.email, subject, html_content)


def send_keyword_notification(
    user: User,
    articles: List[Article],
    keyword: str
) -> None:
    """
    Send a notification email to a user about articles matching their keywords.
    """
    subject = f"New Articles Matching Your Keyword: {keyword}"

    html_content = f"""
    <html>
        <body>
            <h2>Hello {user.username},</h2>
            <p>We found some new articles matching your keyword "{keyword}":</p>
            <ul>
    """

    for article in articles:
        html_content += f"""
            <li>
                <h3>{article.title}</h3>
                <p>{article.description}</p>
                <a href="{article.url}">Read more</a>
            </li>
        """

    html_content += """
            </ul>
            <p>Best regards,<br>News Aggregator Team</p>
        </body>
    </html>
    """

    send_email(user.email, subject, html_content) 