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
from PackageManager.Packages.XFiles.Resources import RESOURCES_DIR, ICON_DIR

PACKAGE_NAME = 'XFiles'

from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage
from PackageManager.Packages.XFiles import AppMDI
from PackageManager.Packages.ProgramBase.UI.DockWindows.RibbonBar import RibbonBar

from PackageManager.Packages.ProgramBase.UI.DockWindows.HistoryTool import HistoryTool
from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool
from PackageManager.Packages.ProgramBase.Commands.Preferences import Preferences

# [Imports]
from PackageManager.Packages.XFiles.Commands.NewFile import NewFile
from PackageManager.Packages.XFiles.Commands.SaveFile import SaveFile
from PackageManager.Packages.XFiles.Commands.OpenFile import OpenFile
from PackageManager.Packages.XFiles.Commands.CloseFile import CloseFile

from PackageManager.Packages.XFiles.Commands.About import About
from PackageManager.Packages.XFiles.Commands.HomePage import HomePage

from PackageManager.Packages.XFiles.Commands.ChatGPT import ChatGPT
try:
    from PackageManager.Packages.XFiles.Commands.WhatsApp import WhatsApp
    loadWhatsApp = True
except:
    loadWhatsApp = False
# from PackageManager.Packages.ProgramBase.UI.DockWindows.SearchResultsTool import SearchResultsTool

# [Prefs widgets]
from PackageManager.Packages.XFiles.PrefsWidgets.General import GeneralPreferences
from PackageManager.Packages.XFiles.PrefsWidgets.InputPrefs import InputPreferences

# [Commands]
_COMMANDS = OrderedDict()
_COMMANDS[NewFile.__name__] = NewFile
_COMMANDS[SaveFile.__name__] = SaveFile
_COMMANDS[OpenFile.__name__] = OpenFile
_COMMANDS[CloseFile.__name__] = CloseFile
_COMMANDS[About.__name__] = About
_COMMANDS[HomePage.__name__] = HomePage
_COMMANDS[ChatGPT.__name__] = ChatGPT

if loadWhatsApp == True:
    _COMMANDS[WhatsApp.__name__] = WhatsApp

_COMMANDS[RibbonBar.__name__] = RibbonBar
_COMMANDS[HistoryTool.__name__] = HistoryTool
_COMMANDS[PropertiesTool.__name__] = PropertiesTool
_COMMANDS[Preferences.__name__] = Preferences

# [Exporters]
_EXPORTERS = OrderedDict()

# [Bases]
_BASES = OrderedDict()
# from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase
_BASES = OrderedDict()
# _BASES["MainBase"] = MainBase

# [Tables]
_TABLES = OrderedDict()
# from PackageManager.Database.dbAllLists import *

# [Preferred Widgets]
_PREFS_WIDGETS = OrderedDict()
_PREFS_WIDGETS["XFiles - General"] = GeneralPreferences
_PREFS_WIDGETS["XFiles - Inputs"] = InputPreferences

_FOO_LIBS = {
}

_NODES = {
}

_PINS = {
}


# [Base Package]
class XFiles(IPackage):
    """Base PackageManager package
    """

    def __init__(self, Parent):
        super(XFiles, self).__init__()
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
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "NewFile"})
        fileMenuList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "OpenFile"})
        menuDict["File"] = fileMenuList

        editToolList = []
        # editToolList.append({"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "CommandBuilder"})
        editToolList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "History"})
        editToolList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "Properties"})
        editToolList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "SearchResults"})
        menuDict["Tools"] = editToolList

        helpMenuList = []
        helpMenuList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "About"})
        helpMenuList.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "HomePage"})
        menuDict["Help"] = helpMenuList

        return menuDict

    @staticmethod
    def GetDefaultRibbonOrder():
        ribbonOrder = ["Home"]
        return ribbonOrder

    @staticmethod
    def GetDefaultRibbonLayout():
        barDict = {}
        itemDict = {}
        itemList = []

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'ChatGPT4All.jpeg',
                         'mediumIconLocation': ICON_DIR + 'ChatGPT4All.jpeg',
                         'largeIconLocation': ICON_DIR + 'ChatGPT4All.jpeg', 'Action': 'Add Action',
                         'Package': 'XFiles', 'PackageGroup': 'XFiles', 'Command': 'ChatGPT',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'New File',
                         'ShowName': False, 'ToolTip': 'New File', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemList.append({'Bar': 'Home', 'Section': 'File', 'Widget': 'Large Button',
                         'smallIconLocation': ICON_DIR + 'WhatsApp.png',
                         'mediumIconLocation': ICON_DIR + 'WhatsApp.png',
                         'largeIconLocation': ICON_DIR + 'WhatsApp.png', 'Action': 'Add Action',
                         'Package': 'XFiles', 'PackageGroup': 'XFiles', 'Command': 'WhatsApp',
                         'Order': 1,
                         'StartPosition': (1, 1), 'Fixity': 'Order', 'WidgetSize': (1, 1), 'DisplayName': 'New File',
                         'ShowName': False, 'ToolTip': 'New File', 'IsActive': True, 'MainVisible': True,
                         'InstanceVisible': True})

        itemDict["File"] = itemList

        barDict["Home"] = itemDict

        return barDict

    @staticmethod
    def GetDefaultToolBarLayout():
        toolBarDict = {}
        ToolBar = []
        ToolBar.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "NewFile"})
        ToolBar.append(
            {"Action": "Add Action", "Package": "XFiles", "PackageGroup": "XFiles", "Command": "OpenFile"})
        toolBarDict["File"] = ToolBar

        return toolBarDict
