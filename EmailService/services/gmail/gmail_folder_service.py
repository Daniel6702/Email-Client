from ...util import GmailSession 
from email_util import Folder, Email
from ..service_interfaces import FolderService

class GmailFolderService(FolderService):
    def __init__(self, session: GmailSession):
        self.service = session.gmail_service

    def get_folders(self) -> list[Folder]:
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        folders = []
        for label in labels:
            folders.append(Folder(name=label['name'], id=label['id']))
        
        return folders
    
    def create_folder(self, folder: Folder, parent_folder: Folder = None) -> Folder:
        new_label = {
            'name': folder.name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'color': {
                'textColor': '#000000',
                'backgroundColor': '#ffffff'
            }
        }
        try:
            label = self.service.users().labels().create(userId='me', body=new_label).execute()
            print('Label with id: %s created.' % label['id'])
            folder.id = label['id']
            return folder
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
        
    def move_email_to_folder(self, from_folder: Folder, to_folder: Folder, email: Email):
        try:
            body = {
                'addLabelIds': [to_folder.id],
                'removeLabelIds': [from_folder.id]
            }
            message = self.service.users().messages().modify(userId='me', id=email.id, body=body).execute()
            print(f'Message with id: {email.id} moved to label with id: {to_folder.id}')
            return message
        except Exception as error:
            print(f'An error occurred: {error}')
            return None

    def delete_folder(self, folder: Folder):
        try:
            self.service.users().labels().delete(userId='me', id=folder.id).execute()
            print(f'Label with id: {folder.id} deleted.')
        except Exception as error:
            print(f'An error occurred: {error}')

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        try:
            label = {'name': new_folder_name}
            updated_label = self.service.users().labels().update(userId='me', id=folder.id, body=label).execute()
            folder.name = updated_label['name']
            return folder
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
        
    def delete_email(self, email: Email):
        try:
            self.service.users().messages().delete(userId='me', id=email.id).execute()
            print(f'Email with id: {email.id} has been deleted.')
        except Exception as error:
            print(f'An error occurred: {error}')