import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

class EmailSender:

    def __init__(self):
        self.port = 465
        self.context = ssl.create_default_context()
        self.load_config()

    def send_email(self, subject, message):
        # sender_email = "andreasioannou192@gmail.com"
        # receiver_email = "giorgos.christofi12@gmail.com"

        # Create a multipart message and set headers
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(message, 'plain'))

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.sender_email, self.email_password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.sender_email = config.get('Email', 'sender_email')
        self.receiver_email = config.get('Email', 'receiver_email')
        self.email_password = config.get('Email', 'sender_password')