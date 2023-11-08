from abc import ABC, abstractmethod
from email_util import Email, User, Folder

###############################

class LoginService(ABC):
    def login(self, user: User = None):
        if user:
            self.login_user(user)
        else:
            self.new_login()

    @abstractmethod
    def new_login(self):
        pass

    @abstractmethod
    def login_user(self, user: User):
        pass

###############################

class SendMailService(ABC):
    @abstractmethod
    def send_mail(self, email: Email):
        pass

###############################

class GetMailsService(ABC):
    @abstractmethod
    def get_mails(self, folder_id: str, query: str, max_results: int) -> list[Email]:
        pass

###############################

class DraftService(ABC):
    @abstractmethod
    def save_mail(self, email: Email, folder_id: str):
        pass

###############################

class FolderService(ABC):
    @abstractmethod
    def get_folders(self) -> list[Folder]:
        pass

    @abstractmethod
    def create_folder(self, folder: Folder, parent_folder: Folder) -> Folder:
        pass

    @abstractmethod
    def move_email_to_folder(self, from_folder: Folder, to_folder: Folder, email: Email):
        pass

    @abstractmethod
    def delete_folder(self, folder: Folder):
        pass

    @abstractmethod
    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        pass

    @abstractmethod
    def delete_email(self, email: Email):
        pass

###############################

class GetUserService(ABC):
    @abstractmethod
    def get_user(self) -> User:
        pass

###############################

class EmailService(ABC):
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_user(self) -> User:
        pass

    @abstractmethod
    def get_mails(self, folder_id: str, query: str, max_results: int) -> list[Email]:
        pass

    @abstractmethod
    def send_mail(self, email: Email):
        pass

    @abstractmethod
    def save_mail(self, email: Email):
        pass

    @abstractmethod
    def get_folders(self) -> list[Folder]:
        pass

    @abstractmethod
    def delete_mail(self, email: Email):
        pass

    @abstractmethod
    def create_folder(self, folder: Folder, parent_folder: Folder) -> Folder:
        pass

    @abstractmethod
    def move_email_to_folder(self, from_folder: Folder, to_folder: Folder, email: Email):
        pass

    @abstractmethod
    def delete_folder(self, folder: Folder):
        pass

    @abstractmethod
    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        pass    