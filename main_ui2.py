import os
from typing import List

import cv2
from PySide2.QtCore import Qt, QObject, Signal, QThread, Slot, QSize, QModelIndex
from PySide2.QtGui import QFontMetrics, QResizeEvent, QPalette, QColor
from PySide2.QtWidgets import *

from config import cfg, ConfigName
from data import FrameData
from enums import OperationMode
from item import ColorWidget
from tracker import Tracker
from ui.ui_color_editor import Ui_ColorEditor
from ui.ui_main import Ui_MainWindow
from ui.ui_settings import Ui_dialog
from utils import split_indexes_text, color_pixmap
from view import VideoView


class CustomSignal(QObject):
    update_settings = Signal(int)


global_sig = CustomSignal()

AUTO_SEC = 'Auto'
COMMON_SEC = 'Common'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_path = None
        self.tracker = None
        self.frame_index = None
        self.frame = None
        self.particles = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_status_bar()
        self.init_file_tree()
        self.settings = Settings()
        self.th_video = Reader(self)
        self.ui.graphicsView = VideoView(self.th_video.fps, self.ui.widget)
        self.ui.horizontalLayout_7.addWidget(self.ui.graphicsView)
        self.ui.bt_select.setChecked(True)
        self.init_color_label()

        self.ui.bt_settings.clicked.connect(self.show_settings)
        self.ui.list_files.clicked.connect(self.clicked_file)
        self.ui.list_files.doubleClicked.connect(self.double_clicked_file)
        self.ui.bt_file_path_up.clicked.connect(self.clicked_file_path_up)
        self.ui.bt_start.clicked.connect(self.start)
        self.th_video.sig_read_finish.connect(self.read_video_finished)
        self.th_video.sig_read_progress.connect(self.read_video_progress)
        self.ui.sb_frames.valueChanged.connect(self.frame_changed)
        self.ui.cb_show_marks.stateChanged.connect(self.show_mark_changed)
        self.ui.cb_show_particles.stateChanged.connect(self.show_particle_changed)
        self.ui.bt_mark_color.clicked.connect(self.mark_color_clicked)
        self.ui.bt_particle_color.clicked.connect(self.particle_color_clicked)
        self.ui.bt_select.clicked.connect(lambda: self.update_mode(self.ui.bt_select))
        self.ui.bt_add.clicked.connect(lambda: self.update_mode(self.ui.bt_add))
        self.ui.bt_combine.clicked.connect(self.combine_particles)
        self.ui.bt_move.clicked.connect(lambda: self.update_mode(self.ui.bt_move))
        self.ui.bt_crop.clicked.connect(lambda: self.update_mode(self.ui.bt_crop))
        self.ui.le_particle_filter.textChanged.connect(self.particle_filter_changed)
        self.ui.bt_post.clicked.connect(self.calc_trajectories)
        self.ui.bt_export_video.clicked.connect(self.export_video)
        self.ui.cb_show_traj.stateChanged.connect(self.show_trajectory_changed)
        self.ui.dsb_traj_size.valueChanged.connect(self.set_trajectory_size)
        self.ui.bt_edit_traj_color.clicked.connect(self.edit_traj_color)

    def resizeEvent(self, event: QResizeEvent):
        self.update_file_path()

    def init_status_bar(self):
        self.ui.status_progress = QProgressBar(self.ui.statusbar)
        self.ui.status_progress.setRange(0, 100)
        self.ui.status_progress.setValue(0)
        self.ui.statusbar.addWidget(self.ui.status_progress)

    def init_file_tree(self):
        dir_path = cfg.get(COMMON_SEC, ConfigName.DIR_PATH.value)
        self.file_path = cfg.get(COMMON_SEC, ConfigName.FILE_PATH.value)
        filters = ['*.avi', '*.mp4', '*.mpeg']
        file_system_model = QFileSystemModel(self.ui.list_files)
        file_system_model.setRootPath(dir_path)
        file_system_model.setNameFilters(filters)
        file_system_model.setNameFilterDisables(False)
        index = file_system_model.index(dir_path)
        self.ui.list_files.setModel(file_system_model)
        self.ui.list_files.setRootIndex(index)
        self.ui.list_files.setCurrentIndex(index)
        self.update_file_path()

    def init_color_label(self):
        label = self.ui.lb_traj_color
        width = label.width()
        height = label.height()
        colors = self.ui.graphicsView.scene_config.trajectory_colors
        pixmap = color_pixmap(width, height, colors)
        label.setPixmap(pixmap)

    def double_clicked_file(self, index):
        model = self.ui.list_files.model()
        path = model.filePath(index)
        if os.path.isdir(path):
            self.ui.list_files.setRootIndex(index)
            cfg.set(COMMON_SEC, ConfigName.DIR_PATH.value, path)
            cfg.flush()
            self.update_file_path()

    def show_settings(self):
        self.settings.exec_()

    def clicked_file_path_up(self):
        dir_path = cfg.get(COMMON_SEC, ConfigName.DIR_PATH.value)
        parent, _ = os.path.split(dir_path)
        parent_index = self.ui.list_files.model().index(parent)
        cfg.set(COMMON_SEC, ConfigName.FILE_PATH.value, '')
        cfg.set(COMMON_SEC, ConfigName.DIR_PATH.value, parent)
        self.ui.list_files.setCurrentIndex(parent_index)
        self.ui.list_files.setRootIndex(parent_index)
        cfg.flush()
        self.file_path = None
        self.update_file_path()

    def clicked_file(self, index):
        file_path = self.ui.list_files.model().filePath(index)
        if os.path.isfile(file_path):
            self.file_path = file_path
            cfg.set(COMMON_SEC, ConfigName.FILE_PATH.value, file_path)
            cfg.flush()
            self.update_file_path()

    def update_file_path(self):
        dir_path = cfg.get(COMMON_SEC, ConfigName.DIR_PATH.value)
        file_path = cfg.get(COMMON_SEC, ConfigName.FILE_PATH.value)
        if file_path is not None and len(file_path) > 0:
            text = file_path
        else:
            text = dir_path
        font_metrics = QFontMetrics(self.ui.lb_file_path.font())
        elide_text = font_metrics.elidedText(text, Qt.ElideMiddle, self.ui.lb_file_path.width())
        self.ui.lb_file_path.setText(elide_text)
        self.ui.lb_file_path.setToolTip(text)

    def start(self):
        if self.file_path is not None and self.file_path != '':
            if self.th_video.file == self.file_path:
                self.read_video_finished()
            else:
                self.th_video.set_file(self.file_path)
                self.th_video.start()
        else:
            QMessageBox.warning(None, '错误', '请选择一个文件')

    @Slot()
    def read_video_finished(self):
        frames = self.th_video.frames
        configs = cfg.get_config_map(AUTO_SEC, self.settings)
        self.tracker = Tracker(frames, configs, self.th_video.vid)
        self.tracker.sig_analyze_progress.connect(self.read_video_progress)
        self.tracker.sig_frame_finished.connect(self.frame_finished)
        self.tracker.start()

    @Slot(int, int, str)
    def read_video_progress(self, total: int, current: int, info: str):
        val = int(current / total * self.ui.status_progress.maximum())
        if val == self.ui.status_progress.maximum():
            self.ui.status_progress.setFormat('finished')
        else:
            self.ui.status_progress.setFormat(info + '...%p%')
        self.ui.status_progress.setValue(val)

    @Slot(int, FrameData)
    def frame_finished(self, frame_index: int, frame_data: FrameData):
        if frame_index is None:
            print('index is None')
            return
        self.ui.graphicsView.add_scene(frame_index, frame_data)

    def frame_changed(self, frame_index):
        self.ui.graphicsView.change_scene(frame_index)

    def show_mark_changed(self, state: int):
        if state == Qt.Checked:
            self.ui.graphicsView.set_show_mark(True)
        elif state == Qt.Unchecked:
            self.ui.graphicsView.set_show_mark(False)

    def show_particle_changed(self, state: int):
        if state == Qt.Checked:
            self.ui.graphicsView.set_show_particle(True)
        elif state == Qt.Unchecked:
            self.ui.graphicsView.set_show_particle(False)

    def mark_color_clicked(self):
        color = QColorDialog.getColor(Qt.white, self)
        self.ui.graphicsView.set_mark_color(color)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.ui.bt_mark_color.setPalette(palette)

    def particle_color_clicked(self):
        color = QColorDialog.getColor(Qt.white, self)
        self.ui.graphicsView.set_particle_color(color)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, color)
        self.ui.bt_particle_color.setPalette(palette)

    def update_mode(self, button: QPushButton):
        mode = None
        if button == self.ui.bt_select:
            mode = OperationMode.SELECT
        elif button == self.ui.bt_add:
            mode = OperationMode.ADD
        elif button == self.ui.bt_crop:
            mode = OperationMode.CROP
        elif button == self.ui.bt_move:
            mode = OperationMode.MOVE
        elif button == self.ui.bt_combine:
            mode = OperationMode.COMBINE
        if mode is not None:
            self.ui.graphicsView.set_operation_mode(mode)

    def combine_particles(self):
        self.ui.graphicsView.combine_particles()

    def particle_filter_changed(self):
        text = self.ui.le_particle_filter.text()
        indexes = split_indexes_text(text)
        self.ui.graphicsView.filter_particles(indexes)

    def show_trajectory_changed(self, state: int):
        if state == Qt.Checked:
            self.ui.graphicsView.set_show_trajectory(True)
        elif state == Qt.Unchecked:
            self.ui.graphicsView.set_show_trajectory(False)

    def set_trajectory_size(self, value):
        self.ui.graphicsView.set_trajectory_size(value)

    def edit_traj_color(self):
        editor = ColorEditor(self, self.ui.graphicsView.scene_config.trajectory_colors)
        editor.exec_()

    def set_traj_colors(self, colors: List[QColor]):
        self.ui.graphicsView.set_trajectory_colors(colors)

    def calc_trajectories(self):
        self.ui.graphicsView.calc_trajectories(self.th_video.fps)

    def export_video(self):
        file_dir = ''
        file_name, file_type = QFileDialog.getSaveFileName(self, 'Save Video', file_dir, 'AVI Files (*.avi)')
        file_path = os.path.join(file_dir, file_name)
        if len(file_path) > 0:
            self.ui.graphicsView.export_video(file_path, self.th_video.width, self.th_video.height)


class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self.init_config()
        self.ui.bt_ok.clicked.connect(self.ok)

    def ok(self):
        self.save_config()
        self.accept()

    def save_config(self, widget: QWidget = None):
        if widget is None:
            widget = self
        for child in widget.children():
            if isinstance(child, QWidget) and child.whatsThis() != '':
                cfg.set_widget_value(AUTO_SEC, child)
            self.save_config(child)
        cfg.flush()

    def init_config(self, widget: QWidget = None):
        if widget is None:
            widget = self
        for child in widget.children():
            if isinstance(child, QWidget) and child.whatsThis() != '':
                cfg.get_widget_value(AUTO_SEC, child)
            self.init_config(child)


class ColorEditor(QDialog):
    def __init__(self, main, colors: List[QColor]):
        super().__init__()
        self.main = main
        self.ui = Ui_ColorEditor()
        self.ui.setupUi(self)
        self.colors = colors
        self.ui.bt_add.clicked.connect(self.add_color)
        self.ui.bt_ok.clicked.connect(self.ok)
        self.ui.lv_color.doubleClicked.connect(self.edit_color)
        for color in colors:
            self.add_color(color)

    def add_color(self, color: QColor = None):
        color = Qt.black if color is None else color
        item = QListWidgetItem(self.ui.lv_color)
        size = self.ui.lv_color.gridSize()
        widget = ColorWidget(color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.ui.lv_color.addItem(item)
        self.ui.lv_color.setItemWidget(item, widget)

    def edit_color(self, model_index: QModelIndex):
        widget = self.ui.lv_color.indexWidget(model_index)
        origin_color = widget.color
        color = QColorDialog.getColor(origin_color, self)
        widget.update_color(color)

    def ok(self):
        colors = []
        for row in range(self.ui.lv_color.count()):
            item = self.ui.lv_color.item(row)
            widget = self.ui.lv_color.itemWidget(item)
            colors.append(widget.color)
        self.main.set_traj_colors(colors)
        self.main.init_color_label()
        print(colors)
        self.accept()


class Reader(QThread):
    sig_read_finish = Signal()
    sig_read_progress = Signal(int, int, str)

    def __init__(self, parent=None):
        super(Reader, self).__init__(parent)
        self.file = None
        self.width = None
        self.height = None
        self.fps = None
        self.count = 0
        self.params = None
        self.status = True
        self.vid = None
        self.frames = {}

    def set_file(self, name):
        self.file = name
        self.vid = cv2.VideoCapture(self.file)
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.count = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        if self.vid is None:
            return
        label = 0
        while self.status:
            ret, frame = self.vid.read()
            if not ret:
                break
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frames[label] = color_frame
            label += 1
            self.sig_read_progress.emit(self.count, label, 'reading')
        self.sig_read_finish.emit()


if __name__ == '__main__':
    app = QApplication()
    desktop = app.desktop()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    main = MainWindow()
    main.show()
    app.exec_()
