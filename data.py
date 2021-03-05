from typing import Dict, Tuple
from PySide6.QtCore import QObject
import numpy as np


class VideoData(object):
    def __init__(self):
        self._file_path = None
        self._fps = 0
        self._width = 0
        self._height = 0
        self._frames = 0

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self._file_path = file_path

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps: int):
        self._fps = fps

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def frame_count(self):
        return self._frames

    @frame_count.setter
    def frame_count(self, frames: int):
        self._frames = frames


class ParticleData(object):
    def __init__(self):
        self._frame_count = 0
        self._particle_pos = {}

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def particle_pos(self):
        return self._particle_pos

    def clear_data(self):
        self._frame_count = 0
        self._particle_pos.clear()

    def add_data(self, frame_index: int, particles: Dict[int, Tuple[int, int]]):
        if frame_index not in self._particle_pos:
            self._frame_count += 1
        self._particle_pos[frame_index] = particles
