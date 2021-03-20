import os
from typing import List, Optional, Dict, Tuple

from PySide6.QtCore import Qt, Slot, QModelIndex, QSize, Signal
from PySide6.QtGui import QFontMetrics, QResizeEvent, QColor, QMouseEvent
from PySide6.QtWidgets import *

import constant
import default_settings
from settings import Settings
from ui import MainUi, SettingUi, ColorEditorUi, ColorWidgetUi, ColorLabel
from worker import VideoLoader
from utils import split_indexes_text


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # ui
        self.settings = Settings('settings.ini')
        self.settings.set_value(default_settings.index_filter, [])
        self.ui = MainUi(self, self.settings)
        self.file_path = None

        # data
        self.frames = {}

        # thread
        self.file_loader = self.init_file_loader()

        # connect
        self.ui.bt_select_file.clicked.connect(self.select_file)
        self.ui.bt_settings.clicked.connect(self.show_settings)
        self.ui.bt_load_file.clicked.connect(self.load_file)
        self.ui.sl_frames.valueChanged.connect(self.frame_changed)
        self.ui.le_filter.textChanged.connect(self.filter_changed)

    def init_file_loader(self):
        """
        初始化视频加载器
        """
        file_loader = VideoLoader(self.settings, self)
        file_loader.sig_start.connect(self.load_start)
        file_loader.sig_progress.connect(self.progressing)
        file_loader.sig_frame_finished.connect(self.load_frame_finished)
        file_loader.sig_all_finished.connect(self.load_all_finished)
        return file_loader

    # def init_analyzer(self):
    #     analyzer = Analyzer(self.settings, self)
    #     analyzer.sig_start.connect(self.analyze_start)
    #     analyzer.sig_progress.connect(self.progressing)
    #     analyzer.sig_frame_finished.connect(self.analyze_frame_finished)
    #     analyzer.sig_all_finished.connect(self.analyze_all_finished)
    #     return analyzer

    def select_file(self):
        """
        选择文件
        点击选择文件触发
        """
        file_path = self.settings.value(default_settings.dir_path)
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr(constant.msg_select_file), file_path,
                                                   'AVI Files (*.avi)')
        path, _ = os.path.split(file_path)
        self.file_path = file_path
        self.settings.set_value(default_settings.file_path, file_path)
        self.settings.set_value(default_settings.dir_path, path)
        self.update_file_path()

    def show_settings(self):
        """
        显示设置窗口
        点击设置触发
        """
        dialog = SettingDialog(self.settings)
        ret = dialog.exec_()
        if ret:
            self.ui.scene.update_frame()

    def update_file_path(self):
        """
        更新文件路径
        选择文件结束后、窗口大小改变后触发
        """
        if self.file_selected():
            font_metrics = QFontMetrics(self.ui.lb_file_path.font())
            elide_text = font_metrics.elidedText(self.file_path, Qt.ElideMiddle, self.ui.lb_file_path.width())
            self.ui.lb_file_path.setText(elide_text)
            self.ui.lb_file_path.setToolTip(self.file_path)
        else:
            self.ui.lb_file_path.setText(self.tr(constant.msg_file_unselected))
            self.ui.lb_file_path.setToolTip(self.tr(constant.msg_file_unselected))

    def load_file(self):
        """
        加载(分析)视频
        点击分析按钮触发
        """
        if self.file_selected():
            self.file_loader.set_file(self.file_path)
            self.file_loader.start()
        else:
            QMessageBox.warning(self.parent(), self.tr(constant.msg_error), self.tr(constant.msg_file_unselected))

    def filter_changed(self):
        text = self.ui.le_filter.text()
        selected_indexes = split_indexes_text(text)
        self.settings.set_value(default_settings.index_filter, list(selected_indexes))
        self.ui.scene.update_frame()

    @Slot(int)
    def load_start(self, frame_count: int):
        """
        视频开始加载时触发
        :param frame_count: 总帧数
        """
        self.ui.sl_frames.setMaximum(frame_count)
        self.ui.lb_frame_index.setText(str(frame_count))

    @Slot(int, int, str)
    def progressing(self, total: int, current: int, info: str):
        """
        更新进度条
        分析完每一帧后触发

        :param total: 最大值
        :param current: 当前值
        :param info: 状态栏显示信息
        """
        val = int(current / total * self.ui.status_progress.maximum())
        if val == self.ui.status_progress.maximum():
            self.ui.status_bar.showMessage(self.tr(constant.status_ready))
        else:
            self.ui.status_bar.showMessage(info)
        self.ui.status_progress.setValue(val)

    @Slot(int, bytes, dict)
    def load_frame_finished(self, frame_index: int, frame_base64: bytes, frame_particles: Dict[int, Tuple[int, int]]):
        """
        更新scene数据
        分析完每一帧后触发
        :param frame_index: 帧索引
        :param frame_base64: 帧base64数据
        :param frame_particles:  粒子数据{粒子索引: (x, y)}
        """
        self.ui.scene.add_frame_image(frame_index, frame_base64)
        self.ui.scene.add_particle_pos(frame_index, frame_particles)
        if frame_index == 1:
            self.ui.scene.update_frame(frame_index)

    @Slot(int, dict)
    def load_all_finished(self):
        """
        所有帧分析完后触发
        """
        self.ui.scene.calc_trajectory()
        pass

    def frame_changed(self, value):
        """
        切换帧, 更新Scene
        帧滑块值变化时触发
        :param value: 帧数
        """
        self.ui.scene.update_frame(value)

    def file_selected(self):
        """
        是否已选择文件
        """
        return self.file_path is not None and len(self.file_path) > 0

    def resizeEvent(self, event: QResizeEvent):
        """
        窗口大小改变事件
        """
        self.settings.set_value(default_settings.main_width, event.size().width())
        self.settings.set_value(default_settings.main_height, event.size().height())
        self.update_file_path()
        pass


class SettingDialog(QDialog):
    def __init__(self, settings: Settings):
        super(SettingDialog, self).__init__()
        self.settings = settings
        self.ui = SettingUi(self, settings)

        self.ui.lb_particle_color_display.clicked.connect(lambda x: self.edit_color(self.ui.lb_particle_color_display))
        self.ui.lb_mark_color_display.clicked.connect(lambda x: self.edit_color(self.ui.lb_mark_color_display))
        self.ui.lb_trajectory_color_display.clicked.connect(
            lambda x: self.edit_color(self.ui.lb_trajectory_color_display))

    def edit_color(self, label: ColorLabel):
        editor = ColorEditor(self, label)
        editor.add_colors(label.colors)
        editor.sig_color_changed.connect(self.update_color)
        editor.exec_()

    @Slot(ColorLabel, list)
    def update_color(self, label: ColorLabel, colors: List[QColor]):
        label.set_color(colors)

    def accept(self):
        # analyze
        self.settings.set_value(default_settings.median_blur, self.ui.sb_median_blur.value())
        self.settings.set_value(default_settings.gaussian_blur, self.ui.sb_gaussian_blur.value())
        self.settings.set_value(default_settings.opening_size, self.ui.sb_opening_size.value())
        self.settings.set_value(default_settings.closing_size, self.ui.sb_closing_size.value())
        self.settings.set_value(default_settings.apply_hist_eq, self.ui.cb_apply_hist_eq.isChecked())
        self.settings.set_value(default_settings.adaptive_hist_eq, self.ui.sb_adaptive_hist_eq.value())
        self.settings.set_value(default_settings.bilateral_size, self.ui.sb_bilateral_filter_size.value())
        self.settings.set_value(default_settings.bilateral_color, self.ui.sb_bilateral_filter_color.value())
        self.settings.set_value(default_settings.bilateral_space, self.ui.sb_bilateral_filter_space.value())
        self.settings.set_value(default_settings.search_radius, self.ui.sb_search_radius.value())
        self.settings.set_value(default_settings.memory_frames, self.ui.sb_memory_frames.value())
        self.settings.set_value(default_settings.minimum_area_for_detection, self.ui.le_minimum_detect_area.text())
        self.settings.set_value(default_settings.maximum_area_for_detection, self.ui.le_maximum_detect_area.text())
        self.settings.set_value(default_settings.threshold, self.ui.le_threshold.text())
        self.settings.set_value(default_settings.derivative_order, self.ui.sb_derivative_order.value())
        self.settings.set_value(default_settings.kernel_size, self.ui.cb_kernel_size.currentText())
        self.settings.set_value(default_settings.split_circular_particles, self.ui.cb_split_particles.isChecked())
        self.settings.set_value(default_settings.split_radius, self.ui.sb_particle_radius_for_split.value())
        self.settings.set_value(default_settings.fit_to_screen, self.ui.cb_fit_to_screen.isChecked())
        self.settings.set_value(default_settings.skip_frames, self.ui.sb_skip_frames.value())
        self.settings.set_value(default_settings.from_frames, self.ui.le_from_frames.text())
        self.settings.set_value(default_settings.to_frames, self.ui.le_to_frames.text())
        # display
        self.settings.set_value(default_settings.particle_color, self.ui.lb_particle_color_display.colors)
        self.settings.set_value(default_settings.particle_size, self.ui.sb_particle_size.value())
        self.settings.set_value(default_settings.mark_color, self.ui.lb_mark_color_display.colors)
        self.settings.set_value(default_settings.mark_size, self.ui.sb_mark_size.value())
        self.settings.set_value(default_settings.trajectory_color, self.ui.lb_trajectory_color_display.colors)
        self.settings.set_value(default_settings.trajectory_size, self.ui.sb_trajectory_size.value())

        super(SettingDialog, self).accept()


class ColorWidget(QWidget):
    def __init__(self, parent: QListView, color: QColor, height: int):
        super().__init__(parent)
        self.ui = ColorWidgetUi(self, color, height)
        self.color = color
        self.color_name = QColor(color).name()

    def update_color(self, color: QColor):
        self.color = color
        self.color_name = QColor(color).name()
        self.ui.lb_color.set_color(color)
        self.ui.lb_color_name.setText(self.color_name)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.parent().mouseDoubleClickEvent(event)


class ColorEditor(QDialog):
    default_color = QColor(255, 0, 0)
    sig_color_changed = Signal(ColorLabel, list)

    def __init__(self, parent: QDialog, label: Optional[ColorLabel] = None):
        super().__init__(parent)
        self.parent = parent
        self.label = label
        self.ui = ColorEditorUi(self)

        self.ui.bt_add.clicked.connect(lambda x: self.add_color())
        self.ui.lv_color.doubleClicked.connect(self.edit_color)

    def add_colors(self, colors: List[QColor]):
        for color in colors:
            self.add_color(color)

    def add_color(self, color: Optional[QColor] = None):
        color = ColorEditor.default_color if color is None else color
        item = QListWidgetItem(self.ui.lv_color)
        size = self.ui.lv_color.gridSize()
        widget = ColorWidget(self.ui.lv_color, color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.ui.lv_color.addItem(item)
        self.ui.lv_color.setItemWidget(item, widget)

    def edit_color(self, model_index: QModelIndex):
        widget = self.ui.lv_color.indexWidget(model_index)
        origin_color = widget.color
        color = QColorDialog.getColor(origin_color, self)
        if color.isValid():
            widget.update_color(color)

    def get_colors(self):
        colors = []
        for i in range(self.ui.lv_color.count()):
            item = self.ui.lv_color.item(i)
            color_widget = self.ui.lv_color.itemWidget(item)
            colors.append(color_widget.color)
        return colors

    def accept(self) -> None:
        self.sig_color_changed.emit(self.label, self.get_colors())
        super(ColorEditor, self).accept()


if __name__ == '__main__':
    app = QApplication()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    main = MainWindow()
    main.show()
    app.exec_()
