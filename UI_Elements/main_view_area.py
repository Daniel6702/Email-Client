from PyQt5.QtWidgets import QStackedWidget,QApplication, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *

class MainView(QWidget):
    def __init__(self,parent=None):
        super(MainView, self).__init__(parent)
        self.layout = QVBoxLayout()
        
        self.new_user_widget = QWidget()
        self.EmailView(self.loading_widget)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.existing_user_widget)

    def EmailView(self,parent_widget):
        layout = QVBoxLayout(parent_widget)
        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        layout.addWidget(self.browser)
        self.layout.addLayout(layout)