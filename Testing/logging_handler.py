import sys
import logging
from PyQt5.QtCore import QObject, pyqtSignal

class QtHandler(logging.Handler, QObject):
    newLogMessage = pyqtSignal(int, str)

    def __init__(self, log_window):
        logging.Handler.__init__(self)
        QObject.__init__(self)
        self.log_window = log_window
        self.newLogMessage.connect(self.log_window.addLogMessage)

    def emit(self, record):
        msg = self.format(record)
        self.newLogMessage.emit(record.levelno, msg)

def setup_logger(log_window, console_print=True):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # QtHandler
    qt_handler = QtHandler(log_window)
    qt_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    qt_handler.setFormatter(qt_formatter)
    logger.addHandler(qt_handler)

    # StreamHandler for console output
    if console_print:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
