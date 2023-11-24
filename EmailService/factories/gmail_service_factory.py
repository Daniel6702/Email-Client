from .email_service_factory import EmailServiceFactory
from ..services.gmail.gmail_login_service import GmailLoginService
from ..services.gmail.gmail_get_user_service import GmailGetUserService
from ..services.gmail.gmail_send_mail_service import GmailSendMailService
from ..services.gmail.gmail_get_mails_service import GmailGetMailsService
from ..services.gmail.gmail_draft_service import GmailDraftService
from ..services.gmail.gmail_folder_service import GmailFolderService
from ..services.gmail.gmail_mail_management_service import GmailMailManagementService
from ..services.gmail.gmail_contacts_service import GmailContactsService


class GmailServiceFactory(EmailServiceFactory):
    def create_login_service(self):
        return GmailLoginService()

    def create_get_user_service(self, session):
        return GmailGetUserService(session)

    def create_send_mail_service(self, session):
        return GmailSendMailService(session)
    
    def create_get_mails_service(self, session):
        return GmailGetMailsService(session)
    
    def create_draft_service(self, session):
        return GmailDraftService(session)
    
    def create_folder_service(self, session):
        return GmailFolderService(session)
    
    def create_mail_management_service(self, session):
        return GmailMailManagementService(session)
    
    def create_contacts_service(self, session):
        return GmailContactsService(session)