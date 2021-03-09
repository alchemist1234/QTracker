from typing import Dict, Tuple
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPainter, QPixmap, QImageReader

from data import ParticleData
from settings import Settings


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView, settings: Settings):
        super(VideoScene, self).__init__(parent)
        self.settings = settings
        self._frame_base64_dict = {}
        self._particle_data = {}
        self.particle_group_items = {}
        self.current_frame_item = QGraphicsPixmapItem(None)
        self.current_frame_index = -1
        self.addItem(self.current_frame_item)

    def clear(self):
        self._frame_base64_dict = {}

    def add_frame_image(self, frame_index: int, img: bytes):
        self._frame_base64_dict[frame_index] = img

    def add_particle_pos(self, frame_index: int, particle_pos: Dict[int, Tuple[int, int]]):
        self._particle_data[frame_index] = ParticleData(self.settings, particle_pos)

    def update_frame_image(self, frame_index: int):
        base64 = self._frame_base64_dict[frame_index]
        byte_arr = QByteArray(base64)
        img = QImage()
        img.loadFromData(QByteArray.fromBase64(byte_arr))
        pixmap = QPixmap.fromImage(img)
        self.current_frame_item.setPixmap(pixmap)
        self.current_frame_index = frame_index

    def update_particle(self, frame_index: int):
        for groups in self.particle_group_items.values():
            self.removeItem(groups)
        self.particle_group_items = self._particle_data[frame_index].particle_group_items()
        for groups in self.particle_group_items.values():
            self.addItem(groups)

    def update_frame_label(self, frame_index: int):
        pass

    def update_particle_label(self, frame_index: int):
        pass

    def update_trajectory(self, frame_index: int):
        pass

    def update_frame(self, frame_index: int):
        if frame_index in self._frame_base64_dict:
            self.update_frame_image(frame_index)
            self.update_particle(frame_index)
