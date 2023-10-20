from email_util import Email, generate_attachment_dict, print_email
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *

from UI_Elements.folder_field import FolderField
from UI_Elements.email_list_field import EmailList
from UI_Elements.search_area import SearchArea

class MainWindow(QMainWindow):
    
    email_clicked = pyqtSignal(object)

    def __init__(self, client):
        super(MainWindow, self).__init__()
        self.client = client
        self.initialize_ui()
    

        # Create a central widget for the main window
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Create a QVBoxLayout for the central widget
        self.main_layout = QVBoxLayout(main_widget)
        # Create a QSplitter widget
        splitter = QSplitter(Qt.Horizontal)
        # Create a widget for the left section (search bar and email list)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        '''Search bar area'''
        search_area = SearchArea()
        search_bar_layout = search_area.layout

        '''Email list'''
        self.email_list = EmailList(client)
        self.email_list.email_clicked.connect(self.get_clicked_email)
        left_layout.addLayout(search_bar_layout)
        left_layout.addLayout(self.email_list.list_layout)

        '''Folders'''
        self.folder_field = FolderField(self.client)
        self.folder_field.email_signal.connect(self.update_mails)
        self.folder_layout = self.folder_field.folder_field_layout()
        left_layout.addLayout(self.folder_layout) #FIX THIS

        # Set the layout for the left widget
        left_widget.setLayout(left_layout)

        # Create a widget for the right section (web view)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.from_user = QLineEdit()
        self.from_user.setPlaceholderText("From:")
        self.too_user = QLineEdit()
        self.too_user.setPlaceholderText("To:")
        self.subject = QLineEdit()
        self.subject.setPlaceholderText("Subject:")
        # Add the 'From', 'Too', 'Subject' QLineEdit widgets to the right layout
        right_layout.addWidget(self.from_user)
        right_layout.addWidget(self.too_user)
        right_layout.addWidget(self.subject)

        # Create an instance of QWebEngineView
        self.browser = QWebEngineView()
       

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
        self.main_layout.addWidget(splitter)

        #improtant for making dark/light mode work
        self.is_light_mode = True

        self.show()
    
    '''This function is run by the folder field when a folder is clicked. the emails parameter is a list of email objects from that folder'''
    def update_mails(self, emails):
        for i in reversed(range(self.email_list.list_layout.count())): 
            self.email_list.list_layout.itemAt(i).widget().setParent(None)
        self.email_list.setup_email_list(emails)
        self.main_layout.update()

    def get_clicked_email(self,mail):
        self.browser.setHtml(mail.body)

    def initialize_ui(self):
        self.setWindowTitle("Smail")
        # Get the screen geometry using QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        # Set the window's geometry to match the screen size
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        # Controls the logo of the window
        icon = QIcon("Images\icon_logo.png")
        self.setWindowIcon(icon)

    #toggle button for the background
    def toggleDarkMode(self):
        #Toggle the mode flag
        self.is_light_mode = not self.is_light_mode
        #Apply the appropriate stylesheet
        self.setStyleSheet(self.getStylesheet(self.is_light_mode))
        # Change the dark mode button icon
        if self.is_light_mode:
            self.light_dark.setIcon(self.dark_mode_icon)
        else:
            self.light_dark.setIcon(self.light_mode_icon)

    #Changes the color of the background
    def getStylesheet(self, is_light_mode):
        if is_light_mode:
            return ""
        else:
            # Set the background color to an RGB value
            dark_stylesheet = "background-color: rgb(255, 91, 165); color: white;"
            return dark_stylesheet
        
    # Slot method to handle login success and display MainWindow
    def on_login_successful(self, html):
        # Create an instance of MainWindow and show it
        main_window = MainWindow(html)
        main_window.show()

        # Set the HTML content for the email view
        main_window.set_email_html(html)

    def on_email_clicked(self, item):
        # Get the index of the selected item
        index = self.list.row(item)

        # Fetch the corresponding email from your Outlook or Google service
        selected_email = self.client.get_emails(number_of_mails=15)[index]

        # Update the QLineEdit widgets with information from the selected email
        self.from_user.setText(f"From: {selected_email.from_email}")
        self.too_user.setText(f"To: {selected_email.to_email}")
        self.subject.setText(f"Subject: {selected_email.subject}")
        # Update the displayed HTML content using the utility class
        # UiUtility.update_email_html(self.browser, selected_email)
        # Emit the signal with the selected email
        self.email_clicked.emit(selected_email)

    def setup_email_list(self):
        emails = self.client.get_emails(number_of_mails=15)
        for i, mail in enumerate(emails):
            email_item_text = f"Subject: {mail.subject}\nFrom: {mail.from_email}\nDate: {mail.datetime_info['date']} {mail.datetime_info['time'].split('.')[0]}"
            item = QListWidgetItem(email_item_text)
            self.list.addItem(item)
        # Connect the itemClicked signal to the on_email_clicked slot
        self.list.itemClicked.connect(self.on_email_clicked)

