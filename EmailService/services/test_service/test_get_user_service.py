from EmailService.models import User
from ..service_interfaces import GetUserService
from ...util import TestSession 
from ...models import User
import requests
import logging
import json

class TestGetUserService(GetUserService):
    def __init__(self, session: TestSession):
        self.result = session.credentials

    def get_user(self) -> User:
        with open('EmailService\\services\\test_service\\test_service_mock_data.json', 'r') as f:
            data = json.load(f)
        user_data = data.get('user', [])
        user = User(**user_data)
        return user
