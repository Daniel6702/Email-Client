from PyQt5.QtCore import pyqtSignal, Qt, QCoreApplication, QSize, QThread, QPoint
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QMovie
from Views.windows.main_window import MainWindow
from EmailService.models import Email, Filter, Folder
from EmailService.models.email_client import EmailClient   
import logging
import threading
import time

PAGE_SIZE = 10
    
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
        self.spam_folder = next((folder for folder in self.folders if is_spam_folder(folder)), None)
        self.inbox_folder = next((folder for folder in self.folders if is_inbox_folder(folder)), None)
        
    def setup_connections(self):
        self.main_window.folder_area.folder_selected.connect(self.on_folder_selected)
        self.main_window.folder_area.add_folder_signal.connect(self.on_add_folder)
        self.main_window.folder_area.delete_folder_signal.connect(self.on_folder_delete)
        self.main_window.folder_area.edit_folder_signal.connect(self.on_folder_edit)
        self.main_window.email_list_area.email_clicked.connect(self.on_email_clicked)
        self.main_window.email_list_area.mark_email_as.connect(self.on_mark_email_as)
        self.main_window.email_list_area.email_deleted.connect(self.on_email_delete)
        self.main_window.email_list_area.new_page.connect(self.on_new_page)
        self.main_window.email_list_area.refresh_signal.connect(self.refresh_cache)
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

    def refresh_cache(self):
        self.email_client.refresh_cache()
        self.retrieve_emails(self.current_folder, "", self.main_window.email_list_area.current_page, refresh=True)

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
        new_folder = self.email_client.update_folder(folder, new_folder_name)
        if new_folder is not None:
            self.folders.remove(folder)
            self.folders.append(new_folder)
            self.main_window.folder_area.clear_folders()
            self.main_window.folder_area.add_folders(self.folders)
    
    def set_filter(self, filter: Filter):
        self.main_window.search_area.set_filter(filter)

    def on_folder_selected_from_folder_selector_window(self, folder: Folder):
        self.main_window.email_view_area.selected_folder.emit(folder)

    def on_folder_selected(self, folder: Folder):
        self.current_folder = folder
        self.main_window.email_list_area.current_page = 1
        self.main_window.email_list_area.page_number_label.setText(f"Page {self.main_window.email_list_area.current_page}")
        self.retrieve_emails(folder, "", 1)

    def show_loading(self):
        self.loading_popup = LoadingPopup()
        self.main_window.setEnabled(False)
        self.loading_popup.show()

    def hide_loading(self):
        self.main_window.setEnabled(True)
        if self.loading_popup:
            self.loading_popup.close()

    def retrieve_emails(self, folder: Folder, query: str, page_number: int, refresh=False):
        self.show_loading()
        self.worker = EmailRetrievalThread(self.email_client, folder, query, page_number, refresh=refresh)
        self.worker.finished.connect(self.on_retrieval_finished)
        self.worker.start()

    def on_retrieval_finished(self, accepted_emails, spam_emails):
        self.hide_loading()
        if self.current_folder == self.spam_folder:
            self.main_window.email_list_area.add_emails_to_list(spam_emails)
        else:
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
            print("1")
            self.email_client.delete_mail(email)
        else:     
            print("2")
            delete_folder = next((folder for folder in self.folders if is_delete_folder(folder)), None)
            if delete_folder: 
                self.email_client.move_email_to_folder(self.current_folder, delete_folder, email)

    def on_new_page(self, page_number: int):
        self.show_loading()
        self.main_window.email_list_area.current_page = page_number
        self.worker = EmailRetrievalThread(self.email_client, self.current_folder, "", page_number)
        self.worker.finished.connect(self.on_new_page_finished)
        self.worker.start()

    def on_new_page_finished(self, accepted_emails, spam_emails):
        self.hide_loading()
        if accepted_emails:
            self.main_window.email_list_area.add_emails_to_list(accepted_emails)
        #elif self.main_window.email_list_area.current_page > 1:
        #    self.main_window.email_list_area.current_page -= 1
        for email in spam_emails:
            self.email_client.move_email_to_folder(self.current_folder, self.spam_folder, email)

    def on_search(self, search_criteria: str, filter: Filter = None):
        self.current_folder = self.inbox_folder
        self.show_loading()
        mode = 'search'
        if filter.is_empty() and search_criteria:
            mode = 'search'
        elif filter.is_empty() and not search_criteria:
            mode = 'get_mails'
            self.main_window.email_list_area.current_page = 1
        elif not filter.is_empty() and search_criteria:
            mode = 'search_filter'
        elif not filter.is_empty() and not search_criteria:
            mode = 'filter'

        self.worker = EmailRetrievalThread(self.email_client, self.current_folder, search_criteria, 1, mode, filter)
        self.worker.finished.connect(self.on_search_finished)
        self.worker.start()

    def on_search_finished(self, accepted_emails, spam_emails):
        self.hide_loading()
        self.main_window.email_list_area.add_emails_to_list(accepted_emails)
        self.main_window.email_list_area.current_page = 1
        for email in spam_emails:
            self.email_client.move_email_to_folder(self.current_folder, self.spam_folder, email)

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
    
def is_spam_folder(folder: Folder) -> bool:
    if folder.name in ["Spam", "Spam", "SPAM", "spam", "Junk", "JUNK", "junk", "Junk Email"]:
        return True
    else:
        return False
    
def is_inbox_folder(folder: Folder) -> bool:
    if folder.name in ["Inbox", "Inbox", "INBOX", "inbox"]:
        return True
    else:
        return False
    
class EmailRetrievalThread(QThread):
    finished = pyqtSignal(list, list)

    def __init__(self, email_client, folder, query, page_number, mode=None, filter=None, refresh=False):
        super().__init__()
        self.email_client = email_client
        self.folder = folder
        self.query = query
        self.page_number = page_number
        self.mode = mode
        self.filter = filter
        self.refresh = refresh

    def run(self):
        #if self.refresh: #dont ask
        #    time.sleep(0.25)
        if self.mode == 'search':
            emails = self.email_client.search(self.query, PAGE_SIZE)
        elif self.mode == 'search_filter':
            emails = self.email_client.search_filter(self.query, self.filter, PAGE_SIZE)
        elif self.mode == 'filter':
            emails = self.email_client.filter(self.filter, PAGE_SIZE)
        else:

            MAX_RETRIES = 4
            retry_delay = 0.75
            for attempt in range(MAX_RETRIES):
                try:
                    emails = self.email_client.get_mails(self.folder, self.query, PAGE_SIZE, self.page_number)
                    break  
                except ConnectionError as e:
                    print(f"Attempt {attempt+1} failed with error: {e}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2 
                    else:
                        raise  
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    raise 
                    
        accepted_emails, spam_emails = self.email_client.filter_emails(emails, [], [])
        self.finished.emit(accepted_emails, spam_emails)

class LoadingPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        gif_container = QWidget()
        gif_layout = QVBoxLayout(gif_container)
        gif_label = QLabel()
        movie = QMovie('Images\\loading.gif')
        gif_label.setMovie(movie)
        movie.start()
        gif_label.setFixedSize(QSize(118, 118))
        gif_label.setAlignment(Qt.AlignCenter)
        gif_layout.addWidget(gif_label)
        self.layout.addWidget(gif_container, 0, Qt.AlignCenter)
        window_size = 100
        self.setGeometry(0, 0, window_size, window_size)
        self.setWindowTitle('Loading')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.centerWindow()

    def centerWindow(self):
        screen = QCoreApplication.instance().desktop().screenNumber(QCoreApplication.instance().desktop().cursor().pos())
        centerPoint = QCoreApplication.instance().desktop().screenGeometry(screen).center()
        windowWidth = self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        newX = centerPoint.x() - windowWidth 
        newY = centerPoint.y() - windowHeight
        self.move(newX, newY)