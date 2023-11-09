from ..service_interfaces import FolderService
from ...util import OutlookSession 
from email_util import Email, Folder
import requests
import json

class OutlookFolderService(FolderService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def get_folders(self) -> list[Folder]:
        def _get_email_folders(folder_id=None, parent=None):
            headers = {
                "Authorization": f"Bearer {self.result['access_token']}"
            }

            try:
                endpoint_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/childFolders" if folder_id else "https://graph.microsoft.com/v1.0/me/mailFolders"

                response = requests.get(endpoint_url, headers=headers, timeout=30)
                response.raise_for_status()

                folder_data = response.json()

                folders = [Folder(name=f['displayName'], id=f['id']) for f in folder_data['value']]
                
                if parent:
                    parent.children.extend(folders)

                for folder in folders:
                    _get_email_folders(folder.id, folder)

                return folders if parent is None else parent.children
            except requests.RequestException as e:
                raise Exception(f"Request failed: {e}")
        return _get_email_folders()


    def create_folder(self, folder: Folder, parent_folder: Folder = None) -> Folder:
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}",
            "Content-Type": "application/json"
        }

        endpoint_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
        if parent_folder.id:
            endpoint_url = f"{endpoint_url}/{parent_folder.id}/childFolders"

        payload = {"displayName": folder.name}

        try:
            response = requests.post(endpoint_url, headers=headers, json=payload)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def move_email_to_folder(self, from_folder: Folder = None, to_folder: Folder = None, email: Email = None):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}",
            "Content-Type": "application/json"
        }

        endpoint_url = f"https://graph.microsoft.com/v1.0/me/messages/{email.id}/move"
        payload = {"destinationId": to_folder.id}

        try:
            response = requests.post(endpoint_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def delete_folder(self, folder: Folder):
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}",
        }

        endpoint_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder.id}"

        try:
            response = requests.delete(endpoint_url, headers=headers)
            response.raise_for_status()
            print(f"Folder with ID {folder.id} deleted successfully.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}",
            "Content-Type": "application/json"
        }

        endpoint_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder.id}"
        payload = {"displayName": new_folder_name}

        try:
            response = requests.patch(endpoint_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None



    
