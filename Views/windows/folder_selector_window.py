from PyQt5.QtWidgets import QDesktopWidget, QWidget, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from EmailService.models import Folder
from Views.components.email_folder_layout import FolderArea

class FolderWindow(QWidget):
    on_folder_selected = pyqtSignal(Folder)
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initial_layout()
        self.folder_area = FolderArea()
        self.folder_area.folder_selected.connect(self.emit_folder_selected)
        self.setLayout(self.folder_area)

    def emit_folder_selected(self, folder: Folder):
        self.on_folder_selected.emit(folder)
        self.close()

    def add_folders(self, folders: list[Folder]):
        self.folder_area.add_folders(folders)

    def initial_layout(self):
        self.setWindowTitle("Select a Folder")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 300, 800
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)
        
    def closeEvent(self, event):
        # This method is called when the widget is being closed
        if self.isVisible():
            self.controller.set_user_initiated_selection(False)
        super().closeEvent(event)