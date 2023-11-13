import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Controllers.window_controller import WindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("Views\\styles\\style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    manager = WindowController(app)
    sys.exit(app.exec_())