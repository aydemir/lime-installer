from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint
import os
import json


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(779, 219)
        self.keyboard_image = QPixmap(":/images/keyboard.png")


    def setKeyboardMap(self, key_map):pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform|QPainter.Antialiasing|QPainter.HighQualityAntialiasing)

        painter.drawPixmap(QPoint(0, 0), self.keyboard_image)