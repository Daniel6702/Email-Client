from abc import ABC, abstractmethod
from ..models import Email, Folder, User, Contact, Filter, Rule

###############################

class RulesService(ABC):
    @abstractmethod
    def get_rules(self) -> list[Rule]:
        pass

    @abstractmethod
    def add_rule(self, rule: Rule) -> Rule:
        pass

    @abstractmethod
    def remove_rule(self, rule: Rule):
        pass

###############################

class ContactsService(ABC):
    @abstractmethod
    def get_contacts(self) -> list[Contact]:
        pass

    @abstractmethod
    def add_contact(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def update_contact(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def delete_contact(self, contact: Contact):
        pass

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
    def get_mails(self, folder: Folder, query: str, max_results: int, page_number: int) -> list[Email]:
        pass

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> list[Email]:
        pass

    @abstractmethod
    def search_filter(self, query: str, filter: Filter, max_results: int = 10) -> list[Email]:
        pass

    @abstractmethod
    def filter(self, filter: Filter, max_results: int = 10) -> list[Email]:
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

    @abstractmethod
    def get_email_count_in_folder(self, folder: Folder) -> int:
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
