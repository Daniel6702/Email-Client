import sys
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QStyle, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt

class VideoPlayerWidget(QWidget):
    def __init__(self, file_data, parent=None):
        super().__init__(parent)

        # Write the byte data to a temporary file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        self.temp_file.write(file_data)
        self.temp_file.close()

        # Set up the media player
        self.player = QMediaPlayer()
        self.video_widget = QVideoWidget()

        self.player.setVideoOutput(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.temp_file.name)))

        # Create play and stop buttons
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_video)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.clicked.connect(self.player.stop)

        # Create a slider for seeking
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Connect signals
        self.player.durationChanged.connect(self.duration_changed)
        self.player.positionChanged.connect(self.position_changed)

        # Set up the layout for buttons
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.slider)
        layout.addLayout(control_layout)
        self.setLayout(layout)

    def play_video(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.player.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def position_changed(self, position):
        self.slider.setValue(position)

    def set_position(self, position):
        self.player.setPosition(position)

    def closeEvent(self, event):
        # Clean up the temporary file
        self.player.stop()
        self.temp_file.close()
        event.accept()