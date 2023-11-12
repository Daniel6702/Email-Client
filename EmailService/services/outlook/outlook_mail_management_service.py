from ...util import OutlookSession 
from ..service_interfaces import MailManagementService
from email_util import Email
import requests
import logging

class OutlookMailManagementService(MailManagementService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def delete_email(self, email: Email):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}"
        }

        endpoint_url = f"https://graph.microsoft.com/v1.0/me/messages/{email.id}"

        try:
            response = requests.delete(endpoint_url, headers=headers)
            response.raise_for_status()
            logging.info(f"Email with ID {email.id} deleted successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
        
    def mark_email_as_unread(self, email: Email):
        self.mark_email_as(email, is_read=False)
        
    def mark_email_as_read(self, email: Email):
        self.mark_email_as(email, is_read=True)
        
    def mark_email_as(self, email: Email, is_read: bool):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}",
            "Content-Type": "application/json"
        }
        endpoint_url = f"https://graph.microsoft.com/v1.0/me/messages/{email.id}"

        payload = {
            "isRead": is_read
        }
        try:
            response = requests.patch(endpoint_url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Email with ID {email.id} marked is_read as {is_read} successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
