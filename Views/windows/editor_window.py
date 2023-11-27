from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDesktopWidget, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton
from EmailService.models import Email, Contact

from Views.components.editor_window_components.toolbar import Toolbar
from Views.components.editor_window_components.email_processing import EditorEmailProcessing    
from Views.components.editor_window_components.recipient_line import RecipientLine

class EditorWindow(QWidget):
    mail_signal_from_editor = pyqtSignal(Email, str)
    open_attachment_signal = pyqtSignal(dict)

    def __init__(self, draft_email: Email = None, contacts: list[Contact] = []):
        super().__init__()
        self.window_settings()
        self.setup_ui()
        self.update_window(draft_email, contacts)

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.recipient_label = QLabel("Recipient(s)")
        self.main_layout.addWidget(self.recipient_label)
        self.recipient_line_edit = RecipientLine()
        self.main_layout.addWidget(self.recipient_line_edit)
        self.subject_label = QLabel("Subject")
        self.main_layout.addWidget(self.subject_label)
        self.subject_line_edit = QLineEdit()
        self.main_layout.addWidget(self.subject_line_edit)
        self.mail_body_edit = QTextEdit()
        self.main_layout.addWidget(self.mail_body_edit)
        self.attachments_list = QListWidget()
        self.attachments_list.setStyleSheet("QListWidget { border: none; }")
        self.attachments_list.setFixedHeight(1)
        self.attachments_list.itemClicked.connect(self.on_attachment_clicked)  # Connect the signal
        self.main_layout.addWidget(self.attachments_list)
        self.email_processing = EditorEmailProcessing(self.recipient_line_edit, self.subject_line_edit, self.mail_body_edit, self.attachments_list)
        self.email_processing.mail_signal_from_editor.connect(self.mail_signal_from_editor)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.email_processing.send_email)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.email_processing.save_email)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.send_button,4)
        self.button_layout.addWidget(self.save_button,1)
        self.main_layout.addLayout(self.button_layout)
        self.toolbar = Toolbar(self.mail_body_edit)
        self.toolbar.add_attachment.connect(self.add_attachment)
        self.main_layout.addLayout(self.toolbar)
        self.setLayout(self.main_layout)

    def update_window(self, draft_email: Email = None, contacts: list[Contact] = []):
        self.recipient_line_edit.init(draft_email, contacts)
        if draft_email:
            self.subject_line_edit.setText(draft_email.subject)
            self.mail_body_edit.setHtml(draft_email.body)
            self.attachments_list.clear()
            for attachment in draft_email.attachments:
                file_name = attachment.get('file_name')
                item = QListWidgetItem(file_name)
                item.setData(Qt.UserRole, file_name) 
                self.add_attachment(item)
        self.email_processing.update(draft_email, self.recipient_line_edit, self.subject_line_edit, self.mail_body_edit, self.attachments_list)

    def on_attachment_clicked(self, item):
        file_path = item.data(Qt.UserRole)  
        attachment = self.email_processing.generate_attachment_dict(file_path)
        self.open_attachment_signal.emit(attachment)

    def add_attachment(self, item):
        self.attachments_list.addItem(item)
        item_height = 20
        total_height = item_height * self.attachments_list.count() + 5
        if total_height > 200:
            total_height = 200
        self.attachments_list.setFixedHeight(total_height)

    def window_settings(self):
        self.setWindowTitle("Editor")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)