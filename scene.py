from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPainter, QPixmap


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView):
        super(VideoScene, self).__init__(parent)
        self.frame_images = {}
        self.current_frame_item = None

    def clear(self):
        self.frame_images = {}

    def add_frame_image(self, frame_index: int, img: QImage):
        self.frame_images[frame_index] = img

    def change_frame(self, frame_index: int):
        if frame_index in self.frame_images:
            self.removeItem(self.current_frame_item)
            self.current_frame_item = QGraphicsPixmapItem()
            pixmap = QPixmap.fromImage(self.frame_images[frame_index])
            self.current_frame_item.setPixmap(pixmap)
            self.addItem(self.current_frame_item)
