import client_controller
from email_util import Email, generate_attachment_dict, print_email
import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QLabel, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
import imaplib
from email.header import decode_header
import os
from email_util import Email

class LoginScreen(QWidget):
    login_successful = pyqtSignal(str)  # Custom signal for successful login

    def __init__(self, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.setWindowTitle("Smail")
        # Set the window's geometry to match the screen size
        screen = QDesktopWidget().screenGeometry()
        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.setGeometry(x, y, 400, 250)

        # Controls the logo of the window
        icon = QIcon("icon_logo.png")
        self.setWindowIcon(icon)

        layout = QVBoxLayout()
        # Create a QLabel for the logo
        logo_label = QLabel(self)
        # Replace 'icon_logo.png' with the correct path to your logo file
        pixmap = QPixmap("icon_logo.png")
        logo_width = 150
        pixmap = pixmap.scaledToWidth(logo_width, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center
        layout.addWidget(logo_label)   

        # creates an email line
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        layout.addWidget(self.email_input)
        #creates a password line
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        #Hides password from other
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        #creates a login button, to connect to main window
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
         # Create a checkbox for "Remember Me"
        self.remember_me_checkbox = QCheckBox("Remember Me")
        layout.addWidget(self.remember_me_checkbox)

        # Load the saved email and password (if available)
        self.load_saved_credentials()
        
        self.setLayout(layout)


    def save_credentials(self, email, password):
        settings = QSettings("MyApp", "Login")
        settings.setValue("email", email)
        settings.setValue("password", password)
        settings.setValue("remember_me", self.remember_me_checkbox.isChecked())


    def load_saved_credentials(self):
        settings = QSettings("MyApp", "Login")
        email = settings.value("email", "")
        password = settings.value("password", "")
        remember_me = settings.value("remember_me", False)  # Explicitly convert to bool
    
        self.email_input.setText(email)
        self.password_input.setText(password)
        self.remember_me_checkbox.setChecked(bool(remember_me))  # Convert to bool

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
    
        if self.authenticate(email, password):
            if self.remember_me_checkbox.isChecked():
                self.save_credentials(email, password)
            dynamic_html_content = self.fetch_dynamic_email_content()
            self.login_successful.emit(dynamic_html_content)
            self.handle_successful_login()
        
    def authenticate(self, email, password):    
        # Example: Authenticate using dummy credentials
        if email == 'DACASoftDev_test@hotmail.com' and password == 'DACAtest':
            return True
        else:
            return False

    def handle_successful_login(self, html):
        try:
            # Retrieve the dynamic email HTML content after successful login
            # Replace this with the code to fetch email content from your email service
            dynamic_html_content = self.fetch_dynamic_email_content()

            # Emit the login_successful signal with the dynamic HTML content
            self.login_successful.emit(dynamic_html_content)
        except Exception as e:
            print("Error in handle_successful_login:", str(e))
    
    def fetch_dynamic_email_content(self):
         # Create a test email for demonstration
        email_client = Email(
        from_email='dacasoftdev_test@hotmail.com',
        to_email=['dacasoftdev_test@hotmail.com'],
        subject='Sample Email',
        body='<p>This is a sample email body.</p>',
        datetime_info={'date': '2023-09-18', 'time': '15:43:56.111501'},
        )

        # Extract the HTML content from the test email
        email_content = email_client.body

        return email_content


class MainWindow(QMainWindow):
    def __init__(self, html=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Smail")
        # Get the screen geometry using QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        # Set the window's geometry to match the screen size
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        # Controls the logo of the window
        icon = QIcon("icon_logo.png")
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
        self.dark_mode_icon = QIcon("icon_moon.png")
        self.light_mode_icon = QIcon("icon_sun.png")
        contact_tab = QPushButton(QIcon("icon_contact.png"), "Contacts")
        mail_tab = QPushButton(QIcon("icon_mail.png"), "Mail")
        settings_tab = QPushButton(QIcon("icon_gear.png"), "Settings")
        self.light_dark = QPushButton(self.dark_mode_icon, "Barbie mode")
        self.light_dark.clicked.connect(self.toggleDarkMode)

        # Add the search bar widgets to the search layout
        search_layout.addWidget(self.searchbar)

        # Create a horizontal layout for the icons
        icons_layout = QHBoxLayout()
        icons_layout.addWidget(contact_tab)
        icons_layout.addWidget(mail_tab)
        icons_layout.addWidget(settings_tab)
        icons_layout.addWidget(self.light_dark)

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

        #improtant for making dark/light mode work
        self.is_light_mode = True

        self.show()
    
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
        main_window = MainWindow()
        main_window.show()

        # Set the HTML content for the email view
        main_window.set_email_html(html)