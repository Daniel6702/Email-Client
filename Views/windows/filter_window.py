from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QApplication, QDesktopWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from EmailService.models import Filter

class FilterWindow(QWidget):
    filter_signal = pyqtSignal(Filter)

    def __init__(self):
        super().__init__()
        self.window_settings()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.from_label = QLabel('Fra')
        self.from_input = QLineEdit(self)

        self.to_label = QLabel('Til')
        self.to_input = QLineEdit(self)

        self.subject_label = QLabel('Emne')
        self.subject_input = QLineEdit(self)

        self.contains_label = QLabel('Indeholder ordene')
        self.contains_input = QLineEdit(self)

        self.not_contains_label = QLabel('Indeholder ikke')
        self.not_contains_input = QLineEdit(self)

        self.size_label = QLabel('Størrelse')
        self.size_combobox = QComboBox(self)
        self.size_combobox.addItems(['større end', 'mindre end'])

        self.size_input = QLineEdit(self)
        self.size_input.setFixedWidth(50)

        self.size_units_combobox = QComboBox(self)
        self.size_units_combobox.addItems(['MB', 'KB'])

        self.date_label = QLabel('Dato inden for')
        self.date_combobox = QComboBox(self)
        self.date_combobox.addItems(['1 dag', '2 dage', '1 uge', '2 uger', '1 måned', '3 måneder', '6 måneder', '1 år'])

        self.search_button = QPushButton('Søg', self)
        self.search_button.clicked.connect(self.on_search)

        self.attachments_checkbox = QCheckBox('Indeholder vedhæftede filer', self)
        self.attachments_checkbox.setObjectName('filter_checkbox')
        self.exclude_chats_checkbox = QCheckBox('Inkluder ikke chatsamtaler', self)
        self.exclude_chats_checkbox.setObjectName('filter_checkbox')

        # Arrange widgets
        layout.addWidget(self.from_label)
        layout.addWidget(self.from_input)
        layout.addWidget(self.to_label)
        layout.addWidget(self.to_input)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.contains_label)
        layout.addWidget(self.contains_input)
        layout.addWidget(self.not_contains_label)
        layout.addWidget(self.not_contains_input)

        size_hbox = QHBoxLayout()
        size_hbox.addWidget(self.size_label)
        size_hbox.addWidget(self.size_combobox)
        size_hbox.addWidget(self.size_input)
        size_hbox.addWidget(self.size_units_combobox)
        layout.addLayout(size_hbox)

        date_hbox = QHBoxLayout()
        date_hbox.addWidget(self.date_label)
        date_hbox.addWidget(self.date_combobox)
        layout.addLayout(date_hbox)

        layout.addWidget(self.attachments_checkbox)
        layout.addWidget(self.exclude_chats_checkbox)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def on_search(self):
        filter_obj = Filter() 
        self.filter_signal.emit(filter_obj)


    def window_settings(self):
        self.setWindowTitle("Create filter")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 350, 350
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)