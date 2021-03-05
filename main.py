import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFontMetrics, QResizeEvent
from PySide6.QtWidgets import *
import numpy as np

import default_settings
from settings import Settings
from ui import MainUi, SettingUi
from worker import VideoLoader, Analyzer
import constant


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # ui
        self.settings = Settings('settings.ini')
        self.ui = MainUi(self, self.settings)
        self.file_path = None

        # data
        self.frames = {}

        # thread
        self.file_loader = self.init_file_loader()
        self.analyzer = self.init_analyzer()

        # connect
        self.ui.bt_select_file.clicked.connect(self.select_file)
        self.ui.bt_settings.clicked.connect(self.show_settings)
        self.ui.bt_load_file.clicked.connect(self.load_file)
        self.ui.bt_analyze.clicked.connect(self.analyze)

    def init_file_loader(self):
        file_loader = VideoLoader(self)
        file_loader.sig_start.connect(self.load_start)
        file_loader.sig_progress.connect(self.progressing)
        file_loader.sig_all_finished.connect(self.load_all_finished)
        return file_loader

    def init_analyzer(self):
        analyzer = Analyzer(self.settings, self)
        analyzer.sig_start.connect(self.analyze_start)
        analyzer.sig_progress.connect(self.progressing)
        analyzer.sig_frame_finished.connect(self.analyze_frame_finished)
        analyzer.sig_all_finished.connect(self.analyze_all_finished)
        return analyzer

    def select_file(self):
        file_path = self.settings.value(default_settings.dir_path)
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr(constant.msg_select_file), file_path, 'AVI Files (*.avi)')
        path, _ = os.path.split(file_path)
        self.file_path = file_path
        self.settings.set_value(default_settings.file_path, file_path)
        self.settings.set_value(default_settings.dir_path, path)
        self.update_file_path()

    def show_settings(self):
        dialog = SettingDialog()
        dialog.exec_()

    def update_file_path(self):
        if self.file_selected():
            font_metrics = QFontMetrics(self.ui.lb_file_path.font())
            elide_text = font_metrics.elidedText(self.file_path, Qt.ElideMiddle, self.ui.lb_file_path.width())
            self.ui.lb_file_path.setText(elide_text)
            self.ui.lb_file_path.setToolTip(self.file_path)
        else:
            self.ui.lb_file_path.setText(self.tr(constant.msg_file_unselected))
            self.ui.lb_file_path.setToolTip(self.tr(constant.msg_file_unselected))

    def load_file(self):
        if self.file_selected():
            self.file_loader.set_file(self.file_path)
            self.file_loader.start()
        else:
            QMessageBox.warning(self.parent(), self.tr(constant.msg_error), self.tr(constant.msg_file_unselected))

    @Slot()
    def load_start(self):
        pass

    @Slot(int, int, str)
    def progressing(self, total: int, current: int, info: str):
        val = int(current / total * self.ui.status_progress.maximum())
        if val == self.ui.status_progress.maximum():
            self.ui.status_bar.showMessage(self.tr(constant.status_ready))
        else:
            self.ui.status_bar.showMessage(info)
        self.ui.status_progress.setValue(val)

    @Slot(int, np.ndarray)
    def load_frame_finished(self, frame_index: int, frame: np.ndarray):
        pass

    @Slot(int, dict)
    def load_all_finished(self, frames: dict):
        self.frames = frames

    def analyze(self):
        if len(self.frames) > 0:
            self.analyzer.frames = self.frames
            self.analyzer.start()
        else:
            QMessageBox.warning(self.parent(), self.tr(constant.msg_error), self.tr(constant.msg_file_unselected))

    @Slot()
    def analyze_start(self):
        pass

    @Slot()
    def analyze_frame_finished(self):
        pass

    @Slot()
    def analyze_all_finished(self):
        pass

    def file_selected(self):
        return self.file_path is not None and len(self.file_path) > 0

    def resizeEvent(self, event: QResizeEvent):
        self.settings.set_value(default_settings.main_width, event.size().width())
        self.settings.set_value(default_settings.main_height, event.size().height())
        self.update_file_path()
        pass


class SettingDialog(QDialog):
    def __init__(self):
        super(SettingDialog, self).__init__()
        self.ui = SettingUi(self)


if __name__ == '__main__':
    app = QApplication()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    main = MainWindow()
    main.show()
    app.exec_()
