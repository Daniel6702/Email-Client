from PyQt5.QtWidgets import QMessageBox, QSpacerItem, QSizePolicy, QWidget
import threading

class PopupWindowController(QWidget):
    def __init__(self):
        super().__init__()

    def show_popup(self, type: str, title: str, message: str, informative_text: str, auto_close_time: int = 0):
        def message_thread():
            self.msg.exec_()
        self.msg = QMessageBox()
        if type == "info":
            self.msg.setIcon(QMessageBox.Information)
        elif type == "warning":
            self.msg.setIcon(QMessageBox.Warning)
        elif type == "error":
            self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText(message)
        self.msg.setInformativeText(informative_text)
        self.msg.setWindowTitle(title)
        spacer = QSpacerItem(500, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout = self.msg.layout()
        layout.addItem(spacer, layout.rowCount(), 0, 1, layout.columnCount())

        if auto_close_time > 0:
            timer = threading.Timer(auto_close_time/1000, self.msg.close)
            timer.start()
        
        self.msg.show()
        message_process_thread = threading.Thread(target=message_thread)
        message_process_thread.start()