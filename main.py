import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_Elements.main_window import MainWindow
from UI_Elements.login_window import LoginScreen

class WindowController:
    def __init__(self, app):
        self.app = app
        self.show_login()
        
    def show_login(self):
        self.login_window = LoginScreen()
        self.login_window.login_successful.connect(self.show_main)
        self.login_window.show()
        
    def show_main(self, client_obj):
        self.main_window = MainWindow(client_obj)
        self.main_window.show()
        self.login_window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("UI_Elements\\style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    manager = WindowController(app)
    sys.exit(app.exec_())