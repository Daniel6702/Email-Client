from .email_service_factory import EmailServiceFactory
from ..services.outlook.outlook_draft_service import OutlookDraftService
from ..services.outlook.outlook_folder_service import OutlookFolderService
from ..services.outlook.outlook_get_mails_service import OutlookGetMailsService
from ..services.outlook.outlook_get_user_service import OutlookGetUserService
from ..services.outlook.outlook_login_service import OutlookLoginService
from ..services.outlook.outlook_send_mail_service import OutlookSendMailService
from ..services.outlook.outlook_mail_management_service import OutlookMailManagementService
from ..services.outlook.outlook_contacts_service import OutlookContactsService

class OutlookServiceFactory(EmailServiceFactory):
    def create_login_service(self):
        return OutlookLoginService()

    def create_get_user_service(self, session):
        return OutlookGetUserService(session)

    def create_send_mail_service(self, session):
        return OutlookSendMailService(session)
    
    def create_get_mails_service(self, session):
        return OutlookGetMailsService(session)
    
    def create_draft_service(self, session):
        return OutlookDraftService(session)
    
    def create_folder_service(self, session):
        return OutlookFolderService(session)
    
    def create_mail_management_service(self, session):
        return OutlookMailManagementService(session)
    
    def create_contacts_service(self, session):
        return OutlookContactsService(session)