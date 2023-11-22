'''
from EmailService.models import EmailClient, Email, Folder, Filter, User
from EmailService.factories import GmailServiceFactory, OutlookServiceFactory, TestServiceFactory
import logging
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from Views.windows import EditorWindow, LoginWindow, MainWindow, FilterWindow, FolderWindow, AttachmentWindow, SettingsWindow, ContactWindow
from Views.styles.style_manager import StyleManager

#util
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


PAGE_SIZE = 5


class MainWindowController(QObject):
    open_editor_window = pyqtSignal(object)
    open_settings_window = pyqtSignal()
    open_filter_window = pyqtSignal(object)
    open_attachment_window = pyqtSignal(dict)
    open_folder_selector_window = pyqtSignal(object)
    open_contacts_window = pyqtSignal()
    def __init__(self, email_client: EmailClient):
        self.window = MainWindow()
        self.email_client = email_client
        self.folders = self.email_client.get_folders()
        self.setup_connections()

    def setup_connections(self):
        self.window.folder_area.folder_selected.connect(self.on_folder_selected)
        self.window.email_list_area.email_clicked.connect(self.on_email_clicked)
        self.window.email_list_area.mark_email_as.connect(self.on_mark_email_as)
        self.window.email_list_area.email_deleted.connect(self.on_email_delete)
        self.window.email_list_area.new_page.connect(self.on_new_page)
        self.window.search_area.search_signal.connect(self.on_search)
        self.window.search_area.new_mail_signal.connect(self.open_editor_window.emit)
        self.window.search_area.open_settings_signal.connect(self.open_settings_window.emit)
        self.window.search_area.open_filter_signal.connect(lambda: self.open_filter_window.emit(self.folders))
        self.window.email_view_area.delete_email_signal.connect(self.on_email_delete)
        self.window.email_view_area.open_attachment_window.connect(self.open_attachment_window.emit)
        self.window.email_view_area.open_email_editor_window.connect(self.open_editor_window.emit)
        self.window.email_view_area.mark_email_as.connect(self.on_mark_email_as)
        self.window.email_view_area.open_folder_window.connect(lambda: self.open_folder_selector_window.emit(self.folders))
        self.window.email_view_area.move_email_to_folder.connect(self.move_email_to_folder)
        self.window.search_area.open_contacts_signal.connect(self.open_contacts_window.emit)

    def set_filter(self, filter: Filter):
        self.window.search_area.set_filter(filter)

    def on_folder_selected_from_folder_selector_window(self, folder: Folder):
        self.window.email_view_area.selected_folder.emit(folder)

    def on_folder_selected(self, folder: Folder):
        logging.info(f"Folder Selected: {folder.name}")
        self.current_folder = folder
        self.window.email_list_area.current_page = 1
        emails = self.email_client.get_mails(folder, "", PAGE_SIZE)
        self.window.email_list_area.add_emails_to_list(emails)

    def on_email_clicked(self, mail: Email):
        logging.info(f"Email Selected: {mail.subject}")
        if is_draft_folder(self.current_folder):
            self.open_editor_window.emit(mail)
        else:
            self.window.email_view_area.updateEmailView(mail)

    def on_mark_email_as(self, email: Email, is_read: bool):
        self.email_client.mark_email_as(email, is_read)
        self.window.email_list_area.mark_as_func(email, is_read)

    def on_email_delete(self, email: Email):
        empty_mail = Email(from_email="",to_email="",subject="",body="Select an email to view it here",datetime_info={},attachments=[], id="")
        self.window.email_view_area.updateEmailView(empty_mail)
        self.window.email_list_area.remove_email_from_list(email)
        if is_delete_folder(self.current_folder):
            self.email_client.delete_mail(email)
        else:     
            delete_folder = next((folder for folder in self.folders if is_delete_folder(folder)), None)
            if delete_folder: 
                self.email_client.move_email_to_folder(self.current_folder, delete_folder, email)

    def on_new_page(self, page_number: int):
        emails = self.email_client.get_mails(folder=self.current_folder, query="", max_results=PAGE_SIZE, page_number=page_number)
        self.window.email_list_area.add_emails_to_list(emails)

    def on_search(self, search_criteria: str, filter: Filter = None):
        if not filter:
            mails = self.email_client.search(search_criteria, PAGE_SIZE)
        else:
            mails = self.email_client.search_filter(search_criteria, filter, PAGE_SIZE)
        self.window.email_list_area.add_emails_to_list(mails)

    def move_email_to_folder(self, email: Email, folder: Folder):
        self.email_client.move_email_to_folder(email.folder, folder, email)
        if email.folder is not self.current_folder:
            self.window.email_list_area.remove_email_from_list(email)



class MainWindowController2():
    def __init__(self, main_window, email_client: EmailClient):
        self.main_window = main_window
        self.email_client = email_client
        self.setup_connections()
        self.current_folder = None
        self.folders = self.email_client.get_folders()
        self.delete_folder = self.get_delete_folder(self.folders)
        self.main_window.folder_area.add_folders(self.folders)
        
    def setup_connections(self):
        self.main_window.folder_area.folder_selected.connect(self.on_folder_selected)
        self.main_window.email_list_area.email_clicked.connect(self.on_email_clicked)
        self.main_window.email_list_area.mark_email_as.connect(self.on_mark_email_as)
        self.main_window.email_list_area.email_deleted.connect(self.on_email_delete)
        self.main_window.email_list_area.new_page.connect(self.on_new_page)

        self.main_window.search_area.search_signal.connect(self.on_search)
        self.main_window.search_area.new_mail_signal.connect(self.main_window.open_editor_window.emit)
        self.main_window.search_area.open_settings_signal.connect(self.main_window.open_settings_window.emit)
        self.main_window.search_area.open_filter_signal.connect(self.open_filter)

        self.main_window.email_view_area.delete_email_signal.connect(self.on_email_delete)
        self.main_window.email_view_area.open_attachment_window.connect(self.main_window.open_attachment_window.emit)
        self.main_window.email_view_area.open_email_editor_window.connect(self.main_window.open_editor_window.emit)
        self.main_window.email_view_area.mark_email_as.connect(self.on_mark_email_as)
        self.main_window.email_view_area.open_folder_window.connect(self.open_folder_selector)
        self.main_window.email_view_area.move_email_to_folder.connect(self.move_email_to_folder)
        self.main_window.folder_selected.connect(self.main_window.email_view_area.selected_folder.emit)
        self.main_window.get_email_from_editor.connect(self.get_mail_from_editor)
        self.main_window.search_area.open_contacts_signal.connect(self.main_window.open_contacts_window.emit)

    def open_filter(self):
        self.main_window.open_filter_window.emit(self.folders)

    def on_new_page(self, page_number: int):
        emails = self.email_client.get_mails(folder=self.current_folder, query="", max_results=PAGE_SIZE, page_number=page_number)
        self.main_window.email_list_area.add_emails_to_list(emails)

    def move_email_to_folder(self, email: Email, folder: Folder):
        self.email_client.move_email_to_folder(email.folder, folder, email)
        if email.folder is not self.current_folder:
            self.main_window.email_list_area.remove_email_from_list(email)

    def open_folder_selector(self):
        self.main_window.open_folder_selector_window.emit(self.folders)

    def on_folder_selected(self, folder: Folder):
        logging.info(f"Folder Selected: {folder.name}")
        self.current_folder = folder
        self.main_window.email_list_area.current_page = 1
        logging.info(f"Retrieving {PAGE_SIZE} emails from {folder.id}")
        emails = self.email_client.get_mails(folder, "", PAGE_SIZE)
        self.main_window.email_list_area.add_emails_to_list(emails)

    def on_search(self, search_criteria: str, filter: Filter = None):
        if not filter:
            mails = self.email_client.search(search_criteria, PAGE_SIZE)
        else:
            mails = self.email_client.search_filter(search_criteria, filter, PAGE_SIZE)
        self.main_window.email_list_area.add_emails_to_list(mails)

    def get_delete_folder(self, folders: list[Folder]):
        for folder in folders:
            if folder.name in ["Delete", "Delete", "DELETE", "delete", "DELETED", "deleted", "Deleted", "trash", "Trash", "TRASH", "bin", "Bin", "BIN", "Deleted Items"]:
                return folder
            else:
                pass

    def on_mark_email_as(self, email: Email, is_read: bool):
        self.email_client.mark_email_as(email, is_read)
        self.main_window.email_list_area.mark_as_func(email, is_read)

    def on_email_delete(self, email: Email):
        empty_mail = Email(from_email="",to_email="",subject="",body="Select an email to view it here",datetime_info={},attachments=[], id="")
        self.main_window.email_view_area.updateEmailView(empty_mail)
        self.main_window.email_list_area.remove_email_from_list(email)
        if self.current_folder is self.delete_folder:
            self.email_client.delete_mail(email)
        else:
            self.email_client.move_email_to_folder(self.current_folder, self.delete_folder, email)

    def on_email_clicked(self,mail: Email):
        logging.info(f"Email Selected: {mail.subject}")
        if self.current_folder.name in ["Drafts", "Draft", "DRAFT", "draft", "DRAFTS", "drafts"]:
            self.main_window.open_editor_window.emit(mail)
        else:
           self.main_window.email_view_area.updateEmailView(mail)
    
    def get_mail_from_editor(self,email: Email, action: str):
        if action == "send":
            respone = self.email_client.send_mail(email)
            if respone is False:
                self.main_window.show_warning_signal.emit("Error", "Email not sent", "likely invalid email address")
        elif action == "save":
            self.email_client.save_draft(email)
        elif action == "update":
            self.email_client.update_draft(email)
    
    '''