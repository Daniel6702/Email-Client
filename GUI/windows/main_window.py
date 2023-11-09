from email_util import Email, generate_attachment_dict, print_email
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *

from GUI.layouts.email_folder_area import FolderArea, FolderSignal
from GUI.layouts.email_list_area import EmailListArea
from GUI.layouts.search_area import SearchArea
from GUI.layouts.email_view_area import EmailView

class MainWindow(QMainWindow):
    open_editor_window = pyqtSignal(object)
    open_settings_window = pyqtSignal()
    test_signal = pyqtSignal(list)
    open_attachment_window = pyqtSignal(dict)
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
        self.search_area = SearchArea(self.open_editor_window,self.open_settings_window,self.appController, self.test_signal)
        self.folder_area = FolderArea(self.appController)
        self.email_view_area = EmailView(self.open_attachment_window)

        #Connect Signals
        self.email_list_area.email_clicked.connect(self.get_clicked_email)
        self.folder_area.email_signal.connect(self.get_folder_signal)

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

    def get_folder_signal(self, folder_signal: FolderSignal) -> None:
        self.current_folder = folder_signal.folder_name
        emails = folder_signal.emails
        self.email_list_area.add_emails_to_list(emails)

    def get_clicked_email(self,mail: Email):
        print("CLICKED EMAIL:", mail.subject)
        if self.current_folder in ["Drafts", "Draft", "DRAFT", "draft", "DRAFTS", "drafts"]:
            self.open_editor_window.emit(mail)
        else:
            self.email_view_area.updateEmailView(mail)

    def get_mail_from_editor(self,mail_signal):
        email = mail_signal.email
        if mail_signal.action == "send":
            self.appController.send_mail(email)
        elif mail_signal.action == "save":
            self.appController.save_mail(email)

    def initialize_ui(self):
        self.setWindowTitle("Smail")
        self.setWindowState(Qt.WindowMaximized)
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
