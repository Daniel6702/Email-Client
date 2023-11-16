import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Controllers.window_controller import WindowController
from Views.styles.style_manager import StyleManager

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window_controller = WindowController(app)
    sys.exit(app.exec_())