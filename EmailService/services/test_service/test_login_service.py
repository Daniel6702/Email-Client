import threading
from ...util import TestSession
from ..service_interfaces import LoginService
from ...models import User

class TestLoginService(LoginService):
    session = TestSession(credentials=None)
    login_event = threading.Event()

    def new_login(self):
        self.test() 

    def login_user(self, user: User):
        self.test() 

    def test(self):
        self.login_event.set()

    def get_session(self):
        return self.session