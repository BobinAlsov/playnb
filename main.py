# PyQt5 Video player
#!/usr/bin/env python

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Playnb") 

        self.setWindowIcon(QIcon('images/other/playnb.png'))

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('images/open.png'), '&Открыть', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Открыть')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('images/exit.png'), '&Выйти', self)       
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Выйти')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Файл')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

STYLE_SHEET = '''
QSlider::groove:horizontal {
    background: white;
    height: 10px;
    border-radius: 4px;
}

QSlider::sub-page:horizontal {
    background: #DD7CFF;
    border: 1px solid #777;
    height: 10px;
    border-radius: 4px;
}

QSlider::add-page:horizontal {
    background: #fff;
    border: 1px solid #777;
    height: 10px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: white;
    border: 1px solid #777;
    width: 13px;
    margin-top: -2px;
    margin-bottom: -2px;
    border-radius: 4px;
}

QSlider::handle:horizontal:hover {
    background: white;
    border: 1px solid #444;
    border-radius: 4px;
}

QSlider::sub-page:horizontal:disabled {
    background: #bbb;
    border-color: #999;
}

QSlider::add-page:horizontal:disabled {
    background: #eee;
    border-color: #999;
}

QSlider::handle:horizontal:disabled {
    background: #eee;
    border: 1px solid #aaa;
    border-radius: 4px;
}

QVideoWidget {
    background-color: #121212;
}
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())