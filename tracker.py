from collections import namedtuple
from enum import Enum

import cv2
import numpy as np
from PySide2.QtCore import Signal, QThread

from config import ConfigName
from data import FrameData

AUTO_SEC = 'Auto'

HistoryParticle = namedtuple('HistoryParticle', ['center', 'frame'])


class Judgement(Enum):
    FALSE = 0b_00
    TRUE = 0b_01
    TOUCHING_FALSE = 0b_10
    TOUCHING_TRUE = 0b_11


class Tracker(QThread):
    sig_analyze_start = Signal()
    sig_analyze_progress = Signal(int, int, str)
    sig_analyze_finish = Signal()
    sig_frame_finished = Signal(int, FrameData)

    def __init__(self, frames: dict, configs: dict, vid: cv2.VideoCapture, parent=None):
        super(Tracker, self).__init__(parent)
        self.frames = frames
        self.configs = configs
        self.vid = vid
        self.frame_particles = {}
        self.history_particles = {}
        self.max_label = 0

    def run(self):
        frame_indexes = list(self.frames.keys())
        frame_indexes.sort()
        self.sig_analyze_start.emit()
        for i in range(len(frame_indexes)):
            index = frame_indexes[i]
            self.analyze(index)
            self.sig_frame_finished.emit(index, FrameData(index, self.frames[index], self.frame_particles[index]))
            self.sig_analyze_progress.emit(len(frame_indexes), i + 1, 'analyzing')
        self.sig_analyze_finish.emit()
        print('analyze finished')

    def analyze(self, frame_index):
        self.frame_particles[frame_index] = {}
        frame = self.frames[frame_index].copy()
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

        max_stack = ordered_centers.shape[2]

        memory_frames = self.configs[ConfigName.MEMORY_FRAMES.value]
        for center in ordered_centers:
            center_tuple = tuple(np.ravel(center).astype(int))
            for index, history_center in self.history_particles.items():
                if frame_index - history_center.frame <= memory_frames and \
                        self.same_particle(history_center.center, center_tuple):
                    self.history_particles[index] = HistoryParticle(center_tuple, frame_index)
                    self.frame_particles[frame_index][index] = center_tuple
                    break
            else:
                self.frame_particles[frame_index][self.max_label] = center_tuple
                self.history_particles[self.max_label] = HistoryParticle(center_tuple, frame_index)
                self.max_label += 1

    def same_particle(self, old_center, new_center):
        dis = 40
        return abs(new_center[0] - old_center[0]) <= dis and abs(new_center[1] - old_center[1]) <= dis

    def smooth(self, frame):
        if len(frame.shape) == 3:
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = frame

        if self.configs[ConfigName.APPLY_HIST_EQ.value]:
            image_gray = cv2.equalizeHist(image_gray)

        for j in range(self.configs[ConfigName.ADAPTIVE_HIST_EQ.value]):
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            image_gray = clahe.apply(image_gray)

        bilateral_size = self.configs[ConfigName.BILATERAL_SIZE.value]
        bilateral_color = self.configs[ConfigName.BILATERAL_COLOR.value]
        bilateral_space = self.configs[ConfigName.BILATERAL_SPACE.value]
        if bilateral_size != 0:
            image_gray = cv2.bilateralFilter(image_gray, bilateral_size, bilateral_color, bilateral_space)

        image_gray = cv2.medianBlur(image_gray, self.configs[ConfigName.MEDIAN_BLUR.value])
        image_gray = cv2.GaussianBlur(image_gray, (self.configs[ConfigName.GAUSSIAN_BLUR.value],) * 2, 0)
        frame = image_gray.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame, image_gray

    def binary(self, image):
        derivative_order = self.configs[ConfigName.DERIVATIVE_ORDER.value]
        sobel_x = self.get_sobel(image, derivative_order, 0)
        sobel_y = self.get_sobel(image, 0, derivative_order)
        sobel_both = cv2.bitwise_or(sobel_x, sobel_y)
        return sobel_both

    def get_sobel(self, image, x, y):
        sobel = cv2.Sobel(image, cv2.CV_64F, x, y, self.configs[ConfigName.KERNEL_SIZE.value])
        sobel = np.absolute(sobel)
        sobel = sobel - sobel.min()
        thresh = np.zeros(sobel.shape, np.uint8)
        thresh[sobel > self.configs[ConfigName.KERNEL_SIZE.value]] = 255
        sobel = self.morphology(thresh)
        return sobel

    def morphology(self, image):
        kernel = np.ones((self.configs[ConfigName.CLOSING_SIZE.value],) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((self.configs[ConfigName.OPENING_SIZE.value],) * 2, np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return image

    def get_contours(self, contours):
        m_list = []
        cnt_list = []
        for cnt_index in range(len(contours)):
            cnt = contours[cnt_index]
            judgement, moment = self.particle_test(cnt)

            if judgement == Judgement.TRUE.value:
                m_list.append(moment)
                cnt_list.append(cnt)
            elif judgement >> 1:
                cnt_list_split = Tracker.split_particles_roi(self.configs[ConfigName.SPLIT_RADIUS], cnt)
                if len(cnt_list_split) > 1:
                    for c in cnt_list_split:
                        m_list.append(cv2.moments(c))
                        cnt_list.append(c)
                elif len(cnt_list_split) == 1 and judgement & 1:
                    m_list.append(moment)
                    cnt_list.append(cnt_list_split[0])
        return m_list, cnt_list

    def particle_test(self, contours):
        max_area = self.configs[ConfigName.MAXIMUM_AREA_FOR_DETECTION.value]
        min_area = self.configs[ConfigName.MINIMUM_AREA_FOR_DETECTION.value]
        moments = cv2.moments(contours)
        area = moments['m00']

        judgement = Judgement.FALSE.value
        if min_area < area <= max_area:
            judgement = Judgement.TRUE.value

        if self.configs[ConfigName.SPLIT_CIRCULAR_PARTICLES.value]:
            r_approx = np.sqrt(area / np.pi)
            is_touching = self.configs[ConfigName.SPLIT_RADIUS.value] <= r_approx
            if is_touching:
                judgement = judgement | 2
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
        roi_touching = cv2.resize(roi_touching, dsize=None, fx=ff, fy=ff, interpolation=cv2.INTER_LINEAR)
        radius = ff * radius
        cnt_list_split = Tracker.split_particles(roi_touching, radius)
        cnt_list_split = [c / ff + np.array([x, y]) for c in cnt_list_split]
        return cnt_list_split

    @staticmethod
    def split_particles(binary, radius):
        r = int(radius * 0.75)
        kernel = Tracker.circular_kernel(r)
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
