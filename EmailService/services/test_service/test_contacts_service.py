from ...models import Contact
from ..service_interfaces import ContactsService
from ...util import TestSession 
from EmailService.models.contact import generate_random_contact

class TestContactsService(ContactsService):
    def __init__(self, session: TestSession):
        pass

    def get_contacts(self) -> list[Contact]:
        [generate_random_contact() for _ in range(10)]
        
    def add_contact(self, contact: Contact) -> Contact:
        return generate_random_contact()    

    def delete_contact(self, contact: Contact):
        pass
        
    def update_contact(self, contact: Contact) -> Contact:
        return generate_random_contact()