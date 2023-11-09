from ...util import GmailSession 
from ..service_interfaces import MailManagementService
from email_util import Email

class GmailMailManagementService(MailManagementService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def delete_email(self, email: Email):
        try:
            self.service.users().messages().delete(userId='me', id=email.id).execute()
            print(f'Email with id: {email.id} has been deleted.')
        except Exception as error:
            print(f'An error occurred: {error}')

    def mark_email_as_unread(self, email: Email):
        self.mark_email_as(email, is_read=False)

    def mark_email_as_read(self, email: Email):
        self.mark_email_as(email, is_read=True)

    def mark_email_as(self, email: Email, is_read: bool):
        if is_read:
            body = {'removeLabelIds': ['UNREAD']}
        else:
            body = {'addLabelIds': ['UNREAD']}
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email.id,
                body=body
            ).execute()
            print(f"Email with ID {email.id} has marked is_read as {is_read} successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")