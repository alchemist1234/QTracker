from PySide2.QtWidgets import *
from PySide2.QtGui import QImage, QPainter

from data import FrameData
from enums import OperationMode
from item import ParticleGroup, SceneConfig
from exporter import VideoExporter


class VideoScene(QGraphicsScene):

    def __init__(self, parent: QGraphicsView, frame_index: int, frame_data: FrameData):
        super(VideoScene, self).__init__(parent)
        # config versions
        self.particle_version = -1
        self.mark_version = -1
        self.frame_version = -1
        self.trajectory_style_version = -1
        self.trajectory_data_version = -1
        self.view = parent
        self.frame_index = frame_index
        self.frame_item = frame_data.get_frame_item(self.view.scene_config)
        self.particle_items = frame_data.get_particle_items(self.view.scene_config)
        self.trajectory_items = {}
        self.addItem(self.frame_item)
        # self.operation_mode = OperationMode.SELECT
        for p in self.particle_items.values():
            self.addItem(p)

    def update_all(self, config: SceneConfig):
        if self.particle_version != config.particle_version:
            self.__update_particle(config)
        if self.mark_version != config.mark_version:
            self.__update_mark(config)
        if self.trajectory_data_version != config.trajectory_data_version:
            pass
        if self.trajectory_style_version != config.trajectory_style_version:
            print(f'update traj: {self.frame_index}')
            self.__update_trajectories(config)

    def __update_particle(self, config: SceneConfig):
        self.particle_version = config.particle_version
        radius = config.particle_radius
        for item in self.particle_items.values():
            particle = item.particle
            # brush
            brush = config.particle_brush(particle.index)
            particle.setBrush(brush)
            # pen
            pen = config.particle_pen(particle.index)
            particle.setPen(pen)
            # size
            rect = particle.rect()
            center_x = rect.x() + rect.width() / 2
            center_y = rect.y() + rect.height() / 2
            particle.setRect(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
            # visible
            particle.show() if config.visible(config.show_particle, particle.index) else particle.hide()

    def __update_mark(self, config: SceneConfig):
        self.mark_version = config.mark_version
        for item in self.particle_items.values():
            mark = item.mark
            # brush
            brush = config.mark_brush(mark.index)
            mark.setBrush(brush)
            # font
            mark.setFont(config.mark_font)
            # visible
            mark.show() if config.visible(config.show_mark, mark.index) else mark.hide()

    def __update_trajectories(self, config: SceneConfig):
        self.trajectory_style_version = config.trajectory_style_version
        self.clear_trajectories()
        self.trajectory_items = config.trajectory_groups(self.frame_index)
        for index, trajectory_item in self.trajectory_items.items():
            self.addItem(trajectory_item)

    def clear_trajectories(self):
        for t in self.trajectory_items.values():
            self.removeItem(t)
        self.trajectory_items = {}

    def remove_particles(self, indexes: set):
        for i in indexes:
            item = self.particle_items.pop(i)
            self.removeItem(item)
            self.destroyItemGroup(item)

    def combine_particles(self, indexes: set):
        exist_indexes = indexes & self.particle_items.keys()
        if len(exist_indexes) == 0:
            return
        else:
            self._combine_particles(exist_indexes, min(indexes))

    def _combine_particles(self, exist_indexes, min_index):
        groups = [self.particle_items[i] for i in exist_indexes]
        bounding_rects = [g.particle.boundingRect() for g in groups]
        particle_x = sum([r.x() + r.width() / 2 for r in bounding_rects]) / len(exist_indexes)
        particle_y = sum([r.y() + r.height() / 2 for r in bounding_rects]) / len(exist_indexes)
        new_group = ParticleGroup(self.frame_index, min_index, particle_x, particle_y, self.view.scene_config)
        self.remove_particles(exist_indexes)
        self.addItem(new_group)
        self.particle_items[min_index] = new_group

    def add_particle(self, index: int, x: float, y: float):
        new_group = ParticleGroup(self.frame_index, index, x, y, self.view.scene_config)
        if index in self.particle_items.keys():
            ret = QMessageBox.information(None, '提示', f'当前帧已存在粒子{index}, 继续添加会覆盖原粒子, 是否继续?',
                                          QMessageBox.Cancel, QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                return
            self.remove_particles({index})
        self.addItem(new_group)
        self.particle_items[index] = new_group

    def snapshot(self, config: SceneConfig):
        self.update_all(config)
        print(f'snapshot: {self.frame_index}')
        image = QImage(config.crop_size, QImage.Format_ARGB32)
        painter = QPainter()
        painter.begin(image)
        print(f'render begin: {self.frame_index}')
        self.render(painter)
        painter.end()
        print(f'render end: {self.frame_index}')
        return image

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.operation_mode == OperationMode.SELECT:
            super(VideoScene, self).mousePressEvent(event)

    #     if event.button() != Qt.LeftButton:
    #         return
    #     self.clearSelection()
    #     scene_pos = event.scenePos()
    #     transform = self.view.transform()
    #     item = self.itemAt(scene_pos, transform)
    #     print(item, item.isSelected())
    #     item.setSelected(True)
    #     # print(item.flags())
    #     item.mousePressEvent(event)
    #     super(VideoScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print('scene move event')
        # if event.button() != Qt.LeftButton:
        #     return
        for item in self.selectedItems():
            print('selected item', item)
            item.mouseMoveEvent(event)
        super(VideoScene, self).mouseMoveEvent(event)
