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

    def send_email(self, subject, message, to_emails, file_path=None):
        # Compondo o email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Adicionando anexo
        if file_path:
            attachment = open(file_path, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {file_path.split("/")[-1]}')
            msg.attach(part)

        # Iniciando a conexão SMTP e enviando o email
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_emails, msg.as_string())

# Exemplo de uso da classe
# if __name__ == "__main__":
#     email_sender = EmailSender()
#     subject = 'Your file is ready.'
#     message = 'You can make download your file in link below.'
#     to_emails = ['lourdilene.souza@gmail.com', 'example@example.com']
#     file_path = '/home/lour/python-projects/fleet_management/debug.log'  # Opcional
#     email_sender.send_email(subject, message, to_emails, file_path)
