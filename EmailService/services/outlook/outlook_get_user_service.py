from ..service_interfaces import GetUserService
from ...util import OutlookSession 
from ...models import User
import requests
import logging

from dataclasses import asdict
import json

class OutlookGetUserService(GetUserService):
    def __init__(self, session: OutlookSession):
        self.result = session.result

    def get_user(self) -> User:
        headers = {
            "Authorization": f"Bearer {self.result['access_token']}"
        }

        try:
            response = requests.get("https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail,userPrincipalName", headers=headers, timeout=30)
            response.raise_for_status()
            user_data = response.json()
            email = user_data.get("mail", user_data.get("userPrincipalName", None))
            name = user_data.get("displayName", None)
            credentials = {'credentials': self.result.get('refresh_token')}
            user = User(name = name, email = email, client_type="outlook", credentials=credentials)
            logging.info(f"Successfully retrieved user data from Outlook")


            user_dict = asdict(user)
            with open("EmailService\\services\\test_service\\test_service_mock_data.json", "r") as f:
                existing_data = json.load(f)
            existing_data['user'] = user_dict
            with open("EmailService\\services\\test_service\\test_service_mock_data.json", "w") as f:
                json.dump(existing_data, f, indent=4)

            return user
        except requests.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"Request failed: {e}")