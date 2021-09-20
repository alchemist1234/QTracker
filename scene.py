from typing import Dict, Tuple, Optional, Set

from PySide6.QtCore import QByteArray, QPointF, Qt, QRectF, QMarginsF, QTimer
from PySide6.QtGui import QImage, QPixmap, QKeyEvent, QPen
from PySide6.QtWidgets import *

from base import LinkedMap
from data import ParticleData, SettingWidgetHelper, VideoData
from enums import OperationMode
from settings import Settings
import default_settings


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView, settings: Settings):
        super(VideoScene, self).__init__(parent)
        self.settings = settings
        self.video_data = VideoData()
        self.setting_helper = SettingWidgetHelper(settings)
        self.mode = OperationMode.SELECT
        # 视频帧base64字典 {帧数: base64}
        self._frame_base64_dict = {}
        # 粒子数据字典 {帧数: ParticleData}
        self._particle_data = ParticleData(settings)
        # 粒子+标签 Item
        self.particle_group_items = LinkedMap()
        # 轨迹Item
        self.trajectory_items = LinkedMap()
        # 已更新轨迹的帧
        self.particle_updated_frame_index = set()
        self.trajectory_updated_frame_index = set()
        # 当前帧图像对象
        self.current_frame_item = QGraphicsPixmapItem(None)
        # 当前帧索引
        self.current_frame_index = 0
        self.config_changed = False
        self.addItem(self.current_frame_item)

        self.selected_items = []
        self.mouse_press_pos = QPointF()
        self._selection_rect = self.create_selection_rect()
        self._crop_rect = self.create_crop_rect()
        self._crop_select_rect = self.create_crop_select_rect()

        self.background_timer = self.background_timer()
        self.background_timer.start()

    @property
    def crop_rect(self) -> QRectF:
        if self._crop_rect.rect().isEmpty():
            return self.current_frame_item.boundingRect()
        else:
            rect = self._crop_rect.rect()
            # 去掉边框
            m = self._crop_rect.pen().width() + 1
            margins = QMarginsF(m, m, m, m)
            return rect.marginsRemoved(margins)

    @property
    def video_data(self):
        return self._video_data

    @video_data.setter
    def video_data(self, video_data: VideoData):
        self._video_data = video_data

    def background_timer(self):
        timer = QTimer()
        timer.setInterval(100)
        timer.timeout.connect(self.update_background)
        return timer

    def update_background(self):
        all_frame_indexes = self._particle_data.frame_indexes()
        trajectory_frame_indexes = all_frame_indexes - self.trajectory_updated_frame_index
        if len(trajectory_frame_indexes) > 0:
            frame_index = trajectory_frame_indexes.pop()
            self.update_trajectory(frame_index)
            self.trajectory_updated_frame_index.add(frame_index)
            print(f'frame:{frame_index} trajectory updated background')

    def create_selection_rect(self):
        selection_rect = QGraphicsRectItem()
        selection_pen = QPen()
        selection_pen.setStyle(Qt.CustomDashLine)
        selection_pen.setDashPattern([5, 10])
        selection_pen.setWidth(2)
        selection_pen.setColor(Qt.red)
        selection_rect.setPen(selection_pen)
        self.addItem(selection_rect)
        return selection_rect

    def create_crop_rect(self):
        crop_rect = QGraphicsRectItem()
        crop_pen = QPen()
        crop_pen.setWidth(2)
        crop_pen.setColor(Qt.green)
        crop_rect.setPen(crop_pen)
        self.addItem(crop_rect)
        return crop_rect

    def create_crop_select_rect(self):
        crop_select_rect = QGraphicsRectItem()
        crop_select_pen = QPen()
        crop_select_pen.setStyle(Qt.CustomDashLine)
        crop_select_pen.setDashPattern([5, 10])
        crop_select_pen.setWidth(2)
        crop_select_pen.setColor(Qt.yellow)
        crop_select_rect.setPen(crop_select_pen)
        self.addItem(crop_select_rect)
        return crop_select_rect

    def sorted_frame_indexes(self):
        frame_indexes = list(self._frame_base64_dict.keys())
        frame_indexes.sort()
        return frame_indexes

    def clear(self):
        """
        清除所有数据
        """
        self._frame_base64_dict = {}
        self._particle_data.clear()
        self._trajectory_data.clear()
        for group in self.particle_group_items:
            self.removeItem(group)
        self.particle_group_items.clear()
        self.trajectory_items.clear()
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
        self._particle_data.update_frame_particles(frame_index, particle_pos)
        self.update_particle(frame_index)
        self.update_trajectory(frame_index)
        # self.trajectory_items.put(frame_index, self._particle_data.line_map_of_frame(frame_index))

    def update_particle_pos(self, index: int, pos: Tuple[int, int]):
        point_map = self.particle_group_items[self.current_frame_index]
        if index in point_map.keys():
            ret = QMessageBox.information(None, '提示', f'当前帧已存在粒子{index}, 继续添加会覆盖原粒子, 是否继续?',
                                          QMessageBox.Cancel, QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                return
        self._particle_data.update_particle(self.current_frame_index, index, pos[0], pos[1])
        self.particle_updated_frame_index -= {self.current_frame_index}
        self.update_particle(self.current_frame_index)

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
        if frame_index not in self.particle_updated_frame_index:
            point_item_map = self.particle_group_items[frame_index]
            if point_item_map:
                for index, groups in point_item_map.items():
                    self.removeItem(groups)
            self.particle_group_items[frame_index] = self._particle_data.particle_map_of_frame(frame_index)
            for groups in self.particle_group_items[frame_index].values():
                self.addItem(groups)
        self.update_particle_visibility()
        self.particle_updated_frame_index.add(frame_index)

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
        if frame_index not in self.trajectory_updated_frame_index:
            if frame_index in self.trajectory_items:
                line_item_map = self.trajectory_items[frame_index]
                for item in line_item_map.values():
                    self.removeItem(item)
                self.trajectory_items.remove_by_index(frame_index)
            line_item_map = self._particle_data.line_map_of_frame(frame_index)
            self.trajectory_items[frame_index] = line_item_map
            for item in line_item_map.values():
                self.addItem(item)
            self.trajectory_updated_frame_index.add(frame_index)
        self.update_trajectory_visibility()

    def update_trajectory_visibility(self):
        visibility_map = {}
        for node in self.trajectory_items:
            if node.index <= self.current_frame_index:
                for index, line_item in node.item.items():
                    if index not in visibility_map:
                        show_trajectory = self.setting_helper.visible(default_settings.show_trajectory, index)
                        visibility_map[index] = show_trajectory
                    line_item.setVisible(visibility_map[index])
            else:
                for index, line_item in node.item.items():
                    line_item.setVisible(False)

    def update_particle_visibility(self):
        for frame_index, node in self.particle_group_items.items():
            if frame_index != self.current_frame_index:
                for index, particle_item in node.item.items():
                    particle_item.setVisible(False)
            else:
                for index, particle_group_item in node.item.items():
                    show_particle = self.setting_helper.visible(default_settings.show_particle, index)
                    show_mark = self.setting_helper.visible(default_settings.show_mark, index)
                    particle_group_item.particle.setVisible(show_particle)
                    particle_group_item.mark.setVisible(show_mark)
                    particle_group_item.setVisible(show_particle or show_mark)

    def update_frame(self, frame_index: Optional[int] = None):
        """
        刷新帧
        :param frame_index: 帧索引
        :return: None
        """
        frame_index = self.current_frame_index if frame_index is None else frame_index
        # modified_frame_index = set(
        #     range(min(frame_index, self.current_frame_index), max(frame_index, self.current_frame_index)))
        # self.trajectory_updated_frame_index -= modified_frame_index
        if frame_index in self._frame_base64_dict:
            self.update_frame_image(frame_index)
            self.update_particle(frame_index)
            self.update_trajectory(frame_index)

    def combine_particles(self, indexes: set):
        if len(indexes) > 1:
            for frame_index in self._particle_data.frame_indexes():
                self._particle_data.combine_particle(frame_index, indexes)
                self.particle_updated_frame_index -= {frame_index}
                self.update_particle(frame_index)
                self.trajectory_updated_frame_index -= {frame_index}

    def buffer_random_frame(self):
        pass

    def start_selecting(self):
        self._selection_rect.setRect(self.mouse_press_pos.x(), self.mouse_press_pos.y(), 0, 0)
        self._selection_rect.show()

    def selecting(self, rect: QRectF):
        self._selection_rect.setRect(rect)
        selection = self.selectionArea()
        selection.clear()
        selection.addRect(rect)
        self.setSelectionArea(selection)

    def stop_selecting(self):
        self.selected_items = self.selectedItems()
        self._selection_rect.hide()

    def start_moving(self):
        if len(self.selectedItems()) > 0 and self.selectedItems()[0] not in self.selected_items:
            self.selected_items = self.selectedItems()

    def moving(self, event: QGraphicsSceneMouseEvent):
        if len(self.selectedItems()) > 0 and self.selectedItems()[0] in self.selected_items:
            for item in self.selected_items:
                delta = event.scenePos() - event.lastScenePos()
                item.moveBy(delta.x(), delta.y())

    def stop_moving(self, pos: QPointF):
        moved = pos - self.mouse_press_pos
        affected_frame_indexes = {}
        if moved.manhattanLength() > 0:
            if len(self.selectedItems()) > 0:
                for item in self.selectedItems():
                    index = item.index
                    self._particle_data.update_particle_by(self.current_frame_index, index, moved.x(), moved.y())
                    affected_frame_indexes = self._particle_data.affected_frame_indexes(index, self.current_frame_index)
                self.particle_updated_frame_index = {i for i in self.particle_updated_frame_index
                                                     if i < self.current_frame_index}
                # 更新影响到轨迹的帧
                self.trajectory_updated_frame_index -= affected_frame_indexes

    def add_particle(self):
        scene_pos = self.mouse_press_pos.toPoint()
        index, ok = QInputDialog.getInt(None, '输入', '粒子编号', 1)
        if ok:
            self.update_particle_pos(index, (scene_pos.x(), scene_pos.y()))
            # 更新影响到轨迹的帧
            self.trajectory_updated_frame_index -= self._particle_data.affected_frame_indexes(
                index, self.current_frame_index)

    def start_cropping(self):
        self._crop_rect.hide()
        self._crop_select_rect.setRect(self.mouse_press_pos.x(), self.mouse_press_pos.y(), 0, 0)
        self._crop_select_rect.show()

    def cropping(self, rect: QRectF):
        self._crop_select_rect.setRect(rect)

    def stop_cropping(self):
        self._crop_select_rect.hide()
        self._crop_rect.setRect(self._crop_select_rect.rect())
        self._crop_rect.show()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super(VideoScene, self).mousePressEvent(event)
        self.mouse_press_pos = self.mouse_pos(event.scenePos())
        if self.mode == OperationMode.SELECT:
            self.start_selecting()
        if self.mode == OperationMode.MOVE:
            self.start_moving()
        elif self.mode == OperationMode.ADD:
            self.add_particle()
        elif self.mode == OperationMode.CROP:
            self.start_cropping()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super(VideoScene, self).mouseReleaseEvent(event)
        pos = self.mouse_pos(event.scenePos())
        if self.mode == OperationMode.SELECT:
            self.stop_selecting()
        elif self.mode == OperationMode.MOVE:
            self.stop_moving(pos)
        elif self.mode == OperationMode.ADD:
            pass
        if self.mode == OperationMode.CROP:
            self.stop_cropping()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super(VideoScene, self).mouseMoveEvent(event)
        bg_rect = self.current_frame_item.boundingRect()
        pos = event.scenePos()
        x1 = self.mouse_press_pos.x()
        y1 = self.mouse_press_pos.y()
        x2 = max(bg_rect.left(), min(pos.x(), bg_rect.right()))
        y2 = max(bg_rect.top(), min(pos.y(), bg_rect.bottom()))
        rect = QRectF(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
        if self.mode == OperationMode.SELECT:
            self.selecting(rect)
        elif self.mode == OperationMode.MOVE:
            self.moving(event)
        elif self.mode == OperationMode.CROP:
            self.cropping(rect)

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
                self.particle_updated_frame_index = {i for i in self.particle_updated_frame_index if
                                                     i < self.current_frame_index}
                self.calc_trajectory()

        super(VideoScene, self).keyPressEvent(event)

    def mouse_pos(self, real_pos: QPointF) -> QPointF:
        bg_rect = self.current_frame_item.boundingRect()
        if bg_rect.contains(real_pos):
            return real_pos
        x = max(bg_rect.left(), min(real_pos.x(), bg_rect.right()))
        y = max(bg_rect.top(), min(real_pos.y(), bg_rect.bottom()))
        return QPointF(x, y)
