from PyQt5.QtWidgets import QWidget
from Views.windows.attachment_window import AttachmentWindow

class AttachmentWindowController(QWidget):
    def __init__(self):
        super().__init__()
        self.attachment_window = AttachmentWindow()

    def show_attachment(self, attachment: dict):
        self.attachment_window = AttachmentWindow()
        self.attachment_window.add_attachment(attachment)
        self.attachment_window.show()