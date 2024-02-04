## Copyright 2023 David Lario
__author__ = 'David Lario'
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created


from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


from PackageManager.Packages.ProgramBase.Commands import RESOURCES_DIR
from PackageManager.UI.Commands.Command import DockTool
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget
class HeadButton(QtWidgets.QPushButton):
    """docstring for HeadButton."""
    def __init__(self, parent=None, maxHeight=25):
        super(HeadButton, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setDefault(True)
        self.setMaximumHeight(maxHeight)

class ToolBar(DockTool):
    """docstring for Properties tool."""
    def __init__(self):
        super(ToolBar, self).__init__()
        self.TabWidget = QtWidgets.QTabWidget(self)
        #self.scrollArea.setWidgetResizable(True)
        #https://www.tutorialspoint.com/pyqt/pyqt_qtabwidget.htm

        self.tab1 = QtWidgets.QScrollArea(self)
        self.tab2 = QtWidgets.QScrollArea(self)
        self.tab3 = QtWidgets.QScrollArea(self)

        self.TabWidget.addTab(self.tab1, "Tab 1")
        self.TabWidget.addTab(self.tab2, "Tab 2")
        self.TabWidget.addTab(self.tab3, "Tab 3")
        self.TabWidget.setTabText(0, "Project Manager")
        self.TabWidget.setTabText(1, "PyFlow")
        self.TabWidget.setTabText(2, "Timesheet")
        self.TabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.setWidget(self.TabWidget)
        self.setFixedHeight(100)
        self.tab1UI()

        '''self.propertiesWidget.searchBoxLayout.removeWidget(self.propertiesWidget.lockCheckBox)
        self.addButton(self.propertiesWidget.lockCheckBox)
        self.propertiesWidget.searchBoxLayout.removeWidget(self.propertiesWidget.tearOffCopy)
        self.addButton(self.propertiesWidget.tearOffCopy)'''
        # self.addButton(self.propertiesWidget.settingsButton)

        #self.setWindowTitle(self.uniqueName())
        self.fillDelegate = None

    def tab1UI(self):
        self.resize(400, 300)
        self.mainHLayout = QtWidgets.QHBoxLayout(self)
        self.mainHLayout.setSpacing(2)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.setObjectName("mainHLayout")
        self.mainHLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.pbHead = QtWidgets.QPushButton(self)
        self.pbHead.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead.setFixedSize(50, 50)
        self.mainHLayout.addWidget(self.pbHead)
        self.pbHead2 = QtWidgets.QPushButton(self)
        self.pbHead2.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead2.setFixedSize(50, 50)
        #self.pbHead2.setIcon(QIcon(QPixmap("python.gif")))
        self.mainHLayout.addWidget(self.pbHead2)
        #self.setMinimumHeight(30)

        self.mainGLayout = QtWidgets.QGridLayout(self)
        self.pbHead3 = QtWidgets.QPushButton(self)
        self.pbHead3.setFixedSize(22, 22)
        self.pbHead3.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead4 = QtWidgets.QPushButton(self)
        self.pbHead4.setFixedSize(22, 22)
        self.pbHead4.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead5 = QtWidgets.QPushButton(self)
        self.pbHead5.setFixedSize(22, 22)
        self.pbHead5.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead6 = QtWidgets.QPushButton(self)
        self.pbHead6.setFixedSize(22, 22)
        self.pbHead6.setIcon(QtGui.QIcon(RESOURCES_DIR + "history.png"))
        self.pbHead7 = QtWidgets.QComboBox(self)
        self.pbHead7.setFixedSize(150, 22)

        self.mainGLayout.addWidget(self.pbHead3, 1, 1)
        self.mainGLayout.addWidget(self.pbHead4, 1, 2)
        self.mainGLayout.addWidget(self.pbHead5, 2, 1)
        self.mainGLayout.addWidget(self.pbHead6, 2, 2)
        self.mainGLayout.addWidget(self.pbHead7, 1, 3)
        self.mainGLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.addLayout(self.mainGLayout)

        self.ContentWidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContentWidget.sizePolicy().hasHeightForWidth())
        self.ContentWidget.setSizePolicy(sizePolicy)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))

        self.ContentWidget.setObjectName("ContentWidget")
        self.ContentWidget.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.addWidget(self.ContentWidget)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainHLayout.addItem(self.spacerItem)
        #self.setWindowTitle(self.objectName())

        self.pbHead.setStyleSheet(self.pbHead.styleSheet() + "\nText-align:left;")
        self.contentHiddenIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_TitleBarUnshadeButton)
        self.contentVisibleIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_TitleBarShadeButton)
        #self.setTabText(0,"Contact Details")
        self.tab1.setLayout(self.mainHLayout)

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def toolTip():
        return "Tool Bar"

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.TopDockWidgetArea

    @staticmethod
    def name():
        return str("ToolBar")

    def do(self):
        self.ProgramManagerInstance.invokeDockToolByName(self.packageName, "Tool Bar")