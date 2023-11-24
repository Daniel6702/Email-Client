from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication
from Views.windows.folder_selector_window import FolderWindow
from EmailService.models import Folder

class FolderSelectorWindowController(QWidget):
    folder_selected = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.folder_window = FolderWindow(self)
        self.user_initiated_selection = False #try to flag user action
        self.setup_connections()

    def setup_connections(self):
        self.folder_window.on_folder_selected.connect(self.on_folder_selected)


    def on_folder_selected(self, folder: Folder):
        if self.user_initiated_selection:
            self.folder_window.close()
            self.folder_selected.emit(folder)
            self.user_initiated_selection = False
        else:
            self.user_initiated_selection = True  # Reset the flag for the next time


    def show_folder_selector(self, folders: list[Folder]):
        self.folder_window.add_folders(folders)
        self.folder_window.show()

    def set_user_initiated_selection(self, value):
        self.user_initiated_selection = value
        
          