from PyQt5.QtWidgets import QMessageBox, QMainWindow, QDesktopWidget, QWidget, QGridLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import *

from Views.components.email_folder_layout import FolderArea
from Views.components.email_list_layout import EmailListArea
from Views.components.search_layout import SearchArea
from Views.components.email_view_area.email_view_layout import EmailView

PAGE_SIZE = 15

class MainWindow(QMainWindow):
    def __init__(self):
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

        #Create Grid
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(0, 2)
        grid_layout.setColumnStretch(1, 5)
        grid_layout.setColumnStretch(2, 7)
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
    