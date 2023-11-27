from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from Views.windows.editor_window import EditorWindow
from EmailService.models import Email
from EmailService.models.email_client import EmailClient
import threading

class EditorWindowController(QWidget):
    open_attachment_signal = pyqtSignal(dict)
    def __init__(self, email_client: EmailClient):
        super().__init__()
        self.editor_window = EditorWindow()
        self.email_client = email_client
        self.setup_connections()

    def setup_connections(self):
        self.editor_window.mail_signal_from_editor.connect(self.on_signal_from_editor)
        self.editor_window.open_attachment_signal.connect(self.open_attachment_signal.emit)

    def on_signal_from_editor(self, email: Email, action: str):
        thread = threading.Thread(target=self.handle_action, args=(email, action))
        thread.start()

    def handle_action(self, email: Email, action: str):
        if action == "send":
            self.email_client.send_mail(email)
        elif action == "save":
            self.email_client.save_draft(email)
        elif action == "update":
            self.email_client.update_draft(email)
        self.editor_window.close()

    def show_editor(self, email: Email = None):
        contacts = self.email_client.get_contacts()
        self.editor_window.update_window(email, contacts)
        self.editor_window.show()