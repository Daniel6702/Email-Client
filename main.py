import sys
from PyQt5.QtWidgets import QApplication
from Controllers.app_controller import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    app_controller = AppController(app)
    sys.exit(app.exec_())