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

def setup_logger(log_window):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = QtHandler(log_window)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)