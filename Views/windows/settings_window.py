from PyQt5.QtWidgets import QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from datetime import datetime
import os

class SettingsWindow(QWidget):
    style_signal = pyqtSignal(str)
    switch_account_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self, style_manager=None):
        super().__init__()
        self.style_manager = style_manager
        self.initial_layout()

        main_layout = QGridLayout()

        # Left layout for buttons
        buttons_layout = QVBoxLayout()

        display_button = QPushButton("Display")
        rules_button = QPushButton("Rules")
        blacklist_button = QPushButton("Blacklist")
        switch_account_button = QPushButton("Switch Account")
        logout_button = QPushButton("Log Out")

  
        display_button.clicked.connect(self.display_settings)
        rules_button.clicked.connect(self.rules_settings)
        blacklist_button.clicked.connect(self.blacklist_settings)
        switch_account_button.clicked.connect(self.switch_account_settings)
        logout_button.clicked.connect(self.logout_settings)

        
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
        self.content_layout = QVBoxLayout()
        # Placeholder labels for content
        self.content_label = QLabel("Select an option on the left to view content.")

        # Add content labels to the right layout

        # Set the right layout for content
        main_layout.addLayout(self.content_layout, 0, 1)

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


    def display_settings(self):
    # Clear the existing content layout
        self.clear_content_layout()

        # Create a new widget for display settings
        display_widget = QWidget()

        # Layout for display settings
        display_layout = QVBoxLayout()

        # Add buttons for different display options
        button1 = QPushButton("Light mode")
        button2 = QPushButton("Dark mode")
        button3 = QPushButton("Barbiemode")

        # Connect buttons to functions if needed
        button1.clicked.connect(self.light_mode_option)
        button2.clicked.connect(self.dark_mode_option)
        button3.clicked.connect(self.barbie_mode_option)

        # Add buttons to the layout
        display_layout.addWidget(button1)
        display_layout.addWidget(button2)
        display_layout.addWidget(button3)

        # Set the layout for the display widget
        display_widget.setLayout(display_layout)

        # Add the display widget to the content layout
        self.content_layout.addWidget(display_widget)


    def rules_settings(self):
        # Implement the functionality for rules settings here
        # Emit the settings_signal with the "logout" action
        self.clear_content_layout()
        print("Show Rules Settings")

    def blacklist_settings(self):
        # Implement the functionality for blacklist settings here
        # Emit the settings_signal with the "logout" action
        self.clear_content_layout()
        print("Show Blacklist Settings")

    def switch_account_settings(self):
        # Emit the settings_signal with the "logout" action
        self.clear_content_layout()
        display_widget = QWidget()
        # Layout for display settings
        display_layout = QVBoxLayout()
        self.content_label = QLabel("Are you sure you want to switch account?")
        self.content_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.content_label)
        # Add buttons for different display options
        button1 = QPushButton("Switch account")
        button1.clicked.connect(self.switch_account)
        display_layout.addWidget(button1)
          # Set the layout for the display widget
        display_widget.setLayout(display_layout)
        # Add the display widget to the content layout
        self.content_layout.addWidget(display_widget)
        print("Show Switch Account Settings")

    def logout_settings(self):
        # Emit the settings_signal with the "logout" action
        self.clear_content_layout()
        # Create a new widget for display settings
        display_widget = QWidget()
        # Layout for display settings
        display_layout = QVBoxLayout()
        self.content_label = QLabel("Are you sure you want to logout?")
        

        self.content_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.content_label)
        # Add buttons for different display options
        button1 = QPushButton("Logout")
        button1.clicked.connect(self.logout)
        display_layout.addWidget(button1)
          # Set the layout for the display widget
        display_widget.setLayout(display_layout)
        # Add the display widget to the content layout
        self.content_layout.addWidget(display_widget)



    def light_mode_option(self):
         self.style_signal.emit('lightmode')
    def dark_mode_option(self):
        self.style_signal.emit('darkmode')
    def barbie_mode_option(self):
         self.style_signal.emit('barbiemode')
        

    def switch_account(self):
        self.switch_account_signal.emit()

    def logout(self):
        self.logout_signal.emit()


    def clear_content_layout(self):
        # Check if the content layout has any items
        if self.content_layout.count() > 0:
            # Create a list to store items for removal
            items_to_remove = []

            # Add items to the removal list
            for i in range(self.content_layout.count()):
                items_to_remove.append(self.content_layout.itemAt(i).widget())

            # Clear the layout
            for item in items_to_remove:
                item.setParent(None)
