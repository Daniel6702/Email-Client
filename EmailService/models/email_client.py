from ..factories.email_service_factory import EmailServiceFactory
from ..models.email import Email
from ..models.folder import Folder
from ..models.user import User
from ..models.contact import Contact
from ..models.filter import Filter

class EmailClient():
    def __init__(self, service_factory: EmailServiceFactory):
        self.service_factory = service_factory
        self.login_service = service_factory.create_login_service()

    def initialize_services(self, session):
        self.send_mail_service = self.service_factory.create_send_mail_service(session)
        self.get_user_service = self.service_factory.create_get_user_service(session)
        self.get_mails_service = self.service_factory.create_get_mails_service(session)
        self.draft_service = self.service_factory.create_draft_service(session)
        self.folder_service = self.service_factory.create_folder_service(session)
        self.mail_management_service = self.service_factory.create_mail_management_service(session)
        self.user_manager = self.service_factory.create_user_manager()
        self.spam_filter = self.service_factory.create_spam_filter()
        self.contacts_service = self.service_factory.create_contacts_service(session)
   
    def login(self, user: User, save_user: bool):
        self.login_service.login(user)
        self.login_service.login_event.wait()
        session = self.login_service.get_session()
        self.initialize_services(session)

        self.user = self.get_user()
        if save_user and user is None:
            self.add_user(self.user)
        else:
            self.update_user(self.user)

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

    def get_mails(self, folder: Folder, query: str, max_results: int, page_number: int = 1) -> list[Email]:
        emails = self.get_mails_service.get_mails(folder, query, max_results, page_number)
        [email.__setattr__('to_email', self.user.email) for email in emails if email.to_email is None]
        return emails
    
    def search(self, query: str, max_results: int = 10) -> list[Email]:
        return self.get_mails_service.search(query, max_results)
    
    def search_filter(self, query: str, filter: Filter, max_results: int = 10) -> list[Email]:
        return self.get_mails_service.search_filter(query, filter, max_results)
    
    def filter(self, filter: Filter, max_results: int = 10) -> list[Email]:
        return self.get_mails_service.filter(filter, max_results)
    
    def save_draft(self, email: Email):
        self.draft_service.save_draft(email)
    
    def update_draft(self, email: Email):
        self.draft_service.update_draft(email)

    def get_folders(self) -> list[Folder]:
        return self.folder_service.get_folders()
    
    def create_folder(self, folder: Folder, parrent_folder: Folder = None) -> Folder:
        return self.folder_service.create_folder(folder, parrent_folder)
    
    def move_email_to_folder(self, from_folder_id: str, to_folder_id: str, message_id: str):
        self.folder_service.move_email_to_folder(from_folder_id, to_folder_id, message_id)

    def delete_folder(self, folder_id: str):
        self.folder_service.delete_folder(folder_id)

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        return self.folder_service.update_folder(folder, new_folder_name)
    
    def delete_mail(self, email: Email):
        self.mail_management_service.delete_email(email)

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