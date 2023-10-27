from PyQt5.QtWidgets import QStackedWidget,QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *

class EmailView(QVBoxLayout):
    def __init__(self):
        super().__init__()
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
        self.browser.setHtml("<html><body><p>No email content to display</p></body></html>")

        # Add the components to the layout
        self.addWidget(self.from_user)
        self.addWidget(self.to_user)
        self.addWidget(self.subject)
        self.addWidget(self.browser)        

    def updateEmailView(self, email):
        self.from_user.setText(f"From: {email.from_email}")
        self.to_user.setText(f"To: {email.to_email}")
        self.subject.setText(f"Subject: {email.subject}")
        self.browser.setHtml(email.body)
        
            
