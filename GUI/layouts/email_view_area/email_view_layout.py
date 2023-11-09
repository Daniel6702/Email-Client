from PyQt5.QtWidgets import QListWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import *
from email_util import Email
from PyQt5.QtWebEngineWidgets import QWebEngineView
from GUI.layouts.email_view_area.tool_bar_menu import ToolBarMenu
from GUI.layouts.email_view_area.web_engine_page import WebEnginePage

class EmailView(QVBoxLayout):
    def __init__(self, open_attachment_window: pyqtSignal(dict), open_email_editor_window: pyqtSignal(Email), delete_email_signal: pyqtSignal(Email), mark_email_as: pyqtSignal(Email, bool), parent=None):
        super().__init__()
        self.delete_email_signal = delete_email_signal
        self.open_attachment_window = open_attachment_window
        self.open_email_editor_window = open_email_editor_window
        self.mark_email_as = mark_email_as
        self.current_email = None
        self.setupUIComponents()

    def setupUIComponents(self):
        #Email header
        self.from_user = QLineEdit()
        self.to_user = QLineEdit()
        self.subject = QLineEdit()
        self.from_user.setText("From: ")
        self.to_user.setText("To: ")
        self.subject.setText("Subject: ")

        #Toolbar
        self.toolbar = ToolBarMenu(self.current_email, self.open_email_editor_window, self.delete_email_signal, self.mark_email_as)
        self.toolbar.setVisible(False)

        #Email body
        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setHtml("<html><body><p>No email content to display. Select an email</p></body></html>")

        #Attachments list
        self.label = QLabel("attachments:")
        self.label.setVisible(False)
        self.label.setAlignment(Qt.AlignBottom)
        self.attachments_list = QListWidget()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.attachments_list.itemClicked.connect(self.onAttachmentClicked)

        #Layout
        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.from_user, 0, 0)
        grid_layout.addWidget(self.to_user, 1, 0)
        grid_layout.addWidget(self.subject, 2, 0)
        grid_layout.addWidget(self.toolbar, 3, 0)
        grid_layout.addWidget(self.browser, 4, 0)
        grid_layout.addWidget(self.label, 5, 0)
        grid_layout.addWidget(self.attachments_list, 6, 0)
        self.addLayout(grid_layout)

    def clearEmailView(self) -> None:
        self.from_user.setText("From: ")
        self.to_user.setText("To: ")
        self.subject.setText("Subject: ")
        self.browser.setHtml("<html><body><p>No email content to display. Select an email</p></body></html>")
        self.attachments_list.clear()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.label.setVisible(False)
        self.toolbar.setVisible(False)
      
    def updateEmailView(self, email: Email) -> None:
        self.clearEmailView()
        self.toolbar.setVisible(True)
        self.toolbar.current_email = email
        self.current_email = email
        self.from_user.setText(f"From: {email.from_email}")
        self.to_user.setText(f"To: {email.to_email}")
        self.subject.setText(f"Subject: {email.subject}")
        self.browser.setHtml(email.body)
        for attachment in email.attachments:
            self.label.setVisible(True)
            self.attachments_list.addItem(attachment['file_name'])
            self.attachments_list.setStyleSheet("QListWidget { border: 1px solid gray; }")
            item_height = 20
            total_height = item_height * self.attachments_list.count() + 4
            self.attachments_list.setFixedHeight(total_height)
            
    def onAttachmentClicked(self, item):
        for attachment in self.current_email.attachments:
            if attachment['file_name'] == item.text():
                self.previewAttachment(attachment)
                break
    
    def previewAttachment(self, attachment):
        self.open_attachment_window.emit(attachment)        