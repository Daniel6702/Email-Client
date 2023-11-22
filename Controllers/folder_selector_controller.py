from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from Views.windows.folder_selector_window import FolderWindow
from EmailService.models import Folder

class FolderSelectorWindowController(QWidget):
    folder_selected = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.folder_window = FolderWindow()
        self.setup_connections()

    def setup_connections(self):
        self.folder_window.on_folder_selected.connect(self.on_folder_selected)

    def on_folder_selected(self, folder: Folder):
        self.folder_window.close()
        self.folder_selected.emit(folder)

    def show_folder_selector(self, folders: list[Folder]):
        self.folder_window.add_folders(folders)
        self.folder_window.show()