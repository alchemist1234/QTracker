from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import QGraphicsItemGroup


class TrajectoryGenerator(QThread):
    sig_group_generated = Signal(int, dict)

    def __init__(self, frame_index: int, scene_config):
        super().__init__()
        self.frame_index = frame_index
        self.scene_config = scene_config

    def run(self) -> None:
        groups = {}
        for index, trajectory_dict in self.scene_config.trajectories.items():
            g = QGraphicsItemGroup()
            for frame_index, trajectory in trajectory_dict.items():
                if frame_index <= self.frame_index:
                    line_item = trajectory.line_item()
                    pen = self.scene_config.trajectory_pen(index, frame_index)
                    line_item.setPen(pen)
                    g.addToGroup(line_item)
                    groups[index] = g
        self.sig_group_generated.emit(self.frame_index, groups)
