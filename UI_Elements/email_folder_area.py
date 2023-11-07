from PyQt5.QtWidgets import QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from dataclasses import dataclass

@dataclass
class FolderSignal:
    emails: list
    folder_id: str
    folder_name: str

class FolderArea(QVBoxLayout):
    email_signal = pyqtSignal(object)

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.folders = self.client.get_email_folders()
        self.setup_folder_field_layout()

    def setup_folder_field_layout(self):
        label = QLabel("Folders:")
        self.addWidget(label)
        self.list_widget = QListWidget()
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)
        
        for folder in self.folders:
            item = QListWidgetItem(folder.name)
            item.setData(Qt.UserRole, folder.id)
            self.list_widget.addItem(item)

    def handle_item_clicked(self, item):
        folder_id = item.data(Qt.UserRole)
        print("Getting emails from folder:", folder_id)
        emails = self.client.get_emails(folder_id, query="", number_of_mails=10)
        signal = FolderSignal(emails, folder_id, item.text())
        self.email_signal.emit(signal)
        