from ..service_interfaces import SendMailService
from ...util import TestSession 
from ...models import Email
import requests
import base64
import logging

class TestSendMailService(SendMailService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def send_mail(self, email: Email):
        return super().send_mail(email)