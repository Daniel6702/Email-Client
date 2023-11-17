from abc import ABC, abstractmethod
from ..models import Email, Folder, User

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

    @abstractmethod
    def get_session(self):
        pass

###############################

class SendMailService(ABC):
    @abstractmethod
    def send_mail(self, email: Email) -> bool:
        pass

###############################

class GetMailsService(ABC):
    @abstractmethod
    def get_mails(self, folder: Folder, query: str, max_results: int) -> list[Email]:
        pass

###############################

class DraftService(ABC):
    @abstractmethod
    def save_draft(self, email: Email):
        pass

    @abstractmethod
    def update_draft(self, email: Email):
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

###############################

class MailManagementService(ABC):
    @abstractmethod
    def delete_email(self, email: Email):
        pass
    
    @abstractmethod
    def mark_email_as_read(self, email: Email):
        pass

    @abstractmethod
    def mark_email_as_unread(self, email: Email):
        pass

    @abstractmethod
    def mark_email_as(self, email: Email, is_read: bool):
        pass

###############################

class GetUserService(ABC):
    @abstractmethod
    def get_user(self) -> User:
        pass

###############################
