from ...models import Contact
from ..service_interfaces import ContactsService
from ...util import GmailSession 
import logging

class GmailContactsService(ContactsService):
    def __init__(self, session: GmailSession):
        self.service = session.people_service

    def get_contacts(self) -> list[Contact]:
        try:
            request = self.service.people().connections().list(
                resourceName='people/me',
                pageSize=1000,  
                personFields='names,emailAddresses,metadata'
            )
            response = request.execute()
            contacts = response.get('connections', [])
            contact_list = []

            for contact in contacts:
                if 'names' in contact and contact['names']:
                    name = contact['names'][0].get('displayName', 'No Name')
                else:
                    name = 'No Name'

                if 'emailAddresses' in contact and contact['emailAddresses']:
                    email = contact['emailAddresses'][0].get('value', 'No Email')
                else:
                    email = 'No Email'

                resource_name = contact.get('resourceName', '')
                contact_list.append(Contact(name=name, email=email, resource_name=resource_name))

            return contact_list
        except Exception as e:
            logging.error(f'An error occurred while getting contacts: {e}')
            return []
        
    def add_contact(self, contact: Contact) -> Contact:
        try:
            contact_body = {
                'names': [{'displayName': contact.name}],
                'emailAddresses': [{'value': contact.email}]
            }
            created_contact = self.service.people().createContact(body=contact_body).execute()
            contact.resource_name = created_contact.get('resourceName', '')
            return contact
        except Exception as e:
            logging.error(f'An error occurred while adding contact: {e}')
            return None
        
    def delete_contact(self, contact: Contact):
        try:
            self.service.people().deleteContact(resourceName=contact.resource_name).execute()
        except Exception as e:
            logging.error(f'An error occurred while deleting contact: {e}')
        
    def update_contact(self, contact: Contact) -> Contact:
        try:
            contact_body = {
                'names': [{'displayName': contact.name}],
                'emailAddresses': [{'value': contact.email}]
            }
            updated_contact = self.service.people().updateContact(
                resourceName=contact.resource_name,
                body=contact_body,
                updatePersonFields='names,emailAddresses'
            ).execute()
            contact.name = updated_contact.get('names', [])[0].get('displayName', 'No Name')
            contact.email = updated_contact.get('emailAddresses', [])[0].get('value', 'No Email')
            return contact
        except Exception as e:
            logging.error(f'An error occurred while updating contact: {e}')
            return None