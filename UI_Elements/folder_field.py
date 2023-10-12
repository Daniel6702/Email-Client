from PyQt5.QtWidgets import QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal

class FolderField(QWidget):
    email_signal = pyqtSignal(list)
    def __init__(self,client,parent=None):
        super(FolderField, self).__init__(parent)
        self.client = client
        self.folders = self.client.get_email_folders()

    def folder_field_layout(self):
        layout = QVBoxLayout()
        label = QLabel("Folders:")
        grid = QGridLayout()
        for i, folder in enumerate(self.folders):
            button = QPushButton(folder.name)
            button.setObjectName('folder_button')
            button.clicked.connect(lambda checked, folder=folder: self.get_emails(folder.id))
            grid.addWidget(button, i, 0)
        layout.addWidget(label)
        layout.addLayout(grid)
        return layout
    
    def get_emails(self,folder_id):
        print("Getting emails from folder: ", folder_id)
        emails = self.client.get_emails(folder_id,query="", number_of_mails=10)
        self.email_signal.emit(emails)