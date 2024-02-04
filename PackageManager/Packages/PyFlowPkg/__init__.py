PACKAGE_NAME = 'PyFlow'
"""Base package
"""
from PackageManager.Packages.PyFlowPkg.Resources import ICON_DIR
from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage
from PyFlow import AppMDI

# Pins
from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyFlowBase.Pins.BoolPin import BoolPin
from PyFlow.Packages.PyFlowBase.Pins.ExecPin import ExecPin
from PyFlow.Packages.PyFlowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyFlowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyFlowBase.Pins.StringPin import StringPin

# Function based nodes
from PyFlow.Packages.PyFlowBase.FunctionLibraries.ArrayLib import ArrayLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.MathAbstractLib import MathAbstractLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.RandomLib import RandomLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.PathLib import PathLib

# Class based nodes
from PyFlow.Packages.PyFlowBase.Nodes.branch import branch
from PyFlow.Packages.PyFlowBase.Nodes.tick import tick
from PyFlow.Packages.PyFlowBase.Nodes.charge import charge
from PyFlow.Packages.PyFlowBase.Nodes.delay import delay
from PyFlow.Packages.PyFlowBase.Nodes.deltaTime import deltaTime
from PyFlow.Packages.PyFlowBase.Nodes.doN import doN
from PyFlow.Packages.PyFlowBase.Nodes.doOnce import doOnce
from PyFlow.Packages.PyFlowBase.Nodes.flipFlop import flipFlop
from PyFlow.Packages.PyFlowBase.Nodes.forLoop import forLoop
from PyFlow.Packages.PyFlowBase.Nodes.forLoopBegin import forLoopBegin
from PyFlow.Packages.PyFlowBase.Nodes.loopEnd import loopEnd
from PyFlow.Packages.PyFlowBase.Nodes.whileLoopBegin import whileLoopBegin
from PyFlow.Packages.PyFlowBase.Nodes.forEachLoop import forEachLoop
from PyFlow.Packages.PyFlowBase.Nodes.forLoopWithBreak import forLoopWithBreak
from PyFlow.Packages.PyFlowBase.Nodes.retriggerableDelay import retriggerableDelay
from PyFlow.Packages.PyFlowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyFlowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyFlowBase.Nodes.timer import timer
from PyFlow.Packages.PyFlowBase.Nodes.whileLoop import whileLoop
from PyFlow.Packages.PyFlowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyFlowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyFlowBase.Nodes.reroute import reroute
from PyFlow.Packages.PyFlowBase.Nodes.rerouteExecs import rerouteExecs
from PyFlow.Packages.PyFlowBase.Nodes.makeArray import makeArray
from PyFlow.Packages.PyFlowBase.Nodes.makeList import makeList
from PyFlow.Packages.PyFlowBase.Nodes.makeDict import makeDict
from PyFlow.Packages.PyFlowBase.Nodes.makeAnyDict import makeAnyDict
from PyFlow.Packages.PyFlowBase.Nodes.makeDictElement import makeDictElement
from PyFlow.Packages.PyFlowBase.Nodes.dictKeys import dictKeys
from PyFlow.Packages.PyFlowBase.Nodes.floatRamp import floatRamp
from PyFlow.Packages.PyFlowBase.Nodes.colorRamp import colorRamp
from PyFlow.Packages.PyFlowBase.Nodes.stringToArray import stringToArray
from PyFlow.Packages.PyFlowBase.Nodes.cliexit import cliexit

from PyFlow.Packages.PyFlowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyFlowBase.Nodes.stickyNote import stickyNote

from PyFlow.Packages.PyFlowBase.Nodes.consoleOutput import consoleOutput
from PyFlow.Packages.PyFlowBase.Nodes.address import address
from PyFlow.Packages.PyFlowBase.Nodes.graphNodes import graphInputs, graphOutputs
from PyFlow.Packages.PyFlowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyFlowBase.Nodes.compound import compound
from PyFlow.Packages.PyFlowBase.Nodes.constant import constant
from PyFlow.Packages.PyFlowBase.Nodes.convertTo import convertTo
from PyFlow.Packages.PyFlowBase.Nodes.imageDisplay import imageDisplay

from PackageManager.Packages.ProgramBase.UI.DockWindows.RibbonBar import RibbonBar

# [Commands]
from PackageManager.Packages.PyFlowPkg.Commands.NewFile import NewFile
from PackageManager.Packages.PyFlowPkg.Commands.SaveFile import SaveFile
from PackageManager.Packages.PyFlowPkg.Commands.OpenFile import OpenFile
from PackageManager.Packages.PyFlowPkg.Commands.CloseFile import CloseFile

from PackageManager.Packages.PyFlowPkg.Commands.CompileTool import CompileTool

from PackageManager.Packages.PyFlowPkg.UI.DockWindows.HistoryTool import HistoryTool
from PackageManager.Packages.PyFlowPkg.UI.DockWindows.PropertiesTool import PropertiesTool

from PackageManager.Packages.PyFlowPkg.Commands.Preferences import Preferences
# from PackageManager.Packages.PyFlow.UI.DockWindows.LoggerTool import LoggerTool
# from PackageManager.Packages.PyFlow.UI.DockWindows.SearchResultsTool import SearchResultsTool

from PackageManager.Packages.PyFlowPkg.PrefsWidgets.General import GeneralPreferences
from PackageManager.Packages.PyFlowPkg.PrefsWidgets.InputPrefs import InputPreferences

from PackageManager.Packages.PyFlowPkg.Commands.About import About
from PackageManager.Packages.PyFlowPkg.Commands.HomePage import HomePage

# [Commands]
_COMMANDS = OrderedDict()
_COMMANDS[NewFile.__name__] = NewFile
_COMMANDS[SaveFile.__name__] = SaveFile
_COMMANDS[OpenFile.__name__] = OpenFile
_COMMANDS[CloseFile.__name__] = CloseFile
_COMMANDS[About.__name__] = About
_COMMANDS[HomePage.__name__] = HomePage

_COMMANDS[CompileTool.__name__] = CompileTool

_COMMANDS[RibbonBar.__name__] = RibbonBar
_COMMANDS[HistoryTool.__name__] = HistoryTool
_COMMANDS[PropertiesTool.__name__] = PropertiesTool
_COMMANDS[Preferences.__name__] = Preferences
# _COMMANDS[LoggerTool.__name__] = LoggerTool
# _COMMANDS[SearchResultsTool.__name__] = SearchResultsTool

# [Bases]
_BASES = {}

# [Tables]
_TABLES = OrderedDict()

# [Widgets]
_PREFS_WIDGETS = OrderedDict()
_PREFS_WIDGETS["PyFlow - General"] = GeneralPreferences
_PREFS_WIDGETS["PyFlow - Input"] = InputPreferences

_FOO_LIBS = {
    ArrayLib.__name__: ArrayLib(PACKAGE_NAME),
    BoolLib.__name__: BoolLib(PACKAGE_NAME),
    DefaultLib.__name__: DefaultLib(PACKAGE_NAME),
    FloatLib.__name__: FloatLib(PACKAGE_NAME),
    IntLib.__name__: IntLib(PACKAGE_NAME),
    MathLib.__name__: MathLib(PACKAGE_NAME),
    MathAbstractLib.__name__: MathAbstractLib(PACKAGE_NAME),
    RandomLib.__name__: RandomLib(PACKAGE_NAME),
    PathLib.__name__: PathLib(PACKAGE_NAME),
}

_NODES = {
    branch.__name__: branch,
    charge.__name__: charge,
    delay.__name__: delay,
    deltaTime.__name__: deltaTime,
    doN.__name__: doN,
    doOnce.__name__: doOnce,
    flipFlop.__name__: flipFlop,
    forLoop.__name__: forLoop,
    forLoopBegin.__name__: forLoopBegin,
    loopEnd.__name__: loopEnd,
    forLoopWithBreak.__name__: forLoopWithBreak,
    retriggerableDelay.__name__: retriggerableDelay,
    sequence.__name__: sequence,
    switchOnString.__name__: switchOnString,
    timer.__name__: timer,
    whileLoop.__name__: whileLoop,
    whileLoopBegin.__name__: whileLoopBegin,
    commentNode.__name__: commentNode,
    stickyNote.__name__: stickyNote,
    getVar.__name__: getVar,
    setVar.__name__: setVar,
    reroute.__name__: reroute,
    rerouteExecs.__name__: rerouteExecs,
    graphInputs.__name__: graphInputs,
    graphOutputs.__name__: graphOutputs,
    compound.__name__: compound,
    pythonNode.__name__: pythonNode,
    makeArray.__name__: makeArray,
    makeList.__name__: makeList,
    makeDict.__name__: makeDict,
    makeAnyDict.__name__: makeAnyDict,
    makeDictElement.__name__: makeDictElement,
    consoleOutput.__name__: consoleOutput,
    forEachLoop.__name__: forEachLoop,
    address.__name__: address,
    constant.__name__: constant,
    tick.__name__: tick,
    convertTo.__name__: convertTo,
    dictKeys.__name__: dictKeys,
    floatRamp.__name__: floatRamp,
    colorRamp.__name__: colorRamp,
    stringToArray.__name__: stringToArray,
    imageDisplay.__name__: imageDisplay,
    cliexit.__name__: cliexit
}

_PINS = {
    AnyPin.__name__: AnyPin,
    BoolPin.__name__: BoolPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    IntPin.__name__: IntPin,
    StringPin.__name__: StringPin,
}


class PyFlowPkg(IPackage):
    """Base PackageManager package
    """

    def __init__(self, Parent):
        super(PyFlowPkg, self).__init__()
        self.parent = Parent

    @staticmethod
    def CreateInstance(main, parent=None):
        newinstance = AppMDI.MDIMain(main, parent)
        return newinstance

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

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
    def GetBases():
        return _BASES

    @staticmethod
    def GetTables():
        return _TABLES

    @staticmethod
    def GetPreferences():
        return _PREFS_WIDGETS

    @staticmethod
    def GetIcon():
        return ICON_DIR + "ProgramLogo.png"

    @staticmethod
    def GetSmallIcon():
        return ICON_DIR + "ProgramLogo.png"

    @staticmethod
    def GetMediumIcon():
        return ICON_DIR + "ProgramLogo.png"

    @staticmethod
    def GetLargeIcon():
        return ICON_DIR + "ProgramLogo.png"

    @staticmethod
    def GetDefaultMenuOrder():
        menuOrder = ["File", "Edit", "Tools", "Windows", "Help"]
        return menuOrder

    @staticmethod
    def GetDefaultMenuLayout():
        itemDict = {}
        separatorCount = 0

        itemList = []
        itemList.append({"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "NewFile"})
        itemList.append({"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "OpenFile"})
        itemDict["File"] = itemList

        itemList = []
        # itemList.append({"Action": "Add Action", "Package": "PyFlow", "PackageGroup": "PyFlow", "Command": "CommandBuilder"})
        itemList.append({"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "History"})
        itemList.append(
            {"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "Properties"})
        itemList.append(
            {"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "SearchResults"})
        itemDict["Tools"] = itemList

        itemList = []
        itemList.append({"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "About"})
        itemList.append({"Action": "Add Action", "Package": "PyFlowPkg", "PackageGroup": "PyFlowPkg", "Command": "HomePage"})
        itemDict["Help"] = itemList

        return itemDict

    @staticmethod
    def GetDefaultRibbonOrder():
        ribbonOrder = ["File",  "Tools"]
        return ribbonOrder

    @staticmethod
    def GetDefaultRibbonLayout():
        barDict = {}
        itemDict = {}

        itemList = []

        itemList.append({"Bar": "File", "Section": "File", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "newFile - Small.png",
                         "mediumIconLocation": ICON_DIR + "newFile - Medium.png",
                         "largeIconLocation": ICON_DIR + "newFile - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "NewFile",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "New",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "File", "Section": "File", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "openFile - Small.png",
                         "mediumIconLocation": ICON_DIR + "openFile - Medium.png",
                         "largeIconLocation": ICON_DIR + "openFile - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "OpenFile",
                         "Order": 2, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Open",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "File", "Section": "File", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "saveFile - Small.png",
                         "mediumIconLocation": ICON_DIR + "saveFile - Medium.png",
                         "largeIconLocation": ICON_DIR + "saveFile - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "SaveFile",
                         "Order": 3, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Save",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemDict["File"] = itemList
        barDict["File"] = itemDict

        itemDict = {}
        itemList = []
        itemList.append({"Bar": "Tools", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "history - Small.png",
                         "mediumIconLocation": ICON_DIR + "history - Medium.png",
                         "largeIconLocation": ICON_DIR + "history - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "HistoryTool",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "History",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Tools", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "property - Small.png",
                         "mediumIconLocation": ICON_DIR + "property - Medium.png",
                         "largeIconLocation": ICON_DIR + "property - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "PropertiesTool",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Property",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Tools", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "preferences - Small.png",
                         "mediumIconLocation": ICON_DIR + "preferences - Medium.png",
                         "largeIconLocation": ICON_DIR + "preferences - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "Preferences",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Preference",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Tools", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "search - Small.png",
                         "mediumIconLocation": ICON_DIR + "search - Medium.png",
                         "largeIconLocation": ICON_DIR + "search - Large.png",
                         "Action": "Add Action", "Package": "PyFlowPkg",
                         "PackageGroup": "PyFlowPkg", "Command": "SearchResultsTool",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Search",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemDict["Tools"] = itemList
        barDict["Tools"] = itemDict

        return barDict

    @staticmethod
    def GetDefaultToolBarLayout():
        itemDict = {}
        itemList = []
        itemList.append({"Action": "Add Action", "Package": "PyFlow", "PackageGroup": "PyFlowPkg", "Command": "NewFile"})
        itemList.append({"Action": "Add Action", "Package": "PyFlow", "PackageGroup": "PyFlowPkg", "Command": "OpenFile"})
        itemDict["File"] = itemList

        return itemDict
