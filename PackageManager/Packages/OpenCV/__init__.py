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

"""Base package
"""
from PackageManager.Packages.OpenCV.Resources import RESOURCES_DIR, ICON_DIR

PACKAGE_NAME = 'OpenCV'

from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage
from PackageManager.Packages.OpenCV import AppMDI
from PackageManager.Packages.ProgramBase.UI.DockWindows.RibbonBar import RibbonBar

from PackageManager.Packages.ProgramBase.UI.DockWindows.HistoryTool import HistoryTool
from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool
from PackageManager.Packages.ProgramBase.Commands.Preferences import Preferences

# [Imports]
from PackageManager.Packages.OpenCV.Commands.NewFile import NewFile
from PackageManager.Packages.OpenCV.Commands.SaveFile import SaveFile
from PackageManager.Packages.OpenCV.Commands.OpenFile import OpenFile
from PackageManager.Packages.OpenCV.Commands.CloseFile import CloseFile
from PackageManager.Packages.OpenCV.Commands.LoadForm import LoadForm

from PackageManager.Packages.OpenCV.Commands.LoadDefaultData import LoadDefaultData
from PackageManager.Packages.OpenCV.Commands.DropTables import DropTables

from PackageManager.Packages.OpenCV.Commands.About import About
from PackageManager.Packages.OpenCV.Commands.HomePage import HomePage

# from PackageManager.Packages.ProgramBase.UI.DockWindows.SearchResultsTool import SearchResultsTool

# [Prefs widgets]
from PackageManager.Packages.OpenCV.PrefsWidgets.General import GeneralPreferences
from PackageManager.Packages.OpenCV.PrefsWidgets.InputPrefs import InputPreferences

# [Commands]
_COMMANDS = OrderedDict()
_COMMANDS[NewFile.__name__] = NewFile
_COMMANDS[SaveFile.__name__] = SaveFile
_COMMANDS[OpenFile.__name__] = OpenFile
_COMMANDS[CloseFile.__name__] = CloseFile
_COMMANDS[LoadForm.__name__] = LoadForm
_COMMANDS[About.__name__] = About
_COMMANDS[HomePage.__name__] = HomePage

_COMMANDS[LoadDefaultData.__name__] = LoadDefaultData
_COMMANDS[DropTables.__name__] = DropTables

_COMMANDS[RibbonBar.__name__] = RibbonBar
_COMMANDS[HistoryTool.__name__] = HistoryTool
_COMMANDS[PropertiesTool.__name__] = PropertiesTool
_COMMANDS[Preferences.__name__] = Preferences

# [Exporters]
_EXPORTERS = OrderedDict()

# [Bases]
_BASES = OrderedDict()
# from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase

# [Tables]
_TABLES = OrderedDict()
# from PackageManager.Database.dbAllLists import *

# [Preferred Widgets]
_PREFS_WIDGETS = OrderedDict()
_PREFS_WIDGETS["OpenCV - General"] = GeneralPreferences
_PREFS_WIDGETS["OpenCV - Input"] = InputPreferences

_FOO_LIBS = {
}

_NODES = {
}

_PINS = {
}


# [Base Package]
class OpenCV(IPackage):
    """Base PackageManager package
    """

    def __init__(self, Parent):
        super(OpenCV, self).__init__()
        self.parent = Parent

    @staticmethod
    def CreateInstance(main, parent=None):
        return AppMDI.MDIMain.NewInstance(main, parent)

    @staticmethod
    def GetBases():
        return _BASES

    @staticmethod
    def GetTables():
        return _TABLES

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetCommandClasses():
        return _COMMANDS

    @staticmethod
    def GetPreferences():
        return _PREFS_WIDGETS

    @staticmethod
    def GetIcon():
        return ICON_DIR + "ProgramLogo.png"

    @staticmethod
    def GetSmallIcon():
        return ICON_DIR + "ProgramLogo - Small.png"

    @staticmethod
    def GetMediumIcon():
        return ICON_DIR + "ProgramLogo - Medium.png"

    @staticmethod
    def GetLargeIcon():
        return ICON_DIR + "ProgramLogo - Large.png"

    @staticmethod
    def GetDefaultMenuOrder():
        menuOrder = ["File", "Edit", "Tools", "Windows", "Help"]
        return menuOrder

    @staticmethod
    def GetDefaultMenuLayout():
        menuDict = {}
        separatorCount = 0

        fileMenuList = []
        fileMenuList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "NewFile"})
        fileMenuList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "OpenFile"})
        menuDict["File"] = fileMenuList

        editToolList = []
        # editToolList.append({"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "CommandBuilder"})
        editToolList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "History"})
        editToolList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "Properties"})
        editToolList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "SearchResults"})
        menuDict["Tools"] = editToolList

        helpMenuList = []
        helpMenuList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "About"})
        helpMenuList.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "HomePage"})
        menuDict["Help"] = helpMenuList

        return menuDict

    @staticmethod
    def GetDefaultRibbonOrder():
        ribbonOrder = ["Home", "Tools", "Data", "View", "DatabaseTools", "Help"]
        return ribbonOrder

    @staticmethod
    def GetDefaultRibbonLayout():
        barDict = {}
        itemDict = {}
        itemList = []

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'newFile - Small.png',
                         'mediumIconLocation': ICON_DIR + 'newFile - Medium.png',
                         'largeIconLocation': ICON_DIR + 'newFile - Large.png', 'Action': 'Add Action',
                         'Package': 'OpenCV', 'PackageGroup': 'OpenCV', 'Command': 'NewFile',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'New File',
                         'ShowName': False, 'ToolTip': 'New File', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'openFile - Small.png',
                         'mediumIconLocation': ICON_DIR + 'openFile - Medium.png',
                         'largeIconLocation': ICON_DIR + 'openFile - Large.png', 'Action': 'Add Action',
                         'Package': 'OpenCV', 'PackageGroup': 'OpenCV', 'Command': 'OpenFile',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'Open File',
                         'ShowName': False, 'ToolTip': 'Open File', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'saveFile - Small.png',
                         'mediumIconLocation': ICON_DIR + 'saveFile - Medium.png',
                         'largeIconLocation': ICON_DIR + 'saveFile - Large.png', 'Action': 'Add Action',
                         'Package': 'OpenCV', 'PackageGroup': 'OpenCV', 'Command': 'SaveFile',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'Save File',
                         'ShowName': False, 'ToolTip': 'Save File', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'form - Small.png',
                         'mediumIconLocation': ICON_DIR + 'form - Medium.png',
                         'largeIconLocation': ICON_DIR + 'form - Large.png', 'Action': 'Add Action',
                         'Package': 'OpenCV', 'PackageGroup': 'OpenCV', 'Command': 'LoadForm',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'Load Form',
                         'ShowName': False, 'ToolTip': 'Load Form', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})


        itemDict["File"] = itemList

        itemList = []
        itemList.append({'Bar': 'DatabaseTool', 'Section': 'Commands', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'construction - Small.png',
                         'mediumIconLocation': ICON_DIR + 'construction - Medium.png',
                         'largeIconLocation': ICON_DIR + 'construction - Large.png', 'Action': 'Add Action',
                         'Package': 'OpenCV', 'PackageGroup': 'OpenCV', 'Command': 'LoadDefaultData',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'Test 3',
                         'ShowName': False, 'ToolTip': 'New Project', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemList.append({'Bar': 'DatabaseTool', 'Section': 'Commands', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'construction - Small.png',
                         'mediumIconLocation': ICON_DIR + 'construction - Medium.png',
                         'largeIconLocation': ICON_DIR + 'construction - Large.png', 'Action': 'Add Action',
                         'Package': 'ProjectList', 'PackageGroup': 'OpenCV', 'Command': 'DropTables', 'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'Test 3',
                         'ShowName': False, 'ToolTip': 'New Project', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        barDict["DatabaseTool"] = itemDict

        return barDict

    @staticmethod
    def GetDefaultToolBarLayout():
        toolBarDict = {}
        ToolBar = []
        ToolBar.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "NewFile"})
        ToolBar.append(
            {"Action": "Add Action", "Package": "OpenCV", "PackageGroup": "OpenCV", "Command": "OpenFile"})
        toolBarDict["File"] = ToolBar

        return toolBarDict
