from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPainter, QPixmap, QImageReader


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView):
        super(VideoScene, self).__init__(parent)
        self.frame_base64_dict = {}
        self.current_frame_item = QGraphicsPixmapItem()
        self.current_frame_index = -1
        self.addItem(self.current_frame_item)

    def clear(self):
        self.frame_base64_dict = {}

    def add_frame_image(self, frame_index: int, img: bytes):
        self.frame_base64_dict[frame_index] = img

    def change_frame(self, frame_index: int):
        if frame_index in self.frame_base64_dict:
            base64 = self.frame_base64_dict[frame_index]
            byte_arr = QByteArray(base64)
            img = QImage()
            img.loadFromData(QByteArray.fromBase64(byte_arr))
            pixmap = QPixmap.fromImage(img)
            self.current_frame_item.setPixmap(pixmap)
            self.current_frame_index = frame_index
