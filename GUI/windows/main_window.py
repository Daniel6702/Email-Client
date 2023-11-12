from email_util import Email, generate_attachment_dict, print_email, Folder
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
import logging

from GUI.layouts.email_folder_layout import FolderArea
from GUI.layouts.email_list_layout import EmailListArea
from GUI.layouts.search_layout import SearchArea
from GUI.layouts.email_view_area.email_view_layout import EmailView
from EmailService.models.email_client import EmailClient

PAGE_SIZE = 15

class MainWindow(QMainWindow):
    open_editor_window = pyqtSignal(object)
    open_settings_window = pyqtSignal()
    test_signal = pyqtSignal(list)
    open_attachment_window = pyqtSignal(dict)
    delete_email_signal = pyqtSignal(Email)
    mark_as_signal = pyqtSignal(Email, bool)
    def __init__(self, email_client: EmailClient):
        super(MainWindow, self).__init__()
        self.email_client = email_client
        
        #Initialize UI
        self.initialize_ui()
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        #Generate Layouts
        grid_layout = QGridLayout()
        self.email_list_area = EmailListArea()
        self.test_signal.connect(self.email_list_area.add_emails_to_list)
        self.search_area = SearchArea(self.open_editor_window,self.open_settings_window,self.email_client, self.test_signal)

        #Create Folder Area
        self.folder_area = FolderArea()
        folders = self.email_client.get_folders()
        self.delete_folder = self.get_delete_folder(folders)
        self.folder_area.add_folders(folders)

        self.email_view_area = EmailView(self.open_attachment_window, 
                                         self.open_editor_window,
                                         self.delete_email_signal,
                                         self.mark_as_signal)

        #Connect Signals
        self.email_list_area.email_clicked.connect(self.get_clicked_email)
        self.folder_area.folder_selected.connect(self.get_folder_signal)
        self.delete_email_signal.connect(self.get_delete_signal)
        self.mark_as_signal.connect(self.email_client.mark_email_as)

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

    def get_delete_folder(self, folders: list[Folder]):
        for folder in folders:
            if folder.name in ["Delete", "Delete", "DELETE", "delete", "DELETED", "deleted", "Deleted", "trash", "Trash", "TRASH", "bin", "Bin", "BIN", "Deleted Items"]:
                return folder
            else:
                pass

    def get_delete_signal(self, email: Email):
        empty_mail = Email(from_email="",to_email="",subject="",body="Select an email to view it here",datetime_info={},attachments=[], id="")
        self.email_view_area.updateEmailView(empty_mail)
        self.email_list_area.remove_email_from_list(email)
        if self.current_folder is self.delete_folder:
            self.email_client.delete_mail(email)
        else:
            self.email_client.move_email_to_folder(self.current_folder, self.delete_folder, email)

    def get_folder_signal(self, folder: Folder) -> None:
        logging.info(f"Folder Selected: {folder.name}")
        self.current_folder = folder
        logging.info(f"Retrieving {PAGE_SIZE} emails from {folder.id}")
        emails = self.email_client.get_mails(folder.id, "", PAGE_SIZE)
        self.email_list_area.add_emails_to_list(emails)

    def get_clicked_email(self,mail: Email):
        logging.info(f"Email Selected: {mail.subject}")
        if self.current_folder.name in ["Drafts", "Draft", "DRAFT", "draft", "DRAFTS", "drafts"]:
            self.open_editor_window.emit(mail)
        else:
            self.email_view_area.updateEmailView(mail)

    def get_mail_from_editor(self,email: Email, action: str):
        if action == "send":
            self.email_client.send_mail(email)
        elif action == "save":
            self.email_client.save_draft(email)
        elif action == "update":
            self.email_client.update_draft(email)


    def initialize_ui(self):
        self.setWindowTitle("Smail")
        self.setWindowState(Qt.WindowMaximized)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)