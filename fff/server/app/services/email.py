import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings
from typing import List

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password]):
            return False

        msg = MIMEMultipart()
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_news_notification(self, to_email: str, articles: List[dict]) -> bool:
        subject = "Your News Update"
        body = "<h2>Latest News Articles</h2>"
        
        for article in articles:
            body += f"""
            <div style='margin-bottom: 20px;'>
                <h3>{article['title']}</h3>
                <p>{article['description']}</p>
                <p><a href='{article['url']}'>Read more</a></p>
            </div>
            """
        
        return self.send_email(to_email, subject, body)

email_service = EmailService() 