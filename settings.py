from typing import Any

from PySide6.QtCore import QSettings

from default_settings import *


class Settings(object):
    def __init__(self, setting_path: str):
        self.setting_path = setting_path
        self.settings = QSettings(setting_path, QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

    def int_value(self, item: default_setting):
        return int(self.value(item))

    def float_value(self, item: default_setting):
        return float(self.value(item))

    def value(self, item: default_setting):
        return self.settings.value(f'{item.section}/{item.key}', item.value)

    def set_value(self, item: default_setting, value: Any):
        self.settings.setValue(f'{item.section}/{item.key}', value)
