from PyQt5.QtWidgets import QPinchGesture,QMessageBox,QApplication,QFileDialog, QListWidget, QListWidgetItem, QLabel, QMenu, QMainWindow, QDesktopWidget, QSplitter, QCheckBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal,Qt, QUrl, QTimer, QEvent
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QToolBar, QAction, QApplication, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView, QWebEnginePage
from Views.components.audio_player import AudioPlayerWidget
from Views.components.video_player import VideoPlayerWidget

import tempfile
import os
    
class CustomQWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        pass

class AttachmentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initial_layout()   

    def add_attachment(self, attachment: dict):
        self.attachment = attachment
        self.init()

    def init(self):
        self.setWindowTitle(self.attachment['file_name'])
        self.layout = QVBoxLayout()

        self.file_type = self.determine_file_type(self.attachment['file_data'], self.attachment['file_name'])

        if self.file_type == 'pdf':
            self.layout.addWidget(self.PDF(self.attachment['file_data']))
        elif self.file_type == 'txt' or self.file_type == 'py':
            self.layout.addWidget(self.TXT(self.attachment['file_data']))
        elif self.file_type == 'jpeg' or self.file_type == 'png' or self.file_type == 'gif' or self.file_type == 'tiff' or self.file_type == 'bmp' or self.file_type == 'psd':
            self.layout.addWidget(self.IMAGE(self.attachment['file_data']))
        elif self.file_type == 'mp3' or self.file_type == 'wav' or self.file_type == 'aac' or self.file_type == 'ogg':
            self.layout.addWidget(self.AUDIO(self.attachment['file_data']))
        elif self.file_type == 'mp4' or self.file_type == 'webm' or self.file_type == 'asf' or self.file_type == 'mpeg':
            self.layout.addWidget(self.VIDEO(self.attachment['file_data']))
        elif self.file_type == 'Unknown file type':
            self.layout.addWidget(QLabel("Unknown file type"))

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        self.layout.addWidget(self.download_button)
            
        self.setLayout(self.layout)

    def download(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        file_path = os.path.join(path, self.attachment['file_name'])
        with open(file_path, 'wb') as f:
            f.write(self.attachment['file_data'])

    def VIDEO(self, file_data: bytes) -> QWidget:
        player = VideoPlayerWidget(file_data)
        return player

    def AUDIO(self, file_data: bytes) -> QWidget:
        player = AudioPlayerWidget(file_data)
        return player

    def IMAGE(self, file_data: bytes) -> QWidget:
        self.image = QImage()
        self.image.loadFromData(file_data)
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap.fromImage(self.image))
        return self.image_label

    def TXT(self, file_data: bytes) -> QWidget:
        self.textEdit = QTextEdit()
        self.textEdit.setText(file_data.decode('utf-8').strip())
        return self.textEdit

    def PDF(self, file_data: bytes) -> QWidget:
        layout = QVBoxLayout()
        webView = QWebEngineView()
        webView.setPage(CustomQWebEnginePage(webView))
        webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
            tf.write(file_data)
            temp_file_path = tf.name
        path = QUrl.fromLocalFile(temp_file_path)
        webView.setUrl(path)

        QTimer.singleShot(5000, lambda: os.unlink(temp_file_path))

        layout = QVBoxLayout()  # Assuming you're using a QVBoxLayout
        layout.setContentsMargins(10, 10, 10, 10)
        label = QLabel("Zoom doesn't work ¯\_(ツ)_/¯")
        layout.addWidget(label)
        label.setAlignment(Qt.AlignTop)
        layout.addWidget(webView, 1)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def determine_file_type(self, file_data: bytes, file_name: str) -> str:
        file_signatures = {
            #Images
            b'\xFF\xD8\xFF\xDB': 'jpeg',
            b'\xFF\xD8\xFF\xE0': 'jpeg',
            b'\xFF\xD8\xFF\xEE': 'jpeg',
            b'\xFF\xD8\xFF\xE1': 'jpeg',
            b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'png',
            b'\x47\x49\x46\x38\x37\x61': 'gif',
            b'\x47\x49\x46\x38\x39\x61': 'gif',
            b'\x49\x49\x2A\x00': 'tiff',
            b'\x4D\x4D\x00\x2A': 'tiff',
            b'\x42\x4D': 'bmp',
            b'\x38\x42\x50\x53': 'psd',
            #Documents
            b'\x25\x50\x44\x46': 'pdf',
            b'\x50\x4B\x03\x04': 'zip',
            b'\x50\x4B\x07\x08': 'zip',
            b'\x50\x4B\x05\x06': 'zip',
            b'\x1F\x8B\x08': 'gzip',
            b'\x37\x7A\xBC\xAF\x27\x1C': 'x-7z-compressed',
            b'\x52\x61\x72\x21\x1A\x07\x00': 'x-rar-compressed',
            b'\x52\x61\x72\x21\x1A\x07\x01\x00': 'x-rar-compressed',
            b'\xFD\x37\x7A\x58\x5A\x00': 'x-xz',
            b'\xCF\xFA\xED\xFE': 'x-mach-binary',  
            b'\x50\x4B\x03\x04\x14\x00\x06\x00': 'docx', 
            b'\x50\x4B\x03\x04\x14\x00\x08\x08': 'xlsx', 
            b'\x50\x4B\x03\x04\x14\x00\x00\x08': 'pptx', 
            b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': 'xls',
            #Audio
            b'\x49\x44\x33': 'mp3',
            b'\xFF\xFB': 'mp3',
            b'\x52\x49\x46\x46': 'wav',
            b'\xFF\xF1': 'aac',
            b'\xFF\xF9': 'aac',
            b'\x4F\x67\x67\x53': 'ogg',
            #Video
            b'\x66\x74\x79\x70\x69\x73\x6F\x6D': 'mp4', 
            b'\x66\x74\x79\x70\x4D\x53\x4E\x56': 'mp4',  
            b'\x66\x74\x79\x70\x33\x67\x70\x35': 'mp4',
            b'\x1A\x45\xDF\xA3': 'webm',
            b'\x30\x26\xB2\x75\x8E\x66\xCF\x11': 'asf',
            b'\x00\x00\x01\xBA': 'mpeg',
            b'\x00\x00\x01\xB3': 'mpeg',
            # Executables
            b'\x4D\x5A': 'exe',
        }
        for signature, filetype in file_signatures.items():
            if file_data.startswith(signature) or filetype in file_name.lower():
                return filetype   
        try:
            text = file_data.decode('utf-8').strip()
            if text.startswith('#!') or text.startswith('import ') or '.py' in text:
                return 'py'
            elif text and '\x00' not in text:
                return 'txt'
        except UnicodeDecodeError:
            pass

        return 'Unknown file type'

    def initial_layout(self):
        self.setWindowTitle("Attachment")
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)
        icon = QIcon("Images\\icon_logo.png")
        self.setWindowIcon(icon)