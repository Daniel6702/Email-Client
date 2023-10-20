from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class SearchArea(QWidget):
    
    def __init__(self,parent=None):
        super(SearchArea, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setup_layout()

    def setup_layout(self):
        search_bar_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")

        # Adds clickable icons
        self.dark_mode_icon = QIcon("Images\icon_moon.png")
        self.light_mode_icon = QIcon("Images\icon_sun.png")
        contact_tab = QPushButton(QIcon("Images\icon_contact.png"), "Contacts")
        mail_tab = QPushButton(QIcon("Images\icon_mail.png"), "Mail")
        settings_tab = QPushButton(QIcon("Images\icon_gear.png"), "Settings")
        
        # Add the search bar widgets to the search layout
        search_layout.addWidget(self.searchbar)

        # Create a horizontal layout for the icons
        icons_layout = QHBoxLayout()
        icons_layout.addWidget(contact_tab)
        icons_layout.addWidget(mail_tab)
        icons_layout.addWidget(settings_tab)


        # Add the search layout and icons layout to the vertical search bar layout
        search_bar_layout.addLayout(search_layout)
        search_bar_layout.addLayout(icons_layout)
        self.layout.addLayout(search_bar_layout)
