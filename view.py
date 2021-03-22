from typing import NoReturn

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import *


class VideoView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.fixed_widgets = dict()

    def add_fixed_widget(self, widget: QWidget, alignment: Qt.AlignmentFlag):
        """
        添加固定控件
        :param widget: 控件
        :param alignment: 对齐方式
        """
        widget.setParent(self.viewport())
        self.fixed_widgets[widget] = alignment

    def showEvent(self, event):
        self._update_fixed_widgets()
        super(VideoView, self).showEvent(event)

    def resizeEvent(self, event):
        self._update_fixed_widgets()
        super(VideoView, self).resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> NoReturn:
        mouse_pos = event.position()
        scene_pos = self.mapToScene(mouse_pos.toPoint())
        view_w = self.viewport().width()
        view_h = self.viewport().height()
        h_scale = mouse_pos.x() / view_w
        v_scale = mouse_pos.y() / view_h

        wheel_delta = event.angleDelta().y()
        if wheel_delta > 0:
            self.scale(1.2, 1.2)
        else:
            self.scale(1 / 1.2, 1 / 1.2)
        view_point = self.transform().map(scene_pos)
        self.horizontalScrollBar().setValue(view_point.x() - view_w * h_scale)
        self.verticalScrollBar().setValue(view_point.y() - view_h * v_scale)
        self._update_fixed_widgets()

    def _update_fixed_widgets(self):
        r = self.viewport().rect()
        for w, a in self.fixed_widgets.items():
            p = QPoint()

            if a & Qt.AlignHCenter:
                p.setX((r.width() - w.width()) / 2)
            elif a & Qt.AlignRight:
                p.setX(r.width() - w.width())

            if a & Qt.AlignVCenter:
                p.setY((r.height() - w.height()) / 2)
            elif a & Qt.AlignBottom:
                p.setY(r.height() - w.height())
            w.move(p)
