import os
from typing import Dict

from PySide2.QtCore import Signal, QThread
from PySide2.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem
from PySide2.QtGui import QImage, QPainter
from cv2 import VideoWriter
import numpy as np

from item import SceneConfig, FrameItem, MarkItem


class VideoExporter(QThread):
    default_file_ext = '.avi'
    codes_map = {
        '.avi': 'XVID',
        '.flv': 'FLV1',
        '.mp4': 'X264',
        '.ogv': 'THEO'
    }
    sig_update_scene = Signal(int, QImage)

    def __init__(self, file_path: str, width: int, height: int, scenes: Dict[int, QGraphicsScene],
                 config: SceneConfig):
        super(VideoExporter, self).__init__()
        self.file_path = file_path
        self.file_name, self.file_ext = os.path.splitext(file_path)
        if self.file_ext not in VideoExporter.codes_map:
            self.file_ext = VideoExporter.default_file_ext
            self.file_path = self.file_name + self.file_ext
        self.width = width
        self.height = height
        self.scenes = scenes
        self.config = config

    def run(self) -> None:
        writer = VideoWriter()
        fourcc = VideoExporter.codes_map[self.file_ext]
        writer.open(self.file_path, VideoWriter.fourcc(*fourcc), self.config.fps, (self.width, self.height), True)
        for scene in self.scenes.values():
            img = QImage(self.config.crop_size, QImage.Format_ARGB32)
            print(f'exporter emmit: {scene.frame_index}')
            self.sig_update_scene.emit(scene.frame_index, img)
            print(f'exporter emmit over: {scene.frame_index}')
            painter = QPainter()
            painter.begin(img)
            print(f'render begin: {scene.frame_index}')
            scene.render(painter)
            print(f'render finish: {scene.frame_index}')
            painter.end()

            shape = (img.height(), img.bytesPerLine() * 8 // img.depth(), 4)
            print(f'shape created: {scene.frame_index}')
            ptr = img.bits()
            arr = np.array(ptr, dtype=np.uint8).reshape(shape)
            arr = arr[..., :3]
            print(f'before write: {scene.frame_index}')
            writer.write(arr)
            print(f'write finish: {scene.frame_index}')
        print('exported')
