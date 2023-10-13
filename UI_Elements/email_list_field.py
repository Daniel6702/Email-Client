from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from email_util import Email

class UiUtility:
    @staticmethod
    def update_email_html(browser, html_content):
        browser.setHtml(html_content)
        
class EmailList(QWidget):
    email_clicked = pyqtSignal(Email)
    def __init__(self,client,parent=None):
        super(EmailList, self).__init__(parent)
        self.client = client
        self.list_layout = QVBoxLayout()

    def on_email_clicked(self, mail):
        self.email_clicked.emit(mail)

    def setup_email_list(self, mails):
        label = QLabel("mails:")
        self.list_layout.addWidget(label)
        list = QListWidget()
        for mail in mails:
            email_item_text = f"Subject: {mail.subject}\nFrom: {mail.from_email}\nDate: {mail.datetime_info['date']} {mail.datetime_info['time'].split('.')[0]}"
            item = QListWidgetItem(email_item_text)
            list.addItem(item)

            # Use an additional default argument to capture the current value of mail by value
            item.setData(Qt.UserRole, mail)  # Storing the mail object as item data
        
        list.itemClicked.connect(self.handle_item_clicked)
        self.list_layout.addWidget(list)

    def handle_item_clicked(self, item):
        mail = item.data(Qt.UserRole)  # Retrieving the mail object from item data
        self.on_email_clicked(mail)

        


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