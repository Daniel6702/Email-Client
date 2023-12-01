from PyQt5.QtWidgets import QLineEdit, QCompleter
from PyQt5.QtCore import Qt, QModelIndex, QStringListModel
from EmailService.models import Email, Contact

class RecipientLine(QLineEdit):
    def __init__(self, ):
        super().__init__()

    def init(self,draft: Email = None, contacts: list[Contact] = []):
        self.contacts = contacts
        self.init_completer() 
        if draft and isinstance(draft.to_email, list):
            self.setText(", ".join(draft.to_email))
        elif draft and isinstance(draft.to_email, str):
            self.setText(draft.to_email)
        elif not draft:
            self.setText('')
        
    def init_completer(self):
        contact_strings = [contact.display_text() for contact in self.contacts]
        completer = MultiEmailCompleter(self)
        completer.setModel(QStringListModel(contact_strings))
        self.setCompleter(completer)

    def get_email_addresses(self) -> list[str]:
        text = self.text()
        parts = text.split(',')
        email_addresses = []

        for part in parts:
            part = part.strip() 
            if '<' in part and '>' in part:
                start = part.find('<') + 1
                end = part.find('>')
                email = part[start:end].strip()
            else:
                email = part

            if email:  
                email_addresses.append(email)

        return email_addresses
    
class MultiEmailCompleter(QCompleter):
    def __init__(self, parent=None):
        super(MultiEmailCompleter, self).__init__(parent)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.popup().setObjectName("completer")

    def splitPath(self, path):
        path = path.split(',')[-1].strip()
        return [path]

    def pathFromIndex(self, index: QModelIndex):
        text = self.model().data(index, Qt.EditRole)

        old_text = self.widget().text()
        last_comma = old_text.rfind(',')
        if last_comma == -1:
            return text
        return old_text[:last_comma + 1] + ' ' + text