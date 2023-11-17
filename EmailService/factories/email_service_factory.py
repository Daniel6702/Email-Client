from abc import ABC, abstractmethod
from ..services.user_manager.user_manager_service import UserDataManager

class EmailServiceFactory(ABC):
    def create_user_manager(self):
        return UserDataManager()

    @abstractmethod
    def create_login_service(self):
        pass

    @abstractmethod
    def create_get_user_service(self):
        pass

    @abstractmethod
    def create_send_mail_service(self):
        pass

    @abstractmethod
    def create_get_mails_service(self):
        pass

    @abstractmethod
    def create_draft_service(self):
        pass

    @abstractmethod
    def create_folder_service(self):
        pass

    @abstractmethod
    def create_mail_management_service(self):
        pass