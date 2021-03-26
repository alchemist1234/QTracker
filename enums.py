from enum import Enum


class OperationMode(Enum):
    """
    VideoView 的操作类型
    """
    MOVE = 0
    CROP = 1
    ADD = 2
