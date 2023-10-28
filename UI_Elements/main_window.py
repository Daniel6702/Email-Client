from email_util import Email, generate_attachment_dict, print_email
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *

from UI_Elements.email_folder_area import FolderArea
from UI_Elements.email_list_area import EmailListArea
from UI_Elements.search_area import SearchArea
from UI_Elements.email_view_area import EmailView

class MainWindow(QMainWindow):
    open_editor_window = pyqtSignal()
    test_signal = pyqtSignal(list)
    def __init__(self, appController):
        super(MainWindow, self).__init__()
        self.appController = appController

        #Initialize UI
        self.initialize_ui()
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        #Generate Layouts
        grid_layout = QGridLayout()
        self.email_list_area = EmailListArea()
        self.test_signal.connect(self.email_list_area.add_emails_to_list)
        self.search_area = SearchArea(self.open_editor_window,self.appController, self.test_signal)
        self.folder_area = FolderArea(self.appController)
        self.email_view_area = EmailView()

        #Connect Signals
        self.email_list_area.email_clicked.connect(self.get_clicked_email)
        self.folder_area.email_signal.connect(self.update_mails)

        #Create Grid
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 3) 
        grid_layout.setColumnStretch(2, 6)  
        grid_layout.addLayout(self.search_area, 0, 0, 1, 2)
        grid_layout.addLayout(self.email_list_area, 1, 1)
        grid_layout.addLayout(self.folder_area, 1, 0)
        grid_layout.addLayout(self.email_view_area, 0, 2, 2, 1)

        #Show grid
        main_widget.setLayout(grid_layout)
        self.show()

    def update_mails(self, emails):
        self.email_list_area.add_emails_to_list(emails)

    def get_clicked_email(self,mail):
        self.email_view_area.updateEmailView(mail)

    def get_mail_from_editor(self,mail):
        if type(mail) is not str:
            self.appController.send_email(mail)

    def initialize_ui(self):
        self.setWindowTitle("Smail")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        icon = QIcon("Images\\icon_logo.png")
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

