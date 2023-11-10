from .windows.login_window import LoginScreen
from .windows.main_window import MainWindow
from .windows.editor_window import EditorWindow
from .windows.settings_window import SettingsWindow
from .windows.attachment_window import AttachmentWindow
from .windows.log_window import LogWindow	
from Testing.logging import setup_logger

class WindowController:
    def __init__(self, app, logging: bool = True):
        self.app = app
        self.show_login()
        if logging:
            self.show_logging()
        
    def show_login(self):
        self.login_window = LoginScreen()
        self.login_window.login_successful.connect(self.show_main)
        self.login_window.show()
        
    def show_main(self, client_obj):
        self.main_window = MainWindow(client_obj)
        self.main_window.open_editor_window.connect(self.show_editor)
        self.main_window.open_settings_window.connect(self.show_settings)
        self.main_window.open_attachment_window.connect(self.show_attachment)
        self.main_window.show()
        self.login_window.close()
    
    def show_editor(self, draft_email=None):
        self.editor_window = EditorWindow(draft_email)
        self.editor_window.mail_signal_from_editor.connect(self.main_window.get_mail_from_editor)
        self.editor_window.show()

    def show_attachment(self, attachment: dict):
        self.attachment_window = AttachmentWindow(attachment)
        self.attachment_window.show()

    def show_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def show_logging(self):
        self.logging_window = LogWindow()
        self.logging_window.show()
        setup_logger(self.logging_window)