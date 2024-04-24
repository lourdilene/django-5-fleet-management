import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

class Smtp:
    def __init__(self):
        load_dotenv('.env.development')
        self.sender_email = os.getenv('SMTP_GMAIL_USERNAME')
        self.password = os.getenv('SMTP_GMAIL_PASSWORD')
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587  # Porta TLS

    def send_email(self, subject, message, to_emails):
        # Compondo o email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_emails, msg.as_string())