from ...util import TestSession 
from ..service_interfaces import MailManagementService
from ...models import Email
import requests
import logging

class TestMailManagementService(MailManagementService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def delete_email(self, email: Email):
        return super().delete_email(email)
    
    def mark_email_as_read(self, email: Email):
        return super().mark_email_as_read(email)

    def mark_email_as_unread(self, email: Email):
        return super().mark_email_as_unread(email)

    def mark_email_as(self, email: Email, is_read: bool):
        return super().mark_email_as(email, is_read)