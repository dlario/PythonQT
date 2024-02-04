# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PackageBuilder.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFormLayout, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QPlainTextEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTabWidget, QTableView, QTextEdit,
    QTreeView, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1086, 826)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtPackageFolderLocation = QLineEdit(Form)
        self.txtPackageFolderLocation.setObjectName(u"txtPackageFolderLocation")

        self.horizontalLayout_2.addWidget(self.txtPackageFolderLocation)

        self.cmdOpenPackageFolder = QPushButton(Form)
        self.cmdOpenPackageFolder.setObjectName(u"cmdOpenPackageFolder")
        self.cmdOpenPackageFolder.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.cmdOpenPackageFolder)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.txtPackageFilter = QLineEdit(Form)
        self.txtPackageFilter.setObjectName(u"txtPackageFilter")

        self.verticalLayout_4.addWidget(self.txtPackageFilter)

        self.tabWidget_11 = QTabWidget(Form)
        self.tabWidget_11.setObjectName(u"tabWidget_11")
        self.tab_36 = QWidget()
        self.tab_36.setObjectName(u"tab_36")
        self.verticalLayout_48 = QVBoxLayout(self.tab_36)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.lstPackages = QListView(self.tab_36)
        self.lstPackages.setObjectName(u"lstPackages")

        self.verticalLayout_48.addWidget(self.lstPackages)

        self.tabWidget_11.addTab(self.tab_36, "")
        self.tab_37 = QWidget()
        self.tab_37.setObjectName(u"tab_37")
        self.verticalLayout_49 = QVBoxLayout(self.tab_37)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.cmdLoadPackage = QPushButton(self.tab_37)
        self.cmdLoadPackage.setObjectName(u"cmdLoadPackage")

        self.verticalLayout_49.addWidget(self.cmdLoadPackage)

        self.cmdCreateAppPackage = QPushButton(self.tab_37)
        self.cmdCreateAppPackage.setObjectName(u"cmdCreateAppPackage")

        self.verticalLayout_49.addWidget(self.cmdCreateAppPackage)

        self.cmdCreateCommand = QPushButton(self.tab_37)
        self.cmdCreateCommand.setObjectName(u"cmdCreateCommand")

        self.verticalLayout_49.addWidget(self.cmdCreateCommand)

        self.cmdCreateFunction = QPushButton(self.tab_37)
        self.cmdCreateFunction.setObjectName(u"cmdCreateFunction")

        self.verticalLayout_49.addWidget(self.cmdCreateFunction)

        self.cmdCreateNodes = QPushButton(self.tab_37)
        self.cmdCreateNodes.setObjectName(u"cmdCreateNodes")

        self.verticalLayout_49.addWidget(self.cmdCreateNodes)

        self.cmdCreatePins = QPushButton(self.tab_37)
        self.cmdCreatePins.setObjectName(u"cmdCreatePins")

        self.verticalLayout_49.addWidget(self.cmdCreatePins)

        self.tvLoadedApps = QTreeWidget(self.tab_37)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tvLoadedApps.setHeaderItem(__qtreewidgetitem)
        self.tvLoadedApps.setObjectName(u"tvLoadedApps")
        self.tvLoadedApps.header().setVisible(False)

        self.verticalLayout_49.addWidget(self.tvLoadedApps)

        self.tabWidget_11.addTab(self.tab_37, "")

        self.verticalLayout_4.addWidget(self.tabWidget_11)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.tvPackageItems = QTreeWidget(Form)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.tvPackageItems.setHeaderItem(__qtreewidgetitem1)
        self.tvPackageItems.setObjectName(u"tvPackageItems")
        self.tvPackageItems.header().setVisible(False)

        self.horizontalLayout.addWidget(self.tvPackageItems)

        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.txtPackageName = QLineEdit(Form)
        self.txtPackageName.setObjectName(u"txtPackageName")

        self.horizontalLayout_32.addWidget(self.txtPackageName)

        self.cmdUpdateInit = QPushButton(Form)
        self.cmdUpdateInit.setObjectName(u"cmdUpdateInit")

        self.horizontalLayout_32.addWidget(self.cmdUpdateInit)


        self.verticalLayout_36.addLayout(self.horizontalLayout_32)

        self.dteCopyrightYear = QDateEdit(Form)
        self.dteCopyrightYear.setObjectName(u"dteCopyrightYear")
        self.dteCopyrightYear.setDateTime(QDateTime(QDate(2023, 9, 14), QTime(0, 0, 0)))
        self.dteCopyrightYear.setMinimumDate(QDate(2023, 9, 14))

        self.verticalLayout_36.addWidget(self.dteCopyrightYear)

        self.twPackage = QTabWidget(Form)
        self.twPackage.setObjectName(u"twPackage")
        self.tab_45 = QWidget()
        self.tab_45.setObjectName(u"tab_45")
        self.verticalLayout_53 = QVBoxLayout(self.tab_45)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.tabWidget_9 = QTabWidget(self.tab_45)
        self.tabWidget_9.setObjectName(u"tabWidget_9")
        self.tab_32 = QWidget()
        self.tab_32.setObjectName(u"tab_32")
        self.verticalLayout_38 = QVBoxLayout(self.tab_32)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.chkPackageResource = QCheckBox(self.tab_32)
        self.chkPackageResource.setObjectName(u"chkPackageResource")
        self.chkPackageResource.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageResource)

        self.chkPackageCommands = QCheckBox(self.tab_32)
        self.chkPackageCommands.setObjectName(u"chkPackageCommands")
        self.chkPackageCommands.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageCommands)

        self.chkPackageFunctions = QCheckBox(self.tab_32)
        self.chkPackageFunctions.setObjectName(u"chkPackageFunctions")
        self.chkPackageFunctions.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageFunctions)

        self.chkPackageNodes = QCheckBox(self.tab_32)
        self.chkPackageNodes.setObjectName(u"chkPackageNodes")
        self.chkPackageNodes.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageNodes)

        self.chkPackageWidgets = QCheckBox(self.tab_32)
        self.chkPackageWidgets.setObjectName(u"chkPackageWidgets")
        self.chkPackageWidgets.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageWidgets)

        self.chkPackageUI = QCheckBox(self.tab_32)
        self.chkPackageUI.setObjectName(u"chkPackageUI")
        self.chkPackageUI.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageUI)

        self.chkPackagePins = QCheckBox(self.tab_32)
        self.chkPackagePins.setObjectName(u"chkPackagePins")
        self.chkPackagePins.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackagePins)

        self.chkPackageTools = QCheckBox(self.tab_32)
        self.chkPackageTools.setObjectName(u"chkPackageTools")
        self.chkPackageTools.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageTools)

        self.chkPackageExporters = QCheckBox(self.tab_32)
        self.chkPackageExporters.setObjectName(u"chkPackageExporters")
        self.chkPackageExporters.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageExporters)

        self.chkPackageFactories = QCheckBox(self.tab_32)
        self.chkPackageFactories.setObjectName(u"chkPackageFactories")
        self.chkPackageFactories.setChecked(True)

        self.verticalLayout_38.addWidget(self.chkPackageFactories)

        self.verticalSpacer_12 = QSpacerItem(20, 387, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_38.addItem(self.verticalSpacer_12)

        self.tabWidget_9.addTab(self.tab_32, "")
        self.tab_33 = QWidget()
        self.tab_33.setObjectName(u"tab_33")
        self.verticalLayout_37 = QVBoxLayout(self.tab_33)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.cmdCreatePackage = QPushButton(self.tab_33)
        self.cmdCreatePackage.setObjectName(u"cmdCreatePackage")

        self.horizontalLayout_19.addWidget(self.cmdCreatePackage)

        self.cmdCreatePackage_2 = QPushButton(self.tab_33)
        self.cmdCreatePackage_2.setObjectName(u"cmdCreatePackage_2")

        self.horizontalLayout_19.addWidget(self.cmdCreatePackage_2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_6)


        self.verticalLayout_37.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.cmdCreatePackage_3 = QPushButton(self.tab_33)
        self.cmdCreatePackage_3.setObjectName(u"cmdCreatePackage_3")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_3)

        self.cmdCreatePackage_4 = QPushButton(self.tab_33)
        self.cmdCreatePackage_4.setObjectName(u"cmdCreatePackage_4")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_4)

        self.cmdCreatePackage_5 = QPushButton(self.tab_33)
        self.cmdCreatePackage_5.setObjectName(u"cmdCreatePackage_5")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_5)

        self.cmdCreatePackage_6 = QPushButton(self.tab_33)
        self.cmdCreatePackage_6.setObjectName(u"cmdCreatePackage_6")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_6)

        self.cmdCreatePackage_7 = QPushButton(self.tab_33)
        self.cmdCreatePackage_7.setObjectName(u"cmdCreatePackage_7")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_7)

        self.cmdCreatePackage_8 = QPushButton(self.tab_33)
        self.cmdCreatePackage_8.setObjectName(u"cmdCreatePackage_8")

        self.horizontalLayout_23.addWidget(self.cmdCreatePackage_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_8)


        self.verticalLayout_37.addLayout(self.horizontalLayout_23)

        self.txtSearchPackages = QLineEdit(self.tab_33)
        self.txtSearchPackages.setObjectName(u"txtSearchPackages")

        self.verticalLayout_37.addWidget(self.txtSearchPackages)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, -1)
        self.lstPythonPackages = QListView(self.tab_33)
        self.lstPythonPackages.setObjectName(u"lstPythonPackages")

        self.horizontalLayout_27.addWidget(self.lstPythonPackages)

        self.lstPythonPackageFunctions = QListView(self.tab_33)
        self.lstPythonPackageFunctions.setObjectName(u"lstPythonPackageFunctions")

        self.horizontalLayout_27.addWidget(self.lstPythonPackageFunctions)


        self.verticalLayout_37.addLayout(self.horizontalLayout_27)

        self.tabWidget_10 = QTabWidget(self.tab_33)
        self.tabWidget_10.setObjectName(u"tabWidget_10")
        self.tab_28 = QWidget()
        self.tab_28.setObjectName(u"tab_28")
        self.verticalLayout_40 = QVBoxLayout(self.tab_28)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_7.setContentsMargins(-1, 10, -1, -1)
        self.label_30 = QLabel(self.tab_28)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.label_30)

        self.label_32 = QLabel(self.tab_28)
        self.label_32.setObjectName(u"label_32")

        self.formLayout_7.setWidget(2, QFormLayout.LabelRole, self.label_32)

        self.label_33 = QLabel(self.tab_28)
        self.label_33.setObjectName(u"label_33")

        self.formLayout_7.setWidget(3, QFormLayout.LabelRole, self.label_33)

        self.label_37 = QLabel(self.tab_28)
        self.label_37.setObjectName(u"label_37")

        self.formLayout_7.setWidget(4, QFormLayout.LabelRole, self.label_37)

        self.label_31 = QLabel(self.tab_28)
        self.label_31.setObjectName(u"label_31")

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.label_31)

        self.label_38 = QLabel(self.tab_28)
        self.label_38.setObjectName(u"label_38")

        self.formLayout_7.setWidget(5, QFormLayout.LabelRole, self.label_38)

        self.lineEdit = QLineEdit(self.tab_28)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.tab_28)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEnabled(False)

        self.formLayout_7.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)

        self.plainTextEdit = QPlainTextEdit(self.tab_28)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setEnabled(False)

        self.formLayout_7.setWidget(2, QFormLayout.FieldRole, self.plainTextEdit)

        self.lineEdit_3 = QLineEdit(self.tab_28)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEnabled(False)

        self.formLayout_7.setWidget(3, QFormLayout.FieldRole, self.lineEdit_3)

        self.lineEdit_4 = QLineEdit(self.tab_28)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setEnabled(False)

        self.formLayout_7.setWidget(4, QFormLayout.FieldRole, self.lineEdit_4)

        self.lineEdit_5 = QLineEdit(self.tab_28)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setEnabled(False)

        self.formLayout_7.setWidget(5, QFormLayout.FieldRole, self.lineEdit_5)


        self.verticalLayout_40.addLayout(self.formLayout_7)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_11)

        self.tabWidget_10.addTab(self.tab_28, "")
        self.tab_34 = QWidget()
        self.tab_34.setObjectName(u"tab_34")
        self.verticalLayout_42 = QVBoxLayout(self.tab_34)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.formLayout_8 = QFormLayout()
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.formLayout_8.setContentsMargins(-1, 10, -1, -1)
        self.label_39 = QLabel(self.tab_34)
        self.label_39.setObjectName(u"label_39")

        self.formLayout_8.setWidget(0, QFormLayout.LabelRole, self.label_39)

        self.lineEdit_6 = QLineEdit(self.tab_34)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setEnabled(False)

        self.formLayout_8.setWidget(0, QFormLayout.FieldRole, self.lineEdit_6)

        self.label_40 = QLabel(self.tab_34)
        self.label_40.setObjectName(u"label_40")

        self.formLayout_8.setWidget(1, QFormLayout.LabelRole, self.label_40)

        self.plainTextEdit_2 = QPlainTextEdit(self.tab_34)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setEnabled(False)

        self.formLayout_8.setWidget(1, QFormLayout.FieldRole, self.plainTextEdit_2)

        self.lineEdit_7 = QLineEdit(self.tab_34)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setEnabled(False)

        self.formLayout_8.setWidget(2, QFormLayout.FieldRole, self.lineEdit_7)

        self.label_41 = QLabel(self.tab_34)
        self.label_41.setObjectName(u"label_41")

        self.formLayout_8.setWidget(2, QFormLayout.LabelRole, self.label_41)

        self.label_42 = QLabel(self.tab_34)
        self.label_42.setObjectName(u"label_42")

        self.formLayout_8.setWidget(3, QFormLayout.LabelRole, self.label_42)

        self.lineEdit_8 = QLineEdit(self.tab_34)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setEnabled(False)

        self.formLayout_8.setWidget(3, QFormLayout.FieldRole, self.lineEdit_8)


        self.verticalLayout_42.addLayout(self.formLayout_8)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_42.addItem(self.verticalSpacer_13)

        self.tabWidget_10.addTab(self.tab_34, "")

        self.verticalLayout_37.addWidget(self.tabWidget_10)

        self.tabWidget_9.addTab(self.tab_33, "")

        self.verticalLayout_53.addWidget(self.tabWidget_9)

        self.twPackage.addTab(self.tab_45, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_24 = QVBoxLayout(self.tab_4)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.label_23 = QLabel(self.tab_4)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_23)

        self.txtCommandFileName = QLineEdit(self.tab_4)
        self.txtCommandFileName.setObjectName(u"txtCommandFileName")

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.txtCommandFileName)


        self.verticalLayout_24.addLayout(self.formLayout_5)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(-1, 0, -1, -1)
        self.cmdNewCommand = QPushButton(self.tab_4)
        self.cmdNewCommand.setObjectName(u"cmdNewCommand")

        self.horizontalLayout_31.addWidget(self.cmdNewCommand)

        self.cmdSaveCommand = QPushButton(self.tab_4)
        self.cmdSaveCommand.setObjectName(u"cmdSaveCommand")

        self.horizontalLayout_31.addWidget(self.cmdSaveCommand)

        self.cmdSaveAsCommand = QPushButton(self.tab_4)
        self.cmdSaveAsCommand.setObjectName(u"cmdSaveAsCommand")

        self.horizontalLayout_31.addWidget(self.cmdSaveAsCommand)

        self.cmdWriteCommand = QPushButton(self.tab_4)
        self.cmdWriteCommand.setObjectName(u"cmdWriteCommand")

        self.horizontalLayout_31.addWidget(self.cmdWriteCommand)


        self.verticalLayout_24.addLayout(self.horizontalLayout_31)

        self.tabWidget_7 = QTabWidget(self.tab_4)
        self.tabWidget_7.setObjectName(u"tabWidget_7")
        self.tab_23 = QWidget()
        self.tab_23.setObjectName(u"tab_23")
        self.verticalLayout_30 = QVBoxLayout(self.tab_23)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.chkCommandSingleton = QCheckBox(self.tab_23)
        self.chkCommandSingleton.setObjectName(u"chkCommandSingleton")

        self.gridLayout_9.addWidget(self.chkCommandSingleton, 3, 2, 1, 1)

        self.label_64 = QLabel(self.tab_23)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_9.addWidget(self.label_64, 1, 0, 1, 1)

        self.cmbCommandAuthor = QComboBox(self.tab_23)
        self.cmbCommandAuthor.setObjectName(u"cmbCommandAuthor")
        self.cmbCommandAuthor.setEditable(True)

        self.gridLayout_9.addWidget(self.cmbCommandAuthor, 2, 2, 1, 1)

        self.txtCommandToolTip = QLineEdit(self.tab_23)
        self.txtCommandToolTip.setObjectName(u"txtCommandToolTip")

        self.gridLayout_9.addWidget(self.txtCommandToolTip, 7, 2, 1, 1)

        self.txtCommandKeyWords = QLineEdit(self.tab_23)
        self.txtCommandKeyWords.setObjectName(u"txtCommandKeyWords")

        self.gridLayout_9.addWidget(self.txtCommandKeyWords, 6, 2, 1, 1)

        self.txtCommandCategory = QLineEdit(self.tab_23)
        self.txtCommandCategory.setObjectName(u"txtCommandCategory")

        self.gridLayout_9.addWidget(self.txtCommandCategory, 5, 2, 1, 1)

        self.txtCommandName = QLineEdit(self.tab_23)
        self.txtCommandName.setObjectName(u"txtCommandName")

        self.gridLayout_9.addWidget(self.txtCommandName, 1, 2, 1, 1)

        self.label_20 = QLabel(self.tab_23)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_9.addWidget(self.label_20, 5, 0, 1, 1)

        self.label_69 = QLabel(self.tab_23)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_9.addWidget(self.label_69, 2, 0, 1, 1)

        self.label_24 = QLabel(self.tab_23)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_9.addWidget(self.label_24, 6, 0, 1, 1)

        self.label_65 = QLabel(self.tab_23)
        self.label_65.setObjectName(u"label_65")

        self.gridLayout_9.addWidget(self.label_65, 3, 0, 1, 1)

        self.label_34 = QLabel(self.tab_23)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_9.addWidget(self.label_34, 7, 0, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.txtCommandKeyBoardShortcut = QLineEdit(self.tab_23)
        self.txtCommandKeyBoardShortcut.setObjectName(u"txtCommandKeyBoardShortcut")

        self.horizontalLayout_17.addWidget(self.txtCommandKeyBoardShortcut)

        self.cmdCommandAddShortCut = QPushButton(self.tab_23)
        self.cmdCommandAddShortCut.setObjectName(u"cmdCommandAddShortCut")
        self.cmdCommandAddShortCut.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_17.addWidget(self.cmdCommandAddShortCut)


        self.gridLayout_9.addLayout(self.horizontalLayout_17, 8, 2, 1, 1)

        self.label_36 = QLabel(self.tab_23)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_9.addWidget(self.label_36, 8, 0, 1, 1)


        self.horizontalLayout_22.addLayout(self.gridLayout_9)

        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 0, -1, -1)
        self.rdoCommandDT = QRadioButton(self.tab_23)
        self.rdoCommandDT.setObjectName(u"rdoCommandDT")

        self.horizontalLayout_26.addWidget(self.rdoCommandDT)

        self.rdoCommandST = QRadioButton(self.tab_23)
        self.rdoCommandST.setObjectName(u"rdoCommandST")

        self.horizontalLayout_26.addWidget(self.rdoCommandST)

        self.rdoCommandDialog = QRadioButton(self.tab_23)
        self.rdoCommandDialog.setObjectName(u"rdoCommandDialog")

        self.horizontalLayout_26.addWidget(self.rdoCommandDialog)


        self.verticalLayout_29.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_44 = QLabel(self.tab_23)
        self.label_44.setObjectName(u"label_44")

        self.horizontalLayout_39.addWidget(self.label_44)

        self.txtCommandDiUIFile = QLineEdit(self.tab_23)
        self.txtCommandDiUIFile.setObjectName(u"txtCommandDiUIFile")

        self.horizontalLayout_39.addWidget(self.txtCommandDiUIFile)

        self.cmdCommandAddShortCut_4 = QPushButton(self.tab_23)
        self.cmdCommandAddShortCut_4.setObjectName(u"cmdCommandAddShortCut_4")
        self.cmdCommandAddShortCut_4.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_39.addWidget(self.cmdCommandAddShortCut_4)


        self.verticalLayout_29.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_45 = QLabel(self.tab_23)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_41.addWidget(self.label_45)

        self.txtCommandDiUIPyFile = QLineEdit(self.tab_23)
        self.txtCommandDiUIPyFile.setObjectName(u"txtCommandDiUIPyFile")

        self.horizontalLayout_41.addWidget(self.txtCommandDiUIPyFile)

        self.cmdCommandAddShortCut_6 = QPushButton(self.tab_23)
        self.cmdCommandAddShortCut_6.setObjectName(u"cmdCommandAddShortCut_6")
        self.cmdCommandAddShortCut_6.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_41.addWidget(self.cmdCommandAddShortCut_6)


        self.verticalLayout_29.addLayout(self.horizontalLayout_41)

        self.stkCommandClassType = QStackedWidget(self.tab_23)
        self.stkCommandClassType.setObjectName(u"stkCommandClassType")
        self.DockTool = QWidget()
        self.DockTool.setObjectName(u"DockTool")
        self.verticalLayout_41 = QVBoxLayout(self.DockTool)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_66 = QLabel(self.DockTool)
        self.label_66.setObjectName(u"label_66")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_66)

        self.txtCommandDTOnShow = QLineEdit(self.DockTool)
        self.txtCommandDTOnShow.setObjectName(u"txtCommandDTOnShow")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.txtCommandDTOnShow)

        self.label_67 = QLabel(self.DockTool)
        self.label_67.setObjectName(u"label_67")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_67)

        self.txtCommandDTRefresh = QLineEdit(self.DockTool)
        self.txtCommandDTRefresh.setObjectName(u"txtCommandDTRefresh")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.txtCommandDTRefresh)

        self.label_68 = QLabel(self.DockTool)
        self.label_68.setObjectName(u"label_68")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_68)

        self.cmdCommandDTDefaultDockArea = QComboBox(self.DockTool)
        self.cmdCommandDTDefaultDockArea.setObjectName(u"cmdCommandDTDefaultDockArea")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.cmdCommandDTDefaultDockArea)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.txtCommandKeyBoardShortcut_3 = QLineEdit(self.DockTool)
        self.txtCommandKeyBoardShortcut_3.setObjectName(u"txtCommandKeyBoardShortcut_3")

        self.horizontalLayout_37.addWidget(self.txtCommandKeyBoardShortcut_3)

        self.cmdCommandAddShortCut_3 = QPushButton(self.DockTool)
        self.cmdCommandAddShortCut_3.setObjectName(u"cmdCommandAddShortCut_3")
        self.cmdCommandAddShortCut_3.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_37.addWidget(self.cmdCommandAddShortCut_3)


        self.formLayout_4.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_37)

        self.label_70 = QLabel(self.DockTool)
        self.label_70.setObjectName(u"label_70")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_70)


        self.verticalLayout_41.addLayout(self.formLayout_4)

        self.cmdCommandDTCreateUI = QPushButton(self.DockTool)
        self.cmdCommandDTCreateUI.setObjectName(u"cmdCommandDTCreateUI")

        self.verticalLayout_41.addWidget(self.cmdCommandDTCreateUI)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_41.addItem(self.verticalSpacer_18)

        self.stkCommandClassType.addWidget(self.DockTool)
        self.ShelfTool = QWidget()
        self.ShelfTool.setObjectName(u"ShelfTool")
        self.verticalLayout_45 = QVBoxLayout(self.ShelfTool)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.label_28 = QLabel(self.ShelfTool)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_45.addWidget(self.label_28)

        self.cmdCommandSTCreateUI = QPushButton(self.ShelfTool)
        self.cmdCommandSTCreateUI.setObjectName(u"cmdCommandSTCreateUI")

        self.verticalLayout_45.addWidget(self.cmdCommandSTCreateUI)

        self.verticalSpacer_17 = QSpacerItem(20, 95, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_45.addItem(self.verticalSpacer_17)

        self.stkCommandClassType.addWidget(self.ShelfTool)
        self.Form1 = QWidget()
        self.Form1.setObjectName(u"Form1")
        self.verticalLayout_44 = QVBoxLayout(self.Form1)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.cmdCommandDialogCreateUI = QPushButton(self.Form1)
        self.cmdCommandDialogCreateUI.setObjectName(u"cmdCommandDialogCreateUI")

        self.verticalLayout_44.addWidget(self.cmdCommandDialogCreateUI)

        self.verticalSpacer_16 = QSpacerItem(20, 117, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_44.addItem(self.verticalSpacer_16)

        self.stkCommandClassType.addWidget(self.Form1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_43 = QVBoxLayout(self.page)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.stkCommandClassType.addWidget(self.page)

        self.verticalLayout_29.addWidget(self.stkCommandClassType)


        self.horizontalLayout_22.addLayout(self.verticalLayout_29)


        self.verticalLayout_30.addLayout(self.horizontalLayout_22)

        self.label_21 = QLabel(self.tab_23)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_30.addWidget(self.label_21)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.txtCommandDescription = QTextEdit(self.tab_23)
        self.txtCommandDescription.setObjectName(u"txtCommandDescription")
        self.txtCommandDescription.setMinimumSize(QSize(0, 250))
        self.txtCommandDescription.setMaximumSize(QSize(16777215, 50))

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.txtCommandDescription)


        self.verticalLayout_30.addLayout(self.formLayout_6)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_7)

        self.tabWidget_7.addTab(self.tab_23, "")
        self.tab_27 = QWidget()
        self.tab_27.setObjectName(u"tab_27")
        self.verticalLayout_34 = QVBoxLayout(self.tab_27)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.lstCommandImports = QListWidget(self.tab_27)
        self.lstCommandImports.setObjectName(u"lstCommandImports")

        self.verticalLayout_34.addWidget(self.lstCommandImports)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, -1, 0, -1)
        self.tvCommandImportTree = QTreeView(self.tab_27)
        self.tvCommandImportTree.setObjectName(u"tvCommandImportTree")

        self.horizontalLayout_18.addWidget(self.tvCommandImportTree)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.cmdCommandImportSelected = QPushButton(self.tab_27)
        self.cmdCommandImportSelected.setObjectName(u"cmdCommandImportSelected")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.cmdCommandImportSelected)

        self.cmdCommandImportAll = QPushButton(self.tab_27)
        self.cmdCommandImportAll.setObjectName(u"cmdCommandImportAll")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cmdCommandImportAll)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout_3.setItem(2, QFormLayout.FieldRole, self.verticalSpacer_5)


        self.horizontalLayout_18.addLayout(self.formLayout_3)

        self.pushButton_7 = QPushButton(self.tab_27)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_18.addWidget(self.pushButton_7)


        self.verticalLayout_25.addLayout(self.horizontalLayout_18)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_9)


        self.verticalLayout_34.addLayout(self.verticalLayout_25)

        self.tabWidget_7.addTab(self.tab_27, "")
        self.tab_24 = QWidget()
        self.tab_24.setObjectName(u"tab_24")
        self.verticalLayout_33 = QVBoxLayout(self.tab_24)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(-1, 10, -1, -1)
        self.label_25 = QLabel(self.tab_24)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_25, 2, 0, 1, 1)

        self.label_27 = QLabel(self.tab_24)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_27, 2, 2, 1, 1)

        self.cmdCommandAddLargeIcon = QPushButton(self.tab_24)
        self.cmdCommandAddLargeIcon.setObjectName(u"cmdCommandAddLargeIcon")
        self.cmdCommandAddLargeIcon.setMinimumSize(QSize(80, 80))
        self.cmdCommandAddLargeIcon.setMaximumSize(QSize(80, 80))

        self.gridLayout_7.addWidget(self.cmdCommandAddLargeIcon, 0, 2, 1, 1)

        self.label_26 = QLabel(self.tab_24)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_26, 2, 1, 1, 1)

        self.cmdCommandAddMediumIcon = QPushButton(self.tab_24)
        self.cmdCommandAddMediumIcon.setObjectName(u"cmdCommandAddMediumIcon")
        self.cmdCommandAddMediumIcon.setMinimumSize(QSize(60, 60))
        self.cmdCommandAddMediumIcon.setMaximumSize(QSize(60, 60))

        self.gridLayout_7.addWidget(self.cmdCommandAddMediumIcon, 0, 1, 1, 1)

        self.cmdCommandAddSmallIcon = QPushButton(self.tab_24)
        self.cmdCommandAddSmallIcon.setObjectName(u"cmdCommandAddSmallIcon")
        self.cmdCommandAddSmallIcon.setEnabled(True)
        self.cmdCommandAddSmallIcon.setMinimumSize(QSize(40, 40))
        self.cmdCommandAddSmallIcon.setMaximumSize(QSize(40, 40))

        self.gridLayout_7.addWidget(self.cmdCommandAddSmallIcon, 0, 0, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, -1)
        self.txtCommandSmallIcon = QLineEdit(self.tab_24)
        self.txtCommandSmallIcon.setObjectName(u"txtCommandSmallIcon")
        self.txtCommandSmallIcon.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_16.addWidget(self.txtCommandSmallIcon)

        self.cmdEditSmallIcon = QPushButton(self.tab_24)
        self.cmdEditSmallIcon.setObjectName(u"cmdEditSmallIcon")

        self.horizontalLayout_16.addWidget(self.cmdEditSmallIcon)


        self.gridLayout_7.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, -1)
        self.txtCommandMediumIcon = QLineEdit(self.tab_24)
        self.txtCommandMediumIcon.setObjectName(u"txtCommandMediumIcon")
        self.txtCommandMediumIcon.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_24.addWidget(self.txtCommandMediumIcon)

        self.cmdEditMediumIcon = QPushButton(self.tab_24)
        self.cmdEditMediumIcon.setObjectName(u"cmdEditMediumIcon")

        self.horizontalLayout_24.addWidget(self.cmdEditMediumIcon)


        self.gridLayout_7.addLayout(self.horizontalLayout_24, 1, 1, 1, 1)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, -1)
        self.txtCommandLargeIcon = QLineEdit(self.tab_24)
        self.txtCommandLargeIcon.setObjectName(u"txtCommandLargeIcon")
        self.txtCommandLargeIcon.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_25.addWidget(self.txtCommandLargeIcon)

        self.cmdEditLargeIcon = QPushButton(self.tab_24)
        self.cmdEditLargeIcon.setObjectName(u"cmdEditLargeIcon")

        self.horizontalLayout_25.addWidget(self.cmdEditLargeIcon)


        self.gridLayout_7.addLayout(self.horizontalLayout_25, 1, 2, 1, 1)


        self.verticalLayout_33.addLayout(self.gridLayout_7)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, 0, -1, -1)
        self.chkCommandResourceFolder = QCheckBox(self.tab_24)
        self.chkCommandResourceFolder.setObjectName(u"chkCommandResourceFolder")

        self.horizontalLayout_29.addWidget(self.chkCommandResourceFolder)

        self.txtCommandResourceFolder = QLineEdit(self.tab_24)
        self.txtCommandResourceFolder.setObjectName(u"txtCommandResourceFolder")

        self.horizontalLayout_29.addWidget(self.txtCommandResourceFolder)

        self.cmdFindResourceFolder = QPushButton(self.tab_24)
        self.cmdFindResourceFolder.setObjectName(u"cmdFindResourceFolder")
        self.cmdFindResourceFolder.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_29.addWidget(self.cmdFindResourceFolder)


        self.verticalLayout_33.addLayout(self.horizontalLayout_29)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_8)

        self.tabWidget_7.addTab(self.tab_24, "")
        self.tab_25 = QWidget()
        self.tab_25.setObjectName(u"tab_25")
        self.verticalLayout_31 = QVBoxLayout(self.tab_25)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.tabWidget_6 = QTabWidget(self.tab_25)
        self.tabWidget_6.setObjectName(u"tabWidget_6")
        self.tab_21 = QWidget()
        self.tab_21.setObjectName(u"tab_21")
        self.verticalLayout_27 = QVBoxLayout(self.tab_21)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, -1)
        self.txtPyflowFile = QLineEdit(self.tab_21)
        self.txtPyflowFile.setObjectName(u"txtPyflowFile")

        self.horizontalLayout_15.addWidget(self.txtPyflowFile)

        self.cmdCreatePyFlow = QPushButton(self.tab_21)
        self.cmdCreatePyFlow.setObjectName(u"cmdCreatePyFlow")
        self.cmdCreatePyFlow.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_15.addWidget(self.cmdCreatePyFlow)


        self.verticalLayout_27.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.listView_2 = QListView(self.tab_21)
        self.listView_2.setObjectName(u"listView_2")

        self.horizontalLayout_14.addWidget(self.listView_2)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_35 = QLabel(self.tab_21)
        self.label_35.setObjectName(u"label_35")

        self.verticalLayout_26.addWidget(self.label_35)


        self.horizontalLayout_14.addLayout(self.verticalLayout_26)


        self.verticalLayout_27.addLayout(self.horizontalLayout_14)

        self.tabWidget_6.addTab(self.tab_21, "")
        self.tab_26 = QWidget()
        self.tab_26.setObjectName(u"tab_26")
        self.verticalLayout_28 = QVBoxLayout(self.tab_26)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.txtCommandCode = QTextEdit(self.tab_26)
        self.txtCommandCode.setObjectName(u"txtCommandCode")

        self.verticalLayout_28.addWidget(self.txtCommandCode)

        self.tabWidget_6.addTab(self.tab_26, "")

        self.verticalLayout_31.addWidget(self.tabWidget_6)

        self.tabWidget_7.addTab(self.tab_25, "")
        self.tab_22 = QWidget()
        self.tab_22.setObjectName(u"tab_22")
        self.verticalLayout_35 = QVBoxLayout(self.tab_22)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.label_22 = QLabel(self.tab_22)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_35.addWidget(self.label_22)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.txtCommandAuthor = QLineEdit(self.tab_22)
        self.txtCommandAuthor.setObjectName(u"txtCommandAuthor")

        self.horizontalLayout_21.addWidget(self.txtCommandAuthor)

        self.txtCommandRevision = QLineEdit(self.tab_22)
        self.txtCommandRevision.setObjectName(u"txtCommandRevision")

        self.horizontalLayout_21.addWidget(self.txtCommandRevision)

        self.dteCommandRevisionDate = QDateEdit(self.tab_22)
        self.dteCommandRevisionDate.setObjectName(u"dteCommandRevisionDate")

        self.horizontalLayout_21.addWidget(self.dteCommandRevisionDate)

        self.cmdAddCommandRevision = QPushButton(self.tab_22)
        self.cmdAddCommandRevision.setObjectName(u"cmdAddCommandRevision")

        self.horizontalLayout_21.addWidget(self.cmdAddCommandRevision)


        self.verticalLayout_35.addLayout(self.horizontalLayout_21)

        self.lstCommandRevisionHistory = QListWidget(self.tab_22)
        self.lstCommandRevisionHistory.setObjectName(u"lstCommandRevisionHistory")

        self.verticalLayout_35.addWidget(self.lstCommandRevisionHistory)

        self.tabWidget_7.addTab(self.tab_22, "")

        self.verticalLayout_24.addWidget(self.tabWidget_7)

        self.verticalSpacer_3 = QSpacerItem(20, 7, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer_3)

        self.twPackage.addTab(self.tab_4, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_8 = QVBoxLayout(self.tab_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, 0, -1, -1)
        self.cmdCreateNewFunction_2 = QPushButton(self.tab_2)
        self.cmdCreateNewFunction_2.setObjectName(u"cmdCreateNewFunction_2")

        self.horizontalLayout_33.addWidget(self.cmdCreateNewFunction_2)

        self.cmdSaveFunction_2 = QPushButton(self.tab_2)
        self.cmdSaveFunction_2.setObjectName(u"cmdSaveFunction_2")

        self.horizontalLayout_33.addWidget(self.cmdSaveFunction_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_33)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.cmdCreateNewFunction = QPushButton(self.tab_2)
        self.cmdCreateNewFunction.setObjectName(u"cmdCreateNewFunction")
        self.cmdCreateNewFunction.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_4.addWidget(self.cmdCreateNewFunction, 1, 2, 1, 1)

        self.txtFunctionFileName = QLineEdit(self.tab_2)
        self.txtFunctionFileName.setObjectName(u"txtFunctionFileName")

        self.gridLayout_4.addWidget(self.txtFunctionFileName, 0, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_4.addWidget(self.pushButton_3, 0, 2, 1, 1)

        self.txtFunctionName = QLineEdit(self.tab_2)
        self.txtFunctionName.setObjectName(u"txtFunctionName")

        self.gridLayout_4.addWidget(self.txtFunctionName, 1, 1, 1, 1)

        self.label_10 = QLabel(self.tab_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_11 = QLabel(self.tab_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.tabWidget_3 = QTabWidget(self.tab_2)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.verticalLayout_11 = QVBoxLayout(self.tab_14)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.tblFInputPins = QTableView(self.tab_14)
        self.tblFInputPins.setObjectName(u"tblFInputPins")
        self.tblFInputPins.verticalHeader().setVisible(False)

        self.verticalLayout_6.addWidget(self.tblFInputPins)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.cmdUpOrderFInputPin = QPushButton(self.tab_14)
        self.cmdUpOrderFInputPin.setObjectName(u"cmdUpOrderFInputPin")
        self.cmdUpOrderFInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_9.addWidget(self.cmdUpOrderFInputPin)

        self.cmdDownOrderFInputPin = QPushButton(self.tab_14)
        self.cmdDownOrderFInputPin.setObjectName(u"cmdDownOrderFInputPin")
        self.cmdDownOrderFInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_9.addWidget(self.cmdDownOrderFInputPin)

        self.cmdAddFInputPin = QPushButton(self.tab_14)
        self.cmdAddFInputPin.setObjectName(u"cmdAddFInputPin")
        self.cmdAddFInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_9.addWidget(self.cmdAddFInputPin)

        self.cmdRemoveFInputPin = QPushButton(self.tab_14)
        self.cmdRemoveFInputPin.setObjectName(u"cmdRemoveFInputPin")
        self.cmdRemoveFInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_9.addWidget(self.cmdRemoveFInputPin)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, -1, 0, -1)
        self.tblFOutputPins = QTableView(self.tab_14)
        self.tblFOutputPins.setObjectName(u"tblFOutputPins")
        self.tblFOutputPins.verticalHeader().setVisible(False)

        self.verticalLayout_7.addWidget(self.tblFOutputPins)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)

        self.cmdUpOrderFOutputPin = QPushButton(self.tab_14)
        self.cmdUpOrderFOutputPin.setObjectName(u"cmdUpOrderFOutputPin")
        self.cmdUpOrderFOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_11.addWidget(self.cmdUpOrderFOutputPin)

        self.cmdDownOrderFOutputPin = QPushButton(self.tab_14)
        self.cmdDownOrderFOutputPin.setObjectName(u"cmdDownOrderFOutputPin")
        self.cmdDownOrderFOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_11.addWidget(self.cmdDownOrderFOutputPin)

        self.cmdAddFOutputPin = QPushButton(self.tab_14)
        self.cmdAddFOutputPin.setObjectName(u"cmdAddFOutputPin")
        self.cmdAddFOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_11.addWidget(self.cmdAddFOutputPin)

        self.cmdRemoveFOutputPin = QPushButton(self.tab_14)
        self.cmdRemoveFOutputPin.setObjectName(u"cmdRemoveFOutputPin")
        self.cmdRemoveFOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_11.addWidget(self.cmdRemoveFOutputPin)


        self.verticalLayout_7.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)


        self.verticalLayout_11.addLayout(self.horizontalLayout_3)

        self.tabWidget = QTabWidget(self.tab_14)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.txtPSConstraint = QLineEdit(self.tab)
        self.txtPSConstraint.setObjectName(u"txtPSConstraint")

        self.gridLayout.addWidget(self.txtPSConstraint, 2, 1, 1, 1)

        self.txtPSValueList = QLineEdit(self.tab)
        self.txtPSValueList.setObjectName(u"txtPSValueList")

        self.gridLayout.addWidget(self.txtPSValueList, 7, 1, 1, 1)

        self.chkPSInputWidget = QCheckBox(self.tab)
        self.chkPSInputWidget.setObjectName(u"chkPSInputWidget")

        self.gridLayout.addWidget(self.chkPSInputWidget, 5, 0, 1, 1)

        self.chkPSValueList = QCheckBox(self.tab)
        self.chkPSValueList.setObjectName(u"chkPSValueList")

        self.gridLayout.addWidget(self.chkPSValueList, 7, 0, 1, 1)

        self.chkPSDescription = QCheckBox(self.tab)
        self.chkPSDescription.setObjectName(u"chkPSDescription")

        self.gridLayout.addWidget(self.chkPSDescription, 6, 0, 1, 1)

        self.chkPSSupportedDataTypes = QCheckBox(self.tab)
        self.chkPSSupportedDataTypes.setObjectName(u"chkPSSupportedDataTypes")

        self.gridLayout.addWidget(self.chkPSSupportedDataTypes, 0, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.txtPSSupportedDataTypes = QLineEdit(self.tab)
        self.txtPSSupportedDataTypes.setObjectName(u"txtPSSupportedDataTypes")

        self.horizontalLayout_5.addWidget(self.txtPSSupportedDataTypes)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_5.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)

        self.txtPSDraggerSteps = QLineEdit(self.tab)
        self.txtPSDraggerSteps.setObjectName(u"txtPSDraggerSteps")

        self.gridLayout.addWidget(self.txtPSDraggerSteps, 9, 1, 1, 1)

        self.chkPSStructConstraint = QCheckBox(self.tab)
        self.chkPSStructConstraint.setObjectName(u"chkPSStructConstraint")

        self.gridLayout.addWidget(self.chkPSStructConstraint, 3, 0, 1, 1)

        self.chkPSDraggerSteps = QCheckBox(self.tab)
        self.chkPSDraggerSteps.setObjectName(u"chkPSDraggerSteps")

        self.gridLayout.addWidget(self.chkPSDraggerSteps, 9, 0, 1, 1)

        self.txtPSValueRange = QLineEdit(self.tab)
        self.txtPSValueRange.setObjectName(u"txtPSValueRange")

        self.gridLayout.addWidget(self.txtPSValueRange, 8, 1, 1, 1)

        self.txtPSDescription = QLineEdit(self.tab)
        self.txtPSDescription.setObjectName(u"txtPSDescription")

        self.gridLayout.addWidget(self.txtPSDescription, 6, 1, 1, 1)

        self.txtPSDisableOptions = QLineEdit(self.tab)
        self.txtPSDisableOptions.setObjectName(u"txtPSDisableOptions")

        self.gridLayout.addWidget(self.txtPSDisableOptions, 4, 1, 1, 1)

        self.chkPSValueRange = QCheckBox(self.tab)
        self.chkPSValueRange.setObjectName(u"chkPSValueRange")

        self.gridLayout.addWidget(self.chkPSValueRange, 8, 0, 1, 1)

        self.chkPSDisableOptions = QCheckBox(self.tab)
        self.chkPSDisableOptions.setObjectName(u"chkPSDisableOptions")

        self.gridLayout.addWidget(self.chkPSDisableOptions, 4, 0, 1, 1)

        self.txtPSStructConstraint = QLineEdit(self.tab)
        self.txtPSStructConstraint.setObjectName(u"txtPSStructConstraint")

        self.gridLayout.addWidget(self.txtPSStructConstraint, 3, 1, 1, 1)

        self.chkPSConstraint = QCheckBox(self.tab)
        self.chkPSConstraint.setObjectName(u"chkPSConstraint")

        self.gridLayout.addWidget(self.chkPSConstraint, 2, 0, 1, 1)

        self.txtPSInputWidget = QLineEdit(self.tab)
        self.txtPSInputWidget.setObjectName(u"txtPSInputWidget")

        self.gridLayout.addWidget(self.txtPSInputWidget, 5, 1, 1, 1)

        self.chkPSConstraint_3 = QCheckBox(self.tab)
        self.chkPSConstraint_3.setObjectName(u"chkPSConstraint_3")

        self.gridLayout.addWidget(self.chkPSConstraint_3, 1, 0, 1, 1)

        self.comboBox = QComboBox(self.tab)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.pinOptions = QWidget()
        self.pinOptions.setObjectName(u"pinOptions")
        self.verticalLayout_5 = QVBoxLayout(self.pinOptions)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.chkSupportOnlyArrays = QCheckBox(self.pinOptions)
        self.chkSupportOnlyArrays.setObjectName(u"chkSupportOnlyArrays")

        self.gridLayout_3.addWidget(self.chkSupportOnlyArrays, 2, 0, 1, 1)

        self.chkRenamingEnabled = QCheckBox(self.pinOptions)
        self.chkRenamingEnabled.setObjectName(u"chkRenamingEnabled")

        self.gridLayout_3.addWidget(self.chkRenamingEnabled, 5, 0, 1, 1)

        self.chkAllowMultipleConnections = QCheckBox(self.pinOptions)
        self.chkAllowMultipleConnections.setObjectName(u"chkAllowMultipleConnections")

        self.gridLayout_3.addWidget(self.chkAllowMultipleConnections, 3, 0, 1, 1)

        self.chkDynamic = QCheckBox(self.pinOptions)
        self.chkDynamic.setObjectName(u"chkDynamic")

        self.gridLayout_3.addWidget(self.chkDynamic, 6, 0, 1, 1)

        self.chkChangeTypeOnConnection = QCheckBox(self.pinOptions)
        self.chkChangeTypeOnConnection.setObjectName(u"chkChangeTypeOnConnection")

        self.gridLayout_3.addWidget(self.chkChangeTypeOnConnection, 4, 0, 1, 1)

        self.chkAllowAny = QCheckBox(self.pinOptions)
        self.chkAllowAny.setObjectName(u"chkAllowAny")

        self.gridLayout_3.addWidget(self.chkAllowAny, 9, 0, 1, 1)

        self.chkStorable = QCheckBox(self.pinOptions)
        self.chkStorable.setObjectName(u"chkStorable")

        self.gridLayout_3.addWidget(self.chkStorable, 8, 0, 1, 1)

        self.chkDictionaryElementSupported = QCheckBox(self.pinOptions)
        self.chkDictionaryElementSupported.setObjectName(u"chkDictionaryElementSupported")

        self.gridLayout_3.addWidget(self.chkDictionaryElementSupported, 10, 0, 1, 1)

        self.chkArraySupported = QCheckBox(self.pinOptions)
        self.chkArraySupported.setObjectName(u"chkArraySupported")

        self.gridLayout_3.addWidget(self.chkArraySupported, 0, 0, 1, 1)

        self.chkDictionarySupported = QCheckBox(self.pinOptions)
        self.chkDictionarySupported.setObjectName(u"chkDictionarySupported")

        self.gridLayout_3.addWidget(self.chkDictionarySupported, 1, 0, 1, 1)

        self.chkAlwaysPushDirty = QCheckBox(self.pinOptions)
        self.chkAlwaysPushDirty.setObjectName(u"chkAlwaysPushDirty")

        self.gridLayout_3.addWidget(self.chkAlwaysPushDirty, 7, 0, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.pinOptions, "")
        self.tab_35 = QWidget()
        self.tab_35.setObjectName(u"tab_35")
        self.verticalLayout_46 = QVBoxLayout(self.tab_35)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.txtFunctionDefinition = QTextEdit(self.tab_35)
        self.txtFunctionDefinition.setObjectName(u"txtFunctionDefinition")

        self.verticalLayout_46.addWidget(self.txtFunctionDefinition)

        self.tabWidget.addTab(self.tab_35, "")

        self.verticalLayout_11.addWidget(self.tabWidget)

        self.tabWidget_3.addTab(self.tab_14, "")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.verticalLayout_21 = QVBoxLayout(self.tab_17)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.tab_17)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.tab_17)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.txtMetaKeywords = QLineEdit(self.tab_17)
        self.txtMetaKeywords.setObjectName(u"txtMetaKeywords")

        self.gridLayout_2.addWidget(self.txtMetaKeywords, 1, 1, 1, 1)

        self.txtMetaCategory = QLineEdit(self.tab_17)
        self.txtMetaCategory.setObjectName(u"txtMetaCategory")

        self.gridLayout_2.addWidget(self.txtMetaCategory, 0, 1, 1, 1)

        self.label_3 = QLabel(self.tab_17)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.chkMetaCacheEnabled = QCheckBox(self.tab_17)
        self.chkMetaCacheEnabled.setObjectName(u"chkMetaCacheEnabled")

        self.gridLayout_2.addWidget(self.chkMetaCacheEnabled, 2, 1, 1, 1)


        self.verticalLayout_21.addLayout(self.gridLayout_2)

        self.verticalSpacer_6 = QSpacerItem(20, 512, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_21.addItem(self.verticalSpacer_6)

        self.tabWidget_3.addTab(self.tab_17, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_12 = QVBoxLayout(self.tab_3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.txtFImplement = QTextEdit(self.tab_3)
        self.txtFImplement.setObjectName(u"txtFImplement")

        self.verticalLayout_12.addWidget(self.txtFImplement)

        self.tabWidget_3.addTab(self.tab_3, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.verticalLayout_13 = QVBoxLayout(self.tab_10)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.lstFDef = QListWidget(self.tab_10)
        self.lstFDef.setObjectName(u"lstFDef")

        self.verticalLayout_13.addWidget(self.lstFDef)

        self.txtFDef = QTextEdit(self.tab_10)
        self.txtFDef.setObjectName(u"txtFDef")

        self.verticalLayout_13.addWidget(self.txtFDef)

        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.verticalLayout_9 = QVBoxLayout(self.tab_11)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.txtCodeDescription = QTextEdit(self.tab_11)
        self.txtCodeDescription.setObjectName(u"txtCodeDescription")
        self.txtCodeDescription.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_9.addWidget(self.txtCodeDescription)

        self.txtCode = QTextEdit(self.tab_11)
        self.txtCode.setObjectName(u"txtCode")

        self.verticalLayout_9.addWidget(self.txtCode)

        self.tabWidget_3.addTab(self.tab_11, "")

        self.verticalLayout.addWidget(self.tabWidget_3)


        self.verticalLayout_8.addLayout(self.verticalLayout)

        self.cmdSaveFunction = QPushButton(self.tab_2)
        self.cmdSaveFunction.setObjectName(u"cmdSaveFunction")
        self.cmdSaveFunction.setEnabled(False)
        self.cmdSaveFunction.setAutoFillBackground(False)

        self.verticalLayout_8.addWidget(self.cmdSaveFunction)

        self.twPackage.addTab(self.tab_2, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_23 = QVBoxLayout(self.tab_6)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_35 = QPushButton(self.tab_6)
        self.pushButton_35.setObjectName(u"pushButton_35")

        self.horizontalLayout_34.addWidget(self.pushButton_35)

        self.pushButton_36 = QPushButton(self.tab_6)
        self.pushButton_36.setObjectName(u"pushButton_36")

        self.horizontalLayout_34.addWidget(self.pushButton_36)


        self.verticalLayout_23.addLayout(self.horizontalLayout_34)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.label_5 = QLabel(self.tab_6)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_8.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_4 = QLabel(self.tab_6)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_8.addWidget(self.label_4, 2, 0, 1, 1)

        self.txtNodeFileName = QLineEdit(self.tab_6)
        self.txtNodeFileName.setObjectName(u"txtNodeFileName")

        self.gridLayout_8.addWidget(self.txtNodeFileName, 0, 1, 1, 1)

        self.txtNodeCategory = QLineEdit(self.tab_6)
        self.txtNodeCategory.setObjectName(u"txtNodeCategory")

        self.gridLayout_8.addWidget(self.txtNodeCategory, 3, 1, 1, 1)

        self.pushButton_23 = QPushButton(self.tab_6)
        self.pushButton_23.setObjectName(u"pushButton_23")
        self.pushButton_23.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_8.addWidget(self.pushButton_23, 1, 2, 1, 1)

        self.txtNodeHeaderColor = QLineEdit(self.tab_6)
        self.txtNodeHeaderColor.setObjectName(u"txtNodeHeaderColor")

        self.gridLayout_8.addWidget(self.txtNodeHeaderColor, 1, 1, 1, 1)

        self.label_6 = QLabel(self.tab_6)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_8.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_7 = QLabel(self.tab_6)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)

        self.pushButton_21 = QPushButton(self.tab_6)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_8.addWidget(self.pushButton_21, 0, 2, 1, 1)

        self.txtNodeKeyWords = QLineEdit(self.tab_6)
        self.txtNodeKeyWords.setObjectName(u"txtNodeKeyWords")

        self.gridLayout_8.addWidget(self.txtNodeKeyWords, 4, 1, 1, 1)

        self.label_8 = QLabel(self.tab_6)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_8.addWidget(self.label_8, 4, 0, 1, 1)

        self.txtNodeDescription = QTextEdit(self.tab_6)
        self.txtNodeDescription.setObjectName(u"txtNodeDescription")
        self.txtNodeDescription.setMaximumSize(QSize(16777215, 50))

        self.gridLayout_8.addWidget(self.txtNodeDescription, 2, 1, 1, 1)


        self.verticalLayout_23.addLayout(self.gridLayout_8)

        self.label_9 = QLabel(self.tab_6)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_23.addWidget(self.label_9)

        self.tblDefinitions = QTableView(self.tab_6)
        self.tblDefinitions.setObjectName(u"tblDefinitions")

        self.verticalLayout_23.addWidget(self.tblDefinitions)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)

        self.cmdUpOrderNOutputPin_2 = QPushButton(self.tab_6)
        self.cmdUpOrderNOutputPin_2.setObjectName(u"cmdUpOrderNOutputPin_2")
        self.cmdUpOrderNOutputPin_2.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_13.addWidget(self.cmdUpOrderNOutputPin_2)

        self.cmdDownOrderNOutputPin_2 = QPushButton(self.tab_6)
        self.cmdDownOrderNOutputPin_2.setObjectName(u"cmdDownOrderNOutputPin_2")
        self.cmdDownOrderNOutputPin_2.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_13.addWidget(self.cmdDownOrderNOutputPin_2)

        self.cmdAddNOutputPin_2 = QPushButton(self.tab_6)
        self.cmdAddNOutputPin_2.setObjectName(u"cmdAddNOutputPin_2")
        self.cmdAddNOutputPin_2.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_13.addWidget(self.cmdAddNOutputPin_2)

        self.cmdRemoveNOutputPin_2 = QPushButton(self.tab_6)
        self.cmdRemoveNOutputPin_2.setObjectName(u"cmdRemoveNOutputPin_2")
        self.cmdRemoveNOutputPin_2.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_13.addWidget(self.cmdRemoveNOutputPin_2)


        self.verticalLayout_23.addLayout(self.horizontalLayout_13)

        self.tabWidget_4 = QTabWidget(self.tab_6)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_15 = QWidget()
        self.tab_15.setObjectName(u"tab_15")
        self.verticalLayout_14 = QVBoxLayout(self.tab_15)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(-1, -1, 0, -1)
        self.tblNInputPins = QTableView(self.tab_15)
        self.tblNInputPins.setObjectName(u"tblNInputPins")
        self.tblNInputPins.verticalHeader().setVisible(False)

        self.verticalLayout_15.addWidget(self.tblNInputPins)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)

        self.cmdUpOrderNInputPin = QPushButton(self.tab_15)
        self.cmdUpOrderNInputPin.setObjectName(u"cmdUpOrderNInputPin")
        self.cmdUpOrderNInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_10.addWidget(self.cmdUpOrderNInputPin)

        self.cmdDownOrderNInputPin = QPushButton(self.tab_15)
        self.cmdDownOrderNInputPin.setObjectName(u"cmdDownOrderNInputPin")
        self.cmdDownOrderNInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_10.addWidget(self.cmdDownOrderNInputPin)

        self.cmdAddNInputPin = QPushButton(self.tab_15)
        self.cmdAddNInputPin.setObjectName(u"cmdAddNInputPin")
        self.cmdAddNInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_10.addWidget(self.cmdAddNInputPin)

        self.cmdRemoveNInputPin = QPushButton(self.tab_15)
        self.cmdRemoveNInputPin.setObjectName(u"cmdRemoveNInputPin")
        self.cmdRemoveNInputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_10.addWidget(self.cmdRemoveNInputPin)


        self.verticalLayout_15.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_6.addLayout(self.verticalLayout_15)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(-1, -1, 0, -1)
        self.tblNOutputPins = QTableView(self.tab_15)
        self.tblNOutputPins.setObjectName(u"tblNOutputPins")
        self.tblNOutputPins.verticalHeader().setVisible(False)

        self.verticalLayout_16.addWidget(self.tblNOutputPins)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_4)

        self.cmdUpOrderNOutputPin = QPushButton(self.tab_15)
        self.cmdUpOrderNOutputPin.setObjectName(u"cmdUpOrderNOutputPin")
        self.cmdUpOrderNOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_12.addWidget(self.cmdUpOrderNOutputPin)

        self.cmdDownOrderNOutputPin = QPushButton(self.tab_15)
        self.cmdDownOrderNOutputPin.setObjectName(u"cmdDownOrderNOutputPin")
        self.cmdDownOrderNOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_12.addWidget(self.cmdDownOrderNOutputPin)

        self.cmdAddNOutputPin = QPushButton(self.tab_15)
        self.cmdAddNOutputPin.setObjectName(u"cmdAddNOutputPin")
        self.cmdAddNOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_12.addWidget(self.cmdAddNOutputPin)

        self.cmdRemoveNOutputPin = QPushButton(self.tab_15)
        self.cmdRemoveNOutputPin.setObjectName(u"cmdRemoveNOutputPin")
        self.cmdRemoveNOutputPin.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_12.addWidget(self.cmdRemoveNOutputPin)


        self.verticalLayout_16.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_6.addLayout(self.verticalLayout_16)


        self.verticalLayout_14.addLayout(self.horizontalLayout_6)

        self.tabWidget_5 = QTabWidget(self.tab_15)
        self.tabWidget_5.setObjectName(u"tabWidget_5")
        self.tab_16 = QWidget()
        self.tab_16.setObjectName(u"tab_16")
        self.verticalLayout_17 = QVBoxLayout(self.tab_16)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.chkPSConstraint_2 = QCheckBox(self.tab_16)
        self.chkPSConstraint_2.setObjectName(u"chkPSConstraint_2")

        self.gridLayout_5.addWidget(self.chkPSConstraint_2, 2, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.txtPSSupportedDataTypes_2 = QLineEdit(self.tab_16)
        self.txtPSSupportedDataTypes_2.setObjectName(u"txtPSSupportedDataTypes_2")

        self.horizontalLayout_7.addWidget(self.txtPSSupportedDataTypes_2)

        self.pushButton_2 = QPushButton(self.tab_16)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_7.addWidget(self.pushButton_2)


        self.gridLayout_5.addLayout(self.horizontalLayout_7, 0, 1, 1, 1)

        self.chkPSSupportedDataTypes_2 = QCheckBox(self.tab_16)
        self.chkPSSupportedDataTypes_2.setObjectName(u"chkPSSupportedDataTypes_2")

        self.gridLayout_5.addWidget(self.chkPSSupportedDataTypes_2, 0, 0, 1, 1)

        self.chkPSSupportedDataTypes_3 = QCheckBox(self.tab_16)
        self.chkPSSupportedDataTypes_3.setObjectName(u"chkPSSupportedDataTypes_3")

        self.gridLayout_5.addWidget(self.chkPSSupportedDataTypes_3, 1, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.tab_16)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout_5.addWidget(self.comboBox_2, 2, 1, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_4)

        self.tabWidget_5.addTab(self.tab_16, "")

        self.verticalLayout_14.addWidget(self.tabWidget_5)

        self.tabWidget_4.addTab(self.tab_15, "")
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.verticalLayout_22 = QVBoxLayout(self.tab_20)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.txtNodeCode = QTextEdit(self.tab_20)
        self.txtNodeCode.setObjectName(u"txtNodeCode")

        self.verticalLayout_22.addWidget(self.txtNodeCode)

        self.tabWidget_4.addTab(self.tab_20, "")

        self.verticalLayout_23.addWidget(self.tabWidget_4)

        self.twPackage.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.horizontalLayoutWidget_9 = QWidget(self.tab_7)
        self.horizontalLayoutWidget_9.setObjectName(u"horizontalLayoutWidget_9")
        self.horizontalLayoutWidget_9.setGeometry(QRect(-190, 20, 822, 26))
        self.horizontalLayout_35 = QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.pushButton_37 = QPushButton(self.horizontalLayoutWidget_9)
        self.pushButton_37.setObjectName(u"pushButton_37")

        self.horizontalLayout_35.addWidget(self.pushButton_37)

        self.pushButton_38 = QPushButton(self.horizontalLayoutWidget_9)
        self.pushButton_38.setObjectName(u"pushButton_38")

        self.horizontalLayout_35.addWidget(self.pushButton_38)

        self.twPackage.addTab(self.tab_7, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.horizontalLayout_28 = QHBoxLayout(self.tab_9)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.scrollArea = QScrollArea(self.tab_9)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 306, 663))
        self.verticalLayout_39 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.formLayout_12 = QFormLayout()
        self.formLayout_12.setObjectName(u"formLayout_12")
        self.pushButton_13 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.formLayout_12.setWidget(0, QFormLayout.LabelRole, self.pushButton_13)

        self.lineEdit_9 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.formLayout_12.setWidget(0, QFormLayout.FieldRole, self.lineEdit_9)


        self.verticalLayout_39.addLayout(self.formLayout_12)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_39.addItem(self.verticalSpacer_14)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_28.addWidget(self.scrollArea)

        self.tabWidget_8 = QTabWidget(self.tab_9)
        self.tabWidget_8.setObjectName(u"tabWidget_8")
        self.tabWidget_8.setLayoutDirection(Qt.LeftToRight)
        self.tab_29 = QWidget()
        self.tab_29.setObjectName(u"tab_29")
        self.tabWidget_8.addTab(self.tab_29, "")
        self.tab_30 = QWidget()
        self.tab_30.setObjectName(u"tab_30")
        self.tabWidget_8.addTab(self.tab_30, "")
        self.tab_31 = QWidget()
        self.tab_31.setObjectName(u"tab_31")
        self.tabWidget_8.addTab(self.tab_31, "")

        self.horizontalLayout_28.addWidget(self.tabWidget_8)

        self.twPackage.addTab(self.tab_9, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.verticalLayout_10 = QVBoxLayout(self.tab_12)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_39 = QPushButton(self.tab_12)
        self.pushButton_39.setObjectName(u"pushButton_39")

        self.horizontalLayout_36.addWidget(self.pushButton_39)

        self.pushButton_40 = QPushButton(self.tab_12)
        self.pushButton_40.setObjectName(u"pushButton_40")

        self.horizontalLayout_36.addWidget(self.pushButton_40)


        self.verticalLayout_10.addLayout(self.horizontalLayout_36)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_15 = QLabel(self.tab_12)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_6.addWidget(self.label_15, 0, 0, 1, 1)

        self.txtPinDefaultValue = QLineEdit(self.tab_12)
        self.txtPinDefaultValue.setObjectName(u"txtPinDefaultValue")

        self.gridLayout_6.addWidget(self.txtPinDefaultValue, 1, 1, 1, 1)

        self.label_18 = QLabel(self.tab_12)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 2, 0, 1, 1)

        self.chkPinValue = QCheckBox(self.tab_12)
        self.chkPinValue.setObjectName(u"chkPinValue")

        self.gridLayout_6.addWidget(self.chkPinValue, 2, 1, 1, 1)

        self.label_16 = QLabel(self.tab_12)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_6.addWidget(self.label_16, 1, 0, 1, 1)

        self.txtPinName = QLineEdit(self.tab_12)
        self.txtPinName.setObjectName(u"txtPinName")

        self.gridLayout_6.addWidget(self.txtPinName, 0, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.tab_12)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_6.addWidget(self.pushButton_4, 0, 2, 1, 1)

        self.chkExecPin = QCheckBox(self.tab_12)
        self.chkExecPin.setObjectName(u"chkExecPin")

        self.gridLayout_6.addWidget(self.chkExecPin, 3, 1, 1, 1)

        self.label_19 = QLabel(self.tab_12)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 3, 0, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_6)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_12 = QLabel(self.tab_12)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_12)

        self.lstPinSupportedDataType = QListView(self.tab_12)
        self.lstPinSupportedDataType.setObjectName(u"lstPinSupportedDataType")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lstPinSupportedDataType)

        self.tblPinDataTypeHint = QTableView(self.tab_12)
        self.tblPinDataTypeHint.setObjectName(u"tblPinDataTypeHint")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.tblPinDataTypeHint)

        self.label_13 = QLabel(self.tab_12)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_13)


        self.verticalLayout_10.addLayout(self.formLayout)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_14 = QLabel(self.tab_12)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_14)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.spnPinRColor = QSpinBox(self.tab_12)
        self.spnPinRColor.setObjectName(u"spnPinRColor")

        self.horizontalLayout_4.addWidget(self.spnPinRColor)

        self.spnPinGColor = QSpinBox(self.tab_12)
        self.spnPinGColor.setObjectName(u"spnPinGColor")

        self.horizontalLayout_4.addWidget(self.spnPinGColor)

        self.spnPinBColor = QSpinBox(self.tab_12)
        self.spnPinBColor.setObjectName(u"spnPinBColor")

        self.horizontalLayout_4.addWidget(self.spnPinBColor)

        self.spinBox_4 = QSpinBox(self.tab_12)
        self.spinBox_4.setObjectName(u"spinBox_4")

        self.horizontalLayout_4.addWidget(self.spinBox_4)

        self.cmdPinColorPicker = QPushButton(self.tab_12)
        self.cmdPinColorPicker.setObjectName(u"cmdPinColorPicker")

        self.horizontalLayout_4.addWidget(self.cmdPinColorPicker)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_17 = QLabel(self.tab_12)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_17)

        self.comboBox_3 = QComboBox(self.tab_12)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.comboBox_3)


        self.verticalLayout_10.addLayout(self.formLayout_2)

        self.tabWidget_2 = QTabWidget(self.tab_12)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.verticalLayout_18 = QVBoxLayout(self.tab_13)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.txtPinConnect = QTextEdit(self.tab_13)
        self.txtPinConnect.setObjectName(u"txtPinConnect")

        self.verticalLayout_18.addWidget(self.txtPinConnect)

        self.tabWidget_2.addTab(self.tab_13, "")
        self.tab_18 = QWidget()
        self.tab_18.setObjectName(u"tab_18")
        self.verticalLayout_19 = QVBoxLayout(self.tab_18)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.txtPinDisconnect = QTextEdit(self.tab_18)
        self.txtPinDisconnect.setObjectName(u"txtPinDisconnect")

        self.verticalLayout_19.addWidget(self.txtPinDisconnect)

        self.tabWidget_2.addTab(self.tab_18, "")
        self.tab_19 = QWidget()
        self.tab_19.setObjectName(u"tab_19")
        self.verticalLayout_20 = QVBoxLayout(self.tab_19)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.txtPinDisconnect_2 = QTextEdit(self.tab_19)
        self.txtPinDisconnect_2.setObjectName(u"txtPinDisconnect_2")

        self.verticalLayout_20.addWidget(self.txtPinDisconnect_2)

        self.tabWidget_2.addTab(self.tab_19, "")

        self.verticalLayout_10.addWidget(self.tabWidget_2)

        self.twPackage.addTab(self.tab_12, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.horizontalLayoutWidget_12 = QWidget(self.tab_5)
        self.horizontalLayoutWidget_12.setObjectName(u"horizontalLayoutWidget_12")
        self.horizontalLayoutWidget_12.setGeometry(QRect(-200, 20, 822, 26))
        self.horizontalLayout_38 = QHBoxLayout(self.horizontalLayoutWidget_12)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.pushButton_43 = QPushButton(self.horizontalLayoutWidget_12)
        self.pushButton_43.setObjectName(u"pushButton_43")

        self.horizontalLayout_38.addWidget(self.pushButton_43)

        self.pushButton_44 = QPushButton(self.horizontalLayoutWidget_12)
        self.pushButton_44.setObjectName(u"pushButton_44")

        self.horizontalLayout_38.addWidget(self.pushButton_44)

        self.twPackage.addTab(self.tab_5, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_32 = QVBoxLayout(self.tab_8)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.pushButton_5 = QPushButton(self.tab_8)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_20.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.tab_8)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_20.addWidget(self.pushButton_6)

        self.pushButton_8 = QPushButton(self.tab_8)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_20.addWidget(self.pushButton_8)

        self.pushButton_11 = QPushButton(self.tab_8)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_20.addWidget(self.pushButton_11)

        self.pushButton_9 = QPushButton(self.tab_8)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_20.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.tab_8)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_20.addWidget(self.pushButton_10)

        self.pushButton_12 = QPushButton(self.tab_8)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.horizontalLayout_20.addWidget(self.pushButton_12)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_7)


        self.verticalLayout_32.addLayout(self.horizontalLayout_20)

        self.txtCopyright = QPlainTextEdit(self.tab_8)
        self.txtCopyright.setObjectName(u"txtCopyright")
        self.txtCopyright.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_32.addWidget(self.txtCopyright)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer_10)

        self.twPackage.addTab(self.tab_8, "")

        self.verticalLayout_36.addWidget(self.twPackage)


        self.horizontalLayout.addLayout(self.verticalLayout_36)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        self.tabWidget_11.setCurrentIndex(0)
        self.twPackage.setCurrentIndex(2)
        self.tabWidget_9.setCurrentIndex(1)
        self.tabWidget_10.setCurrentIndex(1)
        self.tabWidget_7.setCurrentIndex(0)
        self.stkCommandClassType.setCurrentIndex(2)
        self.tabWidget_6.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(1)
        self.tabWidget_5.setCurrentIndex(0)
        self.tabWidget_8.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.cmdOpenPackageFolder.setText(QCoreApplication.translate("Form", u"...", None))
        self.tabWidget_11.setTabText(self.tabWidget_11.indexOf(self.tab_36), QCoreApplication.translate("Form", u"Programs", None))
        self.cmdLoadPackage.setText(QCoreApplication.translate("Form", u"Load", None))
        self.cmdCreateAppPackage.setText(QCoreApplication.translate("Form", u"Create Package From App", None))
        self.cmdCreateCommand.setText(QCoreApplication.translate("Form", u"Create Command", None))
        self.cmdCreateFunction.setText(QCoreApplication.translate("Form", u"Create Function", None))
        self.cmdCreateNodes.setText(QCoreApplication.translate("Form", u"Create Nodes", None))
        self.cmdCreatePins.setText(QCoreApplication.translate("Form", u"Find Pins", None))
        self.tabWidget_11.setTabText(self.tabWidget_11.indexOf(self.tab_37), QCoreApplication.translate("Form", u"Loaded Functions", None))
        self.cmdUpdateInit.setText(QCoreApplication.translate("Form", u"Update Package", None))
        self.dteCopyrightYear.setDisplayFormat(QCoreApplication.translate("Form", u"yyyy", None))
        self.chkPackageResource.setText(QCoreApplication.translate("Form", u"Resource Folder", None))
        self.chkPackageCommands.setText(QCoreApplication.translate("Form", u"Commands (Output Only)", None))
        self.chkPackageFunctions.setText(QCoreApplication.translate("Form", u"Functions (Package Commands)", None))
        self.chkPackageNodes.setText(QCoreApplication.translate("Form", u"Nodes (I/O Commands)", None))
        self.chkPackageWidgets.setText(QCoreApplication.translate("Form", u"Widgets", None))
        self.chkPackageUI.setText(QCoreApplication.translate("Form", u"UI", None))
        self.chkPackagePins.setText(QCoreApplication.translate("Form", u"Pins", None))
        self.chkPackageTools.setText(QCoreApplication.translate("Form", u"Tools", None))
        self.chkPackageExporters.setText(QCoreApplication.translate("Form", u"Exporters", None))
        self.chkPackageFactories.setText(QCoreApplication.translate("Form", u"Factories", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_32), QCoreApplication.translate("Form", u"Package Folders", None))
        self.cmdCreatePackage.setText(QCoreApplication.translate("Form", u"New", None))
        self.cmdCreatePackage_2.setText(QCoreApplication.translate("Form", u"Create from Existing", None))
        self.cmdCreatePackage_3.setText(QCoreApplication.translate("Form", u"Local", None))
        self.cmdCreatePackage_4.setText(QCoreApplication.translate("Form", u"PyPi", None))
        self.cmdCreatePackage_5.setText(QCoreApplication.translate("Form", u"Anaconda", None))
        self.cmdCreatePackage_6.setText(QCoreApplication.translate("Form", u"ActiveState", None))
        self.cmdCreatePackage_7.setText(QCoreApplication.translate("Form", u"Github", None))
        self.cmdCreatePackage_8.setText(QCoreApplication.translate("Form", u"JFrog", None))
        self.label_30.setText(QCoreApplication.translate("Form", u"Selected Package", None))
        self.label_32.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"Current Revision", None))
        self.label_37.setText(QCoreApplication.translate("Form", u"Revision Date", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"Author", None))
        self.label_38.setText(QCoreApplication.translate("Form", u"Compatibility", None))
        self.tabWidget_10.setTabText(self.tabWidget_10.indexOf(self.tab_28), QCoreApplication.translate("Form", u"Package", None))
        self.label_39.setText(QCoreApplication.translate("Form", u"Selected Function", None))
        self.label_40.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_41.setText(QCoreApplication.translate("Form", u"Inputs", None))
        self.label_42.setText(QCoreApplication.translate("Form", u"Output", None))
        self.tabWidget_10.setTabText(self.tabWidget_10.indexOf(self.tab_34), QCoreApplication.translate("Form", u"Function", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_33), QCoreApplication.translate("Form", u"LinkPackage", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_45), QCoreApplication.translate("Form", u"Package", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"Filename", None))
        self.cmdNewCommand.setText(QCoreApplication.translate("Form", u"New Command", None))
        self.cmdSaveCommand.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.cmdSaveAsCommand.setText(QCoreApplication.translate("Form", u"SaveAs Command", None))
        self.cmdWriteCommand.setText(QCoreApplication.translate("Form", u"Write Command", None))
        self.chkCommandSingleton.setText("")
        self.label_64.setText(QCoreApplication.translate("Form", u"Name", None))
        self.cmbCommandAuthor.setCurrentText(QCoreApplication.translate("Form", u"David James Lario", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Category", None))
        self.label_69.setText(QCoreApplication.translate("Form", u"Author", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"Keywords", None))
        self.label_65.setText(QCoreApplication.translate("Form", u"Singleton", None))
        self.label_34.setText(QCoreApplication.translate("Form", u"Tool Tip", None))
        self.cmdCommandAddShortCut.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_36.setText(QCoreApplication.translate("Form", u"Keyboard ShortCut", None))
        self.rdoCommandDT.setText(QCoreApplication.translate("Form", u"DockTool", None))
        self.rdoCommandST.setText(QCoreApplication.translate("Form", u"ShelfTool", None))
        self.rdoCommandDialog.setText(QCoreApplication.translate("Form", u"Dialog", None))
        self.label_44.setText(QCoreApplication.translate("Form", u"UI File", None))
        self.cmdCommandAddShortCut_4.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_45.setText(QCoreApplication.translate("Form", u"Py File", None))
        self.cmdCommandAddShortCut_6.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_66.setText(QCoreApplication.translate("Form", u"On Show", None))
        self.label_67.setText(QCoreApplication.translate("Form", u"Refresh", None))
        self.label_68.setText(QCoreApplication.translate("Form", u"Default Dock Area", None))
        self.cmdCommandAddShortCut_3.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_70.setText(QCoreApplication.translate("Form", u"UI File", None))
        self.cmdCommandDTCreateUI.setText(QCoreApplication.translate("Form", u"Create", None))
        self.label_28.setText(QCoreApplication.translate("Form", u"ShelfTool", None))
        self.cmdCommandSTCreateUI.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.cmdCommandDialogCreateUI.setText(QCoreApplication.translate("Form", u"Create Dialog", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"Description", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_23), QCoreApplication.translate("Form", u"General", None))
        self.cmdCommandImportSelected.setText(QCoreApplication.translate("Form", u"Add Selected", None))
        self.cmdCommandImportAll.setText(QCoreApplication.translate("Form", u"Add All", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"Editor", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_27), QCoreApplication.translate("Form", u"Imports", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"Small Icon", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"Large Icon", None))
        self.cmdCommandAddLargeIcon.setText("")
        self.label_26.setText(QCoreApplication.translate("Form", u"Medium Icon", None))
        self.cmdCommandAddMediumIcon.setText("")
        self.cmdCommandAddSmallIcon.setText("")
        self.cmdEditSmallIcon.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.cmdEditMediumIcon.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.cmdEditLargeIcon.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.chkCommandResourceFolder.setText(QCoreApplication.translate("Form", u"Resource Folder", None))
        self.cmdFindResourceFolder.setText(QCoreApplication.translate("Form", u"...", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_24), QCoreApplication.translate("Form", u"Icon", None))
        self.cmdCreatePyFlow.setText(QCoreApplication.translate("Form", u"New File", None))
        self.label_35.setText(QCoreApplication.translate("Form", u"Workspace", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_21), QCoreApplication.translate("Form", u"PyFlow", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_26), QCoreApplication.translate("Form", u"Python", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_25), QCoreApplication.translate("Form", u"Additional Coding", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"Revision History", None))
        self.txtCommandAuthor.setText(QCoreApplication.translate("Form", u"David James Lario", None))
        self.cmdAddCommandRevision.setText(QCoreApplication.translate("Form", u"Add Revision", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_22), QCoreApplication.translate("Form", u"Revision", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_4), QCoreApplication.translate("Form", u"Tools", None))
        self.cmdCreateNewFunction_2.setText(QCoreApplication.translate("Form", u"New Function", None))
        self.cmdSaveFunction_2.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.cmdCreateNewFunction.setText(QCoreApplication.translate("Form", u"Create", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Create", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Filename", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Function Name", None))
        self.cmdUpOrderFInputPin.setText(QCoreApplication.translate("Form", u"U", None))
        self.cmdDownOrderFInputPin.setText(QCoreApplication.translate("Form", u"D", None))
        self.cmdAddFInputPin.setText(QCoreApplication.translate("Form", u"+", None))
        self.cmdRemoveFInputPin.setText(QCoreApplication.translate("Form", u"-", None))
        self.cmdUpOrderFOutputPin.setText(QCoreApplication.translate("Form", u"U", None))
        self.cmdDownOrderFOutputPin.setText(QCoreApplication.translate("Form", u"D", None))
        self.cmdAddFOutputPin.setText(QCoreApplication.translate("Form", u"+", None))
        self.cmdRemoveFOutputPin.setText(QCoreApplication.translate("Form", u"-", None))
        self.chkPSInputWidget.setText(QCoreApplication.translate("Form", u"Input Widget Variant", None))
        self.chkPSValueList.setText(QCoreApplication.translate("Form", u"Value List", None))
        self.chkPSDescription.setText(QCoreApplication.translate("Form", u"Description", None))
        self.chkPSSupportedDataTypes.setText(QCoreApplication.translate("Form", u"Supported Data Types", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.chkPSStructConstraint.setText(QCoreApplication.translate("Form", u"Structured Constraint", None))
        self.chkPSDraggerSteps.setText(QCoreApplication.translate("Form", u"Dragger Steps", None))
        self.chkPSValueRange.setText(QCoreApplication.translate("Form", u"Value Range", None))
        self.chkPSDisableOptions.setText(QCoreApplication.translate("Form", u"Disabled Options", None))
        self.chkPSConstraint.setText(QCoreApplication.translate("Form", u"Contraint", None))
        self.chkPSConstraint_3.setText(QCoreApplication.translate("Form", u"Node Type", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Pin Specifiers", None))
        self.chkSupportOnlyArrays.setText(QCoreApplication.translate("Form", u"Supported Only Arrays", None))
        self.chkRenamingEnabled.setText(QCoreApplication.translate("Form", u"Renaming Enabled", None))
        self.chkAllowMultipleConnections.setText(QCoreApplication.translate("Form", u"Allow Multiple Connections", None))
        self.chkDynamic.setText(QCoreApplication.translate("Form", u"Dynamic", None))
        self.chkChangeTypeOnConnection.setText(QCoreApplication.translate("Form", u"Change Type On Connection", None))
        self.chkAllowAny.setText(QCoreApplication.translate("Form", u"Allow Any", None))
        self.chkStorable.setText(QCoreApplication.translate("Form", u"Storable", None))
        self.chkDictionaryElementSupported.setText(QCoreApplication.translate("Form", u"Dictionary Element Supported", None))
        self.chkArraySupported.setText(QCoreApplication.translate("Form", u"Array Supported", None))
        self.chkDictionarySupported.setText(QCoreApplication.translate("Form", u"Dictionary Supported", None))
        self.chkAlwaysPushDirty.setText(QCoreApplication.translate("Form", u"Always Push Dirty", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pinOptions), QCoreApplication.translate("Form", u"Pin Options", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_35), QCoreApplication.translate("Form", u"Definition", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_14), QCoreApplication.translate("Form", u"Pins", None))
        self.label.setText(QCoreApplication.translate("Form", u"Category", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Keywords", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Cache Enabled", None))
        self.chkMetaCacheEnabled.setText("")
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_17), QCoreApplication.translate("Form", u"Meta", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Implement", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("Form", u"Definition", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), QCoreApplication.translate("Form", u"Code", None))
        self.cmdSaveFunction.setText(QCoreApplication.translate("Form", u"Save", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Functions", None))
        self.pushButton_35.setText(QCoreApplication.translate("Form", u"New Command", None))
        self.pushButton_36.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Category", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Description", None))
        self.pushButton_23.setText(QCoreApplication.translate("Form", u"Header Color", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Header", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Filename", None))
        self.pushButton_21.setText(QCoreApplication.translate("Form", u"New File", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Key Words", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Definition Order", None))
        self.cmdUpOrderNOutputPin_2.setText(QCoreApplication.translate("Form", u"U", None))
        self.cmdDownOrderNOutputPin_2.setText(QCoreApplication.translate("Form", u"D", None))
        self.cmdAddNOutputPin_2.setText(QCoreApplication.translate("Form", u"+", None))
        self.cmdRemoveNOutputPin_2.setText(QCoreApplication.translate("Form", u"-", None))
        self.cmdUpOrderNInputPin.setText(QCoreApplication.translate("Form", u"U", None))
        self.cmdDownOrderNInputPin.setText(QCoreApplication.translate("Form", u"D", None))
        self.cmdAddNInputPin.setText(QCoreApplication.translate("Form", u"+", None))
        self.cmdRemoveNInputPin.setText(QCoreApplication.translate("Form", u"-", None))
        self.cmdUpOrderNOutputPin.setText(QCoreApplication.translate("Form", u"U", None))
        self.cmdDownOrderNOutputPin.setText(QCoreApplication.translate("Form", u"D", None))
        self.cmdAddNOutputPin.setText(QCoreApplication.translate("Form", u"+", None))
        self.cmdRemoveNOutputPin.setText(QCoreApplication.translate("Form", u"-", None))
        self.chkPSConstraint_2.setText(QCoreApplication.translate("Form", u"Input Structure", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"...", None))
        self.chkPSSupportedDataTypes_2.setText(QCoreApplication.translate("Form", u"Data Types", None))
        self.chkPSSupportedDataTypes_3.setText(QCoreApplication.translate("Form", u"Add Type Hint", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_16), QCoreApplication.translate("Form", u"Pin Options", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_15), QCoreApplication.translate("Form", u"Pins", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_20), QCoreApplication.translate("Form", u"Code", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_6), QCoreApplication.translate("Form", u"Nodes", None))
        self.pushButton_37.setText(QCoreApplication.translate("Form", u"New Command", None))
        self.pushButton_38.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_7), QCoreApplication.translate("Form", u"Widgets", None))
        self.pushButton_13.setText(QCoreApplication.translate("Form", u"Command", None))
        self.lineEdit_9.setText(QCoreApplication.translate("Form", u"Description", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_29), QCoreApplication.translate("Form", u"Menu Bar", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_30), QCoreApplication.translate("Form", u"Ribbon Bar", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_31), QCoreApplication.translate("Form", u"Tool Bar", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_9), QCoreApplication.translate("Form", u"UI", None))
        self.pushButton_39.setText(QCoreApplication.translate("Form", u"New Command", None))
        self.pushButton_40.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"Value Pin", None))
        self.chkPinValue.setText("")
        self.label_16.setText(QCoreApplication.translate("Form", u"Default Value", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"New", None))
        self.chkExecPin.setText("")
        self.label_19.setText(QCoreApplication.translate("Form", u"Exec Pin", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Supported Datatype", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Pin Data Type Hint", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Color", None))
        self.cmdPinColorPicker.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"Default Value", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_13), QCoreApplication.translate("Form", u"Pin Connect", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_18), QCoreApplication.translate("Form", u"Pin Disconnect", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_19), QCoreApplication.translate("Form", u"Process Data", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_12), QCoreApplication.translate("Form", u"Pins", None))
        self.pushButton_43.setText(QCoreApplication.translate("Form", u"New Command", None))
        self.pushButton_44.setText(QCoreApplication.translate("Form", u"Save Command", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_5), QCoreApplication.translate("Form", u"Factories", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Apache", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"MIT", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"GNU General", None))
        self.pushButton_11.setText(QCoreApplication.translate("Form", u"GNU Lesser", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"BSD", None))
        self.pushButton_10.setText(QCoreApplication.translate("Form", u"Mozilla", None))
        self.pushButton_12.setText(QCoreApplication.translate("Form", u"Creative Commons", None))
        self.txtCopyright.setPlainText(QCoreApplication.translate("Form", u"## Licensed under the Apache License, Version 2.0 (the \"License\");\n"
"## you may not use this file except in compliance with the License.\n"
"## You may obtain a copy of the License at\n"
"\n"
"##     http://www.apache.org/licenses/LICENSE-2.0\n"
"\n"
"## Unless required by applicable law or agreed to in writing, software\n"
"## distributed under the License is distributed on an \"AS IS\" BASIS,\n"
"## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
"## See the License for the specific language governing permissions and\n"
"## limitations under the License.", None))
        self.twPackage.setTabText(self.twPackage.indexOf(self.tab_8), QCoreApplication.translate("Form", u"Author", None))
    # retranslateUi

