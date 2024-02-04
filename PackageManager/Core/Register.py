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

import importlib
import pkgutil
import collections
from copy import copy
import os
import json
import uuid

from PySide6 import QtGui
from PySide6.QtWidgets import (QMenu, QApplication, QFileDialog, QMainWindow, QMdiArea, QMdiSubWindow, QMessageBox, QWidget, QMenuBar)
from PySide6.QtGui import QAction
from collections import OrderedDict
from PackageManager.UI.Commands.Command import ShelfTool, DockTool
from PackageManager.Input import InputAction, InputActionType
from PackageManager.Input import InputManager
from PackageManager.ConfigManager import ConfigManager
from PySide6.QtWidgets import QMessageBox
from collections import defaultdict

class LoadPackages(object):
    def __init__(self, main, packageRegister):
        self.main = main
        self.packageRegister = packageRegister
        self.instanceList = {}
        self.uuidinstanceList = {}
        self.actionregister = ActionRegister()

    def registerPackageInstance(self, packageName, instance, main=None, parent=None):
        commands = self.packageRegister.GET_PACKAGE_COMMANDS(packageName)
        newinstanceItem = instanceItem(commands, packageName, instance, main, parent)
        if main is None:
            newinstanceItem.main = newinstanceItem
        newinstanceItem.instance.configManager = ConfigManager()
        #Get the value from configuration file
        #Icon = instance.configManager.getPrefsValue("PREFS", "General/RedirectOutput") == "true"
        #If it does not exist then get the default value
        #Store the default values in the preferences file

        newinstanceItem.icon = self.packageRegister.getIcon(packageName)
        newinstanceItem.formDict = self.packageRegister.getFormDict(packageName)
        newinstanceItem.baseDict = self.packageRegister.getBaseDict(packageName)
        newinstanceItem.tableDict = self.packageRegister.getTableDict(packageName)
        newinstanceItem.formItems = self.packageRegister.getFormItems(packageName)
        newinstanceItem.menuOrder = self.packageRegister.getMenuOrder(packageName)
        newinstanceItem.menuLayout = self.packageRegister.getMenuLayout(packageName)
        newinstanceItem.ribbonOrder = self.packageRegister.getRibbonOrder(packageName)
        newinstanceItem.ribbonLayout = self.packageRegister.getRibbonLayout(packageName)
        newinstanceItem.toolbarLayout = self.packageRegister.getToolBarLayout(packageName)
        newinstanceItem.preferences = self.packageRegister.getPreferences(packageName)

        self.uuidinstanceList[newinstanceItem.uuid] = newinstanceItem
        self.instanceList[packageName] = newinstanceItem
        newinstanceItem.loadRibbonBar()

        if newinstanceItem.preferences is not None:
            for categoryName, widgetClass in newinstanceItem.preferences.items():
                newinstanceItem.main.instance.preferencesWindow.addCategory(categoryName, widgetClass())
            #newinstanceItem.main.instance.preferencesWindow.selectByName("General")

        return newinstanceItem

    def createPackageInstance(self, packageName, main, parent=None):
        instance = self.packageRegister.createPackageInstanceByClass(packageName)
        commands = self.packageRegister.GET_PACKAGE_COMMANDS(packageName)
        menu = self.packageRegister.GET_PACKAGE_MENU(packageName)
        #toolbar = self.pa
        newinstanceItem = instanceItem(commands, packageName, main, instance, parent)

        self.uuidinstanceList[newinstanceItem.uuid] = newinstanceItem
        self.instanceList[packageName] = newinstanceItem

        return newinstanceItem

    def getInstancebyPackageName(self, packageName):
        return self.uuidinstanceList[packageName]

    def getInstancebyUUID(self, uuid):
        return self.uuidinstanceList[uuid]

    def createMDIPackageInstance(self, PackageName, instance, MDIClass, Parent):
        pass

class loadPackageRegister(object):
    def __init__(self, defaultpaths, packagelist):
        super(loadPackageRegister, self).__init__()
        self.packageMainCommands = defaultdict(list)
        self.packageInstanceCommands = defaultdict(list)
        self.PACKAGES = {}
        self.PACKAGE_PATHS = {}
        self.HASHABLE_TYPES = []
        self.PACKAGELOCATIONS = []
        self.REGISTERED_COMMANDS = defaultdict(list)
        self.packagePaths = []
        self.Databases = {}
        self.packageList = packagelist
        self.packageCreateInstance = None
        self.packageInstanceForms = defaultdict(list)
        self.packageInstanceTables = defaultdict(list)
        self.packageInstanceBase = defaultdict(list)
        self.packageInstanceFormItems = defaultdict(list)
        self.packageInstanceMenuOrder = defaultdict(list)
        self.packageInstanceIcon = defaultdict(list)
        self.packageInstanceSmallIcon = defaultdict(list)
        self.packageInstanceMediumIcon = defaultdict(list)
        self.packageInstanceLargeIcon = defaultdict(list)
        self.packageInstanceMenuLayout = defaultdict(list)
        self.packageInstanceRibbonOrder = defaultdict(list)
        self.packageInstanceRibbonLayout = defaultdict(list)
        self.packageInstanceToolbarLayout = defaultdict(list)
        self.packageInstancePreferences = defaultdict(list)

        self.addPackagesPaths(defaultpaths)
    def createPackageInstance(self, packagename, main, parent):
        package = self.PACKAGES[packagename]
        return (lambda mainInstance=main, parent=parent: package.CreateInstance(main, parent))

    def registerPackageCommand(self, packageName, toolClass):
        registeredToolNames = [tool.name() for tool in self.packageInstanceCommands[packageName]]
        if toolClass.name() not in registeredToolNames:
            self.packageInstanceCommands[packageName].append(toolClass)
            toolClass.packageName = packageName

    def registerPackageInstanceForm(self, packageName, form):
        self.packageInstanceForms[packageName] = form

    def registerPackageInstanceTable(self, packageName, table):
        self.packageInstanceTables[packageName] = table

    def registerPackageInstanceBase(self, packageName, base):
        self.packageInstanceBase[packageName] = base

    def registerPackageInstanceFormItems(self, packageName, formItems):
        self.packageInstanceFormItems[packageName] = formItems

    def registerPackageInstanceMenuOrder(self, packageName, menuOrder):
        self.packageInstanceMenuOrder[packageName] = menuOrder

    def registerPackageInstanceIcon(self, packageName, icon, smallIcon, mediumIcon, largeIcon):
        self.packageInstanceIcon[packageName] = icon
        self.packageInstanceSmallIcon[packageName] = smallIcon
        self.packageInstanceMediumIcon[packageName] = mediumIcon
        self.packageInstanceLargeIcon[packageName] = largeIcon

    def registerPackageInstanceMenuLayout(self, packageName, menuLayout):
        self.packageInstanceMenuLayout[packageName] = menuLayout

    def registerPackageInstanceRibbonOrder(self, packageName, ribbonOrder):
        self.packageInstanceRibbonOrder[packageName] = ribbonOrder

    def registerPackageInstanceRibbonLayout(self, packageName, ribbonLayout):
        self.packageInstanceRibbonLayout[packageName] = ribbonLayout

    def registerPackageInstanceToolbarLayout(self, packageName, toolbarLayout):
        self.packageInstanceToolbarLayout[packageName] = toolbarLayout

    def registerPackageInstancePreferences(self, packageName, preferences):
        self.packageInstancePreferences[packageName] = preferences

    def getFormDict(self, packageName):
        return self.packageInstanceForms[packageName]

    def getBaseDict(self, packageName):
        return self.packageInstanceBase[packageName]

    def getTableDict(self, packageName):
        return self.packageInstanceTables[packageName]

    def getFormItems(self, packageName):
        return self.packageInstanceForms[packageName]

    def getMenuOrder(self, packageName):
        return self.packageInstanceMenuOrder[packageName]

    def getIcon(self, packageName):
        return self.packageInstanceIcon[packageName]

    def getSmallIcon(self, packageName):
        return self.packageInstanceSmallIcon[packageName]

    def getMediumIcon(self, packageName):
        return self.packageInstanceMediumIcon[packageName]

    def getLargeIcon(self, packageName):
        return self.packageInstanceLargeIcon[packageName]

    def getMenuLayout(self, packageName):
        return self.packageInstanceMenuLayout[packageName]

    def getRibbonOrder(self, packageName):
        return self.packageInstanceRibbonOrder[packageName]

    def getRibbonLayout(self, packageName):
        return self.packageInstanceRibbonLayout[packageName]

    def getToolBarLayout(self, packageName):
        return self.packageInstanceToolbarLayout[packageName]

    def getPreferences(self, packageName):
        return self.packageInstancePreferences[packageName]

    def GET_COMMANDS(self):
        return self.REGISTERED_COMMANDS

    def GET_PACKAGE_COMMANDS(self, packageName):
        return self.packageInstanceCommands[packageName]

    def GET_PACKAGES(self):
        return self.PACKAGES

    def GET_PACKAGE_PATH(self, packageName):
        if packageName in self.PACKAGE_PATHS:
            return self.PACKAGE_PATHS[packageName]

    def GET_PACKAGE_CHECKED(self, package_name):
        assert package_name in self.PACKAGES
        return self.PACKAGES[package_name]

    def getAllPinClasses(self):
        result = []
        for package in list(self.PACKAGES.values()):
            result += list(package.GetPinClasses().values())
        return result

    def findPinClassByType(self, dataType):
        for package_name, package in self.GET_PACKAGES().items():
            pins = package.GetPinClasses()
            if dataType in pins:
                return pins[dataType]
        return None

    def getPinDefaultValueByType(self, dataType):
        pin = self.findPinClassByType(dataType)
        if pin:
            return pin.pinDataTypeHint()[1]
        return None

    def getHashableDataTypes(self):
        if len(self.HASHABLE_TYPES) == 0:
            for pin in self.getAllPinClasses():
                t = pin.internalDataStructure()
                if t is not type(None) and t is not None:
                    if isinstance(pin.pinDataTypeHint()[1], collections.Hashable):
                        self.HASHABLE_TYPES.append(pin.__name__)
        return copy(self.HASHABLE_TYPES)

    def getPinFromData(self, data):
        for pin in [pin for pin in self.getAllPinClasses() if pin.IsValuePin()]:
            pType = pin.internalDataStructure()
            if data == pType:
                return pin

    def CreateRawPin(self, name, owningNode, dataType, direction, **kwds):
        pinClass = self.findPinClassByType(dataType)
        if pinClass is None:
            return None
        inst = pinClass(name, owningNode, direction, **kwds)
        return inst

    def getRawNodeInstance(self, nodeClassName, packageName=None, libName=None, **kwargs):
        from PyFlow.Core.NodeBase import NodeBase
        package = self.GET_PACKAGE_CHECKED(packageName)
        # try find function first
        if libName is not None:
            for key, lib in package.GetFunctionLibraries().items():
                foos = lib.getFunctions()
                if libName == key and nodeClassName in foos:
                    return NodeBase.initializeFromFunction(foos[nodeClassName], **kwargs)

        # try find node class
        nodes = package.GetNodeClasses()
        if nodeClassName in nodes:
            return nodes[nodeClassName](nodeClassName)

        # try find exported py nodes
        packagePath = self.GET_PACKAGE_PATH(packageName)
        pyNodesPath = os.path.join(packagePath, "PyNodes")
        if os.path.exists(pyNodesPath):
            for path, dirs, files in os.walk(pyNodesPath):
                for pyNodeFileName in files:
                    pyNodeName, _ = os.path.splitext(pyNodeFileName)
                    if nodeClassName == pyNodeName:
                        pythonNode = self.getRawNodeInstance("pythonNode", "PyFlowBase")
                        pyNodeFullPath = os.path.join(path, pyNodeFileName)
                        with open(pyNodeFullPath, "r") as f:
                            pythonNode._nodeData = f.read()
                        return pythonNode

        # try find exported compound nodes
        compoundNodesPath = os.path.join(packagePath, "Compounds")
        if os.path.exists(compoundNodesPath):
            for path, dirs, files in os.walk(compoundNodesPath):
                for compoundNodeFileName in files:
                    compoundNodeName, _ = os.path.splitext(compoundNodeFileName)
                    compoundNodeFullPath = os.path.join(path, compoundNodeFileName)
                    with open(compoundNodeFullPath, 'r') as f:
                        compoundData = json.load(f)
                        if compoundData["name"] == nodeClassName:
                            compoundNode = self.getRawNodeInstance("compound", "PyFlowBase")
                            compoundNodeFullPath = os.path.join(path, compoundNodeFileName)
                            with open(compoundNodeFullPath, "r") as f:
                                jsonString = f.read()
                                compoundNode._rawGraphJson = json.loads(jsonString)
                            return compoundNode

    def addPackagesPaths(self, additionalPackageLocations):
        #This loads the items in the package ini file to the package register
        #Commands
        #Default Menulayout
        #Default Toolbarlayout
        #Default Ribbonbarlayout
        #Todo: Make instance and parent version of the layouts

        def ensurePackagePath(inPath):
            for subFolder in os.listdir(inPath):
                subFolderPath = os.path.join(inPath, subFolder)
                if os.path.isdir(subFolderPath):
                    if "PackageManager" in os.listdir(subFolderPath):
                        subFolderPath = os.path.join(subFolderPath, "PackageManager", "Packages")
                        if os.path.exists(subFolderPath):
                            return subFolderPath
            return inPath

        def recursePackagePaths(inPath):
            paths = []
            for subFolder in os.listdir(inPath):
                subFolderPath = os.path.join(inPath, subFolder)
                if os.path.isdir(subFolderPath):
                    if "PackageManager" in os.listdir(subFolderPath):
                        subFolderPath = os.path.join(subFolderPath, "PackageManager", "Packages")
                        if os.path.exists(subFolderPath):
                            paths.append(subFolderPath)
            return paths

        # check for additional package locations
        if "PackageManager_PACKAGES_PATHS" in os.environ:
            delim = ';'
            pathsString = os.environ["PackageManager_PACKAGES_PATHS"]
            # remove delimeters from right
            pathsString = pathsString.rstrip(delim)
            for packagesRoot in pathsString.split(delim):
                if os.path.exists(packagesRoot):
                    paths = recursePackagePaths(packagesRoot)
                    self.packagePaths.extend(paths)

        for packagePathId in range(len(additionalPackageLocations)):
            packagePath = additionalPackageLocations[packagePathId]
            packagePath = ensurePackagePath(packagePath)
            additionalPackageLocations[packagePathId] = packagePath

        self.packagePaths.extend(additionalPackageLocations)

        for importer, modname, ispkg in pkgutil.iter_modules(self.packagePaths):
            try:
                if ispkg:
                    if (modname not in self.PACKAGES and self.packageList is None) \
                            or (modname not in self.PACKAGES and modname in self.packageList):
                        mod = importer.find_module(modname).load_module(modname)
                        # mod = importlib.import_module(modname) #This way can be used too
                        package = getattr(mod, modname)(None)
                        self.PACKAGES[modname] = package
                        self.PACKAGE_PATHS[modname] = os.path.normpath(mod.__path__[0])
            except Exception as e:
                QMessageBox.critical(None, str("Fatal error"), "Error On Module %s :\n%s" % (modname, str(e)))
                continue

        for name, package in self.PACKAGES.items():
            packageName = package.__class__.__name__
            # Does modname equal packageName?
            for commandClass in package.GetCommandClasses().values():
                self.registerPackageCommand(packageName, commandClass)


            self.registerPackageInstanceIcon(packageName, package.GetIcon(), package.GetSmallIcon(),
                                             package.GetMediumIcon(),
                                             package.GetLargeIcon())
            #self.registerPackageInstanceForm(self, packageName, package.GetForms())
            #self.registerPackageInstanceFormItems(packageName, package.GetFormItems())

            self.registerPackageInstanceTable(packageName, package.GetTables())
            self.registerPackageInstanceBase(packageName, package.GetBases())

            self.registerPackageInstanceMenuOrder(packageName, package.GetDefaultMenuOrder())
            self.registerPackageInstanceMenuLayout(packageName, package.GetDefaultMenuLayout())

            self.registerPackageInstanceRibbonOrder(packageName, package.GetDefaultRibbonOrder())
            self.registerPackageInstanceRibbonLayout(packageName, package.GetDefaultRibbonLayout())

            self.registerPackageInstanceToolbarLayout(packageName, package.GetDefaultToolBarLayout())
            self.registerPackageInstancePreferences(packageName, package.GetPreferences())

    def getPackageClassByName(self, packageName):
        if packageName in self.PACKAGES:
            return self.PACKAGES[packageName]
        return None

class instanceItem(object):
    def __init__(self, commands, packageRegisterName, instance=None, mainInstance=None, parentInstance=None):
        #The instance is the main program
        #This class is used to have the main program communicate with the main program and other packages.
        #The menus and actions will be loaded here and attached to this instance

        self.uuid = uuid.uuid4()
        self.packageName = packageRegisterName

        self.parent = parentInstance
        self.commands = commands
        self.icon = None
        self.smallIcon = None
        self.mediumIcon = None
        self.largeIcon = None
        self.prefWidgets = None
        self.instance = instance

        #Having issues trying to create the chicken before the egg
        if mainInstance is None:
            self.main = self
        else:
            self.main = mainInstance

        self.actionRegister = self.main.instance.commandRegister.actionregister

        self.registerAction()

        self.dockWindowRegister = DockWindowRegister(self)
        self.ribbonbar = self.dockWindowRegister.loadDockWindow("RibbonBar")

        self.activeCommands = {}

        self.formDict = {}
        self.baseDict = {}
        self.tableDict = {}
        self.formItems = {}
        self.menuOrder = {}
        self.menuLayout = {}
        self.ribbonOrder = {}
        self.ribbonLayout = {}
        self.toolbarLayout = {}

        #self.menuItems = instance.getMenuLayout()
        #self.menuOrder = instance.getMenuOrder()
        self.MDIInstanceChild = {}
        self.MDIInstanceParent = None
        self.children = {}
        self.parent = parentInstance
        self.isMDIChild = False

    def createInstance(self):
        commandClass = self.actionRegister.getCommandClass(self.packageName, "NewInstance").commandClass
        commandClass.setAppInstance(self.main)
        commandClass.setPackageInstance(self)
        self.instance = commandClass.do(self.main, self)

    def loadRibbonBar(self):
        self.ribbonbar.setIcon(QtGui.QIcon(self.icon))

        ribbonBarOrder = self.ribbonOrder
        ribbonItems = self.ribbonLayout
        ribbonBarDict = {}

        for ribbonBarGroup in ribbonBarOrder:
            ribbonBarDict[ribbonBarGroup] = {}
            sectionList = []
            ribbonSectionDict = {}
            category = self.ribbonbar.addCategory(ribbonBarGroup)
            #Todo: Have this so it processes in custom orders for categories, panels and commands
            if ribbonItems:
                if ribbonBarGroup in ribbonItems:
                    for order, mutableproperties in enumerate(ribbonItems[ribbonBarGroup]):
                        if mutableproperties not in sectionList:
                            ribbonpanel = category.createPanel(mutableproperties)
                            ribbonBarDict[ribbonBarGroup][mutableproperties] = ribbonpanel
                            sectionList.append(mutableproperties)

                        for order2, mutableproperties2 in enumerate(ribbonItems[ribbonBarGroup][mutableproperties]):
                            nonmutableproperties = self.actionRegister\
                            .getAction(mutableproperties2["PackageGroup"], mutableproperties2["Command"])

                            a = ribbonBarGroup
                            b = mutableproperties
                            c = mutableproperties2
                            d = nonmutableproperties
                            e = ribbonBarDict[ribbonBarGroup][mutableproperties]
                            ribbonBarDict[ribbonBarGroup][mutableproperties].addAction(mutableproperties2, nonmutableproperties)

    def setMain(self, maininstance):
        self.main = maininstance

    def addClass(self, instance):
        self.commands.add(instance)

    def getMenuLayout(self):
        return self.menuLayout

    def getMenuOrder(self):
        return self.menuOrder

    def getToolBar(self):
        return self.toolBarRegister

    def getIcon(self):
        return self.icon

    def getSmallIcon(self):
        return self.smallIcon

    def getMediumIcon(self):
        return self.mediumIcon

    def getLargeIcon(self):
        return self.largeIcon()

    def loadDockWindow(self, commandName, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        '''a = self.packageRegister
        commandClass = self.packageRegister'''

        #self.currentinstance

        commandClass = self.actionRegister.getCommandClass(self.packageName, commandName).commandClass
        commandClass.setAppInstance(self.main)
        commandClass.setPackageInstance(self)

        if commandClass is None:
            return
        isSingleton = commandClass.isSingleton()
        if isSingleton:
            # check if already registered
            docWindow = self.dockWindowRegister.getDocWindows(commandName)
            if docWindow:
                docWindow.show()
                docWindow.onShow()
                # Highlight window
                # print("highlight", docWindow.uniqueName())
                return

        if commandClass:
            # self._registerCommandInstance(CommandInstance)
            if settings is not None:
                commandClass.restoreState(settings)
                if not self.main.restoreDockWidget(commandClass):
                    # handle if ui state was not restored
                    pass
            else:
                self.addDockWidget(commandClass.defaultDockArea(), commandClass)
                self.currentPackage.dockWindowRegister.addDocWindows(commandName, commandClass)
            commandClass.onShow()
        return commandClass

    def registerAction(self):
        settings = ConfigManager().getSettings("APP_STATE")
        state = settings.value('Editor/state')
        '''if state is not None:
           self.restoreState(state)'''
        settings.beginGroup("Commands")
        #b = self.toolBarRegister

        for CommandsClass in self.commands:
           CommandInstance = CommandsClass()
           #CommandInstance.setAppInstance(self.instance)
           # This sets the command for particular instance
           # This is excecuted at menu time so that

           if issubclass(CommandsClass, ShelfTool):
               self.actionRegister.addAction(self.packageName, CommandInstance, self.main, self)

               # prevent to be garbage collected
               settings.beginGroup("ShelfTools")
               settings.beginGroup(CommandInstance.name())
               CommandInstance.restoreState(settings)
               settings.endGroup()
               settings.endGroup()

           if issubclass(CommandsClass, DockTool):
               settings.beginGroup("DockTools")
               print(CommandsClass.name())
               #action = lambda packageName=self.packageName, commandName=CommandsClass.name(): self.loadDockWindow(self.packageName, commandName)
               action = lambda packageName=self.packageName, commandName=CommandsClass().name(): self.main.instance.loadDockWindow(packageName, commandName)

               self.actionRegister.addAction(self.packageName, CommandInstance, self.main, self.instance, action, None)

               settings.endGroup()

    def removeClass(self, instance):
        if instance in self.commands:
            self.commands.remove(instance)

    def getCommands(self):
        return self.commands

class ActionItem(QAction):
    def __init__(self, packageName, commandClass, main, instance, customCommand=None):
        super(ActionItem, self).__init__()
        try:
            self.setIcon(commandClass.getIcon())
        except:
            pass

        self.packageName = packageName
        self.commandClass = commandClass
        self.setText(commandClass.name())
        self.setInstance(main, instance)
        self.setObjectName(commandClass.name())
        #self.setObjectName(commandClass.name())

        #TODO I want to move this out of here, i want it to be more dynamic.
        #its been moved to the inifile
        self.smallIconLocation = None
        self.mediumIconLocation = None
        self.largeIconLocation = None
        self.setToolTip(commandClass.toolTip())
        self.handler = None

        if customCommand:
            self.triggered.connect(customCommand)
            self.handler = customCommand
        else:
            try:
                self.triggered.connect(commandClass.do)
                self.handler = commandClass.do
            except:
                print(commandClass.name())

    def isSingleton(self):
        try:
            self.isSingleton = self.commandClass.isSingleton()
        except:
            self.isSingleton = False

    def defaultDockArea(self):
        return self.commandClass.defaultDockArea()

    def setInstance(self, main, instance):
        self.commandClass.setAppInstance(main)
        self.commandClass.setPackageInstance(instance)

class ActionGroup(object):
    def __init__(self, packageName):
        self.packageName = packageName
        self.actionDict = {}
        self.classDict = {}

    def addAction(self, commandName, commandClass, action):
        self.actionDict[commandName] = action
        self.classDict[commandName] = commandClass

    def getClassDict(self):
        return self.classDict

    def getActionDict(self):
        return self.actionDict

    def getAction(self, commandName):
        try:
            #print(self.actionDict)
            return self.actionDict[commandName]
        except:
            print("Command Not Found: " + commandName)

    def getCommandClass(self, commandName):
        try:
            #print(self.actionDict)
            return self.classDict[commandName]
        except:
            print("Command Not Found: " + commandName)


class ActionRegister(object):
    def __init__(self):
        self.actionGroups = {}

    def registerAction(self, action, packageName, commandClass, parent=None):
        if parent:
            if parent not in self.actionGroups:
                newgroup = ActionGroup(packageName)
                self.actionGroups[packageName] = newgroup
            '''            if "MDIChild" not in self.actionGroups:
                newgroup = ActionGroup(packageName)
                self.actionGroups["MDIChild"] = newgroup'''
            packageName = parent

        if packageName not in self.actionGroups:
            newgroup = ActionGroup(packageName)
            self.actionGroups[packageName] = newgroup

        self.actionGroups[packageName].addAction(commandClass.name(), commandClass, action)

    def addAction(self, packageName, commandClass, main, instance, command=None, parent=None):
        self.commandClass = commandClass
        newActionItem = ActionItem(packageName, commandClass, main, instance, command)
        self.registerAction(newActionItem, packageName, commandClass, parent)

    def getAction(self, packageName, commandName, instance=None):
        #print(packageName, commandName)
        #package = self.actionGroups[packageName]
        if packageName in self.actionGroups:
            action = self.actionGroups[packageName].getAction(commandName)
            return action

    def getCommandClass(self, packageName, commandName, instance=None):
        #print(packageName, commandName)
        #package = self.actionGroups[packageName]
        if packageName in self.actionGroups:
            action = self.actionGroups[packageName].getAction(commandName)
            return action

    def getAllActions(self, packageName):
        return self.actionGroups[packageName]


class DockWindowItem(object):
    def __init__(self, packageName, commandClass):
        super(DockWindowItem, self).__init__()
        pass


class DockWindowRegister(object):
    def __init__(self, package):
        self.dockDict = {}
        self.package = package
        self.commandClass = package.commands
        self.actionRegister = package.actionRegister

    def getDocWindows(self, commandName):
        if commandName in self.dockDict:
            return self.dockDict[commandName]
        else:
            return None

    def addDocWindows(self, commandName, commandInstance):
        if commandName not in self.dockDict:
             self.dockDict[commandName] = commandInstance

    def getCommandsClassByName(self, packageName, commandName):
        registeredCommands = self.actionRegister.getAllActions()
        for CommandClass in registeredCommands[packageName]:
            if CommandClass.name() == commandName:
                    return CommandClass
        return None

    def loadInstance(self, package, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        '''a = self.packageRegister
        commandClass = self.packageRegister'''
        commandName = self.package.packageName
        commandInstance = package.actionRegister.getCommandClass(self.package.packageName, "LoadInstance").commandClass
        commandInstance.setAppInstance(self)
        commandInstance.setPackageInstance(self.package.instance)
        commandInstance.hide()

        isSingleton = commandInstance.isSingleton()
        if isSingleton:
            # check if already registered
            docWindow = self.getDocWindows(commandName)
            if docWindow:
                #docWindow.show()
                #docWindow.onShow()
                return

        if commandInstance:
            # self._registerCommandInstance(CommandInstance)
            if settings is not None:
                commandInstance.restoreState(settings)
                if not self.package.main.restoreDockWidget(commandInstance):
                    # handle if ui state was not restored
                    pass
            else:
                self.package.main.instance.addDockWidget(commandInstance.defaultDockArea(), commandInstance)
                self.addDocWindows(commandName, commandInstance)
            #commandInstance.onShow()
        return commandInstance

    def loadDockWindow(self, commandName, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        '''a = self.packageRegister
        commandClass = self.packageRegister'''
        commandInstance = self.package.actionRegister.getCommandClass(self.package.packageName, commandName).commandClass
        commandInstance.setAppInstance(self.package.main)
        commandInstance.setPackageInstance(self.package.instance)
        commandInstance.hide()

        isSingleton = commandInstance.isSingleton()
        if isSingleton:
            # check if already registered
            docWindow = self.getDocWindows(commandName)
            if docWindow:
                #docWindow.show()
                #docWindow.onShow()
                return

        if commandInstance:
            # self._registerCommandInstance(CommandInstance)
            if settings is not None:
                commandInstance.restoreState(settings)
                if not self.package.main.restoreDockWidget(commandInstance):
                    # handle if ui state was not restored
                    pass
            else:
                self.package.main.instance.addDockWidget(commandInstance.defaultDockArea(), commandInstance)
                self.addDocWindows(commandName, commandInstance)
            #commandInstance.onShow()
        return commandInstance

class MenuCategory(object):
    def __init__(self, MenuBar, Title):
        self.menuCategory = MenuBar.addMenu(Title)


class MenuRegister(object):
    def __init__(self):
        #Will Be Able to make database version of this later
        self.menuDict = {}
        self.subMenuDict = {}
        self.menuOrder = ["File", "Edit", "ActiveWindow", "Tools", "Windows", "Help"]
        self.menuBar = QMenuBar()
        self.menuCategoryDict = {}
        self._storage = OrderedDict()
        self._menu = []

    def getPackageList(self):
        packagelist = []
        for name, item in enumerate(self.CommandRegister):
            packagelist.append(name)
        return packagelist

    def setMenuGeometry(self, Rectangle):
        self.menuBar.setGeometry(Rectangle)

    def setMenuObjectName(self, Name):
        self.menuBar.setObjectName(Name)

    def getPackageCommandList(self, packageName):
        commandList = []
        for CommandClass in self.CommandRegister[packageName]:
                commandList.append(CommandClass.name())
        return commandList

    def getCommandsClassByName(self, packageName, commandName):
        for CommandClass in self.CommandRegister[packageName]:
            if CommandClass.name() == commandName:
                return CommandClass
        return None

    def addMenuCategory(self, Name, Position):
        pass

    def getOrCreateMenu(menuBar, title):
        for child in menuBar.findChildren(QMenu):
            if child.title() == title:
                return child
        menu = QMenu(menuBar)
        menu.setObjectName(title)
        menu.setTitle(title)
        return menu

    def loadMenu(self):
        with open("menu.json") as f:
            self.MenuDict = json.load(f)

    def saveMenu(self):
        with open("menu.json", "w") as outfile:
            json.dump(self.MenuDict, outfile)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def getMenuBar(self):
        return self.menuBar

    def addSeparator(self):
        self._menu.append({"separator": True})

    def addEntry(self, name, title, callback=None, icon=None, parentEntry=None):
        if name not in self._menu:

            menu = OrderedDict()
            menu['name'] = name
            menu['title'] = title
            menu['icon'] = icon
            menu['callback'] = callback
            self._storage[name] = menu

            if parentEntry is not None and parentEntry in self._storage:
                self._storage[parentEntry]["sub_menu"] = menu
            else:
                self._menu.append(menu)
                self._storage[name] = menu

        return self

    def reset(self):
        self._storage.clear()
        self.menu.clear()

    def get(self):
        return self._menu

    def getToolClassByName(self, packageName, toolName, toolClass):
        registeredTools = GET_COMMANDS()
        for ToolClass in registeredTools[packageName]:
            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass
        return None

    def createToolInstanceByClass(self, packageName, toolName, toolClass):
        registeredTools = GET_COMMANDS()
        for ToolClass in registeredTools[packageName]:
            supportedSoftwares = ToolClass.supportedSoftwares()
            if "any" not in supportedSoftwares:
                if self.currentSoftware not in supportedSoftwares:
                    continue

            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass()
        return None

    def getRegisteredTools(self, classNameFilters=[]):
        if len(classNameFilters) == 0:
            return self._tools
        else:
            result = []
            for tool in self._tools:
                if tool.__class__.__name__ in classNameFilters:
                    result.append(tool)
            return result

    def invokeDockToolByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name)

        if toolClass is None:
            return
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        tool.show()
                        tool.onShow()
                        # Highlight window
                        #print("highlight", tool.uniqueName())
                        return tool

        ToolInstance = self.createToolInstanceByClass(packageName, name)
        if ToolInstance:
            #self.registerToolInstance(ToolInstance)
            self.dockWindowRegister.addDocWindows(name, ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            else:

                self.addDockWidget(ToolInstance.defaultDockArea(), ToolInstance)
            ToolInstance.setAppInstance(self.main)
            ToolInstance.setPackageInstance(self)
            ToolInstance.onShow()
        return ToolInstance


class ToolBarGroup(object):
    def __init__(self, instance, Title):
        self.name = Title
        self.toolBar = instance.addToolBar(Title)
        self.toolBar.setObjectName(Title)

    def getToolBar(self):
        return self.toolBar


class ToolBarRegister(object):
    def __init__(self):
        #Will Be Able to make database version of this later
        self.toolBarDict = {}
        self.toolBarGroupDict = {}
        self.toolBarGroup = {}

    def buildToolBar(self):
        self.toolBarDict = {}

        self.baseToolBar = []
        self.baseToolBar.append({"Action": "Add Action", "Package": "ProgramBase", "Command": "NewFile"})
        self.toolBarDict["ProgramBase"] = self.baseToolBar

        self.pyFlowToolBar = []
        self.pyFlowToolBar.append({"Action": "Add Action", "Package": "PyFlow", "Command": "NewFile"})
        self.pyFlowToolBar.append({"Action": "Add Action", "Package": "PyFlow", "Command": "OpenFile"})
        self.pyFlowToolBar.append({"Action": "Add Action", "Package": "PyFlow", "Command": "SaveFile"})
        self.toolBarDict["PyFlow"] = self.pyFlowToolBar

    def showToolBar(self, instance, ToolBarName, Location):
        #QtCore.Qt.TopToolBarArea
        toolbar = self.toolBarGroupDict[ToolBarName]
        instance.addToolBar(Location, toolbar)

    def updateToolBar(self, instance, ToolBarName):
        if ToolBarName not in self.toolBarGroupDict:
            newToolGroupBar = ToolBarGroup(instance, ToolBarName)
            newToolBar = newToolGroupBar.getToolBar()
            self.toolBarGroupDict[ToolBarName] = newToolBar
        else:
            newToolBar = self.toolBarGroupDict[ToolBarName]

        for order, toolCategory in enumerate(self.toolBarDict[ToolBarName]):
            if toolCategory["Action"] == "Add Action":
                Action = self.ActionRegister.getAction(toolCategory["Package"], toolCategory["Command"])
                newToolBar.addAction(Action)

    def getToolClassByName(self, packageName, toolName, toolClass):
        registeredTools = toolClass.GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass
        return None

    def createToolInstanceByClass(self, packageName, toolName, toolClass):
        registeredTools = toolClass.GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            supportedSoftwares = ToolClass.supportedSoftwares()
            if "any" not in supportedSoftwares:
                if self.currentSoftware not in supportedSoftwares:
                    continue

            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass()
        return None

    def getRegisteredTools(self, classNameFilters=[]):
        if len(classNameFilters) == 0:
            return self._tools
        else:
            result = []
            for tool in self._tools:
                if tool.__class__.__name__ in classNameFilters:
                    result.append(tool)
            return result

    def invokeDockToolByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name, DockTool)
        if toolClass is None:
            return
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        tool.show()
                        tool.onShow()
                        # Highlight window
                        #print("highlight", tool.uniqueName())
                        return tool

        ToolInstance = self.createToolInstanceByClass(packageName, name)
        if ToolInstance:
            #self.registerToolInstance(ToolInstance)
            self.dockWindowRegister.addDocWindows(name, ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            else:

                self.addDockWidget(ToolInstance.defaultDockArea(), ToolInstance)
            ToolInstance.setAppInstance(self.main)
            ToolInstance.setPackageInstance(self)
            ToolInstance.onShow()
        return ToolInstance


class KeyPressEventRegister(object):
    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        currentInputAction = InputAction(name="temp", actionType=InputActionType.Keyboard, key=event.key(), modifiers=modifiers)

        actionSaveVariants = InputManager()["App.Save"]
        actionNewFileVariants = InputManager()["App.NewFile"]
        actionLoadVariants = InputManager()["App.Load"]
        actionSaveAsVariants = InputManager()["App.SaveAs"]

        if currentInputAction in actionNewFileVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return

            EditorHistory().clear()
            historyTools = self._getRegisteredCommands(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()
            self.newFile()
            EditorHistory().saveState("New file")
            self.currentFileName = None
            self.modified = False
            self.updateLabel()
        if currentInputAction in actionSaveVariants:
            self.save()
        if currentInputAction in actionLoadVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return
            self.load()
        if currentInputAction in actionSaveAsVariants:
            self.save(True)


class DatabaseRegister(object):
    pass