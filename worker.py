import sys
import os
from collections import namedtuple
from typing import List, Dict, Set
from enum import Enum
import time

from PySide6.QtCore import QThread, Signal, QObject, QByteArray, QBuffer, QIODevice, Slot, QTimer, QRectF, QRect
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QMessageBox
import cv2
import numpy as np

from data import VideoData
from settings import Settings
import constant
import default_settings
from scene import VideoScene


class VideoLoader(QThread):
    sig_start = Signal(int)
    sig_progress = Signal(int, int, str)
    sig_frame_finished = Signal(int, bytes, dict)
    sig_all_finished = Signal()

    def __init__(self, settings: Settings, parent=None):
        super(VideoLoader, self).__init__(parent)
        self.settings = settings
        self.video_data = VideoData()
        self.vid = None
        self.analyzer = Analyzer(settings, self)

    def set_file(self, file_path: str) -> VideoData:
        self.video_data.file_path = file_path
        self.vid = cv2.VideoCapture(file_path)
        self.video_data.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_data.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_data.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.video_data.frame_count = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        return self.video_data

    def run(self):
        if self.vid is None:
            QMessageBox.warning(self.parent(), '错误', '未选择文件')
            return
        self.sig_start.emit(self.video_data.frame_count)
        frame_index = 0
        while True:
            ret, frame = self.vid.read()
            if not ret:
                break
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_index += 1
            origin_h, origin_w, ch = frame.shape
            img = QImage(frame.data, origin_w, origin_h, ch * origin_w, QImage.Format_BGR888)
            base64 = self.image_to_base64(img)

            frame_particles = self.analyzer.analyze(frame_index, color_frame)
            self.sig_progress.emit(self.video_data.frame_count, frame_index, self.tr(constant.status_reading))
            self.sig_frame_finished.emit(frame_index, base64, frame_particles)
        self.sig_all_finished.emit()

    def image_to_base64(self, img: QImage) -> bytes:
        quality = self.settings.int_value(default_settings.frame_quality)
        byte_arr = QByteArray()
        buffer = QBuffer(byte_arr)
        buffer.open(QIODevice.WriteOnly)
        img.save(buffer, 'jpg', quality)
        return byte_arr.toBase64().data()


class Analyzer(QObject):
    HistoryParticle = namedtuple('HistoryParticle', ['center', 'frame'])

    class Judgement(Enum):
        FALSE = 0b_00
        TRUE = 0b_01
        TOUCHING_FALSE = 0b_10
        TOUCHING_TRUE = 0b_11

    def __init__(self, settings: Settings, parent=None):
        super(Analyzer, self).__init__(parent)
        self.settings = settings
        self.history_particles = {}
        self.max_label = 0

    def analyze(self, frame_index: int, frame: np.ndarray):
        frame_particles = {}
        frame, frame_gray = self.smooth(frame)
        binary = self.binary(frame_gray)
        contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        m_list, cnt_list = self.get_contours(contours)

        ordered_centers = -1 * np.ones((0, 2, 1))

        for (mind, m) in enumerate(m_list):
            center = self.get_contour_info(m)
            new_row = -1 * np.ones((1, 2, ordered_centers.shape[2]))
            new_row[0, :, 0] = center
            ordered_centers = np.append(ordered_centers, new_row, axis=0)

        memory_frames = self.settings.int_value(default_settings.memory_frames)
        for center in ordered_centers:
            center_tuple = tuple(np.ravel(center).astype(int))
            for index, history_center in self.history_particles.items():
                if frame_index - history_center.frame <= memory_frames and \
                        self.same_particle(history_center.center, center_tuple):
                    self.history_particles[index] = Analyzer.HistoryParticle(center_tuple, frame_index)
                    frame_particles[index] = center_tuple
                    break
            else:
                frame_particles[self.max_label] = center_tuple
                self.history_particles[self.max_label] = Analyzer.HistoryParticle(center_tuple, frame_index)
                self.max_label += 1
        return frame_particles

    def same_particle(self, old_center, new_center):
        dis = self.settings.int_value(default_settings.memory_frames)
        return abs(new_center[0] - old_center[0]) <= dis and abs(new_center[1] - old_center[1]) <= dis

    def smooth(self, frame):
        if len(frame.shape) == 3:
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = frame

        if self.settings.boolean_value(default_settings.apply_hist_eq):
            image_gray = cv2.equalizeHist(image_gray)

        for j in range(self.settings.int_value(default_settings.adaptive_hist_eq)):
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            image_gray = clahe.apply(image_gray)

        bilateral_size = self.settings.int_value(default_settings.bilateral_size)
        bilateral_color = self.settings.int_value(default_settings.bilateral_color)
        bilateral_space = self.settings.int_value(default_settings.bilateral_space)
        if bilateral_size != 0:
            image_gray = cv2.bilateralFilter(image_gray, bilateral_size, bilateral_color, bilateral_space)

        image_gray = cv2.medianBlur(image_gray, self.settings.int_value(default_settings.median_blur))
        image_gray = cv2.GaussianBlur(image_gray, (self.settings.int_value(default_settings.gaussian_blur),) * 2, 0)
        frame = image_gray.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame, image_gray

    def binary(self, image):
        derivative_order = self.settings.int_value(default_settings.derivative_order)
        sobel_x = self.get_sobel(image, derivative_order, 0)
        sobel_y = self.get_sobel(image, 0, derivative_order)
        sobel_both = cv2.bitwise_or(sobel_x, sobel_y)
        return sobel_both

    def get_sobel(self, image, x, y):
        kernel_size = self.settings.int_value(default_settings.kernel_size)
        sobel = cv2.Sobel(image, cv2.CV_64F, x, y, kernel_size)
        sobel = np.absolute(sobel)
        sobel = sobel - sobel.min()
        thresh = np.zeros(sobel.shape, np.uint8)
        thresh[sobel > kernel_size] = 255
        sobel = self.morphology(thresh)
        return sobel

    def morphology(self, image):
        kernel = np.ones((self.settings.int_value(default_settings.closing_size),) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((self.settings.int_value(default_settings.opening_size),) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return image

    def get_contours(self, contours):
        m_list = []
        cnt_list = []
        for cnt_index in range(len(contours)):
            cnt = contours[cnt_index]
            judgement, moment = self.particle_test(cnt)

            if judgement == Analyzer.Judgement.TRUE.value:
                m_list.append(moment)
                cnt_list.append(cnt)
            # elif judgement >> 1:
            #     cnt_list_split = Analyzer.split_particles_roi(self.settings.int_value(default_settings.split_radius),
            #                                                   cnt)
            #     if len(cnt_list_split) > 1:
            #         for c in cnt_list_split:
            #             print(c)
            #             print(c.shape)
            #             m_list.append(cv2.moments(c))
            #             cnt_list.append(c)
            #     elif len(cnt_list_split) == 1 and judgement & 1:
            #         m_list.append(moment)
            #         cnt_list.append(cnt_list_split[0])
        return m_list, cnt_list

    def particle_test(self, contours):
        max_area = self.settings.int_value(default_settings.maximum_area_for_detection)
        min_area = self.settings.int_value(default_settings.minimum_area_for_detection)
        moments = cv2.moments(contours)
        area = moments['m00']

        judgement = Analyzer.Judgement.FALSE.value
        if min_area < area <= max_area:
            judgement = Analyzer.Judgement.TRUE.value

        if self.settings.boolean_value(default_settings.split_circular_particles):
            r_approx = np.sqrt(area / np.pi)
            is_touching = self.settings.int_value(default_settings.split_radius) * 1.05 <= r_approx
            if is_touching:
                judgement = judgement | 0b_10
        return judgement, moments

    @staticmethod
    def get_contour_info(m):
        area = m['m00']
        cx = int(round(m['m10'] / area))
        cy = int(round(m['m01'] / area))
        center = np.array([cx, cy])
        return center

    @staticmethod
    def split_particles_roi(radius, cnt):
        x, y, w, h = cv2.boundingRect(cnt)
        roi_touching = np.zeros((h, w), dtype=np.uint8)
        cnt = cnt - np.array([x, y])
        cv2.drawContours(roi_touching, [cnt], 0, 255, -1)

        ff = 3
        roi_touching = cv2.resize(roi_touching, None, fx=ff, fy=ff, interpolation=cv2.INTER_LINEAR)
        radius = ff * radius
        cnt_list_split = Analyzer.split_particles(roi_touching, radius)
        cnt_list_split = [c / ff + np.array([x, y]) for c in cnt_list_split]
        return cnt_list_split

    @staticmethod
    def split_particles(binary, radius):
        r = int(radius * 0.75)
        kernel = Analyzer.circular_kernel(r)
        eroded = cv2.erode(binary, kernel, iterations=1)
        erode_contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnt_list_split = []
        for cnt in erode_contours:
            split_particle = np.zeros(binary.shape, np.uint8)
            cv2.drawContours(split_particle, [cnt], 0, 255, -1)
            split_particle = cv2.dilate(split_particle, kernel, iterations=1)
            split_cnt, _ = cv2.findContours(split_particle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt_list_split.append(split_cnt[0])
        return cnt_list_split

    @staticmethod
    def circular_kernel(r):
        y, x = np.ogrid[-r: r + 1, -r: r + 1]
        return (y * y + x * x <= r * r).astype(np.uint8)


class VideoExporter(QObject):
    default_file_ext = '.avi'
    codes_map = {
        '.avi': 'XVID',
        '.flv': 'FLV1',
        '.mp4': 'X264',
        '.ogv': 'THEO'
    }
    sig_export_start = Signal()
    sig_export_frame_updated = Signal(int, np.ndarray)
    sig_export_frame = Signal(int)
    sig_export_finish = Signal()

    def __init__(self, scene: VideoScene, settings: Settings):
        super().__init__()
        self._file_path = None
        self._file_name = None
        self._file_ext = None
        self._video_data = None
        self.scene = scene
        self.settings = settings
        self.writer = cv2.VideoWriter()
        # self.sig_export_frame_updated.connect(self.write_data)

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self._file_path = file_path
        self._file_name, self._file_ext = os.path.splitext(file_path)

    @property
    def video_data(self):
        return self._video_data

    @video_data.setter
    def video_data(self, video_data: VideoData):
        self._video_data = video_data

    def open_writer(self, source_rect: QRectF = None):
        rect = QRect(0, 0, self.video_data.width,
                     self.video_data.height) if source_rect is None else source_rect.toRect()
        fourcc_str = VideoExporter.codes_map[self._file_ext]
        fourcc = cv2.VideoWriter.fourcc(*fourcc_str)
        scale = self.settings.float_value(default_settings.export_scale)
        speed = self.settings.float_value(default_settings.export_speed)
        self.writer.open(self._file_path, fourcc, int(self.video_data.fps * speed),
                         (int(rect.width() * scale), int(rect.height() * scale)), True)

    def release_writer(self):
        self.writer.release()

    def export_arr(self, frame_index: int, source_rect: QRectF = None):
        self.scene.update_frame(frame_index)
        rect = QRect(0, 0, self.video_data.width,
                     self.video_data.height) if source_rect is None else source_rect.toRect()
        scale = self.settings.float_value(default_settings.export_scale)
        img = QImage(int(rect.width() * scale), int(rect.height() * scale), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.begin(img)
        self.scene.render(painter, source=rect)
        painter.end()
        shape = (img.height(), img.bytesPerLine() * 8 // img.depth(), 4)
        ptr = img.bits()
        arr = np.array(ptr, dtype=np.uint8).reshape(shape)
        arr = arr[..., :3]
        return arr

    @Slot(int, np.ndarray)
    def write_data(self, arr: np.ndarray):
        self.writer.write(arr)
