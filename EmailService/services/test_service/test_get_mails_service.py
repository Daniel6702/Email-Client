from EmailService.models import Email
from ..service_interfaces import GetMailsService
from ...util import TestSession 
from ...models import Email, Folder
import json

class TestGetMailsService(GetMailsService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def get_mails(self, folder_id: str, query: str, max_results: int) -> list[Email]:
        with open('EmailService\\services\\test_service\\test_service_mock_data.json', 'r') as f:
            data = json.load(f)
        email_data = data.get('emails', [])
        emails = [Email(**email) for email in email_data]
        return emails