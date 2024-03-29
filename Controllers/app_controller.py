from PyQt5.QtCore import QObject
from Controllers.attachment_window_controller import AttachmentWindowController
from Controllers.contacts_window_controller import ContactsWindowController
from Controllers.filter_window_controller import FilterWindowController
from Controllers.folder_selector_controller import FolderSelectorWindowController
from Controllers.login_window_controller import LoginWindowController
from Controllers.main_window_controller import MainWindowController
from Controllers.settings_window_controller import SettingsWindowController
from Controllers.editor_window_controller import EditorWindowController
from Controllers.popup_window_controller import PopupWindowController
from Views.windows.log_window import LogWindow
from Testing.logging_handler import setup_logger
from Views.styles.style_manager import StyleManager
import requests

class AppController(QObject):
    def __init__(self, app):
        super().__init__()
        self.style_manager = StyleManager(app)
        self.style_manager.set_style("lightmode")
        self.start()

    def start(self):
        if self.is_internet_connected():
            self.login_window_controller = LoginWindowController()
            self.login_window_controller.on_login_signal.connect(self.initiate_on_login)
            self.login_window_controller.show_login()

            #setup_logger(LogWindow(),console_print=True)

        else:
            self.show_internet_connection_error()

    def is_internet_connected(self):
        try:
            # Try to connect to Google's DNS server (8.8.8.8) on port 53
            requests.get("http://google.com", timeout=5)
            return True
        except OSError:
            return False

    def show_internet_connection_error(self):
        error_message = "Unable to connect to the internet. Please check your internet connection and try again."
        window = PopupWindowController()
        window.show_popup("error", "Internet Connection Error", error_message, "", 0)

    def initiate_on_login(self, client):
        self.login_window_controller.login_window.close()
        self.settings_window_controller = SettingsWindowController(self.style_manager, client)
        self.editor_window_controller = EditorWindowController(client)
        self.filter_window_controller = FilterWindowController()
        self.folder_selector_window_controller = FolderSelectorWindowController()
        self.attachment_window_controller = AttachmentWindowController()
        self.contacts_window_controller = ContactsWindowController(client)
        self.main_window_controller = MainWindowController(client)
        self.popup_window_controller = PopupWindowController()
        self.setup_connections()

    def setup_connections(self):
        self.main_window_controller.open_editor_window.connect(self.editor_window_controller.show_editor)
        self.main_window_controller.open_folder_selector_window.connect(self.folder_selector_window_controller.show_folder_selector)
        self.main_window_controller.open_filter_window.connect(self.filter_window_controller.show_filter)
        self.main_window_controller.open_attachment_window.connect(self.attachment_window_controller.show_attachment)
        self.main_window_controller.open_settings_window.connect(self.settings_window_controller.show_settings)
        self.main_window_controller.open_contacts_window.connect(self.contacts_window_controller.show_contacts)
        self.filter_window_controller.set_filter_signal.connect(self.main_window_controller.set_filter)
        self.folder_selector_window_controller.folder_selected.connect(self.main_window_controller.on_folder_selected_from_folder_selector_window)
        self.main_window_controller.open_popup_window.connect(self.popup_window_controller.show_popup)
        self.settings_window_controller.close_window_signal.connect(self.main_window_controller.main_window.close)
        self.editor_window_controller.open_attachment_signal.connect(self.attachment_window_controller.show_attachment)
