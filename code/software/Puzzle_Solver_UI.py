from PyQt4 import QtCore, QtGui
import numpy as np
import sys
import time
import cv2
import serial

import Functions_1 as F_1
import Functions_2 as F_2
import Functions_3 as F_3



try:
    cap = cv2.VideoCapture(0)
except:
    cap.release()
    cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,960)

try:
    ser = serial.Serial('COM4', 38400, timeout=0)
except:
    ser.close()
    ser = serial.Serial('COM4', 38400, timeout=0)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.img_Camera = []
        self.img_Detection = []
        self.img_Classification = []
        self.img_Solution = []

        self.Pre_Start = True

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1907, 1022)
        Form.setMinimumSize(QtCore.QSize(1775, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../Icons/puzzle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_CAP = QtGui.QVBoxLayout()
        self.verticalLayout_CAP.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_CAP.setSpacing(0)
        self.verticalLayout_CAP.setObjectName(_fromUtf8("verticalLayout_CAP"))
        spacerItem1 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_CAP.addItem(spacerItem1)
        self.pushButton_Camera = QtGui.QPushButton(Form)
        self.pushButton_Camera.setMinimumSize(QtCore.QSize(225, 100))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_Camera.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../Icons/camera.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Camera.setIcon(icon1)
        self.pushButton_Camera.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Camera.setObjectName(_fromUtf8("pushButton_Camera"))
        self.verticalLayout_CAP.addWidget(self.pushButton_Camera)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_CAP.addItem(spacerItem2)
        self.pushButton_Detection = QtGui.QPushButton(Form)
        self.pushButton_Detection.setMinimumSize(QtCore.QSize(225, 100))
        self.pushButton_Detection.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_Detection.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../Icons/piece.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Detection.setIcon(icon2)
        self.pushButton_Detection.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Detection.setObjectName(_fromUtf8("pushButton_Detection"))
        self.verticalLayout_CAP.addWidget(self.pushButton_Detection)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_CAP.addItem(spacerItem3)
        self.pushButton_Classification = QtGui.QPushButton(Form)
        self.pushButton_Classification.setMinimumSize(QtCore.QSize(275, 100))
        self.pushButton_Classification.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_Classification.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../Icons/pencil.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Classification.setIcon(icon3)
        self.pushButton_Classification.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Classification.setObjectName(_fromUtf8("pushButton_Classification"))
        self.verticalLayout_CAP.addWidget(self.pushButton_Classification)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_CAP.addItem(spacerItem4)
        self.pushButton_Solution = QtGui.QPushButton(Form)
        self.pushButton_Solution.setMinimumSize(QtCore.QSize(300, 100))
        self.pushButton_Solution.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_Solution.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../Icons/solution.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Solution.setIcon(icon4)
        self.pushButton_Solution.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Solution.setObjectName(_fromUtf8("pushButton_Solution"))
        self.verticalLayout_CAP.addWidget(self.pushButton_Solution)
        self.horizontalLayout.addLayout(self.verticalLayout_CAP)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_TAB = QtGui.QVBoxLayout()
        self.verticalLayout_TAB.setSpacing(0)
        self.verticalLayout_TAB.setObjectName(_fromUtf8("verticalLayout_TAB"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QtCore.QSize(1280, 980))
        self.tabWidget.setMaximumSize(QtCore.QSize(1280, 1000))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(60, 20))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Tab_Camera = QtGui.QWidget()
        self.Tab_Camera.setObjectName(_fromUtf8("Tab_Camera"))
        self.Lable_Camera = QtGui.QLabel(self.Tab_Camera)
        self.Lable_Camera.setGeometry(QtCore.QRect(0, 0, 1280, 960))
        self.Lable_Camera.setMinimumSize(QtCore.QSize(1280, 960))
        self.Lable_Camera.setMaximumSize(QtCore.QSize(1280, 960))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Lable_Camera.setFont(font)
        self.Lable_Camera.setAlignment(QtCore.Qt.AlignCenter)
        self.Lable_Camera.setObjectName(_fromUtf8("Lable_Camera"))
        self.tabWidget.addTab(self.Tab_Camera, icon1, _fromUtf8(""))
        self.Tab_Detection = QtGui.QWidget()
        self.Tab_Detection.setObjectName(_fromUtf8("Tab_Detection"))
        self.Label_Detection = QtGui.QLabel(self.Tab_Detection)
        self.Label_Detection.setGeometry(QtCore.QRect(0, 0, 1280, 960))
        self.Label_Detection.setMinimumSize(QtCore.QSize(1280, 960))
        self.Label_Detection.setMaximumSize(QtCore.QSize(1280, 960))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Label_Detection.setFont(font)
        self.Label_Detection.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Detection.setObjectName(_fromUtf8("Label_Detection"))
        self.tabWidget.addTab(self.Tab_Detection, icon2, _fromUtf8(""))
        self.Tab_Classification = QtGui.QWidget()
        self.Tab_Classification.setObjectName(_fromUtf8("Tab_Classification"))
        self.Lable_Classification = QtGui.QLabel(self.Tab_Classification)
        self.Lable_Classification.setGeometry(QtCore.QRect(0, 0, 1280, 960))
        self.Lable_Classification.setMinimumSize(QtCore.QSize(0, 0))
        self.Lable_Classification.setMaximumSize(QtCore.QSize(1280, 960))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Lable_Classification.setFont(font)
        self.Lable_Classification.setAlignment(QtCore.Qt.AlignCenter)
        self.Lable_Classification.setObjectName(_fromUtf8("Lable_Classification"))
        self.tabWidget.addTab(self.Tab_Classification, icon3, _fromUtf8(""))
        self.Tab_Solution = QtGui.QWidget()
        self.Tab_Solution.setObjectName(_fromUtf8("Tab_Solution"))
        self.Lable_Solution = QtGui.QLabel(self.Tab_Solution)
        self.Lable_Solution.setGeometry(QtCore.QRect(0, 0, 1280, 960))
        self.Lable_Solution.setMinimumSize(QtCore.QSize(0, 0))
        self.Lable_Solution.setMaximumSize(QtCore.QSize(1280, 960))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Lable_Solution.setFont(font)
        self.Lable_Solution.setFrameShape(QtGui.QFrame.NoFrame)
        self.Lable_Solution.setAlignment(QtCore.Qt.AlignCenter)
        self.Lable_Solution.setObjectName(_fromUtf8("Lable_Solution"))
        self.tabWidget.addTab(self.Tab_Solution, icon4, _fromUtf8(""))
        self.verticalLayout_TAB.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_TAB)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.verticalLayout_LCD = QtGui.QVBoxLayout()
        self.verticalLayout_LCD.setSpacing(0)
        self.verticalLayout_LCD.setObjectName(_fromUtf8("verticalLayout_LCD"))
        spacerItem7 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout_LCD.addItem(spacerItem7)
        self.label_1 = QtGui.QLabel(Form)
        self.label_1.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_1.setWordWrap(True)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayout_LCD.addWidget(self.label_1)
        self.lcdNumber_1 = QtGui.QLCDNumber(Form)
        self.lcdNumber_1.setMinimumSize(QtCore.QSize(0, 100))
        self.lcdNumber_1.setMaximumSize(QtCore.QSize(250, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.lcdNumber_1.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber_1.setFont(font)
        self.lcdNumber_1.setAutoFillBackground(True)
        self.lcdNumber_1.setNumDigits(4)
        self.lcdNumber_1.setProperty("value", 8888.0)
        self.lcdNumber_1.setObjectName(_fromUtf8("lcdNumber_1"))
        self.verticalLayout_LCD.addWidget(self.lcdNumber_1)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_LCD.addItem(spacerItem8)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_LCD.addWidget(self.label_2)
        self.lcdNumber_2 = QtGui.QLCDNumber(Form)
        self.lcdNumber_2.setMinimumSize(QtCore.QSize(225, 100))
        self.lcdNumber_2.setMaximumSize(QtCore.QSize(250, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.lcdNumber_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber_2.setFont(font)
        self.lcdNumber_2.setAutoFillBackground(True)
        self.lcdNumber_2.setNumDigits(3)
        self.lcdNumber_2.setProperty("value", 888.0)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.verticalLayout_LCD.addWidget(self.lcdNumber_2)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_LCD.addItem(spacerItem9)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_LCD.addWidget(self.label_3)
        self.lcdNumber_3 = QtGui.QLCDNumber(Form)
        self.lcdNumber_3.setMinimumSize(QtCore.QSize(0, 100))
        self.lcdNumber_3.setMaximumSize(QtCore.QSize(250, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.lcdNumber_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumber_3.setFont(font)
        self.lcdNumber_3.setAutoFillBackground(True)
        self.lcdNumber_3.setNumDigits(2)
        self.lcdNumber_3.setProperty("value", 88.0)
        self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))
        self.verticalLayout_LCD.addWidget(self.lcdNumber_3)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_LCD.addItem(spacerItem10)
        self.pushButton_Start = QtGui.QPushButton(Form)
        self.pushButton_Start.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_Start.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Start.setFont(font)
        self.pushButton_Start.setIcon(icon)
        self.pushButton_Start.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_Start.setCheckable(False)
        self.pushButton_Start.setChecked(False)
        self.pushButton_Start.setFlat(False)
        self.pushButton_Start.setObjectName(_fromUtf8("pushButton_Start"))
        self.verticalLayout_LCD.addWidget(self.pushButton_Start)
        self.horizontalLayout.addLayout(self.verticalLayout_LCD)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Jigsaw Puzzle Solver", None))
        self.pushButton_Camera.setText(_translate("Form", "  Capture Camera", None))
        self.pushButton_Detection.setText(_translate("Form", "  Capture Detection", None))
        self.pushButton_Classification.setText(_translate("Form", "  Capture Classification", None))
        self.pushButton_Solution.setText(_translate("Form", "  Capture Solution", None))
        self.Lable_Camera.setText(_translate("Form", "Camera Stream Unavailable", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_Camera), _translate("Form", "Camera", None))
        self.Label_Detection.setText(_translate("Form", "Piece Detection Unavailable", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_Detection), _translate("Form", "Detection", None))
        self.Lable_Classification.setText(_translate("Form", "Piece Classification Unavailable", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_Classification), _translate("Form", "Classification", None))
        self.Lable_Solution.setText(_translate("Form", "Puzzle Solution Unavailable", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_Solution), _translate("Form", "Solution", None))
        self.label_1.setText(_translate("Form", "Software Solution Time [ms]:", None))
        self.label_2.setText(_translate("Form", "Hardware Solution Time [s]:", None))
        self.label_3.setText(_translate("Form", "Piece Count:", None))
        self.pushButton_Start.setText(_translate("Form", "  Start", None))

        self.pushButton_Start.clicked.connect(self.Start)

        self.pushButton_Camera.clicked.connect(self.Capture_Camera)
        self.pushButton_Detection.clicked.connect(self.Capture_Detection)
        self.pushButton_Classification.clicked.connect(self.Capture_Classification)
        self.pushButton_Solution.clicked.connect(self.Capture_Solution)

    def Start(self):
        self.Pre_Start = False
        self.pushButton_Start.setEnabled(False)
        app.processEvents()
        BUILD_BOOL = True       # Does the puzle still need to be built

        recalc_PT_bool = True   # Do PT points still need to be minimised

        recalc_PT_num = 10
        recalc_PT_count = 0

        pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]

        CAM_bool = False        # Display camera image
        DP_bool = False         # Detect Pieces
        SP_mec_bool = False     # Buisy with mechanical piece separation
        CP_bool = False         # Clasify pieces
        SOLVE_soft_bool = True  # Buisy with software solution
        R_mec_bool = False      # Buisy with mechanical rotation
        BUILD_mec_bool = False  # Buisy with mechanical solution

        soft_time = 0
        hard_time = 0
        self.lcdNumber_1.display(soft_time)
        self.lcdNumber_2.display(hard_time)
        app.processEvents()

        sol_rect_start = [0,0]
        sol_rect_stop = [0,0]

        DRAW_SB_bool = False

        while BUILD_BOOL:
            soft_time_0 = time.clock()
            hard_time_0 = time.clock()

            ret, frame = cap.read()

            if recalc_PT_bool:
                pts = F_1.Perspective_Transform_Points(frame)
                pts_min = F_1.Minimise_Perspective_Transform_Points(pts_min, pts)
                pts = np.copy(pts_min)
                if recalc_PT_count >= recalc_PT_num:
                    recalc_PT_bool = False
                    CAM_bool = True
                    DP_bool = True
                    CP_bool = True
                else:
                    recalc_PT_count += 1

            if CAM_bool:
                self.img_Camera = F_1.Perspective_Transform(frame, pts)
                if DRAW_SB_bool:
                    for sol_box in xrange(len(sol_rect_start)):
                        if sol_box == 0:
                            color = (200,150,0)
                        else:
                            color = (0,50,200)
                        cv2.rectangle(self.img_Camera,tuple(sol_rect_start[sol_box]), tuple(sol_rect_stop[sol_box]), (0,0,0), 9)
                        cv2.rectangle(self.img_Camera,tuple(sol_rect_start[sol_box]), tuple(sol_rect_stop[sol_box]), color, 3)
                self.Lable_Camera.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Camera))
                app.processEvents()

            if DP_bool:
                img_B = F_1.Clear_Background(self.img_Camera)
                img_BIN = F_1.Binarise(img_B)
                self.img_Detection, piece_cnt, overlap_cnt = F_1.Detect_Pieces(img_BIN, self.img_Camera)
                self.Label_Detection.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Detection))
                app.processEvents()


                self.lcdNumber_3.display(np.shape(piece_cnt)[0])
                app.processEvents()

                if np.shape(overlap_cnt)[0] != 0:
                    img_SO, From, To, Dir = F_1.Separate_Overlap(img_BIN, self.img_Detection, overlap_cnt)
                    self.img_Detection = img_SO
                    self.Label_Detection.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Detection))
                    app.processEvents()

                    Command = F_3.Generate_Separation_Commands(From, To, Dir)
                    ser.write(Command[0])
                    Command_Count = 1

                    DP_bool = False
                    SP_mec_bool = True
                    CP_bool = False

                elif CP_bool and np.shape(overlap_cnt)[0] == 0 and np.shape(piece_cnt)[0] == 12:
                    classify_successful, Piece = F_1.Classify_Pieces(img_B, piece_cnt)
                    if classify_successful:
                        self.img_Classification = F_2.Draw_Classification(Piece)
                        self.Lable_Classification.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Classification))
                        app.processEvents()

                        CP_bool = False
                        if SOLVE_soft_bool:
                            solution_successful, Solution_Piece, self.img_Solution = F_2.Solve_Puzzle(Piece)
                            if solution_successful:
                                self.Lable_Solution.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Solution))
                                app.processEvents()

                                Command = F_3.Generate_Rotation_Commands(Solution_Piece)
                                if len(Command) > 0:
                                    ser.write(Command[0])
                                    Command_Count = 1

                                    DP_bool = False
                                    CP_bool = False
                                    SOLVE_soft_bool = False
                                    R_mec_bool = True
                                else:
                                    Command, sol_rect_start, sol_rect_stop = F_3.Generate_Movement_Commands(Solution_Piece)
                                    ser.write(Command[0])
                                    Command_Count = 1

                                    DP_bool = False
                                    CP_bool = False
                                    SOLVE_soft_bool = False
                                    BUILD_mec_bool = True
                                    DRAW_SB_bool = True


                            else:
                                CP_bool = True

            if SOLVE_soft_bool and not SP_mec_bool:
                soft_time += time.clock() - soft_time_0

            if SP_mec_bool:
                hard_time += time.clock() - hard_time_0
                Byte = ser.read()
                if "D" in Byte:
                    if Command_Count == Command.shape[0]:
                        DP_bool = True
                        CP_bool = True
                        SP_mec_bool = False
                    else:
                        ser.write(Command[Command_Count])
                        Command_Count += 1


            if R_mec_bool:
                hard_time += time.clock() - hard_time_0
                Byte = ser.read()
                if "D" in Byte:
                    if Command_Count == Command.shape[0]:
                        Solution_Piece, self.img_Detection, Re_Rotate_bool = F_3.Recalculate_Piece_Centers(Solution_Piece, self.img_Camera)
                        self.Label_Detection.setPixmap(self.Convert_OpenCV2_To_QPixmap(self.img_Detection))
                        app.processEvents()

                        if Re_Rotate_bool:
                            Command = F_3.Generate_Rotation_Commands(Solution_Piece)
                            ser.write(Command[0])
                            Command_Count = 1

                            R_mec_bool = True
                        else:
                            R_mec_bool = False
                            BUILD_mec_bool = True

                            Command, sol_rect_start, sol_rect_stop = F_3.Generate_Movement_Commands(Solution_Piece)
                            ser.write(Command[0])
                            Command_Count = 1

                            DRAW_SB_bool = True

                        soft_time += time.clock() - soft_time_0
                    else:
                        ser.write(Command[Command_Count])
                        Command_Count += 1


            if BUILD_mec_bool:
                hard_time += time.clock() - hard_time_0
                Byte = ser.read()
                if "D" in Byte:
                    if Command_Count == Command.shape[0]:
                        self.pushButton_Start.setEnabled(True)
                        app.processEvents()
                        BUILD_BOOL = False
                    else:
                        ser.write(Command[Command_Count])
                        Command_Count += 1


            self.lcdNumber_1.display(int(soft_time*1000))
            self.lcdNumber_2.display(int(hard_time))
            app.processEvents()


    def Convert_OpenCV2_To_QPixmap(self, cv_img):
        height, width, bytesPerComponent = cv_img.shape
        bytesPerLine = bytesPerComponent * width;
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        QImage = QtGui.QImage(cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(QImage)


    def Capture_Camera(self):
        if self.img_Camera != []:
            cv2.imwrite("images\\Camera.png", self.img_Camera)

    def Capture_Detection(self):
        if self.img_Detection != []:
            cv2.imwrite("images\\Detection.png", self.img_Detection)

    def Capture_Classification(self):
        if self.img_Classification != []:
            cv2.imwrite("images\\Classification.png", self.img_Classification)

    def Capture_Solution(self):
        if self.img_Solution != []:
            cv2.imwrite("images\\Solution.png", self.img_Solution)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.showMaximized()

    pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]
    pts_calc_num = 0

    while ex.Pre_Start:
        ret, frame = cap.read()
        if ret:
            if pts_calc_num  <= 10:
                pts = F_1.Perspective_Transform_Points(frame)
                pts_min = F_1.Minimise_Perspective_Transform_Points(pts_min, pts)
                pts = np.copy(pts_min)
                pts_calc_num += 1
            ex.img_Camera = F_1.Draw_Perspective_Transform_Points(frame, pts)
            ex.Lable_Camera.setPixmap(ex.Convert_OpenCV2_To_QPixmap(ex.img_Camera))
            app.processEvents()

    status = app.exec_()
    ser.close()
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(status)

