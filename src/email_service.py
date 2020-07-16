import os
import smtplib
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()


class EmailService:
    port = 587
    link = 'smtp.gmail.com'

    @classmethod
    def send_mail(cls, data):
        with smtplib.SMTP(host=cls.link, port=cls.port) as server:
            server.starttls()
            server.ehlo()
            server.login(os.environ['FROM_ADDR'], os.environ['FROM_PW'])
            message = cls.create_mail(data)
            server.sendmail(os.environ['FROM_ADDR'], os.environ['TO_ADDRS'].split(','), message)

    @classmethod
    def create_mail(cls, data):
        mail = MIMEMultipart('alternative', None, [MIMEText(cls.create_email_content(data), 'html')])
        mail['Subject'] = 'Deal of the Day'
        return mail.as_string()

    @staticmethod
    def create_email_content(parsed_data):
        with open('templates/mail_template.html') as f:
            template = Template(f.read())
            return template.render(parsed_data=parsed_data)
