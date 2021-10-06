import bz2
import os
import pickle
import struct
from datetime import datetime
from shutil import copyfile
from typing import List, Optional, Dict, Tuple

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QFontMetrics, QResizeEvent, QColor
from PySide6.QtWidgets import *

import constant
import default_settings
from data import VideoData
from enums import OperationMode
from settings import Settings
from ui import MainUi, SettingUi, ColorEditorUi, ColorLabel
from utils import split_indexes_text
from worker import VideoLoader, VideoExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # ui
        self.settings = Settings('settings.ini')
        self.init_unsaved_settings()
        self.ui = MainUi(self, self.settings)
        self.file_path = None
        self.waiting_dialog = None

        # data
        self.frames = {}
        self.scene_for_export = None
        self.video_data = VideoData()

        # status
        # need to rewrite
        self.is_loading = False
        self.loaded = False

        # thread
        self.file_loader = self.init_file_loader()
        self.video_exporter = VideoExporter(self.ui.scene, self.settings)

        # connect
        self.ui.sl_frames.valueChanged.connect(self.frame_changed)
        self.ui.le_filter.textChanged.connect(self.filter_changed)

        # tool bar connect
        self.ui.bt_open_file.clicked.connect(self.select_file)
        self.ui.bt_settings.clicked.connect(self.show_settings)
        self.ui.bt_load_file.clicked.connect(self.load_file)
        self.ui.bt_export.clicked.connect(self.export_video)

        # menu bar connect
        # self.ui.action_save_project.triggered.connect(self.save_project)
        # self.ui.action_open_project.triggered.connect(self.open_project)
        self.ui.action_import_settings.triggered.connect(self.import_settings)
        self.ui.action_export_settings.triggered.connect(self.export_settings)

        # scene connect
        self.ui.bt_select.clicked.connect(lambda bt: self.update_mode(OperationMode.SELECT))
        self.ui.bt_move.clicked.connect(lambda bt: self.update_mode(OperationMode.MOVE))
        self.ui.bt_add.clicked.connect(lambda bt: self.update_mode(OperationMode.ADD))
        self.ui.bt_crop.clicked.connect(lambda bt: self.update_mode(OperationMode.CROP))
        self.ui.bt_combine.clicked.connect(self.combine_particles)
        self.ui.bt_show_particle.clicked.connect(lambda x: self.visibility_changed(self.ui.bt_show_particle))
        self.ui.bt_show_mark.clicked.connect(lambda x: self.visibility_changed(self.ui.bt_show_mark))
        self.ui.bt_show_trajectory.clicked.connect(lambda x: self.visibility_changed(self.ui.bt_show_trajectory))

        # background connect
        self.ui.scene.sig_background_update_progress.connect(self.background_update_progress)
        self.ui.scene.sig_background_update_finish.connect(self.background_update_finished)

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

    def init_unsaved_settings(self):
        """
        初始化不在配置文件中的配置
        """
        self.settings.set_value(default_settings.index_filter, [])
        self.settings.set_value(default_settings.fps, -1)

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
        options = 'avi file (*.avi);;mp4 file (*.mp4);;flv file (*.flv);;ogv file (*.ogv)'
        file_path = self.settings.value(default_settings.dir_path)
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr(constant.msg_select_video_file), file_path, options)
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
            if dialog.frame_trajectory_updated:
                self.ui.scene.trajectory_updated_frame_index.clear()
            if dialog.frame_particle_updated:
                self.ui.scene.particle_updated_frame_index.clear()

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
        if self.loaded:
            ret = QMessageBox.information(None, '提示', f'是否重新加载视频',
                                          QMessageBox.Cancel, QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                return
        if self.file_selected():
            # self.ui.scene.clear_data()
            self.video_data = self.file_loader.set_file(self.file_path)
            self.settings.set_value(default_settings.fps, self.video_data.fps)
            self.file_loader.start()
            self.loaded = True
        else:
            QMessageBox.warning(self.parent(), self.tr(constant.msg_error), self.tr(constant.msg_file_unselected))

    def filter_changed(self):
        text = self.ui.le_filter.text()
        selected_indexes = split_indexes_text(text)
        self.settings.set_value(default_settings.index_filter, list(selected_indexes))
        self.ui.scene.update_frame()

    def export_video(self):
        file_dir = ''
        options = 'avi file (*.avi);;mp4 file (*.mp4);;flv file (*.flv);;ogv file (*.ogv)'
        file_name, file_type = QFileDialog.getSaveFileName(self, 'Save Video', file_dir, options)
        file_path = os.path.join(file_dir, file_name)
        if len(file_path) > 0:
            frame_indexes = self.ui.scene.sorted_frame_indexes()
            self.waiting_dialog = QProgressDialog(self)
            self.waiting_dialog.setWindowTitle(self.tr(constant.msg_waiting))
            self.waiting_dialog.setLabelText(self.tr(constant.msg_exporting))
            self.waiting_dialog.setMinimumDuration(100)
            self.waiting_dialog.setWindowModality(Qt.WindowModal)
            self.waiting_dialog.setRange(0, frame_indexes[-1])
            # self.waiting_dialog.setModal(True)
            self.waiting_dialog.show()
            self.video_exporter.file_path = file_path
            self.video_exporter.video_data = self.video_data
            crop_rect = self.ui.scene.crop_rect
            self.video_exporter.open_writer(crop_rect)
            for frame_index in frame_indexes:
                if self.waiting_dialog.wasCanceled():
                    break
                arr = self.video_exporter.export_arr(frame_index, crop_rect)
                self.video_exporter.write_data(arr)
                self.waiting_dialog.setValue(frame_index)
            self.video_exporter.release_writer()
            self.waiting_dialog.close()

    def update_mode(self, mode: OperationMode):
        self.ui.scene.mode = mode

    @Slot(int)
    def load_start(self, frame_count: int):
        """
        视频开始加载时触发
        :param frame_count: 总帧数
        """
        self.ui.sl_frames.setMaximum(frame_count)
        self.ui.lcd_current_frame.display(f'0-{frame_count}')
        self.ui.scene.video_data = self.video_data
        self.is_loading = True

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
        self.ui.scene.set_particle_pos(frame_index, frame_particles)
        if frame_index == 1:
            self.ui.lcd_current_frame.display(f'1-{self.video_data.frame_count}')
            self.ui.scene.update_frame(frame_index)

    @Slot(int, dict)
    def load_all_finished(self):
        """
        所有帧分析完后触发
        """
        # self.ui.scene.calc_trajectory()
        self.is_loading = False
        pass

    @Slot(int, int, str)
    def background_update_progress(self, total: int, current: int, info: str):
        """
        后台更新进度槽
        """
        if not self.is_loading:
            val = int(current / total * self.ui.status_progress.maximum())
            self.ui.status_bar.showMessage(info)
            self.ui.status_progress.setValue(val)

    @Slot()
    def background_update_finished(self):
        """
        后台更新完成槽
        """
        if not self.is_loading:
            self.ui.status_bar.showMessage(self.tr(constant.status_ready))
            self.ui.status_progress.setValue(self.ui.status_progress.maximum())

    def frame_changed(self, value: Optional[int] = None):
        """
        切换帧, 更新Scene
        帧滑块值变化时触发
        :param value: 帧数
        """
        if value is not None:
            self.ui.lcd_current_frame.display(f'{value}-{self.video_data.frame_count}')
        self.ui.scene.update_frame(value)

    def visibility_changed(self, bt: QPushButton):
        if bt == self.ui.bt_show_particle:
            self.settings.set_value(default_settings.show_particle, bt.isChecked())
        if bt == self.ui.bt_show_mark:
            self.settings.set_value(default_settings.show_mark, bt.isChecked())
        if bt == self.ui.bt_show_trajectory:
            self.settings.set_value(default_settings.show_trajectory, bt.isChecked())
        self.frame_changed()

    def file_selected(self):
        """
        是否已选择文件
        """
        return self.file_path is not None and len(self.file_path) > 0

    def combine_particles(self):
        items = self.ui.scene.selectedItems()
        if len(items) == 0:
            text, ok = QInputDialog.getText(self, "输入", "待合并的粒子编号(,或者空格分隔)", QLineEdit.Normal)
            if ok:
                indexes = split_indexes_text(text)
                self.ui.scene.combine_particles(indexes)
        else:
            indexes = {i.index for i in items}
            self.ui.scene.combine_particles(indexes)

    def save_project(self):
        """
        保存工程
        """
        file_name = 'proj.bin'
        setting_file_name = 'settings.ini'
        sep = struct.pack('I', 900314)
        with bz2.open(file_name, 'wb') as f:
            particle_data_byte = pickle.dumps(self.ui.scene.particle_data.data)
            frame_base64_byte = pickle.dumps(self.ui.scene.frame_base64)
            setting_file = open(setting_file_name, 'r')
            settings_byte = pickle.dumps(setting_file.readlines())
            setting_file.close()
            print(f'data: {len(particle_data_byte)}')
            print(f'frame: {len(frame_base64_byte)}')
            print(f'setting: {len(settings_byte)}')
            f.write(particle_data_byte)
            f.write(sep)
            f.write(frame_base64_byte)
            f.write(sep)
            f.write(settings_byte)

    def open_project(self):
        """
        打开工程
        """
        file_name = 'proj.bin'
        sep = struct.pack('I', 900314)
        with bz2.open(file_name, 'rb') as f:
            content = b''.join(f.readlines())
        contents = content.split(sep)
        if len(contents) < 3:
            print(content)
            print('工程文件异常')
        particle_data_byte = contents[0]
        frame_base64_byte = contents[1]
        settings_byte = contents[2]
        particle_data = pickle.loads(particle_data_byte)
        frame_base64 = pickle.loads(frame_base64_byte)
        settings = pickle.loads(settings_byte)
        self.ui.scene.import_data(frame_base64, particle_data)

    def export_settings(self):
        """
        导出配置
        """
        file_path, file_type = QFileDialog.getSaveFileName(self, 'export settings', None, 'ini file (*.ini)')
        ret = None
        if len(file_path) > 0:
            try:
                ret = copyfile(self.settings.setting_path, file_path)
            except Exception as e:
                QMessageBox.warning(None, '警告', '导出配置文件失败', QMessageBox.Ok)
            if ret is not None:
                QMessageBox.information(None, '提示', f'配置文件已导出到{ret}', QMessageBox.Ok)

    def import_settings(self):
        """
        导入设置
        """
        default_settings_path = self.settings.setting_path
        file_path, _ = QFileDialog.getOpenFileName(self, 'import settings', None, 'ini file (*.ini)')
        if len(file_path) > 0:
            file_name, ext = os.path.splitext(default_settings_path)
            # 将原配置文件备份
            back_file = f'{file_name}.{datetime.now():%Y%m%d%H%M%S}{ext}'
            ret1, ret2 = None, None
            try:
                ret1 = copyfile(default_settings_path, back_file)
                ret2 = copyfile(file_path, default_settings_path)
            except Exception as e:
                QMessageBox.warning(None, '警告', '导入配置文件失败', QMessageBox.Ok)
            if ret1 is not None and ret2 is not None:
                # 使导入配置生效
                self.settings.sync()
                QMessageBox.information(None, '提示', f'配置文件{file_path}已导入\n原配置文件备份到{ret1}', QMessageBox.Ok)

    def resizeEvent(self, event: QResizeEvent):
        """
        窗口大小改变事件
        """
        self.settings.set_value(default_settings.main_width, event.size().width())
        self.settings.set_value(default_settings.main_height, event.size().height())
        self.update_file_path()


class SettingDialog(QDialog):
    def __init__(self, settings: Settings):
        super(SettingDialog, self).__init__()
        self.settings = settings
        self.ui = SettingUi(self, settings)
        self.frame_trajectory_updated = False
        self.frame_particle_updated = False

        self.ui.lb_particle_color_display.clicked.connect(lambda x: self.edit_color(self.ui.lb_particle_color_display))
        self.ui.lb_mark_color_display.clicked.connect(lambda x: self.edit_color(self.ui.lb_mark_color_display))
        self.ui.lb_trajectory_color_display.clicked.connect(
            lambda x: self.edit_color(self.ui.lb_trajectory_color_display))
        self.ui.lb_speed_color_display.clicked.connect(lambda x: self.edit_color(self.ui.lb_speed_color_display))
        self.ui.cb_same_mark_color_with_particle.clicked.connect(self.ui.enable_same_mark_color_with_particle)
        self.ui.cb_same_trajectory_color_with_particle.clicked.connect(
            self.ui.enable_same_trajectory_color_with_particle)
        self.ui.cb_speed_color.clicked.connect(self.ui.enable_speed_color)

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
        self.settings.set_value(default_settings.search_radius, self.ui.le_search_radius.text())
        self.settings.set_value(default_settings.memory_frames, self.ui.le_memory_frames.text())
        self.settings.set_value(default_settings.minimum_area_for_detection, self.ui.le_minimum_detect_area.text())
        self.settings.set_value(default_settings.maximum_area_for_detection, self.ui.le_maximum_detect_area.text())
        self.settings.set_value(default_settings.threshold, self.ui.le_threshold.text())
        self.settings.set_value(default_settings.derivative_order, self.ui.sb_derivative_order.value())
        self.settings.set_value(default_settings.kernel_size, self.ui.cb_kernel_size.currentText())
        self.settings.set_value(default_settings.split_circular_particles, self.ui.cb_split_particles.isChecked())
        self.settings.set_value(default_settings.split_radius, self.ui.sb_particle_radius_for_split.value())
        self.settings.set_value(default_settings.from_frames, self.ui.le_from_frames.text())
        self.settings.set_value(default_settings.to_frames, self.ui.le_to_frames.text())
        # display
        self.frame_particle_updated |= self.settings.set_value(default_settings.particle_color,
                                                               self.ui.lb_particle_color_display.colors)
        self.frame_particle_updated |= self.settings.set_value(default_settings.particle_size,
                                                               self.ui.sb_particle_size.value())
        self.frame_particle_updated |= self.settings.set_value(default_settings.mark_color,
                                                               self.ui.lb_mark_color_display.colors)
        self.frame_particle_updated |= self.settings.set_value(default_settings.mark_size, self.ui.sb_mark_size.value())
        self.frame_particle_updated |= self.settings.set_value(default_settings.same_mark_color_with_particle,
                                                               self.ui.cb_same_mark_color_with_particle.isChecked())
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.trajectory_color,
                                                                 self.ui.lb_trajectory_color_display.colors)
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.trajectory_size,
                                                                 self.ui.sb_trajectory_size.value())
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.same_trajectory_color_with_particle,
                                                                 self.ui.cb_same_trajectory_color_with_particle.isChecked())
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.enable_trajectory_speed_color,
                                                                 self.ui.cb_speed_color.isChecked())
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.trajectory_speed_color,
                                                                 self.ui.lb_speed_color_display.colors)
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.min_speed,
                                                                 self.ui.le_min_speed.text())
        self.frame_trajectory_updated |= self.settings.set_value(default_settings.max_speed,
                                                                 self.ui.le_max_speed.text())
        # export
        self.settings.set_value(default_settings.export_scale, self.ui.dsb_export_scale.value())
        self.settings.set_value(default_settings.export_speed, self.ui.dsb_export_speed.value())
        self.settings.set_value(default_settings.export_show_time, self.ui.cb_export_show_time.isChecked())
        self.settings.set_value(default_settings.export_show_info, self.ui.cb_export_show_info.isChecked())

        super(SettingDialog, self).accept()


class ColorEditor(QDialog):
    default_color = QColor(255, 0, 0)
    sig_color_changed = Signal(ColorLabel, list)

    def __init__(self, parent: QDialog, label: Optional[ColorLabel] = None):
        super().__init__(parent)
        self.parent = parent
        self.label = label
        self.ui = ColorEditorUi(self)
        self._dragged_row = None

        self.ui.bt_add.clicked.connect(lambda x: self.ui.lv_color.add_color())
        self.ui.bt_delete.clicked.connect(self.ui.lv_color.remove_color)

    def add_colors(self, colors: List[QColor]):
        self.ui.lv_color.add_colors(colors)

    def accept(self) -> None:
        self.sig_color_changed.emit(self.label, self.ui.lv_color.colors())
        super(ColorEditor, self).accept()


if __name__ == '__main__':
    app = QApplication()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    main = MainWindow()
    main.show()
    app.exec()
