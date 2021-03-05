# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(480, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setLayoutDirection(Qt.LeftToRight)
        dialog.setAutoFillBackground(False)
        self.verticalLayout_2 = QVBoxLayout(dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(dialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 180))
        self.groupBox.setMaximumSize(QSize(16777215, 280))
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(0, 32))
        self.label_4.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout.addWidget(self.label_4)

        self.sb_median_blur = QSpinBox(self.groupBox)
        self.sb_median_blur.setObjectName(u"sb_median_blur")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sb_median_blur.sizePolicy().hasHeightForWidth())
        self.sb_median_blur.setSizePolicy(sizePolicy2)
        self.sb_median_blur.setMinimumSize(QSize(60, 0))
        self.sb_median_blur.setMaximumSize(QSize(80, 16777215))
        self.sb_median_blur.setMinimum(1)
        self.sb_median_blur.setSingleStep(2)

        self.horizontalLayout.addWidget(self.sb_median_blur)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(0, 32))
        self.label_3.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout.addWidget(self.label_3)

        self.sb_opening_size = QSpinBox(self.groupBox)
        self.sb_opening_size.setObjectName(u"sb_opening_size")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sb_opening_size.sizePolicy().hasHeightForWidth())
        self.sb_opening_size.setSizePolicy(sizePolicy3)
        self.sb_opening_size.setMinimumSize(QSize(60, 32))
        self.sb_opening_size.setMaximumSize(QSize(80, 40))
        self.sb_opening_size.setMinimum(1)

        self.horizontalLayout.addWidget(self.sb_opening_size)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(0, 32))
        self.label_5.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.label_5)

        self.sb_gaussian_blur = QSpinBox(self.groupBox)
        self.sb_gaussian_blur.setObjectName(u"sb_gaussian_blur")
        sizePolicy2.setHeightForWidth(self.sb_gaussian_blur.sizePolicy().hasHeightForWidth())
        self.sb_gaussian_blur.setSizePolicy(sizePolicy2)
        self.sb_gaussian_blur.setMinimumSize(QSize(60, 32))
        self.sb_gaussian_blur.setMaximumSize(QSize(80, 40))
        self.sb_gaussian_blur.setMinimum(1)
        self.sb_gaussian_blur.setSingleStep(2)

        self.horizontalLayout_2.addWidget(self.sb_gaussian_blur)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 32))
        self.label.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.label)

        self.sb_closing_size = QSpinBox(self.groupBox)
        self.sb_closing_size.setObjectName(u"sb_closing_size")
        sizePolicy2.setHeightForWidth(self.sb_closing_size.sizePolicy().hasHeightForWidth())
        self.sb_closing_size.setSizePolicy(sizePolicy2)
        self.sb_closing_size.setMinimumSize(QSize(60, 32))
        self.sb_closing_size.setMaximumSize(QSize(80, 40))
        self.sb_closing_size.setMinimum(1)

        self.horizontalLayout_2.addWidget(self.sb_closing_size)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ckb_apply_hist_eq = QCheckBox(self.groupBox)
        self.ckb_apply_hist_eq.setObjectName(u"ckb_apply_hist_eq")
        sizePolicy2.setHeightForWidth(self.ckb_apply_hist_eq.sizePolicy().hasHeightForWidth())
        self.ckb_apply_hist_eq.setSizePolicy(sizePolicy2)
        self.ckb_apply_hist_eq.setMinimumSize(QSize(0, 32))
        self.ckb_apply_hist_eq.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_3.addWidget(self.ckb_apply_hist_eq)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setMinimumSize(QSize(0, 32))
        self.label_6.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_3.addWidget(self.label_6)

        self.sb_adaptive_hist_eq = QSpinBox(self.groupBox)
        self.sb_adaptive_hist_eq.setObjectName(u"sb_adaptive_hist_eq")
        sizePolicy2.setHeightForWidth(self.sb_adaptive_hist_eq.sizePolicy().hasHeightForWidth())
        self.sb_adaptive_hist_eq.setSizePolicy(sizePolicy2)
        self.sb_adaptive_hist_eq.setMinimumSize(QSize(60, 32))
        self.sb_adaptive_hist_eq.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_3.addWidget(self.sb_adaptive_hist_eq)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(0, 32))
        self.label_7.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_4.addWidget(self.label_7)

        self.sb_bilateral_size = QSpinBox(self.groupBox)
        self.sb_bilateral_size.setObjectName(u"sb_bilateral_size")
        sizePolicy2.setHeightForWidth(self.sb_bilateral_size.sizePolicy().hasHeightForWidth())
        self.sb_bilateral_size.setSizePolicy(sizePolicy2)
        self.sb_bilateral_size.setMinimumSize(QSize(60, 32))
        self.sb_bilateral_size.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_4.addWidget(self.sb_bilateral_size)

        self.sb_bilateral_color = QSpinBox(self.groupBox)
        self.sb_bilateral_color.setObjectName(u"sb_bilateral_color")
        sizePolicy2.setHeightForWidth(self.sb_bilateral_color.sizePolicy().hasHeightForWidth())
        self.sb_bilateral_color.setSizePolicy(sizePolicy2)
        self.sb_bilateral_color.setMinimumSize(QSize(60, 32))
        self.sb_bilateral_color.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_4.addWidget(self.sb_bilateral_color)

        self.sb_bilateral_space = QSpinBox(self.groupBox)
        self.sb_bilateral_space.setObjectName(u"sb_bilateral_space")
        sizePolicy2.setHeightForWidth(self.sb_bilateral_space.sizePolicy().hasHeightForWidth())
        self.sb_bilateral_space.setSizePolicy(sizePolicy2)
        self.sb_bilateral_space.setMinimumSize(QSize(60, 32))
        self.sb_bilateral_space.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_4.addWidget(self.sb_bilateral_space)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.groupBox_2.setMinimumSize(QSize(0, 80))
        self.groupBox_2.setMaximumSize(QSize(16777215, 240))
        self.groupBox_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.sb_search_radius = QSpinBox(self.groupBox_2)
        self.sb_search_radius.setObjectName(u"sb_search_radius")
        self.sb_search_radius.setMinimumSize(QSize(60, 32))
        self.sb_search_radius.setMaximumSize(QSize(80, 40))
        self.sb_search_radius.setMinimum(1)
        self.sb_search_radius.setSingleStep(2)

        self.horizontalLayout_5.addWidget(self.sb_search_radius)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.sb_minimum_area_for_detection = QSpinBox(self.groupBox_2)
        self.sb_minimum_area_for_detection.setObjectName(u"sb_minimum_area_for_detection")
        self.sb_minimum_area_for_detection.setMinimumSize(QSize(60, 32))
        self.sb_minimum_area_for_detection.setMaximumSize(QSize(80, 40))
        self.sb_minimum_area_for_detection.setMaximum(10000000)

        self.horizontalLayout_5.addWidget(self.sb_minimum_area_for_detection)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.sb_memory_frames = QSpinBox(self.groupBox_2)
        self.sb_memory_frames.setObjectName(u"sb_memory_frames")
        self.sb_memory_frames.setMinimumSize(QSize(60, 32))
        self.sb_memory_frames.setMaximumSize(QSize(80, 40))
        self.sb_memory_frames.setMinimum(1)
        self.sb_memory_frames.setSingleStep(2)

        self.horizontalLayout_6.addWidget(self.sb_memory_frames)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.sb_maximum_area_for_detection = QSpinBox(self.groupBox_2)
        self.sb_maximum_area_for_detection.setObjectName(u"sb_maximum_area_for_detection")
        self.sb_maximum_area_for_detection.setMinimumSize(QSize(60, 32))
        self.sb_maximum_area_for_detection.setMaximumSize(QSize(80, 40))
        self.sb_maximum_area_for_detection.setMaximum(10000000)

        self.horizontalLayout_6.addWidget(self.sb_maximum_area_for_detection)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setMinimumSize(QSize(0, 60))
        self.groupBox_3.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_7.addWidget(self.label_11)

        self.sb_threshold = QSpinBox(self.groupBox_3)
        self.sb_threshold.setObjectName(u"sb_threshold")
        sizePolicy2.setHeightForWidth(self.sb_threshold.sizePolicy().hasHeightForWidth())
        self.sb_threshold.setSizePolicy(sizePolicy2)
        self.sb_threshold.setMinimumSize(QSize(0, 32))
        self.sb_threshold.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_7.addWidget(self.sb_threshold)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_7.addWidget(self.label_12)

        self.sb_derivative_order = QSpinBox(self.groupBox_3)
        self.sb_derivative_order.setObjectName(u"sb_derivative_order")
        sizePolicy2.setHeightForWidth(self.sb_derivative_order.sizePolicy().hasHeightForWidth())
        self.sb_derivative_order.setSizePolicy(sizePolicy2)
        self.sb_derivative_order.setMinimumSize(QSize(0, 32))
        self.sb_derivative_order.setMaximumSize(QSize(16777215, 40))
        self.sb_derivative_order.setMinimum(1)

        self.horizontalLayout_7.addWidget(self.sb_derivative_order)

        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_7.addWidget(self.label_13)

        self.sb_kernel_size = QSpinBox(self.groupBox_3)
        self.sb_kernel_size.setObjectName(u"sb_kernel_size")
        sizePolicy2.setHeightForWidth(self.sb_kernel_size.sizePolicy().hasHeightForWidth())
        self.sb_kernel_size.setSizePolicy(sizePolicy2)
        self.sb_kernel_size.setMinimumSize(QSize(0, 32))
        self.sb_kernel_size.setMaximumSize(QSize(16777215, 40))
        self.sb_kernel_size.setMinimum(-1)
        self.sb_kernel_size.setMaximum(7)
        self.sb_kernel_size.setSingleStep(2)
        self.sb_kernel_size.setValue(1)

        self.horizontalLayout_7.addWidget(self.sb_kernel_size)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.groupBox_4.setMinimumSize(QSize(0, 60))
        self.groupBox_4.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ckb_split_circular_particles = QCheckBox(self.groupBox_4)
        self.ckb_split_circular_particles.setObjectName(u"ckb_split_circular_particles")
        sizePolicy2.setHeightForWidth(self.ckb_split_circular_particles.sizePolicy().hasHeightForWidth())
        self.ckb_split_circular_particles.setSizePolicy(sizePolicy2)
        self.ckb_split_circular_particles.setMinimumSize(QSize(0, 32))
        self.ckb_split_circular_particles.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_8.addWidget(self.ckb_split_circular_particles)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_8.addWidget(self.label_14)

        self.sb_split_radius = QSpinBox(self.groupBox_4)
        self.sb_split_radius.setObjectName(u"sb_split_radius")
        sizePolicy2.setHeightForWidth(self.sb_split_radius.sizePolicy().hasHeightForWidth())
        self.sb_split_radius.setSizePolicy(sizePolicy2)
        self.sb_split_radius.setMinimumSize(QSize(0, 32))
        self.sb_split_radius.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_8.addWidget(self.sb_split_radius)


        self.verticalLayout_8.addLayout(self.horizontalLayout_8)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(dialog)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 60))
        self.groupBox_5.setMaximumSize(QSize(16777215, 240))
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.chk_fit_to_screen = QCheckBox(self.groupBox_5)
        self.chk_fit_to_screen.setObjectName(u"chk_fit_to_screen")
        self.chk_fit_to_screen.setMinimumSize(QSize(0, 32))
        self.chk_fit_to_screen.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_9.addWidget(self.chk_fit_to_screen)

        self.chk_show_binary_image = QCheckBox(self.groupBox_5)
        self.chk_show_binary_image.setObjectName(u"chk_show_binary_image")
        self.chk_show_binary_image.setMinimumSize(QSize(0, 32))
        self.chk_show_binary_image.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_9.addWidget(self.chk_show_binary_image)

        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 32))
        self.label_15.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_9.addWidget(self.label_15)

        self.sb_skip_frames = QSpinBox(self.groupBox_5)
        self.sb_skip_frames.setObjectName(u"sb_skip_frames")
        self.sb_skip_frames.setMinimumSize(QSize(0, 32))
        self.sb_skip_frames.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_9.addWidget(self.sb_skip_frames)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 32))
        self.label_16.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_10.addWidget(self.label_16)

        self.sb_from_frame = QSpinBox(self.groupBox_5)
        self.sb_from_frame.setObjectName(u"sb_from_frame")
        self.sb_from_frame.setMinimumSize(QSize(0, 32))
        self.sb_from_frame.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_10.addWidget(self.sb_from_frame)

        self.label_17 = QLabel(self.groupBox_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 32))
        self.label_17.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_10.addWidget(self.label_17)

        self.sb_to_frame = QSpinBox(self.groupBox_5)
        self.sb_to_frame.setObjectName(u"sb_to_frame")
        self.sb_to_frame.setMinimumSize(QSize(0, 32))
        self.sb_to_frame.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_10.addWidget(self.sb_to_frame)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)


        self.verticalLayout_9.addLayout(self.verticalLayout_5)


        self.verticalLayout_2.addWidget(self.groupBox_5)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.bt_ok = QPushButton(dialog)
        self.bt_ok.setObjectName(u"bt_ok")
        sizePolicy1.setHeightForWidth(self.bt_ok.sizePolicy().hasHeightForWidth())
        self.bt_ok.setSizePolicy(sizePolicy1)
        self.bt_ok.setMinimumSize(QSize(80, 32))
        self.bt_ok.setMaximumSize(QSize(160, 64))

        self.horizontalLayout_11.addWidget(self.bt_ok)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)


        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("dialog", u"Image Treatment Options", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"Median Blur", None))
#if QT_CONFIG(whatsthis)
        self.sb_median_blur.setWhatsThis(QCoreApplication.translate("dialog", u"median_blur", None))
#endif // QT_CONFIG(whatsthis)
        self.label_3.setText(QCoreApplication.translate("dialog", u"Opening Size", None))
#if QT_CONFIG(whatsthis)
        self.sb_opening_size.setWhatsThis(QCoreApplication.translate("dialog", u"opening_size", None))
#endif // QT_CONFIG(whatsthis)
        self.label_5.setText(QCoreApplication.translate("dialog", u"Gaussian Blur", None))
#if QT_CONFIG(whatsthis)
        self.sb_gaussian_blur.setWhatsThis(QCoreApplication.translate("dialog", u"gaussian_blur", None))
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("dialog", u"Closing Size", None))
#if QT_CONFIG(whatsthis)
        self.sb_closing_size.setWhatsThis(QCoreApplication.translate("dialog", u"closing_size", None))
#endif // QT_CONFIG(whatsthis)
        self.sb_closing_size.setSpecialValueText("")
        self.sb_closing_size.setSuffix("")
#if QT_CONFIG(whatsthis)
        self.ckb_apply_hist_eq.setWhatsThis(QCoreApplication.translate("dialog", u"apply_hist_eq", None))
#endif // QT_CONFIG(whatsthis)
        self.ckb_apply_hist_eq.setText(QCoreApplication.translate("dialog", u"Apply Hist. Eq.", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"Apply adaptive Hist. Eq.", None))
#if QT_CONFIG(whatsthis)
        self.sb_adaptive_hist_eq.setWhatsThis(QCoreApplication.translate("dialog", u"adaptive_hist_eq", None))
#endif // QT_CONFIG(whatsthis)
        self.label_7.setText(QCoreApplication.translate("dialog", u"Bilateral Filter(Size/Color/Space)", None))
#if QT_CONFIG(whatsthis)
        self.sb_bilateral_size.setWhatsThis(QCoreApplication.translate("dialog", u"bilateral_size", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.sb_bilateral_color.setWhatsThis(QCoreApplication.translate("dialog", u"bilateral_color", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.sb_bilateral_space.setWhatsThis(QCoreApplication.translate("dialog", u"bilateral_space", None))
#endif // QT_CONFIG(whatsthis)
        self.groupBox_2.setTitle(QCoreApplication.translate("dialog", u"Detection and Tracking Options", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Search Radius", None))
#if QT_CONFIG(whatsthis)
        self.sb_search_radius.setWhatsThis(QCoreApplication.translate("dialog", u"search_radius", None))
#endif // QT_CONFIG(whatsthis)
        self.label_9.setText(QCoreApplication.translate("dialog", u"Minimum Area for Detection", None))
#if QT_CONFIG(whatsthis)
        self.sb_minimum_area_for_detection.setWhatsThis(QCoreApplication.translate("dialog", u"minimum_area_for_detection", None))
#endif // QT_CONFIG(whatsthis)
        self.label_8.setText(QCoreApplication.translate("dialog", u"Memory Frames", None))
#if QT_CONFIG(whatsthis)
        self.sb_memory_frames.setWhatsThis(QCoreApplication.translate("dialog", u"memory_frames", None))
#endif // QT_CONFIG(whatsthis)
        self.label_10.setText(QCoreApplication.translate("dialog", u"Maximum Area for Detection", None))
#if QT_CONFIG(whatsthis)
        self.sb_maximum_area_for_detection.setWhatsThis(QCoreApplication.translate("dialog", u"maximum_area_for_detection", None))
#endif // QT_CONFIG(whatsthis)
        self.groupBox_3.setTitle(QCoreApplication.translate("dialog", u"Gradient Options", None))
        self.label_11.setText(QCoreApplication.translate("dialog", u"Threshold", None))
#if QT_CONFIG(whatsthis)
        self.sb_threshold.setWhatsThis(QCoreApplication.translate("dialog", u"threshold", None))
#endif // QT_CONFIG(whatsthis)
        self.label_12.setText(QCoreApplication.translate("dialog", u"Derivative Order", None))
#if QT_CONFIG(whatsthis)
        self.sb_derivative_order.setWhatsThis(QCoreApplication.translate("dialog", u"derivative_order", None))
#endif // QT_CONFIG(whatsthis)
        self.label_13.setText(QCoreApplication.translate("dialog", u"Kernel Size", None))
#if QT_CONFIG(whatsthis)
        self.sb_kernel_size.setWhatsThis(QCoreApplication.translate("dialog", u"kernel_size", None))
#endif // QT_CONFIG(whatsthis)
        self.groupBox_4.setTitle(QCoreApplication.translate("dialog", u"Extra Options", None))
#if QT_CONFIG(whatsthis)
        self.ckb_split_circular_particles.setWhatsThis(QCoreApplication.translate("dialog", u"split_circular_particles", None))
#endif // QT_CONFIG(whatsthis)
        self.ckb_split_circular_particles.setText(QCoreApplication.translate("dialog", u"Split Circular Touching Particles", None))
        self.label_14.setText(QCoreApplication.translate("dialog", u"Particle Radius for Spliting", None))
#if QT_CONFIG(whatsthis)
        self.sb_split_radius.setWhatsThis(QCoreApplication.translate("dialog", u"split_radius", None))
#endif // QT_CONFIG(whatsthis)
        self.groupBox_5.setTitle(QCoreApplication.translate("dialog", u"Video Options", None))
#if QT_CONFIG(whatsthis)
        self.chk_fit_to_screen.setWhatsThis(QCoreApplication.translate("dialog", u"fit_to_screen", None))
#endif // QT_CONFIG(whatsthis)
        self.chk_fit_to_screen.setText(QCoreApplication.translate("dialog", u"Fit to Screen", None))
#if QT_CONFIG(whatsthis)
        self.chk_show_binary_image.setWhatsThis(QCoreApplication.translate("dialog", u"show_binary_image", None))
#endif // QT_CONFIG(whatsthis)
        self.chk_show_binary_image.setText(QCoreApplication.translate("dialog", u"Show Binary Image", None))
        self.label_15.setText(QCoreApplication.translate("dialog", u"Skip Frames", None))
#if QT_CONFIG(whatsthis)
        self.sb_skip_frames.setWhatsThis(QCoreApplication.translate("dialog", u"skip_frames", None))
#endif // QT_CONFIG(whatsthis)
        self.label_16.setText(QCoreApplication.translate("dialog", u"From Frame", None))
#if QT_CONFIG(whatsthis)
        self.sb_from_frame.setWhatsThis(QCoreApplication.translate("dialog", u"from_frame", None))
#endif // QT_CONFIG(whatsthis)
        self.label_17.setText(QCoreApplication.translate("dialog", u"To Frame", None))
#if QT_CONFIG(whatsthis)
        self.sb_to_frame.setWhatsThis(QCoreApplication.translate("dialog", u"to_frame", None))
#endif // QT_CONFIG(whatsthis)
        self.bt_ok.setText(QCoreApplication.translate("dialog", u"OK", None))
    # retranslateUi

