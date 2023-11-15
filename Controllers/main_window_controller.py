from EmailService.models import EmailClient, Email, Folder
import logging

PAGE_SIZE = 15

class MainWindowController():
    def __init__(self, main_window, email_client: EmailClient):
        self.main_window = main_window
        self.email_client = email_client
        self.setup_connections()
        self.current_folder = None
        folders = self.email_client.get_folders()
        self.delete_folder = self.get_delete_folder(folders)
        self.main_window.folder_area.add_folders(folders)
        
    def setup_connections(self):
        self.main_window.folder_area.folder_selected.connect(self.on_folder_selected)
        self.main_window.email_list_area.email_clicked.connect(self.on_email_clicked)
        self.main_window.search_area.search_signal.connect(self.on_search)
        self.main_window.search_area.new_mail_signal.connect(self.main_window.open_editor_window.emit)
        self.main_window.search_area.open_settings_signal.connect(self.main_window.open_settings_window.emit)
        self.main_window.email_view_area.delete_email_signal.connect(self.on_email_delete)
        self.main_window.email_view_area.open_attachment_window.connect(self.main_window.open_attachment_window.emit)
        self.main_window.email_view_area.open_email_editor_window.connect(self.main_window.open_editor_window.emit)
        self.main_window.email_view_area.mark_email_as.connect(self.email_client.mark_email_as)
        self.main_window.get_email_from_editor.connect(self.get_mail_from_editor)

    def on_folder_selected(self, folder: Folder):
        logging.info(f"Folder Selected: {folder.name}")
        self.current_folder = folder
        logging.info(f"Retrieving {PAGE_SIZE} emails from {folder.id}")
        emails = self.email_client.get_mails(folder.id, "", PAGE_SIZE)
        self.main_window.email_list_area.add_emails_to_list(emails)

    def on_search(self, search_criteria: str):
        mails = self.email_client.get_mails(query=search_criteria, number_of_mails=PAGE_SIZE)
        self.main_window.email_list_area.add_emails_to_list(mails)

    def get_delete_folder(self, folders: list[Folder]):
        for folder in folders:
            if folder.name in ["Delete", "Delete", "DELETE", "delete", "DELETED", "deleted", "Deleted", "trash", "Trash", "TRASH", "bin", "Bin", "BIN", "Deleted Items"]:
                return folder
            else:
                pass

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
            self.email_client.send_mail(email)
        elif action == "save":
            self.email_client.save_draft(email)
        elif action == "update":
            self.email_client.update_draft(email)