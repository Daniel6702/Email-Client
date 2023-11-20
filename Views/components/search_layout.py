from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class SearchArea(QVBoxLayout):
    search_signal = pyqtSignal(str)
    new_mail_signal = pyqtSignal(object)
    open_settings_signal = pyqtSignal()
    open_contacts_signal = pyqtSignal()
    open_filter_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_layout()

    def toggleDarkMode(self):
        self.dark_mode_signal.emit()

    def setup_layout(self):
        search_bar_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.returnPressed.connect(self.search_update)
        search_layout.addWidget(self.searchbar)

        self.filter_button = QPushButton(QIcon("Images\\filter.png"),"")
        self.filter_button.setObjectName("filter_button")
        self.filter_button.clicked.connect(self.open_filter_signal.emit)
        search_layout.addWidget(self.filter_button)

        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.search_update)
        search_layout.addWidget(self.search_button)
        
        # Adds clickable icons
        contact_button = QPushButton(QIcon("Images\\icon_contact.png"), "Contacts")
        contact_button.setObjectName("Contacts")
        contact_button.clicked.connect(self.open_contacts_signal.emit)

        new_mail_button = QPushButton(QIcon("Images\\icon_mail.png"), "Write New Mail")
        new_mail_button.setObjectName("new_mail_button") 
        new_mail_button.clicked.connect(self.new_mail_button)

        settings_button = QPushButton(QIcon("Images\\icon_gear.png"), "Settings")
        settings_button.setObjectName("Settings") 
        settings_button.clicked.connect(self.open_settings_signal.emit)        

        # Create a horizontal layout for the icons
        icons_layout = QHBoxLayout()
        icons_layout.addWidget(new_mail_button)
        icons_layout.addWidget(contact_button)
        icons_layout.addWidget(settings_button)
    
        # Add the search layout and icons layout to the vertical search bar layout
        search_bar_layout.addLayout(search_layout)
        search_bar_layout.addLayout(icons_layout)
        self.addLayout(search_bar_layout)

    def search_update(self):
        search_criteria = self.searchbar.text()
        self.search_signal.emit(search_criteria)
    
    def new_mail_button(self):
        self.new_mail_signal.emit(None)