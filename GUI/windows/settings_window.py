from PyQt5.QtWidgets import QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from datetime import datetime
import os

class SettingsWindow(QWidget):
    settings_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initial_layout()

        main_layout = QGridLayout()

        # Left layout for buttons
        buttons_layout = QVBoxLayout()

        # Add widgets for different settings options
        notification_button = QPushButton("Notification")
        display_button = QPushButton("Display")
        rules_button = QPushButton("Rules")
        blacklist_button = QPushButton("Blacklist")
        switch_account_button = QPushButton("Switch Account")
        logout_button = QPushButton("Log Out")

        # Connect buttons to functions
        notification_button.clicked.connect(self.notification_settings)
        display_button.clicked.connect(self.display_settings)
        rules_button.clicked.connect(self.rules_settings)
        blacklist_button.clicked.connect(self.blacklist_settings)
        switch_account_button.clicked.connect(self.switch_account_settings)
        logout_button.clicked.connect(self.logout_settings)

        # Add buttons to the left layout
        buttons_layout.addWidget(notification_button)
        buttons_layout.addWidget(display_button)
        buttons_layout.addWidget(rules_button)
        buttons_layout.addWidget(blacklist_button)
        buttons_layout.addWidget(switch_account_button)
        buttons_layout.addWidget(logout_button)

        # Set the left layout for buttons
        #Set the stretch factor for the left layout columns
        main_layout.addLayout(buttons_layout, 0, 0, 2, 1)  # row span for buttons_layout
        main_layout.setColumnStretch(1, 3)  # Make the left column take 1/4 of the window

        # Right layout for content
        content_layout = QVBoxLayout()

        # Right layout for content
        content_layout = QVBoxLayout()
        # Placeholder labels for content
        self.content_label = QLabel("Select an option on the left to view content.")

        # Add content labels to the right layout

        # Set the right layout for content
        main_layout.addLayout(content_layout, 0, 1)

        self.setLayout(main_layout)


    def initial_layout(self):
        self.setWindowTitle("Settings")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

    def notification_settings(self):
        # Implement the functionality for notification settings here
        print("Show Notification Settings")

    def display_settings(self):
        # Implement the functionality for display settings here
        print("Show Display Settings")

    def rules_settings(self):
        # Implement the functionality for rules settings here
        print("Show Rules Settings")

    def blacklist_settings(self):
        # Implement the functionality for blacklist settings here
        print("Show Blacklist Settings")

    def switch_account_settings(self):
        print("Show Switch Account Settings")

    def logout_settings(self):
        # Emit the settings_signal with the "logout" action
        self.settings_signal.emit("logout")
