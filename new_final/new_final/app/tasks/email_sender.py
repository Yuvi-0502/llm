import threading
import time

def send_emails_periodically(interval_minutes=10):
    while True:
        # Here you would fetch pending notifications and send emails
        print("Sending notification emails...")
        time.sleep(interval_minutes * 60)

def start_email_sender():
    thread = threading.Thread(target=send_emails_periodically, daemon=True)
    thread.start() 