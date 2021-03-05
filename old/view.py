from typing import Set, NoReturn, List

from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QWheelEvent, QMouseEvent, QColor, QImage
from PySide2.QtWidgets import *

from data import FrameData
from enums import OperationMode
from exporter import VideoExporter
from item import SceneConfig
from scene import VideoScene
from utils import split_indexes_text
from worker import TrajectoryGenerator


class VideoView(QGraphicsView):
    sig_update_scene = Signal(SceneConfig)
    sig_scene_updated = Signal(int)

    def __init__(self, fps: int, parent=None):
        super(VideoView, self).__init__(parent)
        self.appeared_indexes = set()
        self.scenes = {}
        self.current_scene_index = -1
        self.show_particle = True
        self.show_mark = True
        self.show_frame = True
        self.crop_size = None
        self.particle_color = Qt.green
        self.mark_color = Qt.red
        self.operation_mode = OperationMode.SELECT
        # TODO config init
        self.scene_config = SceneConfig(fps)

        self.updated_scenes = 0

    def add_scene(self, frame_index: int, frame_data: FrameData) -> NoReturn:
        scene = VideoScene(self, frame_index, frame_data)
        self.appeared_indexes.update(scene.particle_items.keys())
        self.scenes[frame_index] = scene

    def change_scene(self, frame_index: int) -> NoReturn:
        if frame_index in self.scenes:
            self.current_scene_index = frame_index
            self.update_scene(frame_index)
            self.setScene(self.scenes[frame_index])
            self.update_crop_size()

    def update_crop_size(self):
        if self.scene() is not None:
            self.scene_config.crop_size = self.scene().sceneRect().size().toSize()

    def set_show_mark(self, show: bool) -> NoReturn:
        self.scene_config.show_mark = show
        self.update_scene()

    def set_show_particle(self, show: bool) -> NoReturn:
        self.scene_config.show_particle = show
        self.update_scene()

    def set_show_frame(self, show: bool) -> NoReturn:
        self.scene_config.show_frame = show
        self.update_scene()

    def set_show_trajectory(self, show: bool) -> NoReturn:
        self.scene_config.show_trajectory = show
        self.update_scene()

    def set_trajectory_size(self, size: float) -> NoReturn:
        self.scene_config.trajectory_size = size
        self.update_scene()

    def set_trajectory_colors(self, colors: List[QColor]):
        self.scene_config.trajectory_colors = colors
        self.update_scene()

    def set_particle_color(self, color: QColor) -> NoReturn:
        self.scene_config.particle_colors = [color]
        self.update_scene()

    def set_mark_color(self, color: QColor) -> NoReturn:
        self.scene_config.mark_colors = [color]
        self.update_scene()

    def set_operation_mode(self, mode: OperationMode) -> NoReturn:
        self.operation_mode = mode

    @Slot(int)
    def update_scene(self, frame_index: int = None) -> NoReturn:
        self.sig_update_scene.emit(self.scene_config)
        # if frame_index is None:
        #     scene = self.scene()
        # else:
        #     scene = self.scenes[frame_index]
        # if scene is not None:
        #     scene.update_all(self.scene_config)

    @Slot(int, dict)
    def update_trajectory(self, frame_index: int, groups: dict):
        if frame_index in self.scenes:
            scene = self.scenes[frame_index]
            scene.update_trajectories(groups)

    def combine_particles(self) -> NoReturn:
        if self.scene() is None:
            return
        items = self.scene().selectedItems()
        if len(items) == 0:
            text, ok = QInputDialog.getText(self, "输入", "待合并的粒子编号(,或者空格分隔)", QLineEdit.Normal)
            if ok:
                indexes = split_indexes_text(text)
                self._combine_particles(indexes)
        else:
            indexes = {i.index for i in items}
            self._combine_particles(indexes)

    def _combine_particles(self, indexes: Set[int]) -> NoReturn:
        for s in self.scenes.values():
            s.combine_particles(indexes)
        self.change_scene(self.current_scene_index)

    def filter_particles(self, indexes: Set[int]) -> NoReturn:
        self.scene_config.particle_filter = indexes
        self.update_scene()

    def calc_trajectories(self, fps: int):
        point_dict = {
            frame_index: {index: group.particle.center() for index, group in scene.particle_items.items()} for
            frame_index, scene in self.scenes.items()}
        self.scene_config.init_trajectories(fps, point_dict)
        self.update_scene()

    def export_video(self, file_path: str, width: int, height: int):
        self.file_path = file_path
        self.width = width
        self.height = height
        self.sig_update_scene.emit(self.scene_config)
        self.sig_scene_updated.connect(self.fun2)

    def fun2(self):
        self.updated_scenes += 1
        if self.updated_scenes == len(self.scenes):
            export = VideoExporter(self.file_path, self.width, self.height, self.scenes, self.scene_config)
            export.start()

    def snapshot(self, file_name: str = None, index: int = None):
        if index is None and self.scene() is not None:
            image = self.scene().snapshot()
        elif index in self.scenes:
            scene = self.scenes[index]
            image = scene.snapshot(self.scene_config)
        else:
            return
        if file_name is not None:
            image.save(file_name)
        else:
            return image

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> NoReturn:
        print('view mouse move')
        scene = self.scene()
        if scene is None:
            return
        view_pos = event.pos()
        scene_pos = self.mapToScene(view_pos)
        transform = self.transform()
        item = scene.itemAt(scene_pos, transform)
        super(VideoView, self).mouseMoveEvent(event)
        # scene.mouseMoveEvent(event)
        # print(item)

    def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
        if self.scene() is None:
            return
        if self.operation_mode == OperationMode.ADD:
            view_pos = event.pos()
            scene_pos = self.mapToScene(view_pos)
            index, ok = QInputDialog.getInt(self, '输入', '待添加粒子编号', QLineEdit.Normal)
            if ok:
                self.current_scene.add_particle(index, scene_pos.x(), scene_pos.y())
            # scene = self.scene()
            # view_pos = event.pos()
            # scene_pos = self.mapToScene(view_pos)
            # transform = self.transform()
            # if scene is not None:
            #     item = scene.itemAt(scene_pos, transform)
            #     if item is not None:
            #         print(item)

    def wheelEvent(self, event: QWheelEvent) -> NoReturn:
        mouse_pos = event.pos()
        scene_pos = self.mapToScene(mouse_pos)
        view_w = self.viewport().width()
        view_h = self.viewport().height()
        h_scale = mouse_pos.x() / view_w
        v_scale = mouse_pos.y() / view_h

        scale_factor = self.matrix().m11()
        wheel_delta = event.delta()
        if wheel_delta > 0:
            self.scale(1.2, 1.2)
        else:
            self.scale(1 / 1.2, 1 / 1.2)
        view_point = self.matrix().map(scene_pos)
        self.horizontalScrollBar().setValue(view_point.x() - view_w * h_scale)
        self.verticalScrollBar().setValue(view_point.y() - view_h * v_scale)
