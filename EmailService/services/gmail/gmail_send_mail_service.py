from ...models import Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import base64
from email import encoders
import logging

from ..service_interfaces import SendMailService
from ...util import GmailSession 

class GmailSendMailService(SendMailService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def send_mail(self, email: Email) -> bool:
        message = self.create_message(email)
        user_id = email.from_email
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            logging.info(f'Message sent: {message["id"]}')
            return True
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            return False

    def create_message(self, email: Email) -> dict:
        message = MIMEMultipart()
        message['to'] = ', '.join(email.to_email) 
        message['subject'] = email.subject

        if self.is_html(email.body):
            part = MIMEText(email.body, 'html')
        else:
            part = MIMEText(email.body, 'plain')

        message.attach(part)

        for attachment in email.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment['file_data'])
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment["file_name"]}"')
            message.attach(part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}
    
    def is_html(self, text):
        tags = ['<html>', '<head>', '<body>', '<p>', '<br>', '<h1>', '<h2>', '<div>']
        return any(tag in text.lower() for tag in tags)