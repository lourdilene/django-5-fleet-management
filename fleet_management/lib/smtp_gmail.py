import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv('.env.development')

def send_email(subject, message, to_email, file_path=None):
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    port = 587  # Porta TLS

    # Para usar SSL
    # port = 465  # Porta SSL

    sender_email = 'lourdilene.souza@gmail.com'
    password = os.getenv('GMAIL_PASSWORD')

    # Compondo o email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
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

    # Iniciando a conexão SMTP
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Habilitando TLS
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())

subject = 'Your file is ready.'
message = 'You can make download your file in link below.'
to_email = 'lourdilene.souza@gmail.com'
file_path = '/home/lour/python-projects/fleet_management/debug.log'  # Opcional

send_email(subject, message, to_email, file_path)
