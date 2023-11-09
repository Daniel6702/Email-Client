from ..services.service_interfaces import EmailService
from ..factories.email_service_factory import EmailServiceFactory
from email_util import Email, User, Folder
from user_manager import UserDataManager

class EmailClient(EmailService):
    def __init__(self, service_factory: EmailServiceFactory, user_manager: UserDataManager):
        self.service_factory = service_factory
        self.user_manager = user_manager
        self.login_service = service_factory.create_login_service()

    def initialize_services(self, session):
        self.send_mail_service = self.service_factory.create_send_mail_service(session)
        self.get_user_service = self.service_factory.create_get_user_service(session)
        self.get_mails_service = self.service_factory.create_get_mails_service(session)
        self.draft_service = self.service_factory.create_draft_service(session)
        self.folder_service = self.service_factory.create_folder_service(session)
   
    def login(self, user: User, save_user: bool):
        self.login_service.login(user)
        self.login_service.login_event.wait()
        session = self.login_service.get_session()
        self.initialize_services(session)
        self.user = self.get_user()
        
        if save_user and user is None:
            self.user_manager.add_user(self.user)
        else:
            self.user_manager.update_user(self.user)

    def get_user(self) -> User:
        if not hasattr(self, 'user'):
            self.user = self.get_user_service.get_user()
        return self.user

    def send_mail(self, email: Email):
        self.send_mail_service.send_mail(email)

    def get_mails(self, folder_id: str, query: str, max_results: int) -> list[Email]:
        return self.get_mails_service.get_mails(folder_id, query, max_results)
    
    def save_mail(self, email: Email):
        self.draft_service.save_mail(email)

    def get_folders(self) -> list[Folder]:
        return self.folder_service.get_folders()
    
    def create_folder(self, folder: Folder) -> Folder:
        return self.folder_service.create_folder(folder)
    
    def move_email_to_folder(self, from_folder_id: str, to_folder_id: str, message_id: str):
        self.folder_service.move_email_to_folder(from_folder_id, to_folder_id, message_id)

    def delete_folder(self, folder_id: str):
        self.folder_service.delete_folder(folder_id)

    def update_folder(self, folder: Folder, new_folder_name: str) -> Folder:
        return self.folder_service.update_folder(folder, new_folder_name)
    
    def delete_mail(self, email: Email):
        self.folder_service.delete_email(email)