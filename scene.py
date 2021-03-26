from typing import Dict, Tuple, Optional
import time

from PySide6.QtCore import QByteArray, QPoint, QPointF, Qt
from PySide6.QtGui import QImage, QPixmap, QPainter, QKeyEvent
from PySide6.QtWidgets import *
import numpy as np

from data import ParticleData, SettingWidgetHelper
from settings import Settings
import default_settings
from enums import OperationMode


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView, settings: Settings):
        super(VideoScene, self).__init__(parent)
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        self.mode = OperationMode.MOVE
        # 视频帧base64字典 {帧数: base64}
        self._frame_base64_dict = {}
        # 粒子数据字典 {帧数: ParticleData}
        self._particle_data = {}
        # 粒子+标签 Item
        self.particle_group_items = {}
        # 轨迹Item
        self.trajectory_items = {}
        # 已更新轨迹的帧
        self.updated_frame_index = set()
        # 当前帧图像对象
        self.current_frame_item = QGraphicsPixmapItem(None)
        # 当前帧索引
        self.current_frame_index = 0
        self.config_changed = False
        self.addItem(self.current_frame_item)
        self.mouse_press_pos = QPointF()

        # np.ndarray 用于缓存导出图像
        self.export_frame_dict = {}

    def sorted_frame_indexes(self):
        frame_indexes = list(self._frame_base64_dict.keys())
        frame_indexes.sort()
        return frame_indexes

    def clear(self):
        """
        清除所有数据
        """
        self._frame_base64_dict = {}
        self._particle_data = {}
        for group in self.particle_group_items:
            self.removeItem(group)
        self.particle_group_items = {}
        self.trajectory_items = {}
        self.current_frame_item = QGraphicsPixmapItem(None)
        self.current_frame_index = 0

    def add_frame_image(self, frame_index: int, img: bytes):
        """
        添加帧
        :param frame_index: 帧索引
        :param img: 帧图像base64数据
        """
        self._frame_base64_dict[frame_index] = img

    def set_particle_pos(self, frame_index: int, particle_pos: Dict[int, Tuple[int, int]]):
        """
        添加粒子数据
        :param frame_index: 帧索引
        :param particle_pos: 粒子坐标
        """
        self._particle_data[frame_index] = ParticleData(self.settings, particle_pos)

    def update_particle_pos(self, index: int, pos: Tuple[int, int]):
        if index in self.particle_group_items.keys():
            ret = QMessageBox.information(None, '提示', f'当前帧已存在粒子{index}, 继续添加会覆盖原粒子, 是否继续?',
                                          QMessageBox.Cancel, QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                return
        self._particle_data[self.current_frame_index].update_particle(index, pos)
        self.update_particle(self.current_frame_index)
        self.calc_trajectory()
        self.updated_frame_index = {i for i in self.updated_frame_index if i < self.current_frame_index}

    def calc_trajectory(self):
        last_pos_dict = {}
        sorted_frame_indexes = list(self._particle_data.keys())
        sorted_frame_indexes.sort()
        for frame_index in sorted_frame_indexes:
            data = self._particle_data[frame_index]
            pos_dict = data.particle_pos
            for index, center in pos_dict.items():
                if index in last_pos_dict:
                    last_pos = last_pos_dict[index]
                    data.update_line(index, last_pos[0], last_pos[1], center[0], center[1], index - last_pos[2])
                last_pos_dict[index] = (center[0], center[1], index)

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
        frame_index_to_be_updated = {i for i in set(self._particle_data.keys()) - self.updated_frame_index if
                                     i <= frame_index}

        for iter_frame_index in frame_index_to_be_updated:
            if iter_frame_index in self.trajectory_items:
                for item in self.trajectory_items[iter_frame_index].values():
                    self.removeItem(item)
            if iter_frame_index in self._particle_data:
                self.trajectory_items[iter_frame_index] = self._particle_data[iter_frame_index] \
                    .trajectory_items(iter_frame_index)
                if len(self.trajectory_items[iter_frame_index]) > 0:
                    for item in self.trajectory_items[iter_frame_index].values():
                        self.addItem(item)
                    self.updated_frame_index.add(iter_frame_index)
        self.update_trajectory_visibility(frame_index)

    def update_trajectory_visibility(self, frame_index: int):
        for iter_frame_index, d in self.trajectory_items.items():
            for index, item in d.items():
                if iter_frame_index <= frame_index and \
                        self.setting_helper.visible(default_settings.show_trajectory, index):
                    if self.config_changed:
                        item.update_pen()
                    item.setVisible(True)
                else:
                    item.setVisible(False)

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
            self.update_trajectory(frame_index)

    def buffer_random_frame(self):
        pass

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.mouse_press_pos = event.scenePos()
        if self.mode == OperationMode.ADD:
            if self.current_frame_index in self._particle_data:
                scene_pos = event.scenePos().toPoint()
                index, ok = QInputDialog.getInt(None, '输入', '粒子编号', 1)
                if ok:
                    self.update_particle_pos(index, (scene_pos.x(), scene_pos.y()))
            else:
                QMessageBox.information(None, '提示', f'未加载视频')
        super(VideoScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        pos = event.scenePos()
        moved = pos - self.mouse_press_pos
        if moved.manhattanLength() > 0:
            if len(self.selectedItems()) > 0:
                for item in self.selectedItems():
                    index = item.index
                    particle_data = self._particle_data[self.current_frame_index]
                    particle_data.update_particle_by(index, (moved.x(), moved.y()))
                self.calc_trajectory()
                self.updated_frame_index = {i for i in self.updated_frame_index if i < self.current_frame_index}
        super(VideoScene, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            if len(self.selectedItems()) > 0:
                for item in self.selectedItems():
                    index = item.index
                    particle_data = self._particle_data[self.current_frame_index]
                    particle_data.remove_particle(index)
                    particle_data.remove_trajectory(index)
                    if self.current_frame_index + 1 in self._particle_data:
                        next_particle_data = self._particle_data[self.current_frame_index + 1]
                        next_particle_data.remove_trajectory(index)
                    del self.particle_group_items[index]
                    self.removeItem(item)
                    if index in self.trajectory_items[self.current_frame_index]:
                        self.removeItem(self.trajectory_items[self.current_frame_index][index])
                # 更新展需要更新轨迹的帧
                self.updated_frame_index = {i for i in self.updated_frame_index if i < self.current_frame_index}
                self.calc_trajectory()
        super(VideoScene, self).keyPressEvent(event)
