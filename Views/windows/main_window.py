from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QGridLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import *

from Views.components.email_folder_layout import FolderArea
from Views.components.email_list_layout import EmailListArea
from Views.components.search_layout import SearchArea
from Views.components.email_view_area.email_view_layout import EmailView
from Controllers.main_window_controller import MainWindowController
from EmailService.models.email_client import EmailClient

PAGE_SIZE = 15

class MainWindow(QMainWindow):
    open_editor_window = pyqtSignal(object)
    open_settings_window = pyqtSignal()
    open_attachment_window = pyqtSignal(dict)
    get_email_from_editor = pyqtSignal(object, str)
    def __init__(self, email_client: EmailClient):
        super(MainWindow, self).__init__()
               
        #Initialize UI
        self.initialize_ui()
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        #Create Layouts
        self.email_view_area = EmailView()
        self.email_list_area = EmailListArea()
        self.folder_area = FolderArea()
        self.search_area = SearchArea()

        #Create Controller to handle signals and integration with email_client
        self.controller = MainWindowController(self, email_client) 

        #Create Grid
        grid_layout = QGridLayout()
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

    def initialize_ui(self):
        self.setWindowTitle("Smail")
        self.setWindowState(Qt.WindowMaximized)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width(), screen.height())
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)
    