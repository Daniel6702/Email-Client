from PyQt5.QtWidgets import QMessageBox,QStackedWidget,QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from email_util import Email

class EmailView(QVBoxLayout):
    def __init__(self, open_attachment_window: pyqtSignal(dict)):
        super().__init__()
        self.open_attachment_window = open_attachment_window
        self.current_email = None
        self.setupUIComponents()

    def setupUIComponents(self):
        # Initialize UI components
        self.from_user = QLineEdit()
        self.to_user = QLineEdit()
        self.subject = QLineEdit()
        self.browser = QWebEngineView()
        self.from_user.setText("From: ")
        self.to_user.setText("To: ")
        self.subject.setText("Subject: ")
        self.browser.setHtml("<html><body><p>No email content to display. Select an email</p></body></html>")
        self.label = QLabel("attachments:")
        self.label.setVisible(False)
        self.label.setAlignment(Qt.AlignBottom)
        self.attachments_list = QListWidget()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.attachments_list.itemClicked.connect(self.onAttachmentClicked)

        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.from_user, 0, 0)
        grid_layout.addWidget(self.to_user, 1, 0)
        grid_layout.addWidget(self.subject, 2, 0)
        grid_layout.addWidget(self.browser, 3, 0)
        grid_layout.addWidget(self.label, 4, 0)
        grid_layout.addWidget(self.attachments_list, 5, 0)
        self.addLayout(grid_layout)
      
    def updateEmailView(self, email: Email) -> None:
        self.current_email = email
        self.from_user.setText(f"From: {email.from_email}")
        self.to_user.setText(f"To: {email.to_email}")
        self.subject.setText(f"Subject: {email.subject}")
        self.browser.setHtml(email.body)
        self.attachments_list.clear()  # Clear existing items
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.label.setVisible(False)
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
        #QMessageBox.information(QWidget(), "Attachment", f"You clicked {attachment['file_name']}")