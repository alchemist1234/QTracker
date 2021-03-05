import configparser
from enum import Enum

from PySide2.QtWidgets import QWidget, QSpinBox, QCheckBox, QListView


class ConfigName(Enum):
    MEDIAN_BLUR = 'median_blur'
    GAUSSIAN_BLUR = 'gaussian_blur'
    OPENING_SIZE = 'opening_size'
    CLOSING_SIZE = 'closing_size'
    APPLY_HIST_EQ = 'apply_hist_eq'
    ADAPTIVE_HIST_EQ = 'adaptive_hist_eq'
    BILATERAL_SIZE = 'bilateral_size'
    BILATERAL_COLOR = 'bilateral_color'
    BILATERAL_SPACE = 'bilateral_space'
    SEARCH_RADIUS = 'search_radius'
    MINIMUM_AREA_FOR_DETECTION = 'minimum_area_for_detection'
    MAXIMUM_AREA_FOR_DETECTION = 'maximum_area_for_detection'
    MEMORY_FRAMES = 'memory_frames'
    THRESHOLD = 'threshold'
    DERIVATIVE_ORDER = 'derivative_order'
    KERNEL_SIZE = 'kernel_size'
    SPLIT_CIRCULAR_PARTICLES = 'split_circular_particles'
    SPLIT_RADIUS = 'split_radius'
    FIT_TO_SCREEN = 'fit_to_screen'
    SHOW_BINARY_IMAGE = 'show_binary_image'
    SKIP_FRAMES = 'skip_frames'
    FROM_FRAME = 'from_frame'
    TO_FRAME = 'to_frame'
    FILE_PATH = "file_path"
    DIR_PATH = "dir_path"


class Config(object):
    config_file = 'config.ini'

    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(Config.config_file, 'GBK')

    def set(self, section: str, key: str, value: str):
        if section not in self.cfg.sections():
            self.cfg.add_section(section)
        self.cfg.set(section, key, value)

    def set_widget_value(self, section: str, widget: QWidget):
        if isinstance(widget, QSpinBox):
            self.set(section, widget.whatsThis(), str(widget.value()))
        if isinstance(widget, QCheckBox):
            self.set(section, widget.whatsThis(), str(widget.isChecked()))
        if isinstance(widget, QListView):
            model = widget.model()
            path = model.filePath(widget.currentIndex())
            self.set(section, widget.whatsThis(), path)

    def get_widget_value(self, section: str, widget: QWidget):
        config = None
        if isinstance(widget, QSpinBox):
            config = self.get_int(section, widget.whatsThis())
            widget.setValue(config)
        if isinstance(widget, QCheckBox):
            config = self.get_bool(section, widget.whatsThis())
            widget.setChecked(config)
        if isinstance(widget, QListView):
            config = self.get(section, widget.whatsThis())
            model = widget.model()
            index = model.index(config)
            parent_index = index.parent()
            widget.setRootIndex(parent_index)
            widget.setCurrentIndex(parent_index)
        return config

    def get(self, section: str, key: str):
        if section in self.cfg.sections():
            if key in self.cfg.options(section):
                return self.cfg.get(section, key)
        return None

    def get_int(self, section: str, key: str):
        if section in self.cfg.sections():
            if key in self.cfg.options(section):
                return self.cfg.getint(section, key)
        return 0

    def get_float(self, section: str, key: str):
        if section in self.cfg.sections():
            if key in self.cfg.options(section):
                return self.cfg.getfloat(section, key)
        return 0

    def get_bool(self, section: str, key: str):
        if section in self.cfg.sections():
            if key in self.cfg.options(section):
                return self.cfg.getboolean(section, key)
        return False

    def get_config_map(self, section: str, widget: QWidget):
        config_map = {}
        for child in widget.children():
            if isinstance(child, QWidget) and child.whatsThis() != '':
                config = self.get_widget_value(section, child)
                config_map[child.whatsThis()] = config
            config_map.update(self.get_config_map(section, child))
        return config_map

    def flush(self):
        with open(Config.config_file, 'w+') as f:
            self.cfg.write(f)


cfg = Config()
