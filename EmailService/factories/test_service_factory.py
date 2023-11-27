from .email_service_factory import EmailServiceFactory
from ..services.test_service.test_draft_service import TestDraftService
from ..services.test_service.test_folder_service import TestFolderService
from ..services.test_service.test_get_mails_service import TestGetMailsService
from ..services.test_service.test_get_user_service import TestGetUserService
from ..services.test_service.test_login_service import TestLoginService
from ..services.test_service.test_mail_management_service import TestMailManagementService
from ..services.test_service.test_send_mail_service import TestSendMailService
from ..services.test_service.test_contacts_service import TestContactsService

class TestServiceFactory(EmailServiceFactory):
    def create_login_service(self):
        return TestLoginService()
    
    def create_get_user_service(self, session):
        return TestGetUserService(session)
    
    def create_send_mail_service(self, session):
        return TestSendMailService(session)
    
    def create_get_mails_service(self, session):
        return TestGetMailsService(session)
    
    def create_draft_service(self, session):
        return TestDraftService(session)
    
    def create_folder_service(self, session):
        return TestFolderService(session)
    
    def create_mail_management_service(self, session):
        return TestMailManagementService(session)
    
    def create_contacts_service(self, session):
        return TestContactsService(session)