from enum import Enum


class OperationMode(Enum):
    """
    VideoView 的操作类型
    """
    SELECT = 0
    CROP = 1
    MOVE = 2
    ADD = 3
    REMOVE = 4
    COMBINE = 5
