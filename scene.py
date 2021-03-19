from typing import Dict, Tuple, Optional

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import *

from data import ParticleData
from settings import Settings


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView, settings: Settings):
        super(VideoScene, self).__init__(parent)
        self.settings = settings
        # 视频帧base64字典 {帧数: base64}
        self._frame_base64_dict = {}
        # 粒子数据字典 {帧数: ParticleData}
        self._particle_data = {}
        # 粒子+标签 Item
        self.particle_group_items = {}
        self.current_frame_item = QGraphicsPixmapItem(None)
        self.current_frame_index = -1
        self.addItem(self.current_frame_item)

    def clear(self):
        """
        清除所有数据
        """
        self._frame_base64_dict = {}
        self._particle_data = {}
        for group in self.particle_group_items:
            self.removeItem(group)
        self.particle_group_items = {}
        self.current_frame_item = QGraphicsPixmapItem(None)
        self.current_frame_index = -1

    def add_frame_image(self, frame_index: int, img: bytes):
        """
        添加帧
        :param frame_index: 帧索引
        :param img: 帧图像base64数据
        """
        self._frame_base64_dict[frame_index] = img

    def add_particle_pos(self, frame_index: int, particle_pos: Dict[int, Tuple[int, int]]):
        """
        添加粒子数据
        :param frame_index: 帧索引
        :param particle_pos: 粒子坐标
        """
        self._particle_data[frame_index] = ParticleData(self.settings, particle_pos)

    def update_frame_image(self, frame_index: int):
        """
        刷新帧图象显示
        :param frame_index: 帧索引
        :return: None
        """
        base64 = self._frame_base64_dict[frame_index]
        byte_arr = QByteArray(base64)
        img = QImage()
        img.loadFromData(QByteArray.fromBase64(byte_arr))
        pixmap = QPixmap.fromImage(img)
        self.current_frame_item.setPixmap(pixmap)
        self.current_frame_index = frame_index

    def update_particle(self, frame_index: int):
        """
        刷新粒子显示
        :param frame_index: 帧索引
        :return: None
        """
        for groups in self.particle_group_items.values():
            self.removeItem(groups)
        self.particle_group_items = self._particle_data[frame_index].particle_group_items()
        for groups in self.particle_group_items.values():
            self.addItem(groups)

    def update_frame_label(self, frame_index: int):
        """
        刷帧索引显示
        :param frame_index: 帧索引
        :return: None
        """
        pass

    def update_trajectory(self, frame_index: int):
        """
        刷新轨迹
        :param frame_index: 帧索引
        :return: None
        """
        pass

    def update_frame(self, frame_index: Optional[int] = None):
        """
        刷新帧
        :param frame_index: 帧索引
        :return: None
        """
        frame_index = self.current_frame_index if frame_index is None else frame_index
        if frame_index in self._frame_base64_dict:
            self.update_frame_image(frame_index)
            self.update_particle(frame_index)
