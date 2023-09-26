import client_controller
from email_util import Email, generate_attachment_dict, print_email
import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QLabel, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, html):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Smail")
        # Get the screen geometry using QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        # Set the window's geometry to match the screen size
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        # Controls the logo of the window
        icon = QIcon("logo.jpg")
        self.setWindowIcon(icon)

        # Create a central widget for the main window
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Create a QVBoxLayout for the central widget
        main_layout = QVBoxLayout(main_widget)
        # Create a QSplitter widget
        splitter = QSplitter(Qt.Horizontal)
        # Create a widget for the left section (search bar and email list)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Create a vertical layout for the search bar and buttons
        search_bar_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")

        # Adds clickable icons
        contact_tab = QPushButton(QIcon("contact_icon.png"), "Contacts")
        mail_tab = QPushButton(QIcon("mail_icon.png"), "Mail")
        settings_tab = QPushButton(QIcon("gear_icon.png"), "Settings")

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

        # Create a list widget for emails
        self.list = QListWidget()
        self.list.insertItem(0, 'Mail 0')
        self.list.insertItem(1, 'Mail 1')
        self.list.insertItem(2, 'Mail 2')
        self.list.insertItem(3, 'Mail 3')
        self.list.insertItem(4, 'Mail 4')

        # Create a horizontal layout for email items
        email_layout = QHBoxLayout()
        email_layout.addWidget(self.list)

        # Add the search bar layout, email layout, and browser to the main layout
        left_layout.addLayout(search_bar_layout)
        left_layout.addLayout(email_layout)

        # Set the layout for the left widget
        left_widget.setLayout(left_layout)

        # Create a widget for the right section (web view)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        right_layout.addWidget(self.browser)

        # Set the layout for the right widget
        right_widget.setLayout(right_layout)

        # Add the left and right widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Set the initial size of the left section to take up 2/3 of the screen
        screen_width = self.geometry().width()  # Get the current screen width
        splitter.setSizes([int(screen_width * 1 / 3), int(screen_width * 2 / 3)])

        # Set the splitter as the central widget
        main_layout.addWidget(splitter)

        self.show()