from typing import Dict, Tuple, List, Set

from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QLineF, QPointF
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QLinearGradient
from PySide6.QtWidgets import *

import default_settings
from base import EnhancedMap
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


class TrajectoryLine(QLineF):
    def __init__(self, frame_index: int, index: int, last_frame_index: int, last_speed: float, next_speed: float,
                 *args):
        super(TrajectoryLine, self).__init__(*args)
        self._frame_index = frame_index
        self._index = index
        self._last_frame_index = last_frame_index
        self._last_speed = last_speed
        self._next_speed = next_speed

    def speed(self, fps: int):
        return self.length() / (self._frame_index - self._last_frame_index) * fps

    @property
    def last_speed(self):
        return self._last_speed

    @property
    def next_speed(self):
        return self._next_speed

    @property
    def index(self):
        return self._index

    @property
    def frame_index(self):
        return self._frame_index


class ParticlePoint(QPointF):
    def __init__(self, frame_index: int, index: int, *args):
        super(ParticlePoint, self).__init__(*args)
        self.frame_index = frame_index
        self.index = index


class ColorHelper(object):
    def __init__(self, colors: List[QColor], min_speed: float, max_speed: float):
        self.duration = 1000
        self.colors = colors
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.animation = self.init_property_animation()

    def init_property_animation(self):
        animation = QPropertyAnimation()
        animation.setEasingCurve(QEasingCurve.Linear)
        animation.setDuration(self.duration)
        size = len(self.colors)
        for i, color in enumerate(self.colors):
            animation.setKeyValueAt(i / (size - 1), color)
        return animation

    def color_at(self, speed: float):
        ratio = (speed - self.min_speed) / (self.max_speed - self.min_speed) if self.max_speed != self.min_speed else 0
        self.animation.setCurrentTime(ratio * self.duration)
        return self.animation.currentValue()


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
            pen = self.particle_pen(index)
            pen.setWidth(self.settings.int_value(default_settings.trajectory_size))
            return pen
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

    def trajectory_speed_pen(self, helper: ColorHelper, line: TrajectoryLine):
        pen = QPen()
        fps = self.settings.int_value(default_settings.fps)
        speed = line.speed(fps)
        start_speed = speed if line.last_speed is None else (line.last_speed + speed) / 2
        end_speed = speed if line.next_speed is None else (line.next_speed + speed) / 2
        start_color = helper.color_at(start_speed)
        middle_color = helper.color_at(speed)
        end_color = helper.color_at(end_speed)
        gradient = QLinearGradient(line.p1(), line.p2())
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(0.5, middle_color)
        gradient.setColorAt(1, end_color)
        brush = QBrush(gradient)
        pen.setBrush(brush)
        pen.setWidth(self.settings.int_value(default_settings.trajectory_size))
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        pen.setStyle(Qt.SolidLine)
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
        # if self.setting_helper.visible(default_settings.show_particle, index):
        self.particle = ParticleItem(settings, index, x, y)
        self.addToGroup(self.particle)
        # if self.setting_helper.visible(default_settings.show_mark, index):
        self.mark = MarkItem(settings, index, x, y)
        self.addToGroup(self.mark)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)


class TrajectoryItem(QGraphicsLineItem):
    def __init__(self, settings: Settings, frame_index: int, index: int, line: TrajectoryLine):
        super().__init__(line)
        self.settings = settings
        self.frame_index = frame_index
        self.index = index
        self.line = line
        self.settings_helper = SettingWidgetHelper(settings)
        self.setLine(line)
        self.update_pen()

    def update_pen(self):
        if self.settings.boolean_value(default_settings.enable_trajectory_speed_color):
            speed_colors = self.settings.list_value(default_settings.trajectory_speed_color)
            max_speed = self.settings.float_value(default_settings.max_speed)
            min_speed = self.settings.float_value(default_settings.min_speed)
            color_helper = ColorHelper(speed_colors, min_speed, max_speed)
            self.setPen(self.settings_helper.trajectory_speed_pen(color_helper, self.line))
        else:
            self.setPen(self.settings_helper.trajectory_pen(self.index))


class CropRectItem(QGraphicsRectItem):
    handle_top_left = 1
    handle_top_middle = 2
    handle_top_right = 3
    handle_middle_left = 4
    handle_middle_right = 5
    handle_bottom_left = 6
    handle_bottom_middle = 7
    handle_bottom_right = 8

    handle_cursors = {
        handle_top_left: Qt.SizeFDiagCursor,
        handle_top_middle: Qt.SizeVerCursor,
        handle_top_right: Qt.SizeBDiagCursor,
        handle_middle_left: Qt.SizeHorCursor,
        handle_middle_right: Qt.SizeHorCursor,
        handle_bottom_left: Qt.SizeBDiagCursor,
        handle_bottom_middle: Qt.SizeVerCursor,
        handle_bottom_right: Qt.SizeFDiagCursor
    }

    def __init__(self, settings: Settings, parent=None):
        super(CropRectItem, self).__init__(parent)
        self.settings = settings
        self.handles = {}
        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        print(type(event))
        print('enter')

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(event)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent):
        if self.isSelected():
            handle = self.handleAt(event.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handle_cursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.handle_selected is not None:
            self.interactiveResize(event.pos())
        else:
            super().mouseMoveEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handle_selected is not None:
            self.interactiveResize(event.pos())
        else:
            super().mouseMoveEvent(event)


class ParticleData(object):
    """
    存储每帧粒子位置信息、配置信息
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.setting_helper = SettingWidgetHelper(settings)
        # row_index 是 粒子编号
        # col_index 是 帧序号
        self._point_data = EnhancedMap()

    def frame_indexes(self):
        return self._point_data.col_keys()

    def indexes(self):
        return self._point_data.row_keys()

    def update_frame_particles(self, frame_index: int, pos: Dict[int, Tuple[float, float]]):
        point_map = {}
        for index, (x, y) in pos.items():
            point_map[index] = ParticlePoint(frame_index, index, x, y)
        self._point_data.add_col(frame_index, point_map)

    def update_particle(self, frame_index: int, index: int, x: float, y: float):
        self._point_data.set_data(row=index, col=frame_index, data=ParticlePoint(frame_index, index, x, y))

    def update_particle_by(self, frame_index: int, index: int, dx: float, dy: float):
        point = self._point_data.get_data(index, frame_index)
        point.setX(point.x() + dx)
        point.setY(point.y() + dy)

    def remove_particle(self, frame_index: int, index: int):
        self._point_data.remove_data(index, frame_index)

    def combine_particle(self, frame_index: int, indexes: set):
        min_index = min(indexes)
        index_list = list(indexes)
        index_list.sort(reverse=True)

        point_map = self._point_data.col(frame_index)
        exist_indexes = indexes & point_map.keys()
        if len(exist_indexes) == 0 or (len(exist_indexes) == 1 and list(exist_indexes)[0] == min_index):
            return
        max_index = max(exist_indexes)
        # 合并粒子时，通常认为是同一粒子，那么同时出现多个编号时，最大的应该最接近真实粒子位置
        self._point_data.set_data(min_index, frame_index, point_map[max_index])
        exist_indexes -= {min_index}
        for index in exist_indexes:
            self._point_data.remove_data(index, frame_index)

    def line(self, frame_index: int, index: int):
        fps = self.settings.int_value(default_settings.fps)
        point_linked_map = self._point_data.row(index)
        if not point_linked_map or frame_index not in point_linked_map:
            return None
        node = point_linked_map.node(frame_index)
        prev_node = node.prev_node
        next_node = node.next_node
        if not prev_node:
            return None
        second_prev_node = prev_node.prev_node
        if second_prev_node:
            prev_speed = QLineF(second_prev_node.item, prev_node.item).length() / (
                    prev_node.index - second_prev_node.index) * fps
        else:
            prev_speed = None
        if next_node:
            next_speed = QLineF(next_node.item, node.item).length() / (next_node.index - node.index) * fps
        else:
            next_speed = None
        return TrajectoryLine(frame_index, index, prev_node.index, prev_speed, next_speed, prev_node.item, node.item)

    def line_map_of_frame(self, frame_index: int):
        line_map = {}
        for index, point_linked_map in self._point_data.row_items():
            if point_linked_map.head and point_linked_map.head.index < frame_index:
                line = self.line(frame_index, index)
                if line:
                    line_item = TrajectoryItem(self.settings, frame_index, index, line)
                    line_map[index] = line_item
        return line_map

    def particle_map_of_frame(self, frame_index: int):
        particle_item_map = {}
        point_map = self._point_data.col(frame_index)
        if point_map is None or len(point_map) == 0:
            return particle_item_map
        for index, point in point_map.items():
            # if self.setting_helper.visible(default_settings.show_particle, index) or \
            #         self.setting_helper.visible(default_settings.show_mark, index):
            group = ParticleGroup(self.settings, index, point.x(), point.y())
            particle_item_map[index] = group
        return particle_item_map

    def particle_next_frame_index(self, index, frame_index):
        all_particle_frame_index = self._point_data.row(index).sorted_indexes()
        after_frame_index = [x for x in all_particle_frame_index if x > frame_index]
        return after_frame_index[0] if len(after_frame_index) > 0 else None

    def affected_frame_indexes(self, index, frame_index) -> Set:
        next_frame_index = self.particle_next_frame_index(index, frame_index)
        return {frame_index} if next_frame_index is None else {frame_index, next_frame_index}

    def clear(self):
        self._point_data.clear()
