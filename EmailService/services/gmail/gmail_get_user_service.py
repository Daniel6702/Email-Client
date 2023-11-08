from email_util import User
from googleapiclient.errors import HttpError
from ...util import GmailSession
from ..service_interfaces import GetUserService

class GmailGetUserService(GetUserService):
    def __init__(self, session: GmailSession):
        self.people_service = session.people_service
        self.service = session.gmail_service
        self.credentials = session.credentials

    def get_user(self):
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            email = profile.get("emailAddress", None)
            people_service = self.people_service
            person = people_service.people().get(resourceName='people/me', 
                                                 personFields='names,emailAddresses').execute()
            name_data = person.get("names", [])[0]
            name = name_data.get("displayName", None)
            user = User(name = name, email = email, client_type="google", credentials=self.credentials.to_json())
            return user

        except HttpError as e:
            raise Exception(f"Request failed: {e}")