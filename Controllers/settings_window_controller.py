from PyQt5.QtWidgets import QWidget
from Views.windows.settings_window import SettingsWindow
from Views.styles.style_manager import StyleManager
from EmailService.models.email_client import EmailClient
from EmailService.models import User
from PyQt5.QtCore import pyqtSignal
from EmailService.services.common.user_manager_service import restart_program

class SettingsWindowController(QWidget):
    close_window_signal = pyqtSignal()
    open_login_signal = pyqtSignal()
    def __init__(self, style_manager: StyleManager, client: EmailClient):
        super().__init__()
        self.style_manager = style_manager
        self.settings_window = SettingsWindow()
        self.email_client = client
        self.setup_connections()

    def setup_connections(self):
        self.settings_window.style_signal.connect(self.on_style_changed)
        self.settings_window.logout_signal.connect(self.delete)
        self.settings_window.switch_account_signal.connect(self.switch_account)
        self.settings_window.add_rule_signal.connect(self.add_rule)
        self.settings_window.delete_rule_signal.connect(self.delete_rule)

    def delete_rule(self, rule):
        self.email_client.remove_rule(rule)

    def add_rule(self, rule):
        self.email_client.add_rule(rule)

    def on_style_changed(self, style: str):
        self.style_manager.set_style(style)

    def show_settings(self):
        rules = self.email_client.get_rules()
        print(rules)
        self.settings_window.add_rules(rules)
        self.settings_window.show()

    def switch_account(self):
        restart_program()
    
    def delete(self):
        current_user = self.email_client.get_user()
        self.email_client.delete_user(current_user)
        self.close_window_signal.emit()
        self.settings_window.close()
        
    