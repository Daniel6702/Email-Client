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
                print(resource_name)
                contact_list.append(Contact(name=name, email=email, resource_name=resource_name))

            return contact_list
        except Exception as e:
            logging.error(f'An error occurred while getting contacts: {e}')
            return []
        
    def add_contact(self, contact: Contact) -> Contact:
        try:
            name_parts = contact.name.split(maxsplit=1)
            given_name = name_parts[0]
            family_name = name_parts[1] if len(name_parts) > 1 else ''

            contact_body = {
                'names': [{'givenName': given_name, 'familyName': family_name}],
                'emailAddresses': [{'value': contact.email}]
            }

            created_contact = self.service.people().createContact(body=contact_body).execute()
            contact.resource_name = created_contact.get('resourceName', '')
            contact.name = created_contact.get('names', [])[0].get('displayName', 'No Name')
            contact.email = created_contact.get('emailAddresses', [])[0].get('value', 'No Email')
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
        if not contact.resource_name or not contact.resource_name.startswith('people/'):
            logging.error('Invalid resource name for contact update.')
            return None

        try:
            # Fetch the contact to get the latest etag
            fetch_response = self.service.people().get(
                resourceName=contact.resource_name,
                personFields='metadata'
            ).execute()
            etag = fetch_response.get('etag', '')

            if not etag:
                logging.error('Could not retrieve etag for contact update.')
                return None

            # Prepare the contact update body with the etag
            name_parts = contact.name.split(maxsplit=1)
            given_name = name_parts[0]
            family_name = name_parts[1] if len(name_parts) > 1 else ''

            contact_body = {
                'etag': etag,
                'names': [{'givenName': given_name, 'familyName': family_name}],
                'emailAddresses': [{'value': contact.email}]
            }

            updated_contact = self.service.people().updateContact(
                resourceName=contact.resource_name,
                body=contact_body,
                updatePersonFields='names,emailAddresses'
            ).execute()

            # Updating the Contact object based on the response
            contact.name = updated_contact.get('names', [])[0].get('displayName', 'No Name')
            contact.email = updated_contact.get('emailAddresses', [])[0].get('value', 'No Email')
            return contact

        except Exception as e:
            logging.error(f'An error occurred while updating contact: {e}')
            return None