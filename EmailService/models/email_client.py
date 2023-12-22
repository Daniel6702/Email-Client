from ..factories.email_service_factory import EmailServiceFactory
from ..models.email import Email
from ..models.folder import Folder
from ..models.user import User
from ..models.contact import Contact
from ..models.filter import Filter
from ..models.rule import Rule
import threading
from queue import Queue
import math
import time

PAGE_SIZE = 10

class EmailClient():
    def __init__(self, service_factory: EmailServiceFactory):
        self.service_factory = service_factory
        self.login_service = service_factory.create_login_service()
        self.get_mails_lock = threading.Lock()
 
    def initialize_services(self, session):
        self.send_mail_service = self.service_factory.create_send_mail_service(session)
        self.get_user_service = self.service_factory.create_get_user_service(session)
        self.get_mails_service = self.service_factory.create_get_mails_service(session)
        self.draft_service = self.service_factory.create_draft_service(session)
        self.folder_service = self.service_factory.create_folder_service(session)
        self.mail_management_service = self.service_factory.create_mail_management_service(session)
        self.user_manager = self.service_factory.create_user_manager()
        self.spam_filter = self.service_factory.create_spam_filter()
        self.cache_manager = self.service_factory.create_cache_service()
        self.contacts_service = self.service_factory.create_contacts_service(session)
        self.rules_service = self.service_factory.create_rules_service(session)
   
    def login(self, user: User, save_user: bool):
        self.login_service.login(user)
        self.login_service.login_event.wait()
        session = self.login_service.get_session()
        self.initialize_services(session)
        threading.Thread(target=self.update_cache_background, daemon=True).start()

        self.user = self.get_user()
        if save_user and user is None:
            self.add_user(self.user)
        else:
            self.update_user(self.user)
    
    ########################################################################################################################## Cache functions
            
    def update_cache_background(self):
        while True:
            folder, query, max_results, page_number = self.cache_manager.get_next_cache_update_task()
            with self.get_mails_lock:
                try:
                    emails = self.get_mails_service.get_mails(folder, query, max_results, page_number)
                except:
                    continue
            self.cache_manager.set_cached_emails(folder.name, page_number, emails)

    def get_mails(self, folder: Folder, query: str, max_results: int, page_number: int = 1) -> list[Email]:
        with self.get_mails_lock:
            cached_emails = self.cache_manager.get_cached_emails(folder.name, page_number)
            if cached_emails is not None:
                [email.__setattr__('to_email', self.user.email) for email in cached_emails if email.to_email is None]
                return cached_emails
            emails = self.get_mails_service.get_mails(folder, query, max_results, page_number)
            self.cache_manager.set_cached_emails(folder.name, page_number, emails)
            self.cache_manager.enqueue_for_cache_update(folder, query, max_results, page_number + 1)
            [email.__setattr__('to_email', self.user.email) for email in emails if email.to_email is None]
            return emails

    def delete_mail(self, email: Email):
        self.mail_management_service.delete_email(email)
        self.cache_manager.delete_cache_for_folder(email.folder.name)
        self.cache_manager.enqueue_for_cache_update(email.folder, "", PAGE_SIZE, 1)

    def move_email_to_folder(self, from_folder: Folder, to_folder: Folder, email: Email):
        self.folder_service.move_email_to_folder(from_folder, to_folder, email)
        self.cache_manager.update_cache_for_folder_move(from_folder.name, to_folder.name, email.id)
        self.cache_manager.enqueue_for_cache_update(from_folder, "", PAGE_SIZE, 1)
        self.cache_manager.enqueue_for_cache_update(to_folder, "", PAGE_SIZE, 1)

    def delete_folder(self, folder: Folder):
        self.folder_service.delete_folder(folder)
        self.cache_manager.delete_cache_for_folder(folder.name)

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        updated_folder = self.folder_service.update_folder(folder, new_folder_name)
        self.cache_manager.delete_cache_for_folder(folder.name)
        self.cache_manager.enqueue_for_cache_update(updated_folder, "", PAGE_SIZE, 1)
        return updated_folder

    def refresh_cache(self): 
        self.cache_manager.clear_cache()
        #for folder in self.get_folders():
        #    self.cache_manager.enqueue_for_cache_update(folder, "", PAGE_SIZE, 1)

    ##########################################################################################################################

    def get_email_count_in_folder(self, folder: Folder) -> int:
        return self.folder_service.get_email_count_in_folder(folder)

    def get_folders(self) -> list[Folder]:
        return self.folder_service.get_folders()

    def add_user(self, user: User):
        self.user_manager.add_user(user)

    def update_user(self, user: User):
        self.user_manager.update_user(user)

    def get_users(self) -> list[User]:
        return self.user_manager.get_users()
    
    def delete_user(self, user: User):
        self.user_manager.delete_user(user)

    def filter_emails(self, emails: list[Email], trusted_senders: list[str], untrusted_senders: list[str]) -> (list[Email], list[Email]):
        return self.spam_filter.filter_emails(emails, trusted_senders, untrusted_senders)

    def get_user(self) -> User:
        if not hasattr(self, 'user'):
            self.user = self.get_user_service.get_user()
        return self.user

    def send_mail(self, email: Email) -> bool:
        return self.send_mail_service.send_mail(email)

    def search(self, query: str, max_results: int = PAGE_SIZE) -> list[Email]:
        return self.get_mails_service.search(query, max_results)
    
    def search_filter(self, query: str, filter: Filter, max_results: int = PAGE_SIZE) -> list[Email]:
        return self.get_mails_service.search_filter(query, filter, max_results)
    
    def filter(self, filter: Filter, max_results: int = PAGE_SIZE) -> list[Email]:
        return self.get_mails_service.filter(filter, max_results)
    
    def save_draft(self, email: Email):
        self.draft_service.save_draft(email)
    
    def update_draft(self, email: Email):
        self.draft_service.update_draft(email)

    def get_folders(self) -> list[Folder]:
        return self.folder_service.get_folders()
    
    def create_folder(self, folder: Folder, parrent_folder: Folder = None) -> Folder:
        return self.folder_service.create_folder(folder, parrent_folder)

    def mark_email_as_read(self, email: Email):
        self.mail_management_service.mark_email_as_read(email)

    def mark_email_as_unread(self, email: Email):
        self.mail_management_service.mark_email_as_unread(email)

    def mark_email_as(self, email: Email, is_read: bool):
        self.mail_management_service.mark_email_as(email, is_read)

    def logout(self):
        self.delete_user(self.get_user())

    def get_contacts(self) -> list[Contact]:
        return self.contacts_service.get_contacts()
    
    def add_contact(self, contact: Contact) -> Contact:
        return self.contacts_service.add_contact(contact)

    def update_contact(self, contact: Contact) -> Contact:
        return self.contacts_service.update_contact(contact)

    def delete_contact(self, contact: Contact):
        self.contacts_service.delete_contact(contact)

    def get_rules(self) -> list[Rule]:
        return self.rules_service.get_rules()
    
    def add_rule(self, rule: Rule) -> Rule:
        return self.rules_service.add_rule(rule)
    
    def remove_rule(self, rule: Rule):
        self.rules_service.remove_rule(rule)