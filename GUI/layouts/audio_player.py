import sys
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt

class AudioPlayerWidget(QWidget):
    def __init__(self, file_data, parent=None):
        super().__init__(parent)

        # Write the byte data to a temporary file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        self.temp_file.write(file_data)
        self.temp_file.close()

        # Set up the media player
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.temp_file.name)))

        # Create play and stop buttons
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.player.play)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.player.stop)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Connect signals
        self.player.durationChanged.connect(self.duration_changed)
        self.player.positionChanged.connect(self.position_changed)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def position_changed(self, position):
        self.slider.setValue(position)

    def set_position(self, position):
        self.player.setPosition(position)

    def closeEvent(self, event):
        self.player.stop()
        self.temp_file.close()
        event.accept()