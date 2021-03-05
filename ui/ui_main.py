# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(927, 655)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bt_choose_file = QPushButton(self.widget)
        self.bt_choose_file.setObjectName(u"bt_choose_file")
        self.bt_choose_file.setMinimumSize(QSize(80, 32))

        self.horizontalLayout_2.addWidget(self.bt_choose_file)

        self.bt_load = QPushButton(self.widget)
        self.bt_load.setObjectName(u"bt_load")
        self.bt_load.setMinimumSize(QSize(80, 32))

        self.horizontalLayout_2.addWidget(self.bt_load)

        self.bt_analyze = QPushButton(self.widget)
        self.bt_analyze.setObjectName(u"bt_analyze")
        self.bt_analyze.setMinimumSize(QSize(80, 32))
        self.bt_analyze.setMaximumSize(QSize(160, 64))
        self.bt_analyze.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.bt_analyze)

        self.bt_track = QPushButton(self.widget)
        self.bt_track.setObjectName(u"bt_track")
        self.bt_track.setMinimumSize(QSize(80, 32))

        self.horizontalLayout_2.addWidget(self.bt_track)

        self.bt_export = QPushButton(self.widget)
        self.bt_export.setObjectName(u"bt_export")
        self.bt_export.setMinimumSize(QSize(80, 32))

        self.horizontalLayout_2.addWidget(self.bt_export)

        self.bt_settings = QPushButton(self.widget)
        self.bt_settings.setObjectName(u"bt_settings")
        self.bt_settings.setMinimumSize(QSize(80, 32))
        self.bt_settings.setMaximumSize(QSize(160, 64))

        self.horizontalLayout_2.addWidget(self.bt_settings)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lb_file_path = QLabel(self.widget)
        self.lb_file_path.setObjectName(u"lb_file_path")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_file_path.sizePolicy().hasHeightForWidth())
        self.lb_file_path.setSizePolicy(sizePolicy)
        self.lb_file_path.setScaledContents(False)
        self.lb_file_path.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.lb_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.graphicsView = QGraphicsView(self.widget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_7.addWidget(self.graphicsView)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.bt_select = QPushButton(self.widget)
        self.bt_select.setObjectName(u"bt_select")
        icon = QIcon()
        icon.addFile(u"C:/Users/zhanchen/.designer/images/cursor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_select.setIcon(icon)
        self.bt_select.setCheckable(True)
        self.bt_select.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.bt_select)

        self.bt_crop = QPushButton(self.widget)
        self.bt_crop.setObjectName(u"bt_crop")
        icon1 = QIcon()
        icon1.addFile(u"C:/Users/zhanchen/.designer/images/crop.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_crop.setIcon(icon1)
        self.bt_crop.setCheckable(True)
        self.bt_crop.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.bt_crop)

        self.bt_move = QPushButton(self.widget)
        self.bt_move.setObjectName(u"bt_move")
        icon2 = QIcon()
        icon2.addFile(u"C:/Users/zhanchen/.designer/images/move.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_move.setIcon(icon2)
        self.bt_move.setCheckable(True)
        self.bt_move.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.bt_move)

        self.bt_add = QPushButton(self.widget)
        self.bt_add.setObjectName(u"bt_add")
        icon3 = QIcon()
        icon3.addFile(u"C:/Users/zhanchen/.designer/images/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_add.setIcon(icon3)
        self.bt_add.setCheckable(True)
        self.bt_add.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.bt_add)

        self.bt_combine = QPushButton(self.widget)
        self.bt_combine.setObjectName(u"bt_combine")
        icon4 = QIcon()
        icon4.addFile(u"C:/Users/zhanchen/.designer/images/combine.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_combine.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.bt_combine)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.sb_frames = QSpinBox(self.widget)
        self.sb_frames.setObjectName(u"sb_frames")
        self.sb_frames.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.sb_frames.setMinimum(0)
        self.sb_frames.setMaximum(999999999)

        self.horizontalLayout_6.addWidget(self.sb_frames)

        self.le_particle_filter = QLineEdit(self.widget)
        self.le_particle_filter.setObjectName(u"le_particle_filter")

        self.horizontalLayout_6.addWidget(self.le_particle_filter)

        self.cb_show_particles = QCheckBox(self.widget)
        self.cb_show_particles.setObjectName(u"cb_show_particles")
        self.cb_show_particles.setChecked(True)

        self.horizontalLayout_6.addWidget(self.cb_show_particles)

        self.cb_show_marks = QCheckBox(self.widget)
        self.cb_show_marks.setObjectName(u"cb_show_marks")
        self.cb_show_marks.setChecked(True)

        self.horizontalLayout_6.addWidget(self.cb_show_marks)

        self.cb_show_frames = QCheckBox(self.widget)
        self.cb_show_frames.setObjectName(u"cb_show_frames")
        self.cb_show_frames.setChecked(True)

        self.horizontalLayout_6.addWidget(self.cb_show_frames)

        self.bt_particle_color = QPushButton(self.widget)
        self.bt_particle_color.setObjectName(u"bt_particle_color")
        self.bt_particle_color.setCheckable(False)
        self.bt_particle_color.setAutoRepeat(False)
        self.bt_particle_color.setAutoExclusive(False)
        self.bt_particle_color.setAutoDefault(False)
        self.bt_particle_color.setFlat(False)

        self.horizontalLayout_6.addWidget(self.bt_particle_color)

        self.bt_mark_color = QPushButton(self.widget)
        self.bt_mark_color.setObjectName(u"bt_mark_color")

        self.horizontalLayout_6.addWidget(self.bt_mark_color)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.cb_show_traj = QCheckBox(self.widget)
        self.cb_show_traj.setObjectName(u"cb_show_traj")

        self.horizontalLayout_8.addWidget(self.cb_show_traj)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.dsb_traj_size = QDoubleSpinBox(self.widget)
        self.dsb_traj_size.setObjectName(u"dsb_traj_size")

        self.horizontalLayout_8.addWidget(self.dsb_traj_size)

        self.lb_traj_color = QLabel(self.widget)
        self.lb_traj_color.setObjectName(u"lb_traj_color")

        self.horizontalLayout_8.addWidget(self.lb_traj_color)

        self.bt_edit_traj_color = QPushButton(self.widget)
        self.bt_edit_traj_color.setObjectName(u"bt_edit_traj_color")

        self.horizontalLayout_8.addWidget(self.bt_edit_traj_color)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.cb_speed_traj = QCheckBox(self.widget)
        self.cb_speed_traj.setObjectName(u"cb_speed_traj")

        self.horizontalLayout_9.addWidget(self.cb_speed_traj)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_9.addWidget(self.label_4)

        self.dsb_speed_traj_lower_limit = QDoubleSpinBox(self.widget)
        self.dsb_speed_traj_lower_limit.setObjectName(u"dsb_speed_traj_lower_limit")

        self.horizontalLayout_9.addWidget(self.dsb_speed_traj_lower_limit)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_9.addWidget(self.label_5)

        self.dsb_speed_traj_upper_limit = QDoubleSpinBox(self.widget)
        self.dsb_speed_traj_upper_limit.setObjectName(u"dsb_speed_traj_upper_limit")

        self.horizontalLayout_9.addWidget(self.dsb_speed_traj_upper_limit)

        self.lb_speed_traj_color = QLabel(self.widget)
        self.lb_speed_traj_color.setObjectName(u"lb_speed_traj_color")

        self.horizontalLayout_9.addWidget(self.lb_speed_traj_color)

        self.bt_edit_speed_tra_color = QPushButton(self.widget)
        self.bt_edit_speed_tra_color.setObjectName(u"bt_edit_speed_tra_color")

        self.horizontalLayout_9.addWidget(self.bt_edit_speed_tra_color)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.verticalLayout_4.setStretch(0, 10)

        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.horizontalLayout_5.setStretch(0, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 927, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.bt_particle_color.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QTracker", None))
        self.bt_choose_file.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6", None))
        self.bt_load.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u89c6\u9891", None))
        self.bt_analyze.setText(QCoreApplication.translate("MainWindow", u"\u7c92\u5b50\u68c0\u6d4b", None))
        self.bt_track.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u8ff9\u8ddf\u8e2a", None))
        self.bt_export.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u89c6\u9891", None))
        self.bt_settings.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lb_file_path.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.bt_select.setToolTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9", None))
#endif // QT_CONFIG(tooltip)
        self.bt_select.setText("")
#if QT_CONFIG(tooltip)
        self.bt_crop.setToolTip(QCoreApplication.translate("MainWindow", u"\u622a\u53d6", None))
#endif // QT_CONFIG(tooltip)
        self.bt_crop.setText("")
#if QT_CONFIG(tooltip)
        self.bt_move.setToolTip(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8", None))
#endif // QT_CONFIG(tooltip)
        self.bt_move.setText("")
#if QT_CONFIG(tooltip)
        self.bt_add.setToolTip(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
#endif // QT_CONFIG(tooltip)
        self.bt_add.setText("")
#if QT_CONFIG(tooltip)
        self.bt_combine.setToolTip(QCoreApplication.translate("MainWindow", u"\u5408\u5e76", None))
#endif // QT_CONFIG(tooltip)
        self.bt_combine.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Frames:", None))
#if QT_CONFIG(whatsthis)
        self.cb_show_particles.setWhatsThis(QCoreApplication.translate("MainWindow", u"vid_show_particles", None))
#endif // QT_CONFIG(whatsthis)
        self.cb_show_particles.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u7c92\u5b50", None))
#if QT_CONFIG(whatsthis)
        self.cb_show_marks.setWhatsThis(QCoreApplication.translate("MainWindow", u"vid_show_marks", None))
#endif // QT_CONFIG(whatsthis)
        self.cb_show_marks.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6807\u8bb0", None))
#if QT_CONFIG(whatsthis)
        self.cb_show_frames.setWhatsThis(QCoreApplication.translate("MainWindow", u"vid_show_frames", None))
#endif // QT_CONFIG(whatsthis)
        self.cb_show_frames.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5e27", None))
        self.bt_particle_color.setText(QCoreApplication.translate("MainWindow", u"\u7c92\u5b50\u989c\u8272", None))
        self.bt_mark_color.setText(QCoreApplication.translate("MainWindow", u"\u6807\u8bb0\u989c\u8272", None))
        self.cb_show_traj.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u8f68\u8ff9", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u8ff9\u7c97\u7ec6", None))
        self.lb_traj_color.setText(QCoreApplication.translate("MainWindow", u"[\u8f68\u8ff9\u989c\u8272]", None))
        self.bt_edit_traj_color.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u989c\u8272", None))
        self.cb_speed_traj.setText(QCoreApplication.translate("MainWindow", u"\u8f68\u8ff9\u989c\u8272\u968f\u901f\u5ea6\u53d8\u5316", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6\u4e0b\u754c\u767e\u5206\u6bd4", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u901f\u5ea6\u4e0a\u754c\u767e\u5206\u6bd4", None))
        self.lb_speed_traj_color.setText(QCoreApplication.translate("MainWindow", u"[\u8f68\u8ff9\u989c\u8272]", None))
        self.bt_edit_speed_tra_color.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u989c\u8272", None))
    # retranslateUi

