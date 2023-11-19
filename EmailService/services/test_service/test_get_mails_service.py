from EmailService.models import Email
from ..service_interfaces import GetMailsService
from ...util import TestSession 
from ...models import Email, Folder, Filter
import json

class TestGetMailsService(GetMailsService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def get_mails(self, folder_id: str, query: str, max_results: int, page_number: int) -> list[Email]:
        with open('EmailService\\services\\test_service\\test_service_mock_data.json', 'r') as f:
            data = json.load(f)
        email_data = data.get('emails', [])
        emails = [Email(**email) for email in email_data]
        return emails
    
    def search(self, query: str, max_results: int = 10) -> list[Email]:
        pass

    def filter(self, filter: Filter, max_results: int = 10) -> list[Email]:
        pass

    def search_filter(self, search_query: str, filter_obj: Filter, max_results: int = 10) -> list[Email]:
        pass

