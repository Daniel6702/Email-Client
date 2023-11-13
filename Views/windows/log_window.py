import logging
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QCheckBox, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QIcon

class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_window()

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
            if cb is not self.cbDebug:
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
    
    def initialize_window(self):
        self.move(600, 800)
        self.showMinimized()
        self.setWindowTitle("Log")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 700, 300
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)

    def addLogMessage(self, level, message):
        # Ensure this method runs in the main thread
        if self.isLevelChecked(level):
            self.appendStyledMessage(level, message)

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