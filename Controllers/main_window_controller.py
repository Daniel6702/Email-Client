from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from Views.windows.main_window import MainWindow
from EmailService.models import Email, Filter, Folder
from EmailService.models.email_client import EmailClient   
import logging

PAGE_SIZE = 30
    
class MainWindowController(QWidget):
    open_editor_window = pyqtSignal(object)
    open_settings_window = pyqtSignal()
    open_filter_window = pyqtSignal(object)
    open_attachment_window = pyqtSignal(dict)
    open_folder_selector_window = pyqtSignal(object)
    open_contacts_window = pyqtSignal()
    open_popup_window = pyqtSignal(str, str, str, str, int)
    def __init__(self, email_client: EmailClient):
        super().__init__()
        self.main_window = MainWindow()
        self.email_client = email_client
        self.setup_connections()
        self.folders = self.email_client.get_folders()
        self.main_window.folder_area.add_folders(self.folders)
        
    def setup_connections(self):
        self.main_window.folder_area.folder_selected.connect(self.on_folder_selected)
        self.main_window.folder_area.add_folder_signal.connect(self.on_add_folder)
        self.main_window.folder_area.delete_folder_signal.connect(self.on_folder_delete)
        self.main_window.folder_area.edit_folder_signal.connect(self.on_folder_edit)
        self.main_window.email_list_area.email_clicked.connect(self.on_email_clicked)
        self.main_window.email_list_area.mark_email_as.connect(self.on_mark_email_as)
        self.main_window.email_list_area.email_deleted.connect(self.on_email_delete)
        self.main_window.email_list_area.new_page.connect(self.on_new_page)
        self.main_window.search_area.search_signal.connect(self.on_search)
        self.main_window.search_area.new_mail_signal.connect(self.open_editor_window.emit)
        self.main_window.search_area.open_settings_signal.connect(self.open_settings_window.emit)
        self.main_window.search_area.open_filter_signal.connect(lambda: self.open_filter_window.emit(self.folders))
        self.main_window.email_view_area.delete_email_signal.connect(self.on_email_delete)
        self.main_window.email_view_area.open_attachment_window.connect(self.open_attachment_window.emit)
        self.main_window.email_view_area.open_email_editor_window.connect(self.open_editor_window.emit)
        self.main_window.email_view_area.mark_email_as.connect(self.on_mark_email_as)
        self.main_window.email_view_area.open_folder_window.connect(lambda: self.open_folder_selector_window.emit(self.folders))
        self.main_window.email_view_area.move_email_to_folder.connect(self.move_email_to_folder)
        self.main_window.search_area.open_contacts_signal.connect(self.open_contacts_window.emit)

    def on_add_folder(self, folder: Folder):
        folder = self.email_client.create_folder(folder, None)
        self.folders.append(folder)
        self.main_window.folder_area.clear_folders()
        self.main_window.folder_area.add_folders(self.folders)

    def on_folder_delete(self, folder: Folder):
        self.email_client.delete_folder(folder)
        self.folders.remove(folder)
        self.main_window.folder_area.clear_folders()
        self.main_window.folder_area.add_folders(self.folders)

    def on_folder_edit(self, folder: Folder, new_folder_name: str):
        self.folders.remove(folder)
        folder = self.email_client.update_folder(folder, new_folder_name)
        self.folders.append(folder)
        self.main_window.folder_area.clear_folders()
        self.main_window.folder_area.add_folders(self.folders)
    
    def set_filter(self, filter: Filter):
        self.main_window.search_area.set_filter(filter)

    def on_folder_selected_from_folder_selector_window(self, folder: Folder):
        self.main_window.email_view_area.selected_folder.emit(folder)

    def on_folder_selected(self, folder: Folder):
        self.open_popup_window.emit("info", "Loading Emails", "Please wait while we load your emails", "THIS IS A TEST POPUP WINDOW", 4000)
        logging.info(f"Folder Selected: {folder.name}")
        self.current_folder = folder
        self.main_window.email_list_area.current_page = 1
        emails = self.email_client.get_mails(folder, "", PAGE_SIZE)
        accepted_emails, spam_emails = self.email_client.filter_emails(emails, [], [])
        print(spam_emails)
        self.main_window.email_list_area.add_emails_to_list(accepted_emails)

    def on_email_clicked(self, mail: Email):
        logging.info(f"Email Selected: {mail.subject}")
        if is_draft_folder(self.current_folder):
            self.open_editor_window.emit(mail)
        else:
            self.main_window.email_view_area.updateEmailView(mail)

    def on_mark_email_as(self, email: Email, is_read: bool):
        self.email_client.mark_email_as(email, is_read)
        self.main_window.email_list_area.mark_as_func(email, is_read)

    def on_email_delete(self, email: Email):
        empty_mail = Email(from_email="",to_email="",subject="",body="Select an email to view it here",datetime_info={},attachments=[], id="")
        self.main_window.email_view_area.updateEmailView(empty_mail)
        self.main_window.email_list_area.remove_email_from_list(email)
        if is_delete_folder(self.current_folder):
            self.email_client.delete_mail(email)
        else:     
            delete_folder = next((folder for folder in self.folders if is_delete_folder(folder)), None)
            if delete_folder: 
                self.email_client.move_email_to_folder(self.current_folder, delete_folder, email)

    def on_new_page(self, page_number: int):
        emails = self.email_client.get_mails(folder=self.current_folder, query="", max_results=PAGE_SIZE, page_number=page_number)
        if emails:
            self.main_window.email_list_area.add_emails_to_list(emails)
        else:
            self.main_window.email_list_area.current_page -= 1

    def on_search(self, search_criteria: str, filter: Filter = None):
        if filter.is_empty() and search_criteria:
            mails = self.email_client.search(search_criteria, PAGE_SIZE)
        elif filter.is_empty() and not search_criteria:
            mails = self.email_client.get_mails(folder=self.current_folder, query="", max_results=PAGE_SIZE, page_number=1)
            self.main_window.email_list_area.current_page = 1
        elif not filter.is_empty() and search_criteria:
            mails = self.email_client.search_filter(search_criteria, filter, PAGE_SIZE)
        elif not filter.is_empty() and not search_criteria:
            mails = self.email_client.filter(filter, PAGE_SIZE)
        else:
            mails = []
        self.main_window.email_list_area.add_emails_to_list(mails)

    def move_email_to_folder(self, email: Email, folder: Folder):
        self.email_client.move_email_to_folder(email.folder, folder, email)

        if folder.name is not self.current_folder.name:
            self.main_window.email_list_area.remove_email_from_list(email)

def is_delete_folder(folder: Folder) -> bool:
    if folder.name in ["Delete", "Delete", "DELETE", "delete", "DELETED", "deleted", "Deleted", "trash", "Trash", "TRASH", "bin", "Bin", "BIN", "Deleted Items"]:
        return True
    else:
        return False

def is_draft_folder(folder: Folder) -> bool:
    if folder.name in ["Drafts", "Draft", "DRAFT", "draft", "DRAFTS", "drafts"]:
        return True
    else:
        return False