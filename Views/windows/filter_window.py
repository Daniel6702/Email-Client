from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QApplication, QDesktopWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from EmailService.models import Filter, Folder
from Views.components.email_folder_layout import FolderArea
from datetime import datetime, timedelta

class FilterWindow(QWidget):
    filter_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.window_settings()
        self.initUI()

    def add_folders(self, folders: list[Folder]):
        self.folders = folders

    def initUI(self):
        self.main_layout = QHBoxLayout(self)
        layout = QVBoxLayout()

        self.folder = Folder("","",[])
        self.folder_widget = None

        self.from_label = QLabel('From')
        self.from_input = QLineEdit(self)

        self.to_label = QLabel('To')
        self.to_input = QLineEdit(self)

        self.subject_label = QLabel('Subject')
        self.subject_input = QLineEdit(self)

        self.contains_label = QLabel('Contains')
        self.contains_input = QLineEdit(self)

        self.not_contains_label = QLabel('Does not contain')
        self.not_contains_input = QLineEdit(self)

        self.date_label = QLabel('Recieved within')
        self.date_combobox = QComboBox(self)
        self.date_combobox.addItems(['1 day', '2 days', '1 week', '2 week', '1 month', '3 months', '6 months', '1 year'])

        self.set_filter_button = QPushButton('Set Filter', self)
        self.set_filter_button.clicked.connect(self.on_set_filter)

        self.reset_filter_button = QPushButton('Reset Filter', self)
        self.reset_filter_button.clicked.connect(self.on_reset_filter)

        self.attachments_checkbox = QCheckBox('Contain attachments', self)
        self.attachments_checkbox.setObjectName('filter_checkbox')

        #self.is_read_checkbox = QCheckBox('Is read', self)
        #self.is_read_checkbox.setObjectName('filter_checkbox')
        self.read_status_label = QLabel('Read Status')
        self.read_status_combobox = QComboBox(self)
        self.read_status_combobox.addItems(['All', 'Read', 'Unread'])

        self.attachments_checkbox.setObjectName('filter_checkbox')

        self.folder_temp_layout = QHBoxLayout()
        self.select_folder_button = QPushButton('Select folder', self)
        self.select_folder_button.clicked.connect(self.on_select_folder)
        self.folder_temp_layout.addWidget(self.select_folder_button)

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

        date_hbox = QHBoxLayout()
        date_hbox.addWidget(self.date_label)
        date_hbox.addWidget(self.date_combobox)
        layout.addLayout(date_hbox)

        layout.addWidget(self.attachments_checkbox)
        #layout.addWidget(self.is_read_checkbox)
        layout.addWidget(self.read_status_label)
        layout.addWidget(self.read_status_combobox)
        layout.addLayout(self.folder_temp_layout)

        temp = QHBoxLayout()
        temp.addWidget(self.set_filter_button)
        temp.addWidget(self.reset_filter_button)
        layout.addLayout(temp)

        self.main_layout.addLayout(layout) 
        self.setLayout(self.main_layout)

    def relative_date_to_datetime(self,relative_date):
        current_date = datetime.now()
        units = relative_date.split()
        amount = int(units[0])
        unit = units[1]

        if unit.startswith('day'):
            delta = timedelta(days=amount)
        elif unit.startswith('week'):
            delta = timedelta(weeks=amount)
        elif unit.startswith('month'):
            delta = timedelta(days=30 * amount)
        elif unit.startswith('year'):
            delta = timedelta(days=365 * amount)
        else:
            raise ValueError("Unsupported time unit")

        past_date = current_date - delta
        return past_date

    def on_folder_selected(self, folder: Folder):
        if self.folder_widget:
            self.folder = folder
            self.folder_widget.setVisible(False)
            self.folder_widget.deleteLater() 
            self.folder_widget = None
            self.resize(self.width() - 200, self.height())

            label = QLabel(f"Folder: {folder.name}")
            self.folder_temp_layout.addWidget(label)

    def on_select_folder(self):
        if self.folder_widget is None:
            self.folder_widget = QWidget()  

            folder_area = FolderArea()  
            folder_area.add_folders(self.folders)
            folder_area.folder_selected.connect(self.on_folder_selected)

            self.folder_widget.setLayout(folder_area)
            self.main_layout.addWidget(self.folder_widget)  
            self.resize(self.width() + 200, self.height())
            self.folder_widget.setVisible(True)

    def on_set_filter(self):
        read = self.read_status_combobox.currentText()
        val = None
        if read == 'All':
            self.is_read_checkbox = None
        elif read == 'Read':
            val = True
        elif read == 'Unread':
            val = False

        filter_obj = Filter(before_date=None, 
                            after_date=self.relative_date_to_datetime(self.date_combobox.currentText()),
                            from_email=self.from_input.text(), 
                            to_email=self.to_input.text(), 
                            is_read=val,
                            has_attachment=self.attachments_checkbox.isChecked(),
                            contains=self.contains_input.text(), 
                            not_contains=self.not_contains_input.text(),
                            folder=self.folder)
        
        self.filter_signal.emit(filter_obj)

    def on_reset_filter(self):
        self.from_input.setText('')
        self.to_input.setText('')
        self.subject_input.setText('')
        self.contains_input.setText('')
        self.not_contains_input.setText('')
        self.date_combobox.setCurrentIndex(0)
        self.attachments_checkbox.setChecked(False)
        self.read_status_combobox.setCurrentIndex(0)
        self.folder = Folder("","",[])
        self.folder_widget = None
        self.filter_signal.emit(None)

    def window_settings(self):
        self.setWindowTitle("Create filter")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 350, 350
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

