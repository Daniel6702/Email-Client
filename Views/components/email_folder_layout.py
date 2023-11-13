from PyQt5.QtWidgets import QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from dataclasses import dataclass, field
from EmailService.models import Folder
from typing import List

class FolderArea(QVBoxLayout):
    folder_selected = pyqtSignal(Folder)

    def __init__(self):
        super().__init__()
        self.folders = []
        self.setup_folder_field_layout()

    def setup_folder_field_layout(self):
        label = QLabel("Folders:")
        self.addWidget(label)
        self.list_widget = QListWidget()
        self.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def add_folders(self, folders: List[Folder]):
        for folder in folders:
            self.add_folder(folder)

    def add_folder(self, folder: Folder):
        item = QListWidgetItem(folder.name)
        item.setData(Qt.UserRole, folder)
        self.list_widget.addItem(item)

    def remove_folder(self, folder: Folder):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.data(Qt.UserRole).id == folder.id:
                self.list_widget.takeItem(index)
                break

    def handle_item_clicked(self, item: QListWidgetItem):
        folder = item.data(Qt.UserRole)
        self.folder_selected.emit(folder) 

    def clear_folders(self):
        self.list_widget.clear()

    def select_folder_by_id(self, folder_id: str):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.data(Qt.UserRole).id == folder_id:
                self.list_widget.setCurrentItem(item)
                break

    def refresh_folder_list(self):
        self.clear_folders()
        self.add_folders(self.folders)