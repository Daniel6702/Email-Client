from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from Views.windows.login_window import LoginWindow
from EmailService.models.email_client import EmailClient
from EmailService.models import User
from EmailService.factories import GmailServiceFactory, OutlookServiceFactory, TestServiceFactory
import threading

class LoginWindowController(QWidget):
    on_login_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.setup_connections()

    def setup_connections(self):
        self.login_window.login_signal.connect(self.on_login)

    def on_login(self, client_type: str, user: User, save_user: bool):
        def login_thread(client_type, user):
            if client_type == "google":
                factory = GmailServiceFactory()
            elif client_type == "outlook":
                factory = OutlookServiceFactory()
            elif client_type == "test":
                factory = TestServiceFactory() 
            client = EmailClient(factory)
            client.login(user=user, save_user=save_user)
            self.on_login_signal.emit(client)

        login_process_thread = threading.Thread(target=login_thread, args=(client_type, user))
        login_process_thread.start()

    def show_login(self):
        self.login_window.show()