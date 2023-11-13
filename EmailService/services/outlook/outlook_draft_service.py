from ..service_interfaces import DraftService
from ...util import OutlookSession 
from ...models import Email
import requests
import json
import logging

class OutlookDraftService(DraftService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def save_draft(self, email: Email) -> None:
        headers, message = self.prepare_message(email)
        url = 'https://graph.microsoft.com/v1.0/me/messages'
        response = requests.post(url, headers=headers, data=json.dumps(message))

        self.handle_response(response, "save")

    def update_draft(self, email: Email) -> None:
        headers, message = self.prepare_message(email)
        url = f'https://graph.microsoft.com/v1.0/me/messages/{email.id}'
        response = requests.patch(url, headers=headers, data=json.dumps(message))

        self.handle_response(response, "update")

    def prepare_message(self, email: Email):
        to_recipients = [
            {'emailAddress': {'address': email_address}}
            for email_address in email.to_email
        ]
        headers = {
            'Authorization': 'Bearer ' + self.result['access_token'],
            'Content-Type': 'application/json',
        }
        message = {
            "subject": email.subject,
            "importance": "Low",
            "body": {
                "contentType": "HTML",
                "content": email.body
            },
            "toRecipients": to_recipients,
            "ccRecipients": to_recipients
        }
        if email.attachments:
            message['attachments'] = [self.draft_attachment(attachment) for attachment in email.attachments]
        
        return headers, message

    def handle_response(self, response, operation: str) -> None:
        if response.status_code in (201, 200):
            draft_message_id = response.json().get('id')
            logging.info(f"Successfully {operation}d draft with id: {draft_message_id}")
        else:
            logging.error(f"Failed to {operation} draft. Error: {response.text}")