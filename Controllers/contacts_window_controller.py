from PyQt5.QtWidgets import QWidget
from Views.windows.contact_window import ContactWindow
from EmailService.models.email_client import EmailClient

class ContactsWindowController(QWidget):
    def __init__(self, email_client: EmailClient):
        super().__init__()
        self.email_client = email_client
        self.contacts = email_client.get_contacts()
        self.contact_window = ContactWindow()
        self.setup_connections()
        self.add_contacts(self.contacts)
        
    def setup_connections(self):
        self.contact_window.add_contact_signal.connect(self.add_contact)
        self.contact_window.delete_contact_signal.connect(self.delete_contact)
        self.contact_window.update_contact_signal.connect(self.update_contact)

    def add_contact(self, contact):
        contact = self.email_client.add_contact(contact)
        self.contacts.append(contact)
        self.contact_window.add_contacts(self.contacts)
    
    def delete_contact(self, contact):
        print(contact)
        self.email_client.delete_contact(contact)
    
    def update_contact(self, contact):
        contact = self.email_client.update_contact(contact)

    def add_contacts(self, contacts):
        self.contacts = contacts
        self.contact_window.add_contacts(contacts)

    def show_contacts(self):
        self.contact_window.show()