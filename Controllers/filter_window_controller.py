from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
from Views.windows.filter_window import FilterWindow
from EmailService.models import Filter, Folder

class FilterWindowController(QWidget):
    set_filter_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.filter_window = FilterWindow()
        self.setup_connections()

    def setup_connections(self):
        self.filter_window.filter_signal.connect(self.on_set_filter)
    
    def on_set_filter(self, filter: Filter):
        self.set_filter_signal.emit(filter)
        self.filter_window.close()

    def show_filter(self, folders: list[Folder]):
        self.filter_window.add_folders(folders)
        self.filter_window.show()