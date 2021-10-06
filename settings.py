from typing import Any

from PySide6.QtCore import QSettings

from default_settings import *


class Settings(object):
    """
    配置信息类
    """

    def __init__(self, setting_path: str):
        self.setting_path = setting_path
        self.settings = QSettings(setting_path, QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.set_value(index_filter, [])

    def sync(self):
        self.settings.sync()

    def int_value(self, item: setting_item):
        return int(self.value(item))

    def float_value(self, item: setting_item):
        return float(self.value(item))

    def boolean_value(self, item: setting_item):
        value = self.value(item)
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def list_value(self, item: setting_item):
        value = self.value(item)
        return value if isinstance(value, list) else [value]

    def str_value(self, item: setting_item):
        return str(self.value(item))

    def value(self, item: setting_item):
        return self.settings.value(f'{item.section}/{item.key}', item.default_value)

    def set_value(self, item: setting_item, value: Any) -> bool:
        key = f'{item.section}/{item.key}'
        old_value = self.settings.value(key)
        self.settings.setValue(f'{item.section}/{item.key}', value)
        # 如果新旧值不同，返回True，表示有更新
        return old_value != value
