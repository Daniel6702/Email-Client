from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class SearchArea(QVBoxLayout):
    dark_mode_signal = pyqtSignal()
    test_signal = pyqtSignal(list)
    def __init__(self,new_mail_signal, appController, signal):
        super().__init__()
        self.setup_layout()
        self.new_mail_signal = new_mail_signal
        self.appController = appController
        self.signal = signal

    def toggleDarkMode(self):
        self.dark_mode_signal.emit()

    def setup_layout(self):
        search_bar_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.returnPressed.connect(self.search_update)
        

        # Adds clickable icons
        self.dark_mode_icon = QIcon("Images\\icon_moon.png")
        self.light_mode_icon = QIcon("Images\\icon_sun.png")
        contact_tab = QPushButton(QIcon("Images\\icon_contact.png"), "Contacts")

        new_mail_button = QPushButton(QIcon("Images\\icon_mail.png"), "Write New Mail")
        new_mail_button.setObjectName("new_mail_button") 
        new_mail_button.clicked.connect(self.new_mail_button)

        settings_tab = QPushButton(QIcon("Images\\icon_gear.png"), "Settings")
        self.light_dark = QPushButton(self.dark_mode_icon, "Barbie mode")
        self.light_dark.clicked.connect(self.toggleDarkMode)

        menu = QMenu(self.searchbar)  # Parented to self.searchbar to avoid error
        menu.addAction('Filter')
        menu.addSeparator()
        dark_mode_action = menu.addAction('Dark Mode')
        dark_mode_action.triggered.connect(self.toggleDarkMode)
        menu.addSeparator()
        menu.addAction('Log Out')
        settings_tab.setMenu(menu)

        # Add the search bar widgets to the search layout
        search_layout.addWidget(self.searchbar)

        # Create a horizontal layout for the icons
        icons_layout = QHBoxLayout()
        icons_layout.addWidget(new_mail_button)
        icons_layout.addWidget(contact_tab)
        icons_layout.addWidget(settings_tab)
        icons_layout.addWidget(self.light_dark)

        # Add the search layout and icons layout to the vertical search bar layout
        search_bar_layout.addLayout(search_layout)
        search_bar_layout.addLayout(icons_layout)
        self.addLayout(search_bar_layout)


    def search_update(self):
        search_criteria = self.searchbar.text()
        emails = self.appController.get_emails(query=search_criteria)
        self.signal.emit(emails)
    
        
    
    def new_mail_button(self):
        self.new_mail_signal.emit()
        
    