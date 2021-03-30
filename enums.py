from enum import Enum


class OperationMode(Enum):
    """
    VideoView 的操作类型
    """
    SELECT = 0
    MOVE = 1
    CROP = 2
    ADD = 3
