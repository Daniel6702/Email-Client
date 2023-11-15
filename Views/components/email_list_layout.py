from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from EmailService.models import Email

'''
TODAY
improve folder list and email list
testing
'''

class EmailWidget(QWidget):
    mark_as_read = pyqtSignal(Email)
    delete_email = pyqtSignal(Email)

    def __init__(self, email: Email, parent=None):
        super().__init__(parent)
        self.email = email
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        # Email details layout
        from_label = QLabel(f"From: {self.email.from_email}")
        from_label.setObjectName("from_label")
        subject_label = QLabel(f"Subject: {self.email.subject}")
        subject_label.setObjectName("subject_label")
        date_label = QLabel(f"Date: {self.email.datetime_info['date']}")
        date_label.setObjectName("subject_label")
        date_label.setAlignment(Qt.AlignRight)
        body_label = QLabel(f"Body: {self.email.body[:50]}...")
        body_label.setObjectName("body_label")

        read_button = QPushButton("Mark as Read")
        read_button.setObjectName("list_button")
        read_button.clicked.connect(self.on_mark_as_read)
        read_button.setMaximumWidth(100)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("list_button")
        delete_button.clicked.connect(self.on_delete_email)
        delete_button.setMaximumWidth(100)

        top_row = QHBoxLayout()
        top_row.addWidget(from_label)
        top_row.addWidget(read_button)
        top_row.addWidget(delete_button)

        mid_row = QHBoxLayout()
        mid_row.addWidget(subject_label)
        mid_row.addWidget(date_label,0, Qt.AlignRight)

        layout.addLayout(top_row)
        layout.addLayout(mid_row)
        layout.addWidget(body_label)

        self.setLayout(layout)
    
    def on_mark_as_read(self):
        self.mark_as_read.emit(self.email)

    def on_delete_email(self):
        self.delete_email.emit(self.email)

class EmailListArea(QVBoxLayout):
    email_clicked = pyqtSignal(Email)
    email_marked_as_read = pyqtSignal(Email)
    email_deleted = pyqtSignal(Email)

    def __init__(self):
        super().__init__()
        self.setup_email_list()
        self.current_page = 0

    def setup_email_list(self):
        label = QLabel("Emails:")
        self.addWidget(label)
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("email_list")
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)
        self.next_page_button = QPushButton("Next Page")
        self.next_page_button.setMaximumWidth(120)
        self.next_page_button.clicked.connect(self.next_page)
        self.previous_page_button = QPushButton("Previous Page")
        self.previous_page_button.setMaximumWidth(120)
        self.previous_page_button.clicked.connect(self.previous_page)
        temp = QHBoxLayout()
        temp.addWidget(self.previous_page_button)
        temp.addWidget(self.next_page_button)
        self.addLayout(temp)

    def next_page(self):
        self.current_page += 1

    def previous_page(self):
        self.current_page -= 1

    def add_emails_to_list(self, mails: list[Email]):
        self.list_widget.clear()
        for mail in mails:
            email_widget = EmailWidget(mail)
            email_widget.setMaximumWidth(650)
            email_widget.mark_as_read.connect(self.mark_as_read)
            email_widget.delete_email.connect(self.delete_email)

            item = QListWidgetItem()
            item.setSizeHint(email_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, email_widget)

    def handle_item_clicked(self, item: QListWidgetItem):
        widget = self.list_widget.itemWidget(item)
        if hasattr(widget, 'email'):
            self.email_clicked.emit(widget.email)

    def mark_as_read(self, mail: Email):
        self.email_marked_as_read.emit(mail)

    def delete_email(self, mail: Email):
        self.email_deleted.emit(mail)
        self.remove_email_from_list(mail)

    def remove_email_from_list(self, mail: Email):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            email_widget = self.list_widget.itemWidget(item)
            if email_widget and email_widget.email == mail:
                self.list_widget.takeItem(index)
                break