from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QVBoxLayout, QListWidgetItem, QFileDialog, QTextEdit, QColorDialog, QFontDialog, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QTextListFormat
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

        # Underline
        underline_action = QAction(QIcon("Images\\underline.png"), "Underline", self)
        underline_action.setShortcut(Qt.CTRL + Qt.Key_U)
        underline_action.setStatusTip("Underline")
        underline_action.setCheckable(True)
        underline_action.triggered.connect(self.toggle_underline)
        formatting_toolbar.addAction(underline_action)
        underline_button = formatting_toolbar.widgetForAction(underline_action)
        underline_button.setObjectName("toolbar_button")

        # Text Color
        text_color_action = QAction(QIcon("Images\\text_color.png"), "Text Color", self)
        text_color_action.setStatusTip("Change Text Color")
        text_color_action.triggered.connect(self.change_text_color)
        formatting_toolbar.addAction(text_color_action)
        text_color_button = formatting_toolbar.widgetForAction(text_color_action)
        text_color_button.setObjectName("toolbar_button")

        # Font Type
        font_type_action = QAction("Font", self)
        font_type_action.setStatusTip("Change Font Type")
        font_type_action.triggered.connect(self.change_font)
        formatting_toolbar.addAction(font_type_action)
        font_type_button = formatting_toolbar.widgetForAction(font_type_action)
        font_type_button.setObjectName("toolbar_button")

        # Text Highlight
        text_highlight_action = QAction(QIcon("Images\\highlight.png"), "Highlight Text", self)
        text_highlight_action.triggered.connect(self.highlight_text)
        formatting_toolbar.addAction(text_highlight_action)
        text_highlight_button = formatting_toolbar.widgetForAction(text_highlight_action)
        text_highlight_button.setObjectName("toolbar_button")

        # Bullet List
        bullet_list_action = QAction(QIcon("Images\\bullet_list.png"), "Bullet List", self)
        bullet_list_action.triggered.connect(self.insert_bullet_list)
        formatting_toolbar.addAction(bullet_list_action)
        bullet_list_button = formatting_toolbar.widgetForAction(bullet_list_action)
        bullet_list_button.setObjectName("toolbar_button")

        #Decrease font size
        decrease_font_action = QAction(QIcon("Images\\down.svg"), "Decrease Font Size", self)
        decrease_font_action.setShortcut(Qt.CTRL + Qt.Key_Minus)
        decrease_font_action.setStatusTip("Decrease Font Size")
        decrease_font_action.triggered.connect(self.decrease_font_size)
        formatting_toolbar.addAction(decrease_font_action)
        decrease_font_button = formatting_toolbar.widgetForAction(decrease_font_action)
        decrease_font_button.setObjectName("toolbar_button")

        #Display font size
        self.font_size_label = QLabel("-12-") 
        formatting_toolbar.addWidget(self.font_size_label)
        self.mail_body_edit.currentCharFormatChanged.connect(self.update_font_size_display)
        
        #Increase font size
        increase_font_action = QAction(QIcon("Images\\up.svg"), "Increase Font Size", self)
        increase_font_action.setShortcut(Qt.CTRL + Qt.Key_Plus)
        increase_font_action.setStatusTip("Increase Font Size")
        increase_font_action.triggered.connect(self.increase_font_size)
        formatting_toolbar.addAction(increase_font_action)
        increase_font_button = formatting_toolbar.widgetForAction(increase_font_action)
        increase_font_button.setObjectName("toolbar_button")

        #Add attachment
        add_attachment_action = QAction(QIcon("Images\\attachment.png"),"Add Attachments", self)
        increase_font_action.setStatusTip("Add Attachments")
        add_attachment_action.triggered.connect(self.add_attachments)
        formatting_toolbar.addAction(add_attachment_action)
        add_attachment_button = formatting_toolbar.widgetForAction(add_attachment_action)
        add_attachment_button.setObjectName("toolbar_button")
        self.addWidget(formatting_toolbar)

        #Insert Image
        insert_image_action = QAction(QIcon("Images\\insert_image.png"), "Insert Image", self)
        insert_image_action.setStatusTip("Insert Image")
        insert_image_action.triggered.connect(self.insert_image)
        formatting_toolbar.addAction(insert_image_action)
        insert_image_action = formatting_toolbar.widgetForAction(insert_image_action)
        insert_image_action.setObjectName("toolbar_button")

        # Insert Hyperlink
        insert_hyperlink_action = QAction(QIcon("Images\\insert_hyperlink.png"), "Insert Hyperlink", self)
        insert_hyperlink_action.setStatusTip("Insert Hyperlink")
        insert_hyperlink_action.triggered.connect(self.insert_hyperlink)
        formatting_toolbar.addAction(insert_hyperlink_action)
        insert_hyperlink_action = formatting_toolbar.widgetForAction(insert_hyperlink_action)
        insert_hyperlink_action.setObjectName("toolbar_button")

    def insert_bullet_list(self):
        cursor = self.mail_body_edit.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)

    def highlight_text(self):
        color = QColorDialog.getColor(Qt.yellow, None)
        if color.isValid():
            self.mail_body_edit.setTextBackgroundColor(color)

    def insert_image(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            image_html = f'<img src="{file_name}" alt="Image">'
            self.mail_body_edit.textCursor().insertHtml(image_html)

    def insert_hyperlink(self):
        text, ok = QInputDialog.getText(None, "Insert Hyperlink", "Enter URL:")
        if ok and text:
            link_html = f'<a href="{text}">{text}</a>'
            self.mail_body_edit.textCursor().insertHtml(link_html)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.mail_body_edit.font(), None)
        if ok:
            self.mail_body_edit.setCurrentFont(font)
            self.font_size_label.setText(f"-{font.pointSize()}-")
  
    def update_font_size_display(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        self.font_size_label.setText(f"-{current_size}-")

    def increase_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        if current_size >= 72:
            return
        new_size = current_size + 1
        current_font.setPointSize(new_size)
        self.mail_body_edit.setCurrentFont(current_font)
        self.font_size_label.setText(f"-{new_size}-")

    def toggle_underline(self):
        self.mail_body_edit.setFontUnderline(not self.mail_body_edit.fontUnderline())

    def change_text_color(self):
        color = QColorDialog.getColor(self.mail_body_edit.textColor(), None)
        if color.isValid():
            self.mail_body_edit.setTextColor(color)

    def decrease_font_size(self):
        current_font = self.mail_body_edit.currentFont()
        current_size = current_font.pointSize()
        if current_size <= 1:
            return
        new_size = max(1, current_size - 1)
        current_font.setPointSize(new_size)
        self.mail_body_edit.setCurrentFont(current_font)
        self.font_size_label.setText(f"-{new_size}-")

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