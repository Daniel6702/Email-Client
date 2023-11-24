from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QDialog, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from EmailService.models import Contact

class ContactWindow(QWidget):
    add_contact_signal = pyqtSignal(Contact)
    delete_contact_signal = pyqtSignal(Contact) 
    update_contact_signal = pyqtSignal(Contact)

    def __init__(self):
        super().__init__()
        self.contacts = []
        self.contact_map = {} 
        self.window_settings()
        self.setup_layout()

    def window_settings(self):
        self.setWindowTitle('Contact Manager')
        self.setGeometry(300, 300, 600, 400)

    def setup_layout(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        add_contact_button = QPushButton("Add Contact")
        add_contact_button.clicked.connect(self.show_contact_form)
        delete_contact_button = QPushButton("Delete Contact")
        delete_contact_button.clicked.connect(self.delete_contact)
        update_contact_button = QPushButton("Update Contact")
        update_contact_button.clicked.connect(self.show_update_form)

        top_layout.addWidget(add_contact_button)
        top_layout.addWidget(delete_contact_button)
        top_layout.addWidget(update_contact_button)
        main_layout.addLayout(top_layout)

        self.contacts_list = QListWidget()
        main_layout.addWidget(self.contacts_list)

        self.setLayout(main_layout)

    def show_contact_form(self, update=False):
        self.contact_dialog = ContactDialog(update)
        self.contact_dialog.accepted.connect(self.add_or_update_contact)
        self.contact_dialog.show()

    def add_contacts(self, contacts):
        self.contacts = contacts
        self.contacts_list.clear()
        self.contact_map.clear()  # Clear existing map entries
        for contact in contacts:
            item_text = f"{contact.name}\n{contact.email}\n----------------------------------"
            self.contacts_list.addItem(item_text)
            self.contact_map[item_text] = contact  # Map the item text to the Contact object

    def add_or_update_contact(self):
        contact_info = self.contact_dialog.get_contact_info()

        if self.contact_dialog.is_update:
            selected_item = self.contacts_list.currentItem()
            if selected_item:
                original_text = selected_item.text()
                original_contact = self.contact_map.get(original_text)

                # Update contact with new details but keep the same resource_name
                updated_contact = Contact(
                    name=contact_info.name, 
                    email=contact_info.email, 
                    resource_name=original_contact.resource_name if original_contact else ''
                )
                
                self.update_contact_signal.emit(updated_contact)
                
                # Update list item and mapping
                updated_item_text = f"{updated_contact.name}\n{updated_contact.email}\n----------------------------------"
                selected_item.setText(updated_item_text)
                self.contact_map[updated_item_text] = updated_contact
                if original_text in self.contact_map:
                    del self.contact_map[original_text]
        else:
            new_contact = Contact(name=contact_info.name, email=contact_info.email)
            self.add_contact_signal.emit(new_contact)
            new_item_text = f"{new_contact.name}\n{new_contact.email}\n----------------------------------"
            self.contacts_list.addItem(new_item_text)
            self.contact_map[new_item_text] = new_contact

        self.contact_dialog.close()

    def show_update_form(self):
        selected_items = self.contacts_list.selectedItems()
        if selected_items:
            self.show_contact_form(update=True)

    def delete_contact(self):
        print("1")
        selected_items = self.contacts_list.selectedItems()
        if selected_items:
            print("2")
            selected_contact_name = selected_items[0].text().split('\n')[0]
            for contact in self.contacts:
                if contact.name == selected_contact_name:
                    print("3")
                    self.contacts.remove(contact)
                    self.delete_contact_signal.emit(contact)
                    self.contacts_list.takeItem(self.contacts_list.row(selected_items[0]))
                    break

class ContactDialog(QDialog):
    def __init__(self, is_update):
        super().__init__()
        self.is_update = is_update
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Update Contact" if self.is_update else "Add Contact")
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

    def get_contact_info(self):
        return Contact(name=self.name_input.text(), email=self.email_input.text())

    def window_settings(self):
        self.setWindowTitle("Contacts")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)