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


from PySide6.QtWidgets import QScrollArea

from PackageManager.UI.Commands.Command import DockTool
from PackageManager.UI.Widgets.SearchandAutomation import *

class SearchResultsTool(DockTool):
    """docstring for NodeBox tool."""
    def __init__(self):
        super(SearchResultsTool, self).__init__()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.setWidget(self.scrollArea)
        self.searchandAutomationWidget = SearchandAutomationWidget()
        self.scrollArea.setWidget(self.searchandAutomationWidget)

        self.searchandAutomationWidget.searchBoxLayout.removeWidget(self.searchandAutomationWidget.lockCheckBox)
        self.addButton(self.searchandAutomationWidget.lockCheckBox)
        self.searchandAutomationWidget.searchBoxLayout.removeWidget(self.searchandAutomationWidget.tearOffCopy)
        self.addButton(self.searchandAutomationWidget.tearOffCopy)
        # self.addButton(self.propertiesWidget.settingsButton)

        self.setWindowTitle(self.uniqueName())
        self.fillDelegate = None
        self.searchandAutomationWidget.spawnDuplicate.connect(self.onTearOffCopy)


    def onTearOffCopy(self, *args, **kwargs):
        instance = self.ProgramManagerInstance.invokeDockToolByName("ProgramBase", self.name())
        if self.fillDelegate is not None:
            instance.assignsearchandAutomationWidget(self.fillDelegate)
        instance.setFloating(True)
        instance.resize(self.size())

    def clear(self):
        self.searchandAutomationWidget.clear()

    def assignsearchandAutomationWidget(self, propertiesFillDelegate):
        self.fillDelegate = propertiesFillDelegate
        propertiesFillDelegate(self.searchandAutomationWidget)

    @staticmethod
    def isSingleton():
        return False

    @staticmethod
    def toolTip():
        return "Searching and Automation"

    @staticmethod
    def name():
        return str("SearchandAutomation")

    def do(self):
        self.ProgramManagerInstance.invokeDockToolByName(self.packageName, "SearchResults")
