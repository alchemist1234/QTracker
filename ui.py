from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from settings import Settings
from view import VideoView
from scene import VideoScene
import default_settings
import constant


class ViewButtonGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        icon_add = QIcon('./images/add.svg')
        icon_select = QIcon('./images/cursor.svg')
        icon_crop = QIcon('./images/crop.svg')
        icon_combine = QIcon('./images/combine.svg')
        self.bt_select = QPushButton(icon_select, '', self)
        self.bt_add = QPushButton(icon_add, '', self)
        self.bt_crop = QPushButton(icon_crop, '', self)
        self.bt_combine = QPushButton(icon_combine, '', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.bt_select)
        layout.addWidget(self.bt_add)
        layout.addWidget(self.bt_crop)
        layout.addWidget(self.bt_combine)


class MainUi(object):
    def __init__(self, main: QMainWindow, settings: Settings):
        self.main = main
        if not main.objectName():
            main.setObjectName('MainWindow')
        height = settings.int_value(default_settings.main_height)
        width = settings.int_value(default_settings.main_width)
        main.resize(width, height)
        self.central_widget = QWidget(main)
        self.vbox_central = QVBoxLayout()
        self.central_widget.setLayout(self.vbox_central)
        self.widget = QWidget(self.central_widget)
        self.vbox_widget = QVBoxLayout()
        self.widget.setLayout(self.vbox_widget)

        # Menu Bar
        # self.menu_bar = QMenuBar()
        # main.setMenuBar(self.menu_bar)
        # self.menu_file = self.menu_bar.addMenu('file')
        # self.action_open = self.menu_file.addAction('open')

        # Tool Bar
        self.tool_bar = main.addToolBar('tool bar')
        icon_select = QIcon('./images/open.svg')
        icon_setting = QIcon('./images/setting.svg')
        icon_load = QIcon('./images/load.svg')
        icon_analyze = QIcon('./images/analyze.svg')
        icon_track = QIcon('./images/track.svg')
        icon_export = QIcon('./images/export.svg')
        self.bt_select_file = QPushButton(icon_select, '', self.widget)
        self.bt_settings = QPushButton(icon_setting, '', self.widget)
        self.bt_load_file = QPushButton(icon_load, '', self.widget)
        self.bt_analyze = QPushButton(icon_analyze, '', self.widget)
        self.bt_track = QPushButton(icon_track, '', self.widget)
        self.bt_export = QPushButton(icon_export, '', self.widget)
        self.tool_bar.addWidget(self.bt_select_file)
        self.tool_bar.addWidget(self.bt_settings)
        self.tool_bar.addWidget(self.bt_load_file)
        self.tool_bar.addWidget(self.bt_analyze)
        self.tool_bar.addWidget(self.bt_track)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.bt_export)

        # Top Layout
        self.vbox_top = QVBoxLayout()
        self.lb_file_path = QLabel(self.widget)
        self.lb_file_path.setText(main.tr(constant.msg_file_unselected))
        self.vbox_top.addWidget(self.lb_file_path)
        self.vbox_widget.addLayout(self.vbox_top)

        # Middle Layout
        self.hbox_middle = QHBoxLayout()
        self.view = VideoView(main)
        self.scene = VideoScene(self.view)
        self._btg_view = ViewButtonGroup(self.widget)
        self.hbox_middle.addWidget(self.view)
        self.view.addFixedWidget(self._btg_view, Qt.AlignRight | Qt.AlignTop)
        self.vbox_widget.addLayout(self.hbox_middle)

        # Bottom Layout
        self.hbox_bottom = QHBoxLayout()
        self.lb_frames = QLabel(self.widget)
        self.sl_frames = QSlider(Qt.Horizontal, self.widget)
        self.lb_frame_index = QLabel(self.widget)
        icon_play = QIcon('./images/play.svg')
        self.bt_play = QPushButton(icon_play, '', self.widget)
        self.ed_filter = QLineEdit(self.widget)
        self.hbox_bottom.addWidget(self.lb_frames)
        self.hbox_bottom.addWidget(self.sl_frames)
        self.hbox_bottom.addWidget(self.lb_frame_index)
        self.hbox_bottom.addWidget(self.bt_play)
        self.hbox_bottom.addWidget(self.ed_filter)
        self.vbox_widget.addLayout(self.hbox_bottom)

        # Status Bar
        self.status_bar = QStatusBar(main)
        self.status_progress = QProgressBar(self.status_bar)
        self.status_progress.setRange(0, 100)
        self.status_progress.setValue(0)
        self.status_progress.setFixedWidth(200)
        self.status_bar.showMessage(main.tr(constant.status_ready))
        self.status_bar.addPermanentWidget(self.status_progress)
        main.setStatusBar(self.status_bar)

        # Global
        self.vbox_central.addWidget(self.widget)
        self.main.setCentralWidget(self.central_widget)

        self.translate()

    def translate(self):
        self.main.setWindowTitle(self.main.tr(constant.main_title))
        self.bt_select_file.setToolTip(constant.main_widget_open_file)
        self.bt_settings.setToolTip(constant.main_widget_settings)
        self.bt_load_file.setToolTip(constant.main_widget_load_file)
        self.bt_analyze.setToolTip(constant.main_widget_analyze)
        self.bt_track.setToolTip(constant.main_widget_track)
        self.bt_export.setToolTip(constant.main_widget_export)
        self.bt_select.setToolTip(constant.main_widget_select)
        self.bt_add.setToolTip(constant.main_widget_add)
        self.bt_crop.setToolTip(constant.main_widget_crop)
        self.bt_combine.setToolTip(constant.main_widget_combine)
        self.lb_frames.setText(constant.main_widget_frames)
        self.bt_play.setToolTip(constant.main_widget_play)
        self.ed_filter.setToolTip(constant.main_widget_filter)

    @property
    def bt_select(self):
        return self._btg_view.bt_select

    @property
    def bt_add(self):
        return self._btg_view.bt_add

    @property
    def bt_crop(self):
        return self._btg_view.bt_crop

    @property
    def bt_combine(self):
        return self._btg_view.bt_combine


class SettingUi(object):
    def __init__(self, dialog: QDialog):
        self.dialog = dialog
        dialog.setLayoutDirection(Qt.LeftToRight)
        dialog.setAutoFillBackground(False)
        base_vbox = QVBoxLayout(dialog)
        self.tab_widget = QTabWidget(dialog)
        # Analyze Tab
        self.tab_analyze = QWidget(dialog)
        vbox_analyze = QVBoxLayout(self.tab_analyze)

        # Analyze Tab - Image Treatment
        self.gb_img_treat = QGroupBox(dialog)
        vbox_img_treat = QVBoxLayout(self.gb_img_treat)

        self.lb_median_blur = QLabel(dialog)
        self.sb_median_blur = QSpinBox(dialog)
        self.lb_opening_size = QLabel(dialog)
        self.sb_open_size = QSpinBox(dialog)
        hbox_img_treat1 = QHBoxLayout()
        hbox_img_treat1.addWidget(self.lb_median_blur)
        hbox_img_treat1.addWidget(self.sb_median_blur)
        hbox_img_treat1.addWidget(self.lb_opening_size)
        hbox_img_treat1.addWidget(self.sb_open_size)

        self.lb_gaussian_blur = QLabel(dialog)
        self.sb_gaussian_blur = QSpinBox(dialog)
        self.lb_closing_size = QLabel(dialog)
        self.sb_closing_size = QSpinBox(dialog)
        hbox_img_treat2 = QHBoxLayout()
        hbox_img_treat2.addWidget(self.lb_gaussian_blur)
        hbox_img_treat2.addWidget(self.sb_gaussian_blur)
        hbox_img_treat2.addWidget(self.lb_closing_size)
        hbox_img_treat2.addWidget(self.sb_closing_size)

        self.cb_apply_hist_eq = QCheckBox(dialog)
        self.lb_adaptive_hist_eq = QLabel(dialog)
        self.sb_adaptive_hist_eq = QSpinBox(dialog)
        hbox_img_treat3 = QHBoxLayout()
        hbox_img_treat3.addWidget(self.cb_apply_hist_eq)
        hbox_img_treat3.addWidget(self.lb_adaptive_hist_eq)
        hbox_img_treat3.addWidget(self.sb_adaptive_hist_eq)

        self.lb_bilateral_filter = QLabel(dialog)
        self.sb_bilateral_filter_size = QSpinBox(dialog)
        self.sb_bilateral_filter_color = QSpinBox(dialog)
        self.sb_bilateral_filter_space = QSpinBox(dialog)
        hbox_img_treat4 = QHBoxLayout()
        hbox_img_treat4.addWidget(self.lb_bilateral_filter)
        hbox_img_treat4.addWidget(self.sb_bilateral_filter_size)
        hbox_img_treat4.addWidget(self.sb_bilateral_filter_color)
        hbox_img_treat4.addWidget(self.sb_bilateral_filter_space)

        vbox_img_treat.addLayout(hbox_img_treat1)
        vbox_img_treat.addLayout(hbox_img_treat2)
        vbox_img_treat.addLayout(hbox_img_treat3)
        vbox_img_treat.addLayout(hbox_img_treat4)

        # Analyze Tab - Detection & Tracking
        self.gb_detection_tracking = QGroupBox(dialog)
        vbox_detection_tracking = QVBoxLayout(self.gb_detection_tracking)

        self.lb_search_radius = QLabel(dialog)
        self.sb_search_radius = QSpinBox(dialog)
        self.lb_minimum_detect_area = QLabel(dialog)
        self.sb_minimum_detect_area = QSpinBox(dialog)
        hbox_detection_tracking1 = QHBoxLayout()
        hbox_detection_tracking1.addWidget(self.lb_search_radius)
        hbox_detection_tracking1.addWidget(self.sb_search_radius)
        hbox_detection_tracking1.addWidget(self.lb_minimum_detect_area)
        hbox_detection_tracking1.addWidget(self.sb_minimum_detect_area)

        self.lb_memory_frames = QLabel(dialog)
        self.sb_memory_frames = QSpinBox(dialog)
        self.lb_maximum_detect_area = QLabel(dialog)
        self.sb_maximum_detect_area = QSpinBox(dialog)
        hbox_detection_tracking2 = QHBoxLayout()
        hbox_detection_tracking2.addWidget(self.lb_memory_frames)
        hbox_detection_tracking2.addWidget(self.sb_memory_frames)
        hbox_detection_tracking2.addWidget(self.lb_maximum_detect_area)
        hbox_detection_tracking2.addWidget(self.sb_maximum_detect_area)

        vbox_detection_tracking.addLayout(hbox_detection_tracking1)
        vbox_detection_tracking.addLayout(hbox_detection_tracking2)

        # Analyze Tab - Gradient
        self.gb_gradient = QGroupBox(dialog)
        vbox_gradient = QVBoxLayout(self.gb_gradient)

        self.lb_threshold = QLabel(dialog)
        self.sb_threshold = QSpinBox(dialog)
        self.lb_derivative_order = QLabel(dialog)
        self.sb_derivative_order = QSpinBox(dialog)
        self.lb_kernel_size = QLabel(dialog)
        self.sb_kernel_size = QSpinBox(dialog)
        hbox_gradient = QHBoxLayout()
        hbox_gradient.addWidget(self.lb_threshold)
        hbox_gradient.addWidget(self.sb_threshold)
        hbox_gradient.addWidget(self.lb_derivative_order)
        hbox_gradient.addWidget(self.sb_derivative_order)
        hbox_gradient.addWidget(self.lb_kernel_size)
        hbox_gradient.addWidget(self.sb_kernel_size)

        vbox_gradient.addLayout(hbox_gradient)

        # Analyze Tab - Extra
        self.gb_extra = QGroupBox(dialog)
        vbox_extra = QVBoxLayout(self.gb_extra)

        self.cb_split_particles = QCheckBox(dialog)
        self.lb_particle_radius_for_split = QLabel(dialog)
        self.sb_particle_radius_for_split = QSpinBox(dialog)
        hbox_extra = QHBoxLayout()
        hbox_extra.addWidget(self.cb_split_particles)
        hbox_extra.addWidget(self.lb_particle_radius_for_split)
        hbox_extra.addWidget(self.sb_particle_radius_for_split)

        vbox_extra.addLayout(hbox_extra)

        # Analyze Tab - Video
        self.gb_video = QGroupBox(dialog)
        vbox_videos = QVBoxLayout(self.gb_video)

        self.cb_fit_to_screen = QCheckBox(dialog)
        self.lb_skip_frames = QLabel(dialog)
        self.sb_skip_frames = QSpinBox(dialog)
        hbox_video1 = QHBoxLayout()
        hbox_video1.addWidget(self.cb_fit_to_screen)
        hbox_video1.addWidget(self.lb_skip_frames)
        hbox_video1.addWidget(self.sb_skip_frames)

        self.lb_from_frames = QLabel(dialog)
        self.sb_from_frames = QSpinBox(dialog)
        self.lb_to_frames = QLabel(dialog)
        self.sb_to_frames = QSpinBox(dialog)
        hbox_video2 = QHBoxLayout()
        hbox_video2.addWidget(self.lb_from_frames)
        hbox_video2.addWidget(self.sb_from_frames)
        hbox_video2.addWidget(self.lb_to_frames)
        hbox_video2.addWidget(self.sb_to_frames)

        vbox_videos.addLayout(hbox_video1)
        vbox_videos.addLayout(hbox_video2)

        vbox_analyze.addWidget(self.gb_img_treat)
        vbox_analyze.addWidget(self.gb_detection_tracking)
        vbox_analyze.addWidget(self.gb_gradient)
        vbox_analyze.addWidget(self.gb_extra)
        vbox_analyze.addWidget(self.gb_video)

        # Display Tab
        self.tab_display = QWidget(dialog)
        vbox_display = QVBoxLayout(self.tab_display)

        # Display Tab - Particle
        self.gb_display_particle = QGroupBox(dialog)
        vbox_particle = QVBoxLayout(self.gb_display_particle)

        self.lb_particle_color = QLabel(dialog)
        self.lb_particle_color_display = QLabel(dialog)
        self.lb_particle_size = QLabel(dialog)
        self.sb_particle_size = QSpinBox(dialog)
        hbox_display = QHBoxLayout()
        hbox_display.addWidget(self.lb_particle_color)
        hbox_display.addWidget(self.lb_particle_color_display)
        hbox_display.addWidget(self.lb_particle_size)
        hbox_display.addWidget(self.sb_particle_size)

        vbox_particle.addLayout(hbox_display)

        # Display Tab - Mark
        self.gb_display_mark = QGroupBox(dialog)
        vbox_mark = QVBoxLayout(self.gb_display_mark)

        self.lb_mark_color = QLabel(dialog)
        self.lb_mark_color_display = QLabel(dialog)
        self.lb_mark_size = QLabel(dialog)
        self.sb_mark_size = QSpinBox(dialog)
        hbox_mark = QHBoxLayout()
        hbox_mark.addWidget(self.lb_mark_color)
        hbox_mark.addWidget(self.lb_mark_color_display)
        hbox_mark.addWidget(self.lb_mark_size)
        hbox_mark.addWidget(self.sb_mark_size)

        vbox_mark.addLayout(hbox_mark)

        # Display Tab - Trajectory
        self.gb_display_trajectory = QGroupBox(dialog)
        vbox_trajectory = QVBoxLayout(self.gb_display_trajectory)

        self.lb_trajectory_color = QLabel(dialog)
        self.lb_trajectory_color_display = QLabel(dialog)
        self.lb_trajectory_size = QLabel(dialog)
        self.sb_trajectory_size = QSpinBox(dialog)
        hbox_trajectory1 = QHBoxLayout()
        hbox_trajectory1.addWidget(self.lb_trajectory_color)
        hbox_trajectory1.addWidget(self.lb_trajectory_color_display)
        hbox_trajectory1.addWidget(self.lb_trajectory_size)
        hbox_trajectory1.addWidget(self.sb_trajectory_size)

        vbox_trajectory.addLayout(hbox_trajectory1)

        vbox_display.addWidget(self.gb_display_particle)
        vbox_display.addWidget(self.gb_display_mark)
        vbox_display.addWidget(self.gb_display_trajectory)

        self.tab_widget.addTab(self.tab_analyze, dialog.tr(constant.settings_tab_analyze))
        self.tab_widget.addTab(self.tab_display, dialog.tr(constant.settings_tab_display))

        self.bt_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        self.bt_box.accepted.connect(dialog.accept)
        self.bt_box.rejected.connect(dialog.reject)

        base_vbox.addWidget(self.tab_widget)
        base_vbox.addWidget(self.bt_box)

        self.translate()

    def translate(self):
        self.dialog.setWindowTitle(self.dialog.tr(constant.settings_title))
        self.lb_median_blur.setText(self.dialog.tr(constant.settings_widget_median_blur))
        self.lb_opening_size.setText(self.dialog.tr(constant.settings_widget_opening_size))
        self.lb_gaussian_blur.setText(self.dialog.tr(constant.settings_widget_gaussian_blur))
        self.lb_closing_size.setText(self.dialog.tr(constant.settings_widget_closing_size))
        self.cb_apply_hist_eq.setText(self.dialog.tr(constant.settings_widget_apply_hist_eq))
        self.lb_adaptive_hist_eq.setText(self.dialog.tr(constant.settings_widget_adaptive_hist_eq))
        self.lb_bilateral_filter.setText(self.dialog.tr(constant.settings_widget_bilateral_filter))
        self.lb_search_radius.setText(self.dialog.tr(constant.settings_widget_search_radius))
        self.lb_minimum_detect_area.setText(self.dialog.tr(constant.settings_widget_minimum_detect_area))
        self.lb_maximum_detect_area.setText(self.dialog.tr(constant.settings_widget_maximum_detect_area))
        self.lb_memory_frames.setText(self.dialog.tr(constant.settings_widget_memory_frames))
        self.lb_threshold.setText(self.dialog.tr(constant.settings_widget_threshold))
        self.lb_derivative_order.setText(self.dialog.tr(constant.settings_widget_derivative_order))
        self.lb_kernel_size.setText(self.dialog.tr(constant.settings_widget_kernel_size))
        self.cb_split_particles.setText(self.dialog.tr(constant.settings_widget_split_particle))
        self.lb_particle_radius_for_split.setText(self.dialog.tr(constant.settings_widget_particle_radius_for_split))
        self.cb_fit_to_screen.setText(self.dialog.tr(constant.settings_widget_fit_to_screen))
        self.lb_skip_frames.setText(self.dialog.tr(constant.settings_widget_skip_frames))
        self.lb_from_frames.setText(self.dialog.tr(constant.settings_widget_from_frames))
        self.lb_to_frames.setText(self.dialog.tr(constant.settings_widget_to_frames))
        self.lb_particle_color.setText(self.dialog.tr(constant.settings_widget_particle_color))
        self.lb_particle_size.setText(self.dialog.tr(constant.settings_widget_particle_size))
        self.lb_mark_color.setText(self.dialog.tr(constant.settings_widget_mark_color))
        self.lb_mark_size.setText(self.dialog.tr(constant.settings_widget_mark_size))
        self.lb_trajectory_color.setText(self.dialog.tr(constant.settings_widget_trajectory_color))
        self.lb_trajectory_size.setText(self.dialog.tr(constant.settings_widget_trajectory_size))
