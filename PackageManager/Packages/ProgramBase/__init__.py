PACKAGE_NAME = 'ProgramBase'
"""Base package
"""
Logger = False

from PackageManager.Packages.ProgramBase.Resources import RESOURCES_DIR, ICON_DIR
from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage

# [Imports]
# region Commands
from PackageManager.Packages.ProgramBase.Commands.NewInstance import NewInstance

from PackageManager.Packages.ProgramBase.Commands.NewFile import NewFile
from PackageManager.Packages.ProgramBase.Commands.LoadFile import LoadFile
from PackageManager.Packages.ProgramBase.Commands.CloseFile import CloseFile
from PackageManager.Packages.ProgramBase.Commands.CloseAll import CloseAll

from PackageManager.Packages.ProgramBase.Commands.CascadeWindows import CascadeWindows
from PackageManager.Packages.ProgramBase.Commands.NextWindow import NextWindow
from PackageManager.Packages.ProgramBase.Commands.PreviousWindow import PreviousWindow
from PackageManager.Packages.ProgramBase.Commands.TileWindows import TileWindows

from PackageManager.Packages.ProgramBase.Commands.ScreenshotTool import ScreenshotTool
# from PackageManager.Packages.ProgramBase.Commands.SearchResultsTool import SearchResultsTool

from PackageManager.Packages.ProgramBase.Commands.About import About
from PackageManager.Packages.ProgramBase.Commands.HomePage import HomePage

from PackageManager.Packages.ProgramBase.Commands.Preferences import Preferences
from PackageManager.Packages.ProgramBase.Commands.CommandBuilder import CommandBuilder

# from PackageManager.Packages.ProgramBase.Commands.FormBuilder import FormBuilder
from PackageManager.Packages.ProgramBase.Commands.PackageBuilder import PackageBuilder
from PackageManager.Packages.ProgramBase.Commands.DataMapper import DataMapper
from PackageManager.Packages.ProgramBase.Commands.TextEditor import TextEditor

# Function based nodes

# [Commands]
_COMMANDS = OrderedDict()
_COMMANDS[NewInstance.__name__] = NewInstance
_COMMANDS[NewFile.__name__] = NewFile
_COMMANDS[LoadFile.__name__] = LoadFile
_COMMANDS[CloseFile.__name__] = CloseFile
_COMMANDS[CloseAll.__name__] = CloseAll
_COMMANDS[CascadeWindows.__name__] = CascadeWindows
_COMMANDS[NextWindow.__name__] = NextWindow
_COMMANDS[PreviousWindow.__name__] = PreviousWindow
_COMMANDS[TileWindows.__name__] = TileWindows
_COMMANDS[ScreenshotTool.__name__] = ScreenshotTool
_COMMANDS[About.__name__] = About
_COMMANDS[HomePage.__name__] = HomePage

_COMMANDS[Preferences.__name__] = Preferences
_COMMANDS[PackageBuilder.__name__] = PackageBuilder
_COMMANDS[DataMapper.__name__] = DataMapper
# _COMMANDS[FormBuilder.__name__] = FormBuilder
_COMMANDS[TextEditor.__name__] = TextEditor
# endregion


# [ToolBar
from PackageManager.Packages.ProgramBase.UI.DockWindows.RibbonBar import RibbonBar
from PackageManager.Packages.ProgramBase.UI.DockWindows.ToolBar import ToolBar
from PackageManager.Packages.ProgramBase.UI.DockWindows.HistoryTool import HistoryTool
from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool

if Logger:
    from PackageManager.Packages.ProgramBase.UI.DockWindows.LoggerTool import LoggerTool
# from PackageManager.Packages.ProgramBase.UI.DockWindows.SearchResultsTool import SearchResultsTool

_COMMANDS[RibbonBar.__name__] = RibbonBar
_COMMANDS[ToolBar.__name__] = ToolBar
_COMMANDS[HistoryTool.__name__] = HistoryTool
_COMMANDS[PropertiesTool.__name__] = PropertiesTool
if Logger:
    _COMMANDS[LoggerTool.__name__] = LoggerTool
# _COMMANDS[SearchResultsTool.__name__] = SearchResultsTool
# endregion

# [Widgets]
from PackageManager.Packages.ProgramBase.PrefsWidgets.General import GeneralPreferences
from PackageManager.Packages.ProgramBase.PrefsWidgets.InputPrefs import InputPreferences
from PackageManager.Packages.ProgramBase.PrefsWidgets.ThemePrefs import ThemePreferences

_PREFS_WIDGETS = OrderedDict()
_PREFS_WIDGETS["Main - General"] = GeneralPreferences
_PREFS_WIDGETS["Main - Input"] = InputPreferences
_PREFS_WIDGETS["Main - Theme"] = ThemePreferences
# endregion

# [Bases]
from PackageManager.Packages.ProgramBase.Database.DefaultData import MainBase

_BASES = OrderedDict()
_BASES["MainBase"] = MainBase

# [Tables]
_TABLES = OrderedDict()
from PackageManager.Packages.ProgramBase.Database import dbFormBuilder
_TABLES["AddonPrograms"] = dbFormBuilder.AddonPrograms
_TABLES["AddonProgramsClasses"] = dbFormBuilder.AddonProgramsClasses
_TABLES["AddonProgramsClassesUsed"] = dbFormBuilder.AddonProgramsClassesUsed
_TABLES["RecordGroup"] = dbFormBuilder.RecordGroup
_TABLES["RecordGroupParents"] = dbFormBuilder.RecordGroupParents
_TABLES["FormInformation"] = dbFormBuilder.FormInformation
_TABLES["FormWidgets"] = dbFormBuilder.FormWidgets
_TABLES["WidgetType"] = dbFormBuilder.WidgetType
_TABLES["WidgetData"] = dbFormBuilder.WidgetData
_TABLES["WidgetDataHandling"] = dbFormBuilder.WidgetDataHandling
_TABLES["FormItemData"] = dbFormBuilder.FormItemData
_TABLES["FormItemTreeViewData"] = dbFormBuilder.FormItemTreeViewData
_TABLES["FormFunctionTemplate"] = dbFormBuilder.FormFunctionTemplate
_TABLES["FormFunction"] = dbFormBuilder.FormFunction
_TABLES["VariableList"] = dbFormBuilder.VariableList
_TABLES["FunctionList"] = dbFormBuilder.FunctionList
_TABLES["FormDesignTree"] = dbFormBuilder.FormDesignTree
_TABLES["FormDesignGeneratedTree"] = dbFormBuilder.FormDesignGeneratedTree
_TABLES["FormDesignComponents"] = dbFormBuilder.FormDesignComponents
_TABLES["FormDesignBranchBuilder"] = dbFormBuilder.FormDesignBranchBuilder
_TABLES["FormDesignPrimaryGroup"] = dbFormBuilder.FormDesignPrimaryGroup
_TABLES["FormDesignSecondaryGroup"] = dbFormBuilder.FormDesignSecondaryGroup
_TABLES["FormDesignDescriptorTable"] = dbFormBuilder.FormDesignDescriptorTable
_TABLES["FormDesignItemTable"] = dbFormBuilder.FormDesignItemTable
_TABLES["FormDesignTreeSetting"] = dbFormBuilder.FormDesignTreeSetting

from PackageManager.Packages.ProgramBase.Database import dbGeography
_TABLES["Country"] = dbGeography.Country
_TABLES["Province"] = dbGeography.Province
_TABLES["City"] = dbGeography.City
_TABLES["PostalCode"] = dbGeography.PostalCode
_TABLES["AoGType"] = dbGeography.AoGType
_TABLES["MunicipalityType"] = dbGeography.MunicipalityType
_TABLES["AreaOfGovernance"] = dbGeography.AreaOfGovernance
_TABLES["Municipality"] = dbGeography.Municipality
_TABLES["LocationGeoTag"] = dbGeography.LocationGeoTag
_TABLES["AllLocationGeoTag"] = dbGeography.AllLocationGeoTag
_TABLES["GPSData"] = dbGeography.GPSData

from PackageManager.Packages.ProgramBase.Database import dbMaster
_TABLES["TableSelectionType"] = dbMaster.TableSelectionType
_TABLES["DataType"] = dbMaster.DataType
_TABLES["TableType"] = dbMaster.TableType
_TABLES["SessionBase"] = dbMaster.SessionBase
_TABLES["SessionNames"] = dbMaster.SessionNames
_TABLES["Reference"] = dbMaster.Reference
_TABLES["MasterTable"] = dbMaster.MasterTable
_TABLES["DataCorrection"] = dbMaster.DataCorrection
_TABLES["SyncRules"] = dbMaster.SyncRules
_TABLES["FieldKeyRegistry"] = dbMaster.FieldKeyRegistry
_TABLES["ForeignKeyRegistry"] = dbMaster.ForeignKeyRegistry
_TABLES["SyncOrder"] = dbMaster.SyncOrder
_TABLES["SyncJournal"] = dbMaster.SyncJournal
_TABLES["DatabaseAction"] = dbMaster.DatabaseAction
_TABLES["DataSyncRecords"] = dbMaster.DataSyncRecords
_TABLES["DataSyncStatements"] = dbMaster.DataSyncStatements
_TABLES["BulkUpdate"] = dbMaster.BulkUpdate
_TABLES["BulkUpdateAffectedTable"] = dbMaster.BulkUpdateAffectedTable
_TABLES["DynamicRecordUpdate"] = dbMaster.DynamicRecordUpdate


from PackageManager.Packages.ProgramBase.Database import dbProgramBase

from PackageManager.Packages.ProgramBase.Database import dbUnits
_TABLES["UnitType"] = dbUnits.UnitType
_TABLES["Unit"] = dbUnits.Unit



# endregion

_FOO_LIBS = {
}

_NODES = {
}

_PINS = {
}

# [Export]
_EXPORTERS = OrderedDict()


class ProgramBase(IPackage):
    """Base PackageManager package
    """

    def __init__(self, Parent):
        super(ProgramBase, self).__init__()
        self.parent = Parent

    @staticmethod
    def CreateInstance(main, parent=None):
        return main

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
        itemOrder = ["Tools", "Windows", "Help"]
        return itemOrder

    @staticmethod
    def GetDefaultMenuLayout():
        itemDict = {}
        separatorCount = 0

        itemList = []
        itemDict["Packages"] = itemList

        itemList = []
        itemDict["File"] = itemList

        itemList = []
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "ToolBar"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "RibbonBar"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "Preferences"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "Logger"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "FormBuilder"})
        itemList.append({"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase",
                         "Command": "PackageBuilder"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "TextEditor"})
        itemDict["Tools"] = itemList

        itemList = []
        itemDict["Windows"] = itemList

        itemList = []
        # helpMenuList.append({"Action": "Add Action", "Package": "ProgramBase", "Command": "loadForm"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "About"})
        itemList.append(
            {"Action": "Add Action", "Package": "ProgramBase", "PackageGroup": "ProgramBase", "Command": "HomePage"})
        itemDict

        return itemDict

    @staticmethod
    def GetDefaultRibbonOrder():
        ribbonOrder = ["Home"]
        return ribbonOrder

    @staticmethod
    def GetDefaultRibbonLayout():
        barDict = {}
        itemDict = {}

        itemList = []
        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "preferences - Small.png",
                         "mediumIconLocation": ICON_DIR + "preferences - Medium.png",
                         "largeIconLocation": ICON_DIR + "preferences - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "Preferences",
                         "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Preferences",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "logger - Small.png",
                         "mediumIconLocation": ICON_DIR + "logger - Medium.png",
                         "largeIconLocation": ICON_DIR + "logger - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "Logger",
                         "Order": 2, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Logger",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "formBuilder - Small.png",
                         "mediumIconLocation": ICON_DIR + "formBuilder - Medium.png",
                         "largeIconLocation": ICON_DIR + "formBuilder - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "FormBuilder",
                         "Order": 3, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Form Builder",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "packageBuilder - Small.png",
                         "mediumIconLocation": ICON_DIR + "packageBuilder - Medium.png",
                         "largeIconLocation": ICON_DIR + "packageBuilder - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "PackageBuilder",
                         "Order": 4, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Package Builder",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "packageBuilder - Small.png",
                         "mediumIconLocation": ICON_DIR + "packageBuilder - Medium.png",
                         "largeIconLocation": ICON_DIR + "packageBuilder - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "DataMapper",
                         "Order": 4, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "DataMapper",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemList.append({"Bar": "Home", "Section": "Tools", "Widget": "Large Button",
                         "smallIconLocation": ICON_DIR + "textEditor - Small.png",
                         "mediumIconLocation": ICON_DIR + "textEditor - Medium.png",
                         "largeIconLocation": ICON_DIR + "textEditor - Large.png",
                         "Action": "Add Action", "Package": "ProgramBase",
                         "PackageGroup": "ProgramBase", "Command": "TextEditor",
                         "Order": 5, "StartPosition": (1, 1), "Fixity": "Order", "WidgetSize": (1, 1),
                         "DisplayName": "New", "ShowName": False, "ToolTip": "Text Editor",
                         "IsEnabled": True, "IsVisible": True, "MainVisible": True, "InstanceVisible": True})

        itemDict["Tools"] = itemList
        barDict["Home"] = itemDict

        return barDict

    @staticmethod
    def GetDefaultToolBarLayout():
        itemDict = {}
        itemList = []
        itemList.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                         "Package": "PyFlow", "PackageGroup": "PyFlow", "Command": "NewFile"})
        itemDict["File"] = itemList

        return itemDict
