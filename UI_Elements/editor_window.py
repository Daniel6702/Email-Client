from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *

class EditorWindow(QWidget):
    mail_signal_from_editor = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.initial_layout()
    
    def initial_layout(self):
        self.setWindowTitle("Editor")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\icon_logo.png")
        self.setWindowIcon(icon)