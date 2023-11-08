from abc import ABC, abstractmethod

class EmailServiceFactory(ABC):
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