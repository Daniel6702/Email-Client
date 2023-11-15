from EmailService.models import Email
from ..service_interfaces import DraftService
from ...util import TestSession 
from ...models import Email

class TestDraftService(DraftService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def save_draft(self, email: Email):
        return super().save_draft(email)
    
    def update_draft(self, email: Email):
        return super().update_draft(email)