from PyQt5.QtWidgets import QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from email_util import Email, print_email
from datetime import datetime
import os




class EditorWindow(QWidget):
    mail_signal_from_editor = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initial_layout()

        # Main layout
        main_layout = QVBoxLayout()

        # Recipient line
        recipient_label = QLabel("Modtagere")
        self.recipient_line_edit = QLineEdit()
        main_layout.addWidget(recipient_label)
        main_layout.addWidget(self.recipient_line_edit)

        # Subject line
        subject_label = QLabel("Emne")
        self.subject_line_edit = QLineEdit()
        main_layout.addWidget(subject_label)
        main_layout.addWidget(self.subject_line_edit)

        # Mail body
        self.mail_body_edit = QTextEdit()
        main_layout.addWidget(self.mail_body_edit)

        # Attachments list
        self.attachments_list = QListWidget()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        main_layout.addWidget(self.attachments_list)

        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_email)
        main_layout.addWidget(send_button)

        '''Toolbar'''
        formatting_toolbar = QToolBar(self)
        formatting_toolbar.layout().setSpacing(10)
        #Font settings
        default_font = QFont()
        default_font.setPointSize(12)
        self.mail_body_edit.setFont(default_font)
        self.mail_body_edit.document().setDefaultFont(default_font)

        #Bold
        bold_action = QAction(QIcon("Images\\bold.png"), "Bold", self)
        bold_action.setShortcut(Qt.CTRL + Qt.Key_B)
        bold_action.setStatusTip("Bold")
        bold_action.setCheckable(True)
        bold_action.triggered.connect(self.toggle_bold)
        formatting_toolbar.addAction(bold_action)
        bold_button = formatting_toolbar.widgetForAction(bold_action)
        bold_button.setObjectName("toolbar_button")

        #Italic
        italic_action = QAction(QIcon("Images\\italic.png"), "Italic", self)
        italic_action.setShortcut(Qt.CTRL + Qt.Key_I)
        italic_action.setStatusTip("Italic")
        italic_action.setCheckable(True)
        italic_action.triggered.connect(self.toggle_italic)
        formatting_toolbar.addAction(italic_action)
        italic_button = formatting_toolbar.widgetForAction(italic_action)
        italic_button.setObjectName("toolbar_button")

        #Decrease font size
        decrease_font_action = QAction(QIcon("Images\\down.svg"), "Decrease Font Size", self)
        decrease_font_action.setShortcut(Qt.CTRL + Qt.Key_Minus)
        decrease_font_action.setStatusTip("Decrease Font Size")
        decrease_font_action.triggered.connect(self.decrease_font_size)
        formatting_toolbar.addAction(decrease_font_action)
        decrease_font_button = formatting_toolbar.widgetForAction(decrease_font_action)
        decrease_font_button.setObjectName("toolbar_button")
        
        #Increase font size
        increase_font_action = QAction(QIcon("Images\\up.svg"), "Increase Font Size", self)
        increase_font_action.setShortcut(Qt.CTRL + Qt.Key_Plus)
        increase_font_action.setStatusTip("Increase Font Size")
        increase_font_action.triggered.connect(self.increase_font_size)
        formatting_toolbar.addAction(increase_font_action)
        increase_font_button = formatting_toolbar.widgetForAction(increase_font_action)
        increase_font_button.setObjectName("toolbar_button")

        #Display font size
        self.font_size_label = QLabel("Font Size: 12") 
        formatting_toolbar.addWidget(self.font_size_label)
        self.mail_body_edit.currentCharFormatChanged.connect(self.update_font_size_display)

        #Add attachment
        add_attachment_action = QAction(QIcon("Images\\attachment.png"),"Add Attachments", self)
        increase_font_action.setStatusTip("Add Attachments")
        add_attachment_action.triggered.connect(self.add_attachments)
        formatting_toolbar.addAction(add_attachment_action)
        add_attachment_button = formatting_toolbar.widgetForAction(add_attachment_action)
        add_attachment_button.setObjectName("toolbar_button")

        main_layout.addWidget(formatting_toolbar)
        self.setLayout(main_layout)

    def update_font_size_display(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        self.font_size_label.setText(f"Font Size: {current_size}")

    def increase_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        new_size = current_size + 1
        current_font.setPointSize(new_size)
        self.mail_body_edit.setCurrentFont(current_font)
        self.font_size_label.setText(f"Font Size: {new_size}")

    def decrease_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        new_size = max(1, current_size - 1)
        current_font.setPointSize(new_size)
        self.mail_body_edit.setCurrentFont(current_font)
        self.font_size_label.setText(f"Font Size: {new_size}")

    def toggle_bold(self):
        if self.mail_body_edit.fontWeight() != QFont.Bold:
            self.mail_body_edit.setFontWeight(QFont.Bold)
        else:
            self.mail_body_edit.setFontWeight(QFont.Normal)

    def add_attachments(self):
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Attachment(s)", "", "All Files (*)", options=options)
        
        if file_names:
            for file_path in file_names:
                file_name = os.path.basename(file_path)
                item = QListWidgetItem(file_name)
                item.setData(Qt.UserRole, file_path) 
                self.attachments_list.addItem(item)

            item_height = 18
            total_height = item_height * self.attachments_list.count()
            self.attachments_list.setFixedHeight(total_height)

    def toggle_italic(self):
        self.mail_body_edit.setFontItalic(not self.mail_body_edit.fontItalic())

    def initial_layout(self):
        self.setWindowTitle("Editor")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

    def get_attachment_paths(self):
        paths = []
        for index in range(self.attachments_list.count()):
            item = self.attachments_list.item(index)
            file_path = item.data(Qt.UserRole)
            paths.append(file_path)
        return paths
    
    def generate_attachment_dict(self,file_path): 
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as file:
            file_data = file.read()

        file_name = os.path.basename(file_path)

        attachment_dict = {
            'file_data': file_data,
            'file_name': file_name,
        }
        return attachment_dict
    
    def generate_email(self):
        recipients = self.recipient_line_edit.text().split(",")
        subject = self.subject_line_edit.text()
        body_html = self.mail_body_edit.toHtml()
        attachments_paths = self.get_attachment_paths()
        attachments = []
        for file_path in attachments_paths:
            attachment_dict = self.generate_attachment_dict(file_path)
            attachments.append(attachment_dict)
        email = Email(from_email="me",
                      to_email=recipients,
                      subject=subject,
                      body=body_html,
                      datetime_info = {'date': str(datetime.now().date()),
                                        'time': str(datetime.now().time())},
                      attachments=attachments)
        return email
    
    def save_email(self):
        email = self.generate_email()
        #email_util.save_email_to_file(email, "Drafts")
    
    def send_email(self):
        email = self.generate_email()
        self.mail_signal_from_editor.emit(email)
        