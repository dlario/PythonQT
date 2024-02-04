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
from PySide6.QtWidgets import *

from PackageManager.Packages.PyFlow.Commands import RESOURCES_DIR
from PackageManager.UI.Commands.Command import DockTool
from PyFlow.UI.Widgets.PropertiesFramework import *


class SearchResultsTool(DockTool):
    """docstring for NodeBox tool."""
    def __init__(self):
        super(SearchResultsTool, self).__init__()
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.content = PropertiesWidget()
        self.content.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionClear = QAction("Clear", None)
        self.actionClear.triggered.connect(self.content.clear)
        self.content.addAction(self.actionClear)

        self.content.setSearchBoxVisible(False)
        self.content.setLockCheckBoxVisible(False)
        self.content.setTearOffCopyVisible(False)

        self.content.setObjectName("SearchResultstent")
        self.scrollArea.setWidget(self.content)
        self.setWindowTitle(self.uniqueName())
        self.setWidget(self.scrollArea)

    def onShowNodesResults(self, uiNodesList):
        self.content.clear()
        category = CollapsibleFormWidget(headName="Results")
        category.setSpacing(0)
        '''for node in uiNodesList:
            locationString = ">".join(node.location())
            btn = QPushButton(locationString)
            btn.clicked.connect(lambda checked=False, n=node: self.ProgramManagerInstance.getCanvas().frameItems([n]))
            category.addWidget(node.getName(), btn)
        self.content.addWidget(category)'''

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.BottomDockWidgetArea

    def onShow(self):
        super(SearchResultsTool, self).onShow()
        print("show")

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def name():
        return str("Search results")