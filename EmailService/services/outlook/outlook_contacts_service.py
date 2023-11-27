from ...models import Contact
from ..service_interfaces import ContactsService
from ...util import OutlookSession 
import logging
import requests

class OutlookContactsService(ContactsService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def get_contacts(self) -> list[Contact]:
        headers = {
            'Authorization': f'Bearer {self.result["access_token"]}',
            'Content-Type': 'application/json'
        }
        url = 'https://graph.microsoft.com/v1.0/me/contacts'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()

            contact_list = []
            for item in data.get('value', []):
                contact_list.append(Contact(
                    name=item.get('displayName', 'No Name'),
                    email=item.get('emailAddresses', [{'address': 'No Email'}])[0]['address'],
                    resource_name=item.get('id', '')
                ))
            return contact_list
        except Exception as e:
            logging.error(f'An error occurred while getting contacts: {e}')
            return []
        
    def add_contact(self, contact: Contact) -> Contact:
        headers = {
            'Authorization': f'Bearer {self.result["access_token"]}',
            'Content-Type': 'application/json'
        }
        url = 'https://graph.microsoft.com/v1.0/me/contacts'
        contact_data = {
            'givenName': contact.name.split()[0] if contact.name else '',
            'surname': contact.name.split()[1] if len(contact.name.split()) > 1 else '',
            'emailAddresses': [{'address': contact.email, 'name': contact.name}]
        }

        try:
            response = requests.post(url, headers=headers, json=contact_data)
            response.raise_for_status()
            data = response.json()
            contact.resource_name = data.get('id', '')
            return contact
        except Exception as e:
            logging.error(f'An error occurred while adding contact: {e}')
            return None
        
    def delete_contact(self, contact: Contact):
        headers = {
            'Authorization': f'Bearer {self.result["access_token"]}',
            'Content-Type': 'application/json'
        }
        url = f'https://graph.microsoft.com/v1.0/me/contacts/{contact.resource_name}'

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            logging.error(f'An error occurred while deleting contact: {e}')
        
    def update_contact(self, contact: Contact) -> Contact:
        headers = {
            'Authorization': f'Bearer {self.result["access_token"]}',
            'Content-Type': 'application/json'
        }
        url = f'https://graph.microsoft.com/v1.0/me/contacts/{contact.resource_name}'
        update_data = {
            'givenName': contact.name.split()[0] if contact.name else '',
            'surname': contact.name.split()[1] if len(contact.name.split()) > 1 else '',
            'emailAddresses': [{'address': contact.email, 'name': contact.name}]
        }

        try:
            response = requests.patch(url, headers=headers, json=update_data)
            response.raise_for_status()
            return contact
        except Exception as e:
            logging.error(f'An error occurred while updating contact: {e}')
            return None