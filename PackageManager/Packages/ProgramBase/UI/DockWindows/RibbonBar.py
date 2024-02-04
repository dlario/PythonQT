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
#from PackageManager.UI.CommandRegister import RibbonRegister

from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget
from pyqtribbon import RibbonBar as qtRibbonBar

class HeadButton(QtWidgets.QPushButton):
    """docstring for HeadButton."""
    def __init__(self, parent=None, maxHeight=25):
        super(HeadButton, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setDefault(True)
        self.setMaximumHeight(maxHeight)

class RibbonBar(DockTool):
    """docstring for Properties tool."""

    def __init__(self):
        super(RibbonBar, self).__init__()
        self.ribbonBar = qtRibbonBar()
        self.setWidget(self.ribbonBar)
        self.setTitleBarWidget(QtWidgets.QWidget(None))

        #self.ribbonBar = qtRibbonBar()
        self.ribbonDict = {}
        self.ribbonCategoryDict = {}
        self.ribbonCategory = {}

    def setIcon(self, icon):
        self.ribbonBar.setApplicationIcon(icon)
        self.ribbonBar.setWhatsThis("Tests2")
        self.ribbonBar.setTitle("test")

    def addCategory(self, categoryname):
        if categoryname not in self.ribbonCategory:
            self.ribbonCategory[categoryname] = ribbonCategory(self.ribbonBar, categoryname)
        return self.ribbonCategory[categoryname]
    def addPanel(self, categoryname, panelname):
        category = self.ribbonCategory[categoryname]
        if panelname not in category.panelDict:
            panel = category.createPanel(panelname)
        return panel

    def addAction(self, categoryname, panelname, ribbonitem, actionitem):
        category = self.ribbonCategory[categoryname]
        panel = category.panelDict[panelname]
        if ribbonitem["Command"] not in panel.actionDict:
            panel.addAction(ribbonitem, actionitem)

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def toolTip():
        return "Ribbon Bar"

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.TopDockWidgetArea

    @staticmethod
    def name():
        return str("RibbonBar")

    def do(self):
        self.ProgramManagerInstance.invokeDockToolByName("Ribbon Bar")
class ribbonCategory(object):
    def __init__(self, ribbon, title):
        self.ribbon = ribbon
        self.name = title
        self.panelDict = {}
        self.ribbonCategory = ribbon.addCategory(title)

    def getribbonCategory(self):
        return self.ribbonCategory

    def getribbonPanel(self, PanelName):
        return self.panelDict[PanelName]

    def getpanelDict(self):
        return self.panelDict

    def createPanel(self, panelname):
        if panelname not in self.panelDict:
            showoptionbutton = False
            self.panelDict[panelname] = RibbonPanel(self.ribbon, self.ribbonCategory, panelname, showoptionbutton)
        return self.panelDict[panelname]
class RibbonPanel(object):
    def __init__(self, ribbon, ribboncategory, title, showoptionbutton=False):
        self.name = title
        self.ribbonCategory = ribboncategory
        self.ribbonPanel = ribboncategory.addPanel(title, showPanelOptionButton=showoptionbutton)
        self.actionDict = {}
        self.ribbon = ribbon

    def addAction(self, ribbondict, ribbonAction):
        if ribbondict["Command"] not in self.actionDict:
            if ribbonAction:
                rslot = ribbonAction.handler
            else:
                rslot = None

            if ribbondict["Widget"] == "Button":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel.addButton(
                    icon=ribbonAction.smallIconLocation,
                    text=ribbondict["Command"],  # ribbonAction.text,
                    showText=False,
                    slot=rslot,
                    shortcut=ribbonAction.shortcut(),
                    statusTip=ribbonAction.statusTip(),
                    checkable=False,
                    rowSpan=1)


            if ribbondict["Widget"] == "Small Button":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel\
                    .addSmallButton(text=ribbondict["Command"],
                                    slot=rslot,
                                    icon=QtGui.QIcon(ribbondict["smallIconLocation"]))

            if ribbondict["Widget"] == "Medium Button":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel\
                    .addLargeButton(text=ribbondict["Command"],
                                    slot=rslot,
                                    icon=QtGui.QIcon(ribbondict["mediumIconLocation"]))
                self.actionDict[ribbondict["Command"]].addAction(ribbonAction)

            if ribbondict["Widget"] == "Large Button":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel\
                    .addLargeButton(text=ribbondict["Command"],
                                    slot=rslot,
                                    icon=QtGui.QIcon(ribbondict["largeIconLocation"]))
                self.actionDict[ribbondict["Command"]].addAction(ribbonAction)

            if ribbondict["Widget"] == "Small Toggle":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel.addSmallToggleButton(full=False,
                                                                                               icon=ribbonAction.smallIconLocation,
                                                                                               text=ribbondict[
                                                                                                   "Command"],
                                                                                               # ribbonAction.text,
                                                                                               slot=ribbonAction.handler,
                                                                                               shortcut=ribbonAction.shortcut,
                                                                                               statusTip=ribbonAction.statusTip)

            if ribbondict["Widget"] == "Medium Toggle":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel.addMediumToggleButton(full=False,
                                                                                                icon=ribbonAction.smallIconLocation,
                                                                                                text=ribbondict[
                                                                                                    "Command"],
                                                                                                # ribbonAction.text,
                                                                                                slot=ribbonAction.handler,
                                                                                                shortcut=ribbonAction.shortcut,
                                                                                                statusTip=ribbonAction.statusTip)

            if ribbondict["Widget"] == "Large Toggle":
                self.actionDict[ribbondict["Command"]] = self.ribbonPanel.addLargeToggleButton(full=False,
                                                                                               icon=ribbonAction.largeIconLocation,
                                                                                               text=ribbondict[
                                                                                                   "Command"],
                                                                                               # ribbonAction.text,
                                                                                               slot=ribbonAction.handler,
                                                                                               shortcut=ribbonAction.shortcut,
                                                                                               statusTip=ribbonAction.statusTip)
            '''
            https://pyqtribbon.haiiliin.com/en/stable/user.html#customize-panels
            addWidget
            addComboBox
            addFontComboBox
            addLineEdit
            addTextEdit
            addPlainTextEdit
            addLabel
            addProgressBar
            addSlider
            addSpinBox
            addDoubleSpinBox
            addDateEdit
            addTimeEdit
            addDateTimeEdit
            addTableWidget
            addTreeWidget
            addListWidget
            addCalendarWidget
            addGallery

            addSeparator
            addHorizontalSeparator
            addVerticalSeparator
          
            except:
                print("Error")
                print("RibbondDict", ribbondict)
                print("Ribbon Action", ribbonAction)  '''



