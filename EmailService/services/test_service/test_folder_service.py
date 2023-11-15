from EmailService.models import Email
from ..service_interfaces import FolderService
from ...util import TestSession 
from ...models import Email, Folder
import json

class TestFolderService(FolderService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def get_folders(self) -> list[Folder]:
        with open('EmailService\\services\\test_service\\test_service_mock_data.json', 'r') as f:
            data = json.load(f)
        folders = [Folder.from_dict(folder_data) for folder_data in data.get('folders', [])]
        return folders    

    def create_folder(self, folder: Folder, parent_folder: Folder) -> Folder:
        return super().create_folder(folder, parent_folder)

    def move_email_to_folder(self, from_folder: Folder, to_folder: Folder, email: Email):
        return super().move_email_to_folder(from_folder, to_folder, email)

    def delete_folder(self, folder: Folder):
        return super().delete_folder(folder)

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        return super().update_folder(folder, new_folder_name)
