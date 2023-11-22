from PyQt5.QtWidgets import QWidget
from Views.windows.settings_window import SettingsWindow
from Views.styles.style_manager import StyleManager

class SettingsWindowController(QWidget):
    def __init__(self, style_manager: StyleManager):
        super().__init__()
        self.style_manager = style_manager
        self.settings_window = SettingsWindow()
        self.setup_connections()

    def setup_connections(self):
        self.settings_window.style_signal.connect(self.on_style_changed)

    def on_style_changed(self, style: str):
        self.style_manager.set_style(style)

    def show_settings(self):
        self.settings_window.show()