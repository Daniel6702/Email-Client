from ..service_interfaces import DraftService
from ...util import OutlookSession 
from email_util import Email
import requests
import json

class OutlookDraftService(DraftService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def save_mail(self, email: Email) -> None:
        to_recipients = [
            {
                'emailAddress': {
                    'address': email_address
                }
            }
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
        if email.id:
            url = f'https://graph.microsoft.com/v1.0/me/messages/{email.id}'
            response = requests.patch(url, headers=headers, data=json.dumps(message))
            operation = "update"
        else:
            url = 'https://graph.microsoft.com/v1.0/me/messages'
            response = requests.post(url, headers=headers, data=json.dumps(message))
            operation = "save"

        if response.status_code in (201, 200):
            print(f"Draft {operation}d successfully.")
            draft_message_id = response.json().get('id')
            print(f"Draft ID: {draft_message_id}")
        else:
            print(f"Failed to {operation} draft.")
            print(f"Status Code: {response.status_code}, Response: {response.text}")