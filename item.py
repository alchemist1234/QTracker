from typing import Dict, Optional, List, Set

import numpy as np
from PySide2.QtCore import Qt, QLineF, QPoint, QPropertyAnimation, QEasingCurve, QSize, QPointF
from PySide2.QtGui import QImage, QPixmap, QBrush, QFont, QPen, QColor
from PySide2.QtWidgets import *

from utils import color_pixmap


class TrajectoryEntry(object):
    def __init__(self, index: int, frame_index: int, x1: float, y1: float, x2: float, y2: float, time_delta: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self. y2 = y2
        self.index = index
        self.line = QLineF(x1, y1, x2, y2)
        self.frame_index = frame_index
        self.time_delta = time_delta

    def line_item(self) -> QGraphicsLineItem:
        return QGraphicsLineItem(self.line)

    def speed(self):
        return self.line.length() / self.time_delta


class SceneConfig(object):

    def __init__(self, fps: int):
        # global
        self._particle_filter = set()
        self._crop_size = None
        self._fps = fps
        # particle
        self._particle_version = 0
        self._particle_colors = [Qt.green]
        self._particle_radius = 4
        self._show_particle = True
        # mark
        self._mark_version = 0
        self._mark_colors = [Qt.red]
        self._mark_size = 4
        self._mark_font = QFont('SimHei')
        self._show_mark = True
        self._same_mark_color_with_particle = False
        # frame
        self._frame_version = 0
        self._show_frame = False
        self._frame_size = 4
        self._frame_color = Qt.blue
        self._frame_font = QFont('SimHei')
        # trajectory
        self._trajectory_style_version = 0
        self._trajectory_data_version = 0
        self._trajectories = {}
        self._trajectory_colors = [Qt.blue]
        self._trajectory_style = Qt.SolidLine
        self._same_trajectory_color_with_particle = False
        self._trajectory_size = 2
        self._show_trajectory = True
        self._trajectory_speed_color = QPropertyAnimation()
        self._trajectory_speed_color.setEasingCurve(QEasingCurve.Linear)
        self._trajectory_speed_color.setDuration(100)
        self._trajectory_speed_color.setKeyValues([(0, Qt.blue), (0.5, Qt.yellow), (1, Qt.red)])
        self._active_speed_color = False
        self._speed_lower_limit = 0
        self._speed_upper_limit = 1

    @property
    def fps(self):
        return self._fps

    @property
    def particle_version(self):
        return self._particle_version

    @property
    def mark_version(self):
        return self._mark_version

    @property
    def frame_version(self):
        return self._frame_version

    @property
    def trajectory_style_version(self):
        return self._trajectory_style_version

    @property
    def trajectory_data_version(self):
        return self._trajectory_data_version

    @property
    def particle_filter(self):
        return self._particle_filter

    @particle_filter.setter
    def particle_filter(self, value: Set[int]):
        self._particle_filter = value
        self._particle_version += 1
        self._mark_version += 1
        self._trajectory_style_version += 1

    @property
    def crop_size(self):
        return self._crop_size

    @crop_size.setter
    def crop_size(self, value: Optional[QSize]):
        self._crop_size = value

    @property
    def particle_colors(self):
        return self._particle_colors

    @particle_colors.setter
    def particle_colors(self, value: List[QColor]):
        self._particle_colors = value
        self._particle_version += 1
        self._mark_version += 1
        self._trajectory_style_version += 1

    @property
    def particle_radius(self):
        return self._particle_radius

    @particle_radius.setter
    def particle_radius(self, value: int):
        self._particle_radius = value
        self._particle_version += 1

    @property
    def show_particle(self):
        return self._show_particle

    @show_particle.setter
    def show_particle(self, value: bool):
        self._show_particle = value
        self._particle_version += 1

    @property
    def mark_colors(self):
        return self._mark_colors

    @mark_colors.setter
    def mark_colors(self, value: List[QColor]):
        self._mark_colors = value
        self._mark_version += 1

    @property
    def mark_size(self):
        return self._mark_size

    @mark_size.setter
    def mark_size(self, value: int):
        self._mark_size = value
        self._mark_version += 1

    @property
    def mark_font(self):
        return self._mark_font

    @mark_font.setter
    def mark_font(self, value: QFont):
        self._mark_font = value
        self._mark_version += 1

    @property
    def show_mark(self):
        return self._show_mark

    @show_mark.setter
    def show_mark(self, value: bool):
        self._show_mark = value
        self._mark_version += 1

    @property
    def same_mark_color_with_particle(self):
        return self._same_mark_color_with_particle

    @same_mark_color_with_particle.setter
    def same_mark_color_with_particle(self, value: bool):
        self._same_mark_color_with_particle = value
        self._mark_version += 1

    @property
    def show_frame(self):
        return self._show_frame

    @show_frame.setter
    def show_frame(self, value: bool):
        self._show_frame = value
        self._frame_version += 1

    @property
    def frame_size(self):
        return self._frame_size

    @frame_size.setter
    def frame_size(self, value: int):
        self._frame_size = value
        self._frame_version += 1

    @property
    def frame_color(self):
        return self._frame_color

    @frame_color.setter
    def frame_color(self, value: QColor):
        self._frame_color = value
        self._frame_version += 1

    @property
    def frame_font(self):
        return self._frame_font

    @frame_font.setter
    def frame_font(self, value: QFont):
        self._frame_font = value
        self._frame_version += 1

    @property
    def trajectories(self):
        return self._trajectories

    # @trajectories.setter
    # def trajectories(self, value: Dict[int, Dict[int, QPoint]]):
    #     self.init_trajectory(value)
    #     self._trajectory_version += 1

    @property
    def trajectory_colors(self):
        return self._trajectory_colors

    @trajectory_colors.setter
    def trajectory_colors(self, value: List[QColor]):
        self._trajectory_colors = value
        self._trajectory_style_version += 1

    @property
    def trajectory_style(self):
        return self._trajectory_style

    @trajectory_style.setter
    def trajectory_style(self, value: Qt.BrushStyle):
        self._trajectory_style = value
        self._trajectory_style_version += 1

    @property
    def same_trajectory_color_with_particle(self):
        return self._same_trajectory_color_with_particle

    @same_trajectory_color_with_particle.setter
    def same_trajectory_color_with_particle(self, value: bool):
        self._same_trajectory_color_with_particle = value
        self._trajectory_style_version += 1

    @property
    def active_speed_color(self):
        return self._active_speed_color

    @active_speed_color.setter
    def active_speed_color(self, value: bool):
        self._active_speed_color = value
        self._trajectory_style_version += 1

    @property
    def trajectory_size(self):
        return self._trajectory_size

    @trajectory_size.setter
    def trajectory_size(self, value: int):
        self._trajectory_size = value
        self._trajectory_style_version += 1

    @property
    def show_trajectory(self):
        return self._show_trajectory

    @show_trajectory.setter
    def show_trajectory(self, value: bool):
        self._show_trajectory = value
        self._trajectory_style_version += 1

    @property
    def trajectory_speed_color(self):
        return self._trajectory_speed_color

    @trajectory_speed_color.setter
    def trajectory_speed_color(self, value: List[QColor]):
        key_values = [(1.0 / i, v) for i, v in enumerate(value)]
        self._trajectory_speed_color.setKeyValues(key_values)
        self._trajectory_style_version += 1

    @property
    def speed_lower_limit(self):
        return self._speed_lower_limit

    @speed_lower_limit.setter
    def speed_lower_limit(self, value: float):
        self._speed_lower_limit = value
        self._trajectory_style_version += 1

    @property
    def speed_upper_limit(self):
        return self._speed_upper_limit

    @speed_upper_limit.setter
    def speed_upper_limit(self, value: float):
        self._speed_upper_limit = value
        self._trajectory_style_version += 1

    def init_trajectories(self, fps: int, points: Dict[int, Dict[int, QPoint]]):
        self._fps = fps
        last_x = {}
        last_y = {}
        last_frame_index = {}
        time_delta = 1.0 / fps
        frame_indexes = list(points.keys())
        frame_indexes.sort()
        for frame_index in frame_indexes:
            point_dict = points[frame_index]
            for index, point in point_dict.items():
                x = point.x()
                y = point.y()
                if last_x.get(index, None) is not None:
                    entry = TrajectoryEntry(index, frame_index, last_x[index], last_y[index], x, y,
                                            time_delta * (frame_index - last_frame_index[index]))
                    if index in self.trajectories:
                        self.trajectories[index][frame_index] = entry
                    else:
                        self.trajectories[index] = {frame_index: entry}
                last_x[index] = x
                last_y[index] = y
                last_frame_index[index] = frame_index
        self._trajectory_data_version += 1
        self._trajectory_style_version += 1

    def visible(self, show: bool, index: int):
        """
        is item visible
        :param show: from self.show_mark or self.show_frame or self.show particle and others
        :param index: particle index
        :return: bool
        """
        return show and (index in self.particle_filter or len(self.particle_filter) == 0)

    def particle_brush(self, index: int):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.particle_colors[index % len(self.particle_colors)])
        return brush

    def particle_pen(self, index: int):
        pen = QPen()
        pen.setColor(self.particle_colors[index % len(self.particle_colors)])
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(0)
        return pen

    def mark_brush(self, index: int):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        if self.same_mark_color_with_particle:
            colors = self.particle_colors
        else:
            colors = self.mark_colors
        brush.setColor(colors[index % len(colors)])
        return brush

    def trajectory_pen(self, index: int, trajectory_index: int = None):
        pen = QPen()
        pen.setStyle(self.trajectory_style)
        pen.setWidth(self.trajectory_size)
        if not self.active_speed_color or trajectory_index is None:
            if self.same_trajectory_color_with_particle:
                colors = self.particle_colors
            else:
                colors = self.trajectory_colors
            pen.setColor(colors[index % len(colors)])
        else:
            pen.setColor(self.speed_color(index, trajectory_index))
        return pen

    def speed_color(self, index: int, trajectory_index: int):
        speeds = [t.entries.speed() for t in self.trajectories[index]]
        max_speed = max(speeds)
        min_speed = min(speeds)
        speed_upper = (max_speed - min_speed) * self.speed_upper_limit + min_speed
        speed_lower = (max_speed - min_speed) * self.speed_lower_limit + min_speed
        index_speed = speeds[trajectory_index]
        ratio = (index_speed - speed_lower) / (speed_upper - speed_lower)
        self.trajectory_speed_color.setCurrentTime(100 * ratio)
        return self.trajectory_speed_color.currentValue()

    def trajectory_groups(self, current_frame_index: int) -> Dict[int, QGraphicsItemGroup]:
        groups = {}
        for index, trajectory_dict in self.trajectories.items():
            g = QGraphicsItemGroup()
            for frame_index, trajectory in trajectory_dict.items():
                if frame_index <= current_frame_index:
                    line_item = trajectory.line_item()
                    pen = self.trajectory_pen(index, frame_index)
                    line_item.setPen(pen)
                    g.addToGroup(line_item)
                    groups[index] = g
        return groups
        # print(f'create traj groups: {frame_index}')
        # group = QGraphicsItemGroup()
        # indexes = set(self.trajectories.keys())
        # if len(self._particle_filter) > 0:
        #     indexes = indexes & self._particle_filter
        # groups = {}
        # for index in indexes:
        #     entry_dict = self.trajectories[index]
        #     entries = [entry_dict[i] for i in entry_dict if i <= frame_index]
        #     for e in entries:
        #         pen = self.trajectory_pen(e.index, frame_index)
        #         line = QGraphicsLineItem(e.line)
        #         line.setPen(pen)
        #         group.addToGroup(line)
        #     groups[index] = group
        # print(f'frame {frame_index} trajectory {len(groups)} updated')
        return groups


class ParticleItem(QGraphicsEllipseItem):
    default_color = Qt.green
    default_radius = 4

    def __init__(self, frame_index: int, index: int, center_x, center_y, config: SceneConfig):
        self.frame_index = frame_index
        self.index = index
        radius = config.particle_radius
        brush = config.particle_brush(index)
        pen = config.particle_pen(index)
        super(ParticleItem, self).__init__(center_x - radius, center_y - radius, radius * 2, radius * 2)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setToolTip(str(index))
        self.setBrush(brush)
        self.setPen(pen)
        self.mark = None

    def attach_mark(self, mark):
        self.mark = mark

    def center(self) -> QPoint:
        rect = self.rect()
        return QPoint(rect.x() + rect.width() / 2, rect.y() + rect.height() / 2)


class MarkItem(QGraphicsSimpleTextItem):
    default_color = Qt.red
    default_font_family = 'SimHei'
    # default particle radius, for calculate mark position
    default_radius = 4

    def __init__(self, frame_index: int, index: int, mark: str, center_x, center_y, config: SceneConfig):
        self.frame_index = frame_index
        self.index = index
        self.particle = None
        radius = config.particle_radius
        brush = config.mark_brush(index)
        font = config.mark_font
        super(MarkItem, self).__init__(mark)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFont(font)
        self.setBrush(brush)
        x = center_x - radius - self.boundingRect().width()
        y = center_y - radius - self.boundingRect().height()
        if x < 0:
            x = center_x + radius
        if y < 0:
            y = center_y + radius
        self.setX(x)
        self.setY(y)

    def attach_particle(self, particle):
        self.particle = particle

    @classmethod
    def default_font(cls):
        font = QFont(cls.default_font_family)
        font.setBold(True)
        return font


class ParticleGroup(QGraphicsItemGroup):
    def __init__(self, frame_index: int, index: int, center_x, center_y, config: SceneConfig):
        super(ParticleGroup, self).__init__()
        self.setX(center_x)
        self.setY(center_y)
        self.particle = ParticleItem(frame_index, index, center_x, center_y, config)
        self.mark = MarkItem(frame_index, index, str(index), center_x, center_y, config)
        self.particle.attach_mark(self.mark)
        self.mark.attach_particle(self.particle)
        self.index = index
        self.addToGroup(self.particle)
        self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)


class FrameItem(QGraphicsPixmapItem):
    def __init__(self, frame_index: int, frame: np.ndarray):
        self.frame_index = frame_index
        super(FrameItem, self).__init__()
        origin_h, origin_w, ch = frame.shape
        img = QImage(frame.data, origin_w, origin_h, ch * origin_w, QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(img))


class ColorWidget(QWidget):
    def __init__(self, color: QColor, height: int):
        super().__init__()
        self.margin = 2
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        self.layout.setMargin(self.margin)
        self.layout.setSpacing(0)
        self.color = color
        self.color_name = QColor(color).name()
        self.lb_color = QLabel()
        self.lb_color.setFixedSize(64, height - 2 * self.margin)
        self.lb_color.setPixmap(color_pixmap(self.lb_color.width(), self.lb_color.height(), [color]))
        self.lb_color_name = QLabel()
        self.lb_color_name.setText(self.color_name)
        self.layout.addWidget(self.lb_color)
        self.layout.addWidget(self.lb_color_name)
        self.layout.addItem(QSpacerItem(20, height, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)

    def update_color(self, color: QColor):
        self.color = color
        self.color_name = QColor(color).name()
        self.lb_color.setPixmap(color_pixmap(self.lb_color.width(), self.lb_color.height(), [color]))
        self.lb_color_name.setText(self.color_name)
