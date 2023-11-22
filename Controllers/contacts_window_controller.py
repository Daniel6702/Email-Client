from PyQt5.QtWidgets import QWidget
from Views.windows.contact_window import ContactWindow

class ContactsWindowController(QWidget):
    def __init__(self):
        super().__init__()
        self.contact_window = ContactWindow()

    def show_contacts(self):
        self.contact_window.show()