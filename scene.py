from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPainter


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView):
        super(VideoScene, self).__init__(parent)
