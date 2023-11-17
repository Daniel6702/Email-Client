from PyQt5.QtWidgets import QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from datetime import datetime
import os
from EmailService.models import Folder
from Views.components.email_folder_layout import FolderArea

class FolderWindow(QWidget):
    on_folder_selected = pyqtSignal(Folder)
    def __init__(self, folders: list[Folder]):
        super().__init__()
        self.initial_layout()
        self.folder_area = FolderArea()
        self.folder_area.add_folders(folders)
        self.folder_area.folder_selected.connect(self.folder_selected)
        self.setLayout(self.folder_area)

    def folder_selected(self, folder: Folder):
        self.on_folder_selected.emit(folder)
        self.close()

    def initial_layout(self):
        self.setWindowTitle("Select a Folder")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 300
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)