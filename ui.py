from typing import List, Union, Callable, Optional

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import constant
import default_settings
from scene import VideoScene
from settings import Settings
from utils import resource_path
from view import VideoView


class ColorLabel(QLabel):
    clicked = Signal(QMouseEvent)

    def __init__(self, parent=None):
        super(ColorLabel, self).__init__(parent=parent)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.painter = QPainter()
        self._colors = []

    @property
    def colors(self):
        return self._colors

    def set_color(self, colors: Union[List[QColor], QColor]):
        if not isinstance(colors, list):
            colors = [colors]
        self._colors = colors
        size = len(colors)
        base_color_width = int(self.width() / size)
        base_color_width = 1 if base_color_width < 1 else base_color_width
        unfilled_width = self.width() - base_color_width * size
        pixmap = QPixmap(self.width(), self.height())
        filled_width = 0
        self.painter.begin(pixmap)
        for color in colors:
            color_width = base_color_width
            if unfilled_width > 0:
                color_width += 1
                unfilled_width -= 1
            self.brush.setColor(color)
            self.painter.fillRect(filled_width, 0, color_width, self.height(), self.brush)
            filled_width += color_width
        self.painter.end()
        self.setPixmap(pixmap)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(ev)
        super(ColorLabel, self).mousePressEvent(ev)


class ViewButtonGroup(QWidget):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        icon_select = QIcon()
        icon_select.addFile(resource_path('images/cursor-default.png'))
        icon_move = QIcon()
        icon_move.addFile(resource_path('images/drag-move-fill.png'))
        icon_add = QIcon()
        icon_add.addFile(resource_path('images/add-circle-line.png'))
        icon_crop = QIcon()
        icon_crop.addFile(resource_path('images/crop-line.png'))
        icon_combine = QIcon()
        icon_combine.addFile(resource_path('images/vector-combine.png'))
        icon_show_particle = QIcon()
        icon_show_particle.addFile(resource_path('images/chart-bubble.png'))
        icon_show_mark = QIcon()
        icon_show_mark.addFile(resource_path('images/numeric.png'))
        icon_show_trajectory = QIcon()
        icon_show_trajectory.addFile(resource_path('images/ray-start-end.png'))
        self.bt_select = QPushButton(icon_select, '', self)
        self.bt_select.setCheckable(True)
        self.bt_select.setAutoExclusive(True)
        self.bt_select.setChecked(True)
        self.bt_move = QPushButton(icon_move, '', self)
        self.bt_move.setCheckable(True)
        self.bt_move.setAutoExclusive(True)
        self.bt_add = QPushButton(icon_add, '', self)
        self.bt_add.setCheckable(True)
        self.bt_add.setAutoExclusive(True)
        self.bt_crop = QPushButton(icon_crop, '', self)
        self.bt_crop.setCheckable(True)
        self.bt_crop.setAutoExclusive(True)
        self.bt_combine = QPushButton(icon_combine, '', self)

        self.bt_show_particle = QPushButton(icon_show_particle, '', self)
        self.bt_show_particle.setCheckable(True)
        self.bt_show_particle.setChecked(settings.boolean_value(default_settings.show_particle))
        self.bt_show_mark = QPushButton(icon_show_mark, '', self)
        self.bt_show_mark.setCheckable(True)
        self.bt_show_mark.setChecked(settings.boolean_value(default_settings.show_mark))
        self.bt_show_trajectory = QPushButton(icon_show_trajectory, '', self)
        self.bt_show_trajectory.setCheckable(True)
        self.bt_show_trajectory.setChecked(settings.boolean_value(default_settings.show_trajectory))

        layout = QVBoxLayout(self)
        layout.addWidget(self.bt_select)
        layout.addWidget(self.bt_move)
        layout.addWidget(self.bt_add)
        layout.addWidget(self.bt_crop)
        layout.addWidget(self.bt_combine)
        layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.bt_show_particle)
        layout.addWidget(self.bt_show_mark)
        layout.addWidget(self.bt_show_trajectory)


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


class ColorListWidget(QListWidget):
    default_color = Qt.red

    def __init__(self, *args):
        super(ColorListWidget, self).__init__(*args)
        self._dragged_item = None
        self._dragged_color = None

    def add_color(self, color: Optional[QColor] = None):
        color = ColorListWidget.default_color if color is None else color
        item = QListWidgetItem(self)
        size = self.gridSize()
        widget = ColorWidget(self, color, size.height())
        item.setSizeHint(QSize(size.width(), size.height()))
        self.addItem(item)
        self.setItemWidget(item, widget)

    def add_colors(self, colors: List[QColor]):
        for color in colors:
            self.add_color(color)

    def edit_color(self, model_index: QModelIndex):
        widget = self.indexWidget(model_index)
        origin_color = widget.color
        color = QColorDialog.getColor(origin_color, self)
        if color.isValid():
            widget.update_color(color)

    def remove_color(self):
        self.takeItem(self.currentRow())

    def colors(self):
        colors = []
        for i in range(self.count()):
            item = self.item(i)
            if item:
                color_widget = self.itemWidget(item)
                colors.append(color_widget.color)
        return colors

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragged_item = self.itemAt(event.pos())
            self._dragged_color = self.itemWidget(self._dragged_item).color

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._dragged_item:
            origin_row = self.row(self._dragged_item)
            current_item = self.itemAt(event.pos())
            current_row = self.row(current_item)
            if current_row != origin_row:
                item = self.takeItem(origin_row)
                self.removeItemWidget(item)
                self.insertItem(current_row, item)
                widget = ColorWidget(self, self._dragged_color, self.gridSize().height())
                self.setItemWidget(self._dragged_item, widget)
            self._dragged_item = None
            self._dragged_color = None

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.edit_color(self.indexAt(event.pos()))


class MainUi(object):
    def __init__(self, main: QMainWindow, settings: Settings):
        self.main = main
        if not main.objectName():
            main.setObjectName('MainWindow')
        height = settings.int_value(default_settings.main_height)
        width = settings.int_value(default_settings.main_width)
        main.resize(width, height)
        icon = QIcon()
        icon.addFile(resource_path('images/logo.png'))
        main.setWindowIcon(icon)
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
        icon_open = QIcon()
        icon_open.addFile(resource_path('images/open-line.png'))
        icon_setting = QIcon()
        icon_setting.addFile(resource_path('images/settings-line.png'))
        icon_analyze = QIcon()
        icon_analyze.addFile(resource_path('images/cpu-line.png'))
        icon_export = QIcon()
        icon_export.addFile(resource_path('images/content-save.png'))
        self.bt_open_file = QPushButton(icon_open, '', self.widget)
        self.bt_settings = QPushButton(icon_setting, '', self.widget)
        self.bt_load_file = QPushButton(icon_analyze, '', self.widget)
        self.bt_export = QPushButton(icon_export, '', self.widget)
        self.tool_bar.addWidget(self.bt_open_file)
        self.tool_bar.addWidget(self.bt_settings)
        self.tool_bar.addWidget(self.bt_load_file)
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
        self.scene = VideoScene(self.view, settings)
        self.view.setScene(self.scene)
        self._btg_view = ViewButtonGroup(settings, self.widget)
        self.hbox_middle.addWidget(self.view)
        self.view.add_fixed_widget(self._btg_view, Qt.AlignRight | Qt.AlignTop)
        self.vbox_widget.addLayout(self.hbox_middle)

        # Bottom Layout
        self.hbox_bottom = QHBoxLayout()
        self.lb_frames = QLabel(self.widget)
        self.sl_frames = QSlider(Qt.Horizontal, self.widget)
        self.sl_frames.setMinimum(1)
        self.sl_frames.setMaximum(1)
        self.sl_frames.setSingleStep(1)
        self.sl_frames.setPageStep(1)
        self.lcd_current_frame = QLCDNumber(self.widget)
        self.lcd_current_frame.setSegmentStyle(QLCDNumber.Flat)
        self.lcd_current_frame.setDigitCount(9)
        icon_play = QIcon()
        icon_play.addFile(resource_path('images/play-circle-outline.png'))
        self.bt_play = QPushButton(icon_play, '', self.widget)
        self.le_filter = QLineEdit(self.widget)
        self.hbox_bottom.addWidget(self.lb_frames)
        self.hbox_bottom.addWidget(self.sl_frames)
        self.hbox_bottom.addWidget(self.lcd_current_frame)
        self.hbox_bottom.addWidget(self.bt_play)
        self.hbox_bottom.addWidget(self.le_filter)
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
        self.bt_open_file.setToolTip(self.main.tr(constant.main_widget_open_file))
        self.bt_settings.setToolTip(self.main.tr(constant.main_widget_settings))
        self.bt_load_file.setToolTip(self.main.tr(constant.main_widget_load_file))
        self.bt_export.setToolTip(self.main.tr(constant.main_widget_export))
        self.bt_select.setToolTip(self.main.tr(constant.main_widget_select))
        self.bt_move.setToolTip(self.main.tr(constant.main_widget_move))
        self.bt_add.setToolTip(self.main.tr(constant.main_widget_add))
        self.bt_crop.setToolTip(self.main.tr(constant.main_widget_crop))
        self.bt_combine.setToolTip(self.main.tr(constant.main_widget_combine))
        self.lb_frames.setText(self.main.tr(constant.main_widget_frames))
        self.bt_play.setToolTip(self.main.tr(constant.main_widget_play))
        self.le_filter.setToolTip(self.main.tr(constant.main_widget_filter))
        self.bt_show_mark.setToolTip(self.main.tr(constant.main_widget_show_mark))
        self.bt_show_particle.setToolTip(self.main.tr(constant.main_widget_show_particle))
        self.bt_show_trajectory.setToolTip(self.main.tr(constant.main_widget_show_trajectory))

    @property
    def bt_select(self):
        return self._btg_view.bt_select

    @property
    def bt_move(self):
        return self._btg_view.bt_move

    @property
    def bt_add(self):
        return self._btg_view.bt_add

    @property
    def bt_crop(self):
        return self._btg_view.bt_crop

    @property
    def bt_combine(self):
        return self._btg_view.bt_combine

    @property
    def bt_show_particle(self):
        return self._btg_view.bt_show_particle

    @property
    def bt_show_mark(self):
        return self._btg_view.bt_show_mark

    @property
    def bt_show_trajectory(self):
        return self._btg_view.bt_show_trajectory


class SettingUi(object):
    def __init__(self, dialog: QDialog, settings: Settings):
        self.dialog = dialog
        self.settings = settings
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
        self.sb_median_blur.setRange(1, 99)
        self.sb_median_blur.setSingleStep(2)
        self.sb_median_blur.editingFinished.connect(
            lambda: spinbox_validation(self.sb_median_blur, is_odd, minus_one))
        self.lb_opening_size = QLabel(dialog)
        self.sb_opening_size = QSpinBox(dialog)
        hbox_img_treat1 = QHBoxLayout()
        hbox_img_treat1.addWidget(self.lb_median_blur)
        hbox_img_treat1.addWidget(self.sb_median_blur)
        hbox_img_treat1.addWidget(self.lb_opening_size)
        hbox_img_treat1.addWidget(self.sb_opening_size)

        self.lb_gaussian_blur = QLabel(dialog)
        self.sb_gaussian_blur = QSpinBox(dialog)
        self.sb_gaussian_blur.setRange(1, 99)
        self.sb_gaussian_blur.setSingleStep(2)
        self.sb_gaussian_blur.editingFinished.connect(
            lambda: spinbox_validation(self.sb_gaussian_blur, is_odd, minus_one))
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
        self.le_search_radius = QLineEdit(dialog)
        self.le_search_radius.setValidator(QIntValidator(0, 999999, self.le_search_radius))
        self.lb_minimum_detect_area = QLabel(dialog)
        self.le_minimum_detect_area = QLineEdit(dialog)
        self.le_minimum_detect_area.setValidator(QIntValidator(0, 999999, self.le_minimum_detect_area))
        hbox_detection_tracking1 = QHBoxLayout()
        hbox_detection_tracking1.addWidget(self.lb_search_radius)
        hbox_detection_tracking1.addWidget(self.le_search_radius)
        hbox_detection_tracking1.addWidget(self.lb_minimum_detect_area)
        hbox_detection_tracking1.addWidget(self.le_minimum_detect_area)

        self.lb_memory_frames = QLabel(dialog)
        self.le_memory_frames = QLineEdit(dialog)
        self.le_memory_frames.setValidator(QIntValidator(0, 999999, self.le_memory_frames))
        self.lb_maximum_detect_area = QLabel(dialog)
        self.le_maximum_detect_area = QLineEdit(dialog)
        self.le_maximum_detect_area.setValidator(QIntValidator(0, 999999, self.le_maximum_detect_area))
        hbox_detection_tracking2 = QHBoxLayout()
        hbox_detection_tracking2.addWidget(self.lb_memory_frames)
        hbox_detection_tracking2.addWidget(self.le_memory_frames)
        hbox_detection_tracking2.addWidget(self.lb_maximum_detect_area)
        hbox_detection_tracking2.addWidget(self.le_maximum_detect_area)

        vbox_detection_tracking.addLayout(hbox_detection_tracking1)
        vbox_detection_tracking.addLayout(hbox_detection_tracking2)

        # Analyze Tab - Gradient
        self.gb_gradient = QGroupBox(dialog)
        vbox_gradient = QVBoxLayout(self.gb_gradient)

        self.lb_threshold = QLabel(dialog)
        self.le_threshold = QLineEdit(dialog)
        self.lb_derivative_order = QLabel(dialog)
        self.sb_derivative_order = QSpinBox(dialog)
        self.sb_derivative_order.setRange(1, 5)
        self.lb_kernel_size = QLabel(dialog)
        self.cb_kernel_size = QComboBox(dialog)
        self.cb_kernel_size.addItems(['-1', '1', '3', '5', '7'])
        hbox_gradient = QHBoxLayout()
        hbox_gradient.addWidget(self.lb_threshold)
        hbox_gradient.addWidget(self.le_threshold)
        hbox_gradient.addWidget(self.lb_derivative_order)
        hbox_gradient.addWidget(self.sb_derivative_order)
        hbox_gradient.addWidget(self.lb_kernel_size)
        hbox_gradient.addWidget(self.cb_kernel_size)

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

        self.lb_from_frames = QLabel(dialog)
        self.le_from_frames = QLineEdit('', dialog)
        self.lb_to_frames = QLabel(dialog)
        self.le_to_frames = QLineEdit('', dialog)
        self.le_from_frames.setValidator(QIntValidator(1, 9999, self.le_from_frames))
        self.le_to_frames.setValidator(QIntValidator(1, 9999, self.le_to_frames))
        hbox_video1 = QHBoxLayout()
        hbox_video1.addWidget(self.lb_from_frames)
        hbox_video1.addWidget(self.le_from_frames)
        hbox_video1.addWidget(self.lb_to_frames)
        hbox_video1.addWidget(self.le_to_frames)

        vbox_videos.addLayout(hbox_video1)

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
        self.lb_particle_color_display = ColorLabel(dialog)
        self.lb_particle_color_display.setFixedSize(76, 20)
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
        self.lb_mark_color_display = ColorLabel(dialog)
        self.lb_mark_color_display.setFixedSize(76, 20)
        self.lb_mark_size = QLabel(dialog)
        self.sb_mark_size = QSpinBox(dialog)
        hbox_mark = QHBoxLayout()
        hbox_mark.addWidget(self.lb_mark_color)
        hbox_mark.addWidget(self.lb_mark_color_display)
        hbox_mark.addWidget(self.lb_mark_size)
        hbox_mark.addWidget(self.sb_mark_size)

        self.cb_same_mark_color_with_particle = QCheckBox(dialog)
        hbox_mark2 = QHBoxLayout()
        hbox_mark2.addWidget(self.cb_same_mark_color_with_particle)

        vbox_mark.addLayout(hbox_mark)
        vbox_mark.addLayout(hbox_mark2)

        # Display Tab - Trajectory
        self.gb_display_trajectory = QGroupBox(dialog)
        vbox_trajectory = QVBoxLayout(self.gb_display_trajectory)

        self.lb_trajectory_color = QLabel(dialog)
        self.lb_trajectory_color_display = ColorLabel(dialog)
        self.lb_trajectory_color_display.setFixedSize(76, 20)
        self.lb_trajectory_size = QLabel(dialog)
        self.sb_trajectory_size = QSpinBox(dialog)
        hbox_trajectory1 = QHBoxLayout()
        hbox_trajectory1.addWidget(self.lb_trajectory_color)
        hbox_trajectory1.addWidget(self.lb_trajectory_color_display)
        hbox_trajectory1.addWidget(self.lb_trajectory_size)
        hbox_trajectory1.addWidget(self.sb_trajectory_size)

        self.cb_same_trajectory_color_with_particle = QCheckBox(dialog)
        hbox_trajectory2 = QHBoxLayout()
        hbox_trajectory2.addWidget(self.cb_same_trajectory_color_with_particle)

        self.cb_speed_color = QCheckBox(dialog)
        self.lb_speed_color_display = ColorLabel(dialog)
        self.lb_speed_color_display.setFixedSize(76, 20)
        hbox_trajectory3 = QHBoxLayout()
        hbox_trajectory3.addWidget(self.cb_speed_color)
        hbox_trajectory3.addWidget(self.lb_speed_color_display)

        self.lb_min_speed = QLabel(dialog)
        self.le_min_speed = QLineEdit('', dialog)
        self.lb_max_speed = QLabel(dialog)
        self.le_max_speed = QLineEdit('', dialog)
        self.le_min_speed.setValidator(QIntValidator(1, 99999, self.le_min_speed))
        self.le_max_speed.setValidator(QIntValidator(1, 99999, self.le_max_speed))
        hbox_trajectory4 = QHBoxLayout()
        hbox_trajectory4.addWidget(self.lb_min_speed)
        hbox_trajectory4.addWidget(self.le_min_speed)
        hbox_trajectory4.addWidget(self.lb_max_speed)
        hbox_trajectory4.addWidget(self.le_max_speed)

        vbox_trajectory.addLayout(hbox_trajectory1)
        vbox_trajectory.addLayout(hbox_trajectory2)
        vbox_trajectory.addLayout(hbox_trajectory3)
        vbox_trajectory.addLayout(hbox_trajectory4)

        vbox_display.addWidget(self.gb_display_particle)
        vbox_display.addWidget(self.gb_display_mark)
        vbox_display.addWidget(self.gb_display_trajectory)

        # Export Tab
        self.tab_export = QWidget(dialog)
        vbox_export = QVBoxLayout(self.tab_export)

        # Export Tab - Param
        self.gb_export_param = QGroupBox(dialog)
        vbox_export_param = QVBoxLayout(self.gb_export_param)

        self.lb_export_scale = QLabel(dialog)
        self.dsb_export_scale = QDoubleSpinBox(dialog)
        self.dsb_export_scale.setDecimals(1)
        self.dsb_export_scale.setRange(0, 10)
        self.lb_export_speed = QLabel(dialog)
        self.dsb_export_speed = QDoubleSpinBox(dialog)
        self.dsb_export_speed.setDecimals(1)
        self.dsb_export_speed.setSingleStep(0.1)
        self.dsb_export_speed.setRange(0, 10)
        hbox_export_param_1 = QHBoxLayout()
        hbox_export_param_1.addWidget(self.lb_export_scale)
        hbox_export_param_1.addWidget(self.dsb_export_scale)
        hbox_export_param_1.addWidget(self.lb_export_speed)
        hbox_export_param_1.addWidget(self.dsb_export_speed)
        vbox_export_param.addLayout(hbox_export_param_1)

        self.cb_export_show_time = QCheckBox(dialog)
        self.cb_export_show_info = QCheckBox(dialog)
        hbox_export_param_2 = QHBoxLayout()
        hbox_export_param_2.addWidget(self.cb_export_show_time)
        hbox_export_param_2.addWidget(self.cb_export_show_info)
        vbox_export_param.addLayout(hbox_export_param_2)

        vbox_export.addWidget(self.gb_export_param)

        self.tab_widget.addTab(self.tab_analyze, dialog.tr(constant.settings_tab_analyze))
        self.tab_widget.addTab(self.tab_display, dialog.tr(constant.settings_tab_display))
        self.tab_widget.addTab(self.tab_export, dialog.tr(constant.settings_tab_export))

        self.bt_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        self.bt_box.accepted.connect(dialog.accept)
        self.bt_box.rejected.connect(dialog.reject)

        base_vbox.addWidget(self.tab_widget)
        base_vbox.addWidget(self.bt_box)
        self.init_data()
        self.translate()

    def init_data(self):
        self.sb_median_blur.setValue(self.settings.int_value(default_settings.median_blur))
        self.sb_gaussian_blur.setValue(self.settings.int_value(default_settings.gaussian_blur))
        self.sb_opening_size.setValue(self.settings.int_value(default_settings.opening_size))
        self.sb_closing_size.setValue(self.settings.int_value(default_settings.closing_size))
        self.cb_apply_hist_eq.setChecked(self.settings.boolean_value(default_settings.apply_hist_eq))
        self.sb_adaptive_hist_eq.setValue(self.settings.int_value(default_settings.adaptive_hist_eq))
        self.sb_bilateral_filter_size.setValue(self.settings.int_value(default_settings.bilateral_size))
        self.sb_bilateral_filter_color.setValue(self.settings.int_value(default_settings.bilateral_color))
        self.sb_bilateral_filter_space.setValue(self.settings.int_value(default_settings.bilateral_space))
        self.le_search_radius.setText(self.settings.str_value(default_settings.search_radius))
        self.le_minimum_detect_area.setText(self.settings.str_value(default_settings.minimum_area_for_detection))
        self.le_maximum_detect_area.setText(self.settings.str_value(default_settings.maximum_area_for_detection))
        self.le_memory_frames.setText(self.settings.str_value(default_settings.memory_frames))
        self.le_threshold.setText(self.settings.str_value(default_settings.threshold))
        self.sb_derivative_order.setValue(self.settings.int_value(default_settings.derivative_order))
        self.cb_kernel_size.setCurrentText(self.settings.str_value(default_settings.kernel_size))
        self.cb_split_particles.setChecked(self.settings.boolean_value(default_settings.split_circular_particles))
        self.sb_particle_radius_for_split.setValue(self.settings.int_value(default_settings.split_radius))
        self.le_from_frames.setText(self.settings.str_value(default_settings.from_frames))
        self.le_to_frames.setText(self.settings.str_value(default_settings.to_frames))
        self.update_color_label(self.lb_particle_color_display, default_settings.particle_color)
        self.sb_particle_size.setValue(self.settings.int_value(default_settings.particle_size))
        self.update_color_label(self.lb_mark_color_display, default_settings.mark_color)
        self.sb_mark_size.setValue(self.settings.int_value(default_settings.mark_size))
        self.cb_same_mark_color_with_particle.setChecked(
            self.settings.boolean_value(default_settings.same_mark_color_with_particle))
        self.update_color_label(self.lb_trajectory_color_display, default_settings.trajectory_color)
        self.sb_trajectory_size.setValue(self.settings.int_value(default_settings.trajectory_size))
        self.cb_speed_color.setChecked(self.settings.boolean_value(default_settings.enable_trajectory_speed_color))
        self.update_color_label(self.lb_speed_color_display, default_settings.trajectory_speed_color)
        self.le_min_speed.setText(self.settings.str_value(default_settings.min_speed))
        self.le_max_speed.setText(self.settings.str_value(default_settings.max_speed))
        self.dsb_export_scale.setValue(self.settings.float_value(default_settings.export_scale))
        self.dsb_export_speed.setValue(self.settings.float_value(default_settings.export_speed))
        self.cb_export_show_time.setChecked(self.settings.boolean_value(default_settings.export_show_time))
        self.cb_export_show_info.setChecked(self.settings.boolean_value(default_settings.export_show_info))

    def update_color_label(self, label: ColorLabel, item: default_settings.setting_item):
        colors = self.settings.list_value(item)
        colors = [QColor(c) for c in colors]
        label.set_color(colors)

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
        self.lb_from_frames.setText(self.dialog.tr(constant.settings_widget_from_frames))
        self.lb_to_frames.setText(self.dialog.tr(constant.settings_widget_to_frames))
        self.lb_particle_color.setText(self.dialog.tr(constant.settings_widget_particle_color))
        self.lb_particle_size.setText(self.dialog.tr(constant.settings_widget_particle_size))
        self.lb_mark_color.setText(self.dialog.tr(constant.settings_widget_mark_color))
        self.lb_mark_size.setText(self.dialog.tr(constant.settings_widget_mark_size))
        self.cb_same_mark_color_with_particle.setText(
            self.dialog.tr(constant.settings_widget_same_mark_color_with_particle))
        self.lb_trajectory_color.setText(self.dialog.tr(constant.settings_widget_trajectory_color))
        self.lb_trajectory_size.setText(self.dialog.tr(constant.settings_widget_trajectory_size))
        self.cb_same_trajectory_color_with_particle.setText(
            self.dialog.tr(constant.settings_widget_same_trajectory_color_with_particle))
        self.cb_speed_color.setText(self.dialog.tr(constant.settings_widget_enable_speed_color))
        self.lb_min_speed.setText(self.dialog.tr(constant.settings_widget_min_speed))
        self.lb_max_speed.setText(self.dialog.tr(constant.settings_widget_max_speed))
        self.lb_export_scale.setText(self.dialog.tr(constant.settings_widget_export_scale))
        self.lb_export_speed.setText(self.dialog.tr(constant.settings_widget_export_speed))
        self.cb_export_show_time.setText(self.dialog.tr(constant.settings_widget_show_time))
        self.cb_export_show_info.setText(self.dialog.tr(constant.settings_widget_show_info))


class ColorEditorUi(object):
    def __init__(self, color_editor: QDialog):
        self.color_editor = color_editor
        self.hbox_base = QHBoxLayout(color_editor)
        self.lv_color = ColorListWidget(color_editor)

        self.lv_color.setGridSize(QSize(100, 32))
        self.lv_color.setViewMode(QListView.ListMode)
        self.lv_color.setMovement(QListView.Free)

        self.bt_add = QPushButton(color_editor)
        self.bt_delete = QPushButton(color_editor)
        self.bt_random = QPushButton(color_editor)
        self.bt_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Vertical, color_editor)
        self.bt_box.addButton(self.bt_add, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.addButton(self.bt_delete, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.addButton(self.bt_random, QDialogButtonBox.ButtonRole.ActionRole)
        self.bt_box.accepted.connect(color_editor.accept)
        self.bt_box.rejected.connect(color_editor.reject)

        self.hbox_base.addWidget(self.lv_color)
        self.hbox_base.addWidget(self.bt_box)

        self.translate()

    def translate(self):
        self.bt_add.setText(self.color_editor.tr(constant.color_edit_widget_add))
        self.bt_delete.setText(self.color_editor.tr(constant.color_edit_widget_delete))
        self.bt_random.setText(self.color_editor.tr(constant.color_edit_widget_random))


class ColorWidgetUi(object):
    def __init__(self, parent: QWidget, color: QColor, height: int):
        margin = 4
        self.layout = QHBoxLayout(parent)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(margin)
        self.color_name = QColor(color).name()
        self.lb_color = ColorLabel(parent)
        self.lb_color.setFixedSize(64, height - 2 * margin)
        self.lb_color.set_color([color])
        self.lb_color_name = QLabel(parent)
        self.lb_color_name.setText(self.color_name)
        self.layout.addWidget(self.lb_color)
        self.layout.addWidget(self.lb_color_name)
        self.layout.addItem(QSpacerItem(20, height, QSizePolicy.Minimum, QSizePolicy.Expanding))


def is_odd(value: int):
    return value % 2 == 1


def minus_one(value: int):
    return value - 1


def spinbox_validation(spinbox: QSpinBox, cond: Callable, correct_func: Callable):
    if not cond(spinbox.value()):
        spinbox.setValue(correct_func(spinbox.value()))
