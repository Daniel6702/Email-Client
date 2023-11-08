from PyQt5.QtWidgets import QStackedWidget,QApplication, QListWidget, QLabel, QMainWindow,QFrame, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget, QLayout
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings,QSize, QEasingCurve, QPropertyAnimation, QRect, QPoint
from PyQt5.QtGui import *
import flask_app
import email_util
import time
from EmailService.models.email_client import EmailClient
from EmailService.factories.gmail_service_factory import GmailServiceFactory
from EmailService.factories.outlook_service_factory import OutlookServiceFactory
'''
The primary purpose of the login screen is to generate and return a 'client' object.
'''
class LoginScreen(QWidget):
    login_successful = pyqtSignal(object)
    def __init__(self, parent=None):
        super(LoginScreen, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        '''load initial window settings'''
        self.initial_layout()

        '''create main widgets'''
        self.new_user_widget = QWidget()
        self.existing_user_widget = QWidget()
        self.loading_widget = QWidget()
        self.new_user_login_layout(self.new_user_widget)
        self.existing_user_login_layout(self.existing_user_widget)
        self.loading_screen_layout(self.loading_widget)
        
        '''create stacked widget and add the main widgets. Such that we can switch between them'''
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.existing_user_widget)
        self.stacked_widget.addWidget(self.new_user_widget)
        self.stacked_widget.addWidget(self.loading_widget)

        '''Check if there are any users saved. If so, switch to existing user login layout. Else, switch to new user login layout'''
        if email_util.load_users_from_file('Certificates\\users.json') != []:
            self.switch_to_existing_user_login_layout()
        else:
            self.switch_to_new_user_login_layout()
            
        self.layout.addWidget(self.stacked_widget)

        '''Animation'''
        self.animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        self.animation.setDuration(100)  # 500 ms
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.stacked_widget.currentChanged.connect(self.start_animation)
        
        self.setLayout(self.layout)

    def loading_screen_layout(self,parent_widget):
        layout = QVBoxLayout(parent_widget)
        label = QLabel("Loading...")
        layout.addWidget(label, 0, Qt.AlignCenter)

    def start_animation(self):
        offset_width = self.stacked_widget.width()
        if self.stacked_widget.currentIndex() == 1: 
            start_rect = QRect(self.stacked_widget.geometry().topLeft() + QPoint(offset_width, 0),
                            self.stacked_widget.geometry().size())
        else:  
            start_rect = QRect(self.stacked_widget.geometry().topLeft() - QPoint(offset_width, 0),
                            self.stacked_widget.geometry().size())

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(self.stacked_widget.geometry())
        self.animation.start()

    def new_user_login_layout(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        '''Add Logo'''
        layout.addWidget(self.create_logo())
        
        '''Add remember me checkbox'''
        self.remember_me_checkbox = QCheckBox("Remember Me")
        self.remember_me_checkbox.setMaximumWidth(145)
        layout.addWidget(self.remember_me_checkbox)

        '''Add login buttons'''
        grid = QGridLayout()
        google_button = QPushButton("Login with Google")
        outlook_button = QPushButton("Login with Outlook")
        google_button.setIcon(QIcon(QPixmap('Images\\google_icon.png')))
        outlook_button.setIcon(QIcon(QPixmap('Images\\outlook_icon.png')))
        icon_size = QSize(32, 32)  # adjust width and height to your needs
        google_button.setIconSize(icon_size)
        outlook_button.setIconSize(icon_size)
        grid.addWidget(google_button, 0, 0)
        grid.addWidget(outlook_button, 0, 1)
        google_button.clicked.connect(self.new_login_google)
        outlook_button.clicked.connect(self.new_login_outlook)
        layout.addLayout(grid)

        '''Add back button'''
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_existing_user_login_layout)
        back_button.setMaximumWidth(80)
        layout.addWidget(back_button)
            
    def existing_user_login_layout(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        '''Add Logo'''
        layout.addWidget(self.create_logo())

        '''text labels'''
        welcome_label = QLabel("Welcome Back")
        welcome_label.setObjectName("welcome_label")
        layout.addWidget(welcome_label)
        select_user_label = QLabel("Please select a user")
        select_user_label.setObjectName("select_user_label")
        layout.addWidget(select_user_label)

        '''lines'''
        login_line1 = QFrame()
        login_line1.setFrameShape(QFrame.HLine)
        login_line1.setObjectName('login_line')
        login_line2 = QFrame()
        login_line2.setFrameShape(QFrame.HLine)
        login_line2.setObjectName('login_line')

        '''Generate user buttons'''
        users = email_util.load_users_from_file('Certificates\\users.json')
        buttons = []
        def make_user_button_function(user):
            def function():
                return self.start_login_process(user.client_type, user)
            return function
        for user in users:
            button = QPushButton(user.name+" ("+user.client_type+")")
            button.clicked.connect(make_user_button_function(user))
            buttons.append(button)

        '''Add user buttons and lines to layout grid'''
        grid = QGridLayout()
        grid.addWidget(login_line1, 0, 0)
        for i, button in enumerate(buttons):
            grid.addWidget(button, i+1, 0)
        grid.addWidget(login_line2, len(buttons)+1, 0)

        '''Create new user button'''
        new_user_button = QPushButton("New User")
        new_user_button.clicked.connect(self.switch_to_new_user_login_layout)
        new_user_button.setObjectName("new_user_button")
        new_user_button.setMaximumWidth(100)

        layout.addLayout(grid)
        layout.addWidget(new_user_button,0, Qt.AlignCenter)

    def switch_to_existing_user_login_layout(self):
        self.previous_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_new_user_login_layout(self):
        self.previous_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_loading_screen(self):
        self.previous_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(2)
    
    def initial_layout(self):
        self.setWindowTitle("Smail")
        # Set the window's geometry to match the screen size
        screen = QDesktopWidget().screenGeometry()

        # Calculate the center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 400, 250
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Controls the logo of the window
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)
    
    def create_logo(self):
        logo_label = QLabel()
        pixmap = QPixmap("Images\\icon_logo.png")
        logo_width = 150
        pixmap = pixmap.scaledToWidth(logo_width, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center
        return logo_label 

    def new_login_google(self):
        self.start_login_process("google", None)

    def new_login_outlook(self):
        self.start_login_process("outlook", None)

    def start_login_process(self,client_type, user):
        if client_type == "google":
            factory = GmailServiceFactory()
        elif client_type == "outlook":
            factory = OutlookServiceFactory()
        client = EmailClient(factory)
        client.login(user=user, save_user=self.remember_me_checkbox.isChecked())
        self.login_successful.emit(client)


