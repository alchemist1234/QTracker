from typing import Dict, Tuple
import math

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from PySide6.QtWidgets import *

import default_settings
from settings import Settings


class VideoData(object):
    """
    视频基础数据
    """

    def __init__(self):
        # 文件路径
        self._file_path = None
        # FPS
        self._fps = 0
        # 视频宽度
        self._width = 0
        # 视频高度
        self._height = 0
        # 总帧数
        self._frames = 0

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self._file_path = file_path

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps: int):
        self._fps = fps

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def frame_count(self):
        return self._frames

    @frame_count.setter
    def frame_count(self, frames: int):
        self._frames = frames


class SettingWidgetHelper(object):
    def __init__(self, settings: Settings):
        self.settings = settings

    def particle_brush(self, index: int):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        colors = self.settings.list_value(default_settings.particle_color)
        colors = [QColor(c) for c in colors]
        brush.setColor(colors[index % len(colors)])
        return brush

    def particle_pen(self, index: int):
        pen = QPen()
        colors = self.settings.list_value(default_settings.particle_color)
        colors = [QColor(c) for c in colors]
        pen.setColor(colors[index % len(colors)])
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(0)
        return pen

    def mark_brush(self, index: int):
        if self.settings.boolean_value(default_settings.same_mark_color_with_particle):
            return self.particle_brush(index)
        else:
            brush = QBrush()
            colors = self.settings.list_value(default_settings.mark_color)
            colors = [QColor(c) for c in colors]
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(colors[index % len(colors)])
            return brush

    def trajectory_pen(self, index: int):
        if self.settings.boolean_value(default_settings.same_trajectory_color_with_particle):
            return self.particle_pen(index)
        else:
            pen = QPen()
            colors = self.settings.list_value(default_settings.trajectory_color)
            colors = [QColor(c) for c in colors]
            pen.setStyle(Qt.SolidLine)
            pen.setColor(colors[index % len(colors)])
            pen.setWidth(self.settings.int_value(default_settings.trajectory_size))
            pen.setJoinStyle(Qt.RoundJoin)
            pen.setCapStyle(Qt.RoundCap)
            return pen

    def visible(self, setting_item: default_settings.setting_item, index: int):
        index_filter = self.settings.list_value(default_settings.index_filter)
        return self.settings.boolean_value(setting_item) and (index in index_filter or len(index_filter) == 0)


class ParticleItem(QGraphicsEllipseItem):

    def __init__(self, settings: Settings, index: int, x, y):
        radius = settings.int_value(default_settings.particle_size)
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.settings = settings
        self.settings_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setToolTip(str(index))
        self.setBrush(self.settings_helper.particle_brush(index))
        self.setPen(self.settings_helper.particle_pen(index))
        self.mark = None

    def center(self) -> QPoint:
        rect = self.rect()
        return QPoint(rect.x() + rect.width() / 2, rect.y() + rect.height() / 2)


class MarkItem(QGraphicsSimpleTextItem):
    def __init__(self, settings: Settings, index: int, center_x, center_y, prefix: str = '', suffix: str = ''):
        super().__init__(prefix + str(index) + suffix)
        self.settings = settings
        self.settings_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        font = QFont(self.settings.value(default_settings.mark_font))
        font.setPixelSize(self.settings.int_value(default_settings.mark_size))
        self.setFont(font)
        self.setBrush(self.settings_helper.mark_brush(index))
        radius = self.settings.int_value(default_settings.particle_size)
        x = center_x - radius - self.boundingRect().width()
        y = center_y - radius - self.boundingRect().height()
        if x < 0:
            x = center_x + radius
        if y < 0:
            y = center_y + radius
        self.setX(x)
        self.setY(y)


class ParticleGroup(QGraphicsItemGroup):
    def __init__(self, settings: Settings, index: int, x, y):
        super().__init__()
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        self.index = index
        self.setX(x)
        self.setY(y)
        if self.setting_helper.visible(default_settings.show_particle, index):
            self.particle = ParticleItem(settings, index, x, y)
            self.addToGroup(self.particle)
        if self.setting_helper.visible(default_settings.show_mark, index):
            self.mark = MarkItem(settings, index, x, y)
            self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)


class TrajectoryItem(QGraphicsLineItem):
    def __init__(self, settings: Settings, frame_index: int, index: int, x1, y1, x2, y2, frame_interval):
        super().__init__(x1, y1, x2, y2)
        self.settings = settings
        self.frame_index = frame_index
        self.index = index
        self.settings_helper = SettingWidgetHelper(settings)
        self.distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.frame_interval = frame_interval
        self.setPen(self.settings_helper.trajectory_pen(index))

    def update_pen(self):
        self.setPen(self.settings_helper.trajectory_pen(self.index))


class ParticleData(object):
    """
    一帧内的粒子数据
    """

    def __init__(self, settings: Settings, particle_pos: Dict[int, Tuple[int, int]]):
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        self._particle_pos = particle_pos
        self._trajectory_lines = {}

    @property
    def particle_pos(self) -> Dict[int, Tuple[int, int]]:
        return self._particle_pos

    @property
    def trajectory_lines(self) -> Dict[int, Tuple[int, int, int, int, int]]:
        return self._trajectory_lines

    def update_line(self, index, x1, y1, x2, y2, frame_interval):
        self._trajectory_lines[index] = (x1, y1, x2, y2, frame_interval)

    def update_particle(self, index: int, pos: Tuple[int, int]):
        self._particle_pos[index] = pos

    def update_particle_by(self, index: int, moved: Tuple[int, int]):
        if moved == (0, 0) or index not in self._particle_pos:
            return
        current_pos = self._particle_pos[index]
        self._particle_pos[index] = (current_pos[0] + moved[0], current_pos[1] + moved[1])

    def remove_particle(self, index: int):
        if index in self._particle_pos:
            del self._particle_pos[index]

    def remove_trajectory(self, index: int):
        if index in self._trajectory_lines:
            del self._trajectory_lines[index]

    def particle_group_items(self) -> Dict[int, ParticleGroup]:
        """
        获取粒子+标签字典
        :return: {粒子索引: ParticleGroup}
        """
        groups = {}
        for index, pos in self._particle_pos.items():
            if self.setting_helper.visible(default_settings.show_particle, index) or \
                    self.setting_helper.visible(default_settings.show_mark, index):
                particle_group = ParticleGroup(self.settings, index, pos[0], pos[1])
                groups[index] = particle_group
        return groups

    def trajectory_items(self, frame_index: int) -> Dict[int, QGraphicsLineItem]:
        items = {}
        for index, (x1, y1, x2, y2, frame_interval) in self._trajectory_lines.items():
            item = TrajectoryItem(self.settings, frame_index, index, x1, y1, x2, y2, frame_interval)
            items[index] = item
        return items
