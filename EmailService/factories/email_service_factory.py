from abc import ABC, abstractmethod
from ..services.common.user_manager_service import UserDataManager
from ..services.common.spamfilter_service import SpamFilter
from ..services.common.cache_service import EmailCacheManager

class EmailServiceFactory(ABC):
    def create_user_manager(self):
        return UserDataManager()
    
    def create_spam_filter(self):
        return SpamFilter()
    
    def create_cache_service(self):
        return EmailCacheManager()

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

    @abstractmethod
    def create_contacts_service(self):
        pass

    @abstractmethod
    def create_rules_service(self):
        pass