from PyQt5.QtWidgets import QWidget
from Views.windows.settings_window import SettingsWindow
from Views.styles.style_manager import StyleManager
from EmailService.models.email_client import EmailClient
from EmailService.models import User
from PyQt5.QtCore import pyqtSignal

class SettingsWindowController(QWidget):
    close_window_signal = pyqtSignal()
    def __init__(self, style_manager: StyleManager, client):
        super().__init__()
        self.style_manager = style_manager
        self.settings_window = SettingsWindow()
        self.email_client = client
        self.setup_connections()

    def setup_connections(self):
        self.settings_window.style_signal.connect(self.on_style_changed)
        self.settings_window.logout_signal.connect(self.delete)

    def on_style_changed(self, style: str):
        self.style_manager.set_style(style)

    def show_settings(self):
        self.settings_window.show()
    
    def delete(self):
        current_user = self.email_client.get_user()
        self.email_client.delete_user(current_user)
        self.close_window_signal.emit()
        self.settings_window.close()
        