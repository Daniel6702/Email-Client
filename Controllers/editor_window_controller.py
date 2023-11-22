from PyQt5.QtWidgets import QWidget
from Views.windows.editor_window import EditorWindow
from EmailService.models import Email

class EditorWindowController(QWidget):
    def __init__(self, email_client):
        super().__init__()
        self.editor_window = EditorWindow()
        self.email_client = email_client
        self.setup_connections()

    def setup_connections(self):
        self.editor_window.mail_signal_from_editor.connect(self.get_mail_from_editor)

    def get_mail_from_editor(self, email: Email, action: str):
        if action == "send":
            respone = self.email_client.send_mail(email)
        elif action == "save":
            self.email_client.save_draft(email)
        elif action == "update":
            self.email_client.update_draft(email)
        
    def show_editor(self):
        self.editor_window.show()