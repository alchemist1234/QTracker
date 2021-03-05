from typing import Set, NoReturn, List

from PySide6.QtCore import Qt, Slot, Signal, QPoint
from PySide6.QtGui import QWheelEvent, QMouseEvent, QColor, QImage
from PySide6.QtWidgets import *


class VideoView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.m_widgets = dict()

    def addFixedWidget(self, widget: QWidget, alignment):
        widget.setParent(self.viewport())
        self.m_widgets[widget] = alignment

    def showEvent(self, event):
        self._update_fixed_widgets()
        super(VideoView, self).showEvent(event)

    def resizeEvent(self, event):
        self._update_fixed_widgets()
        super(VideoView, self).resizeEvent(event)

    def _update_fixed_widgets(self):
        r = self.viewport().rect()
        for w, a in self.m_widgets.items():
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
