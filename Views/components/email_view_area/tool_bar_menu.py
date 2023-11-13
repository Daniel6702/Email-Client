from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import pyqtSignal
from EmailService.models import Email
from datetime import datetime
import copy

class ToolBarMenu(QToolBar):
    open_email_editor_window = pyqtSignal(Email)
    delete_email_signal = pyqtSignal(Email)
    mark_email_as = pyqtSignal(Email, bool)
    def __init__(self, email: Email, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QToolBar {spacing: 10px;}")
        self.current_email = email
        
        # Forward Action  (Opens editor window with the current email as a template)
        self.forward_action = QAction("Forward", self)
        self.forward_action.setStatusTip("Go Forward")
        self.forward_action.triggered.connect(self.forward)
        self.addAction(self.forward_action)
        self.forward_button = self.widgetForAction(self.forward_action)
        self.forward_button.setObjectName("toolbar_button")

        # Answer Action   (Opens editor window with the current email as a template)
        self.answer_action = QAction("Answer", self)
        self.answer_action.setStatusTip("Answer")
        self.answer_action.triggered.connect(self.answer)
        self.addAction(self.answer_action)
        self.answer_button = self.widgetForAction(self.answer_action)
        self.answer_button.setObjectName("toolbar_button")

        # Delete Action   
        self.delete_action = QAction("Delete", self)
        self.delete_action.setStatusTip("Delete")
        self.delete_action.triggered.connect(self.delete)
        self.addAction(self.delete_action)
        self.delete_button = self.widgetForAction(self.delete_action)
        self.delete_button.setObjectName("toolbar_button")

        # Mark as Read Action
        self.mark_as_read_action = QAction("Mark as read", self)
        self.mark_as_read_action.setStatusTip("Mark as read")
        self.mark_as_read_action.triggered.connect(self.mark_as_read)
        self.addAction(self.mark_as_read_action)
        self.mark_as_read_button = self.widgetForAction(self.mark_as_read_action)
        self.mark_as_read_button.setObjectName("toolbar_button")

        # Mark as Unread Action
        self.mark_as_unread_action = QAction("Mark as unread", self)
        self.mark_as_unread_action.setStatusTip("Mark as unread")
        self.mark_as_unread_action.triggered.connect(self.mark_as_unread)
        self.addAction(self.mark_as_unread_action)
        self.mark_as_unread_button = self.widgetForAction(self.mark_as_unread_action)
        self.mark_as_unread_button.setObjectName("toolbar_button")

    # Define the functions that will be called when the toolbar buttons are clicked
    def forward(self):
        mail = copy.copy(self.current_email)
        mail.from_email = 'me'
        mail.to_email = ''
        self.open_email_editor_window.emit(mail)

    def answer(self):
        mail = Email(from_email=self.current_email.to_email,
                     to_email=self.current_email.from_email,
                     subject=f"Re: {self.current_email.subject}",
                     body=None,
                     datetime_info = {'date': str(datetime.now().date()),
                                      'time': str(datetime.now().time())},
                     attachments=[],
                     id=None)
        self.open_email_editor_window.emit(mail)

    def delete(self):
        self.delete_email_signal.emit(self.current_email)

    def mark_as_read(self):
        self.mark_email_as.emit(self.current_email, True)

    def mark_as_unread(self):
        self.mark_email_as.emit(self.current_email, False)