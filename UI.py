import client_controller
from email_util import Email, generate_attachment_dict, print_email
import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QLabel, QMainWindow, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout


class MainWindow(QMainWindow):
    def __init__(self, html):
        super(MainWindow, self).__init__()
        #Names the title of the mail
        self.setWindowTitle("Smail")
        #controls the aspect ratio
        self.setGeometry(900,900,900,900)
        #moves the starting position of the program
        self.move(50,20)


        self.layout = QGridLayout()
        
        self.search = QHBoxLayout()

        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        search_label = QLabel('Search:')
        self.search.addWidget(search_label)
        self.search.addWidget(self.searchbar)
        
        self.list = QListWidget()
        self.list.insertItem(0, 'Mail 0')
        self.list.insertItem(1, 'Mail 1')
        self.list.insertItem(2, 'Mail 2')
        self.list.insertItem(3, 'Mail 3')
        self.list.insertItem(4, 'Mail 4')


        #left_box.addLayout(search_layout)

        #self.layout.addLayout(left_box,0,0)

        self.browser = QWebEngineView()
        self.browser.setHtml(html)

        self.layout.addLayout(self.search,0,0)
        self.layout.addWidget(self.list,1,0)
        self.layout.addWidget(self.browser,1,1)

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)
        self.show()