from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QVBoxLayout, QListWidgetItem, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os

class Toolbar(QVBoxLayout):
    add_attachment = pyqtSignal(QListWidgetItem)
    def __init__(self, mail_body_edit: QTextEdit):
        super().__init__()
        self.mail_body_edit = mail_body_edit
        formatting_toolbar = QToolBar(None)
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
        self.addWidget(formatting_toolbar)
  
    def update_font_size_display(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        self.font_size_label.setText(f"Font Size: {current_size}")

    def increase_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        if current_size >= 72:
            return
        new_size = current_size + 1
        current_font.setPointSize(new_size)
        self.mail_body_edit.setCurrentFont(current_font)
        self.font_size_label.setText(f"Font Size: {new_size}")

    def decrease_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        if current_size <= 1:
            return
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
        file_names, _ = QFileDialog.getOpenFileNames(None, "Select Attachment(s)", "", "All Files (*)", options=options)
        
        if file_names:
            for file_path in file_names:
                file_name = os.path.basename(file_path)
                item = QListWidgetItem(file_name)
                item.setData(Qt.UserRole, file_path) 
                self.add_attachment.emit(item)

    def toggle_italic(self):
        self.mail_body_edit.setFontItalic(not self.mail_body_edit.fontItalic())