from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from email_util import Email

class EmailListArea(QVBoxLayout):
    email_clicked = pyqtSignal(Email)
    def __init__(self):
        super().__init__()
        self.setup_email_list()

    def setup_email_list(self):
        label = QLabel("mails:")
        self.addWidget(label)
        self.list_widget = QListWidget()
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def add_emails_to_list(self, mails):
        self.list_widget.clear()
        for mail in mails:
            email_item_text = f"Subject: {mail.subject}\nFrom: {mail.from_email}\nDate: {mail.datetime_info['date']} {mail.datetime_info['time'].split('.')[0]}"
            item = QListWidgetItem(email_item_text)
            self.list_widget.addItem(item)
            item.setData(Qt.UserRole, mail)

    def handle_item_clicked(self, item):
        mail = item.data(Qt.UserRole)
        self.email_clicked.emit(mail)

        


'''
# Get the index of the selected item
index = self.list.row(item)
# Fetch the corresponding email from your Outlook or Google service
selected_email = self.client.get_emails(number_of_mails=15)[index]
# Update the QLineEdit widgets with information from the selected email
self.from_user.setText(f"From: {selected_email.from_email}")
self.too_user.setText(f"To: {selected_email.to_email}")
self.subject.setText(f"Subject: {selected_email.subject}")
# Update the displayed HTML content using the utility class
UiUtility.update_email_html(self.browser, selected_email)
        # Emit the signal with the selected email
self.email_clicked.emit(selected_email)
        '''