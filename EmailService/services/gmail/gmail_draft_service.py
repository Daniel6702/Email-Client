from ...models import Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import base64
from email import encoders
import logging

from ..service_interfaces import DraftService
from ...util import GmailSession 

class GmailDraftService(DraftService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def save_draft(self, email: Email):
        user_id = 'me'
        message = self.create_message(email)
        try:
            draft = self.service.users().drafts().create(userId=user_id, body={'message': message}).execute()
            logging.info(f'Draft created: {draft["id"]}')
        except Exception as error:
            logging.error(f'An error occurred: {error}')

    def update_draft(self, email: Email):
        user_id = 'me'
        message = self.create_message(email)
        try:
            draft_id = self.get_draft_id_from_message_id(user_id, email.id)
            if draft_id:
                updated_draft = self.service.users().drafts().update(userId=user_id, id=draft_id, body={'message': message}).execute()
                logging.info(f'Draft updated: {updated_draft["id"]}')
            else:
                logging.error(f'No draft found with message id: {email.id}')
        except Exception as error:
            logging.error(f'An error occurred: {error}')

    def get_draft_id_from_message_id(self, user_id: str, message_id: str) -> str:
        try:
            drafts = self.service.users().drafts().list(userId=user_id).execute().get('drafts', [])
            for draft in drafts:
                if 'message' in draft and draft['message']['id'] == message_id:
                    return draft['id']
            return None
        except Exception as error:
            logging.error(f'An error occurred: {error}')
            return None
        
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
    
    def is_html(self, text: str) -> bool:
        tags = ['<html>', '<head>', '<body>', '<p>', '<br>', '<h1>', '<h2>', '<div>']
        return any(tag in text.lower() for tag in tags)