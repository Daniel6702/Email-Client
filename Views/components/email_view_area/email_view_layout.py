from PyQt5.QtWidgets import QListWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import *
from EmailService.models import Email
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Views.components.email_view_area.tool_bar_menu import ToolBarMenu
from Views.components.email_view_area.web_engine_page import WebEnginePage
from EmailService.models import Folder

class EmailView(QVBoxLayout):
    open_attachment_window = pyqtSignal(dict)
    open_email_editor_window = pyqtSignal(Email)
    delete_email_signal = pyqtSignal(Email)
    mark_email_as = pyqtSignal(Email, bool)
    open_folder_window = pyqtSignal()
    move_email_to_folder = pyqtSignal(Email, Folder)
    selected_folder = pyqtSignal(Folder)
    def __init__(self):
        super().__init__()
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
        self.toolbar = ToolBarMenu(self.current_email)
        self.toolbar.open_email_editor_window.connect(self.open_email_editor_window.emit)
        self.toolbar.delete_email_signal.connect(self.delete_email_signal.emit)
        self.toolbar.mark_email_as.connect(self.mark_email_as.emit)
        self.toolbar.move_email_to_folder.connect(self.move_email_to_folder.emit)
        self.toolbar.open_folder_window.connect(self.open_folder_window.emit)
        self.selected_folder.connect(self.toolbar.on_folder_selected)
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