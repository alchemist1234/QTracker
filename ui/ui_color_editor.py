# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_editor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ColorEditor(object):
    def setupUi(self, ColorEditor):
        if not ColorEditor.objectName():
            ColorEditor.setObjectName(u"ColorEditor")
        ColorEditor.resize(475, 300)
        self.horizontalLayout = QHBoxLayout(ColorEditor)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lv_color = QListWidget(ColorEditor)
        self.lv_color.setObjectName(u"lv_color")
        self.lv_color.setGridSize(QSize(100, 32))
        self.lv_color.setViewMode(QListView.ListMode)

        self.horizontalLayout.addWidget(self.lv_color)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bt_ok = QPushButton(ColorEditor)
        self.bt_ok.setObjectName(u"bt_ok")

        self.verticalLayout.addWidget(self.bt_ok)

        self.bt_cancel = QPushButton(ColorEditor)
        self.bt_cancel.setObjectName(u"bt_cancel")

        self.verticalLayout.addWidget(self.bt_cancel)

        self.bt_up = QPushButton(ColorEditor)
        self.bt_up.setObjectName(u"bt_up")

        self.verticalLayout.addWidget(self.bt_up)

        self.bt_down = QPushButton(ColorEditor)
        self.bt_down.setObjectName(u"bt_down")

        self.verticalLayout.addWidget(self.bt_down)

        self.bt_top = QPushButton(ColorEditor)
        self.bt_top.setObjectName(u"bt_top")

        self.verticalLayout.addWidget(self.bt_top)

        self.bt_bottom = QPushButton(ColorEditor)
        self.bt_bottom.setObjectName(u"bt_bottom")

        self.verticalLayout.addWidget(self.bt_bottom)

        self.bt_add = QPushButton(ColorEditor)
        self.bt_add.setObjectName(u"bt_add")

        self.verticalLayout.addWidget(self.bt_add)

        self.bt_delete = QPushButton(ColorEditor)
        self.bt_delete.setObjectName(u"bt_delete")

        self.verticalLayout.addWidget(self.bt_delete)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(ColorEditor)

        QMetaObject.connectSlotsByName(ColorEditor)
    # setupUi

    def retranslateUi(self, ColorEditor):
        ColorEditor.setWindowTitle(QCoreApplication.translate("ColorEditor", u"\u989c\u8272\u9009\u62e9", None))
        self.bt_ok.setText(QCoreApplication.translate("ColorEditor", u"OK", None))
        self.bt_cancel.setText(QCoreApplication.translate("ColorEditor", u"Cancel", None))
        self.bt_up.setText(QCoreApplication.translate("ColorEditor", u"Move Up", None))
        self.bt_down.setText(QCoreApplication.translate("ColorEditor", u"Move Down", None))
        self.bt_top.setText(QCoreApplication.translate("ColorEditor", u"Move to Top", None))
        self.bt_bottom.setText(QCoreApplication.translate("ColorEditor", u"Move to Bottom", None))
        self.bt_add.setText(QCoreApplication.translate("ColorEditor", u"Add", None))
        self.bt_delete.setText(QCoreApplication.translate("ColorEditor", u"Delete", None))
    # retranslateUi

