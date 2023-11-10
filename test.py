import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QCheckBox, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextCursor, QColor

class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.textEdit.clear)

        # Checkboxes for log levels
        self.cbDebug = QCheckBox("Debug")
        self.cbInfo = QCheckBox("Info")
        self.cbWarning = QCheckBox("Warning")
        self.cbError = QCheckBox("Error")
        self.cbCritical = QCheckBox("Critical")

        # Set all checkboxes checked by default
        for cb in [self.cbDebug, self.cbInfo, self.cbWarning, self.cbError, self.cbCritical]:
            cb.setChecked(True)
            cb.stateChanged.connect(self.refreshLogDisplay)

        #create a horizontal layout
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.clearButton)
        layout_checkboxes = QHBoxLayout()
        layout_checkboxes.addWidget(self.cbDebug)
        layout_checkboxes.addWidget(self.cbInfo)
        layout_checkboxes.addWidget(self.cbWarning)
        layout_checkboxes.addWidget(self.cbError)
        layout_checkboxes.addWidget(self.cbCritical)
        layout.addLayout(layout_checkboxes)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.logMessages = []

    def addLogMessage(self, level, message):
        self.logMessages.append((level, message))
        self.refreshLogDisplay()

    @pyqtSlot()
    def refreshLogDisplay(self):
        self.textEdit.clear()
        for level, message in self.logMessages:
            if self.isLevelChecked(level):
                self.appendStyledMessage(level, message)

    def appendStyledMessage(self, level, message):
        color = self.getColorForLevel(level)
        self.textEdit.setTextColor(color)
        self.textEdit.append(message)

    def getColorForLevel(self, level):
        if level == logging.DEBUG:
            return QColor('green')
        elif level == logging.INFO:
            return QColor('black')
        elif level == logging.WARNING:
            return QColor('orange')
        elif level == logging.ERROR:
            return QColor('red')
        elif level == logging.CRITICAL:
            return QColor('darkred')
        else:
            return QColor('black')

    def isLevelChecked(self, level):
        return (level == logging.DEBUG and self.cbDebug.isChecked()) or \
               (level == logging.INFO and self.cbInfo.isChecked()) or \
               (level == logging.WARNING and self.cbWarning.isChecked()) or \
               (level == logging.ERROR and self.cbError.isChecked()) or \
               (level == logging.CRITICAL and self.cbCritical.isChecked())

class QtHandler(logging.Handler):
    def __init__(self, log_window):
        super().__init__()
        self.log_window = log_window

    def emit(self, record):
        msg = self.format(record)
        self.log_window.addLogMessage(record.levelno, msg)

def setup_logger(log_window):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = QtHandler(log_window)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    app = QApplication([])
    log_window = LogWindow()
    log_window.show()

    setup_logger(log_window)

    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")

    app.exec_()

main()  