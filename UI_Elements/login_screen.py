import client_controller
from PyQt5.QtWidgets import QApplication, QListWidget, QLabel, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QLayout
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
import flask_app

'''
The primary purpose of the login screen is to generate and return a 'client' object.
'''
class LoginScreen(QWidget):
    login_successful = pyqtSignal(object)  

    def __init__(self, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.initial_layout()
        
        if (1==2): #check if there exists a user (NOT IMPLEMENTED)
            self.existing_user_login_layout()
        else:
            self.new_user_login_layout()
            
        self.setLayout(self.layout)
        
    def new_user_login_layout(self):
        grid = QGridLayout()
        google_button = QPushButton("Login with Google")
        outlook_button = QPushButton("Login with Outlook")
        grid.addWidget(google_button, 0, 0)
        grid.addWidget(outlook_button, 0, 1)
        google_button.clicked.connect(lambda: self.start_login_process('google'))
        outlook_button.clicked.connect(lambda: self.start_login_process('outlook'))
        self.layout.addLayout(grid)
    
    def existing_user_login_layout(self):
        pass
    
    def initial_layout(self):
        self.setWindowTitle("Smail")
        # Set the window's geometry to match the screen size
        screen = QDesktopWidget().screenGeometry()
        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.setGeometry(x, y, 400, 250)

        # Controls the logo of the window
        icon = QIcon("Images\icon_logo.png")
        self.setWindowIcon(icon)

        # Create a QLabel for the logo
        logo_label = QLabel(self)
        # Replace 'icon_logo.png' with the correct path to your logo file
        pixmap = QPixmap("Images\icon_logo.png")
        logo_width = 150
        pixmap = pixmap.scaledToWidth(logo_width, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center
        self.layout.addWidget(logo_label)   
        
        self.remember_me_checkbox = QCheckBox("Remember Me")
        self.layout.addWidget(self.remember_me_checkbox)
    
    def start_login_process(self,client_type):
        app = flask_app.FlaskAppWrapper('redirect_server')
        client = client_controller.ClientController(client_type, app)
        client.login()
        self.login_successful.emit(client)


    '''
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
    '''