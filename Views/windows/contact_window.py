from PyQt5.QtWidgets import QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from datetime import datetime
import os

class ContactWindow(QWidget):
    contacts_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initial_layout()

    def initial_layout(self):
        self.setWindowTitle("Contacts")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

        # Main layout for the window
        main_layout = QGridLayout()

        left_layout = QHBoxLayout()
        # Add widgets for different settings options
        add_contact_button = QPushButton("Add Contact")
        add_contact_button.clicked.connect(self.show_contact_form)
        sorting_button = QPushButton("Sorting")
        sorting_button.clicked.connect(self.sorting_order)

        # Add buttons to the grid layout
        left_layout.addWidget(add_contact_button)
        left_layout.addWidget(sorting_button)
        # Set the left layout for buttons
        main_layout.addLayout(left_layout, 0, 0)

        left_layout = QVBoxLayout()
        self.contacts_list = QListWidget()
        left_layout.addWidget(self.contacts_list)
        # Set the left layout for buttons
        main_layout.addLayout(left_layout, 1, 0)
        
        # Right layout for content
        right_layout = QVBoxLayout()
         # Placeholder labels for content
        self.content_label = QLabel("Select an option on the left to view content.")
        right_layout.addWidget(self.content_label)
        # Set the right layout for content in the main layout
        main_layout.addLayout(right_layout, 0, 1)
          # Set the stretch factor for the columns in the QGridLayout
        main_layout.setColumnStretch(0, 5)  # Left column
        main_layout.setColumnStretch(1, 5)  # Right column
    
        self.setLayout(main_layout)


    def show_contact_form(self):
        pass

    def sorting_order(self):
        pass