from ..service_interfaces import SendMailService
from ...util import OutlookSession 
from ...models import Email
import requests
import base64
import logging

class OutlookSendMailService(SendMailService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def send_mail(self, email: Email) -> bool:
        to_recipients = [
            {
                'emailAddress': {
                    'address': email_address
                }
            }
            for email_address in email.to_email
        ]
        request_body = {
            'message': {
                'toRecipients': to_recipients,
                'subject': email.subject,
                'importance': 'normal',
                'body': {
                    'contentType': 'html', 
                    'content': email.body
                }
            }
        }

        if email.attachments:
            request_body['message']['attachments'] = [self.draft_attachment(attachment) for attachment in email.attachments]

        headers = {
            'Authorization': 'Bearer ' + self.result['access_token']
        }

        endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'

        try:
            response = requests.post(endpoint, headers=headers, json=request_body)
            response.raise_for_status()
            logging.info(f"Attempting to send email to: {email.to_email}")

            if response.status_code == 202:
                to_email_list = ', '.join(email.to_email)
                logging.info(f"Email successfully sent to: {to_email_list}")
                return True
            else:
                failed_recipients = ', '.join(email.to_email)
                logging.error(f"Email not sent to: {failed_recipients}. Error: {response}")
                return False
            
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            return False

    def draft_attachment(self, attachment: dict) -> dict:
        file_data = base64.b64encode(attachment['file_data'])
        data_body = {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'contentBytes': file_data.decode('utf-8'),
            'name': attachment['file_name'],
        }
        return data_body