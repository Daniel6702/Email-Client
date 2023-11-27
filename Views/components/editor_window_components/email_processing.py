from PyQt5.QtWidgets import QListWidget, QLineEdit, QTextEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from EmailService.models import Email
from Views.components.editor_window_components.recipient_line import RecipientLine
import os
from datetime import datetime

class EditorEmailProcessing(QWidget):
    mail_signal_from_editor = pyqtSignal(Email, str)
    def __init__(self, draft: Email = None, recipient_line: RecipientLine = None, subject_line_edit: QLineEdit = None, mail_body: QTextEdit = None, attachments_list: QListWidget = None):
        super().__init__()
        self.draft = draft
        self.recipient_line = recipient_line
        self.subject_line_edit = subject_line_edit
        self.mail_body = mail_body
        self.attachments_list = attachments_list

    def update(self, draft: Email = None, recipient_line: RecipientLine = None, subject_line_edit: QLineEdit = None, mail_body: QTextEdit = None, attachments_list: QListWidget = None):
        self.draft = draft
        self.recipient_line = recipient_line
        self.subject_line_edit = subject_line_edit
        self.mail_body = mail_body
        self.attachments_list = attachments_list

    def get_attachment_paths(self) -> list[str]:
        paths = []
        for index in range(self.attachments_list.count()):
            item = self.attachments_list.item(index)
            if self.draft and item.text() in [attachment.get('file_name') for attachment in self.draft.attachments]:
                continue
            file_path = item.data(Qt.UserRole)
            paths.append(file_path)
        return paths
    
    def generate_attachment_dict(self, file_path: str) -> dict: 
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)

        attachment_dict = {
            'file_data': file_data,
            'file_name': file_name,
        }
        return attachment_dict
    
    def generate_email(self) -> Email:
        email_addresses = self.recipient_line.get_email_addresses()
        subject = self.subject_line_edit.text()
        body = self.mail_body.toHtml()
        attachments = []
        for file_path in self.get_attachment_paths():
            attachment_dict = self.generate_attachment_dict(file_path)
            attachments.append(attachment_dict)
        
        email = Email(from_email='me', to_email=email_addresses, subject=subject, body=body,datetime_info={'date': str(datetime.now().date()),'time': str(datetime.now().time())}, attachments=attachments)
        if self.draft:
            email.id = self.draft.id
            email.datetime_info = self.draft.datetime_info
        return email
    
    def save_email(self):
        email = self.generate_email()
        if self.draft:
            self.mail_signal_from_editor.emit(email, "update")
        else:
            self.mail_signal_from_editor.emit(email, "save")
        
    def send_email(self):
        email = self.generate_email()
        self.mail_signal_from_editor.emit(email, "send")