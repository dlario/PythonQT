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

import uuid
from Temp.version import *

from PySide6.QtCore import QPoint, QSignalMapper
from PySide6 import QtGui
from PySide6.QtWidgets import *

from PackageManager.UI.Canvas.UICommon import *
from PackageManager.UI.EditorHistory import EditorHistory
from PackageManager.UI.Utils.stylesheet import editableStyleSheet
from PackageManager.UI.Widgets.PreferencesWindow import PreferencesWindow
from PackageManager.Core.Database import SQL
from PackageManager.Core import Register

try:
    from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool
except:
    pass

from PackageManager.Packages.ProgramBase.UI.Forms.PackageBuilder import PackageBuilder

from PackageManager import GET_DEFAULT_PATHS
from PackageManager.ConfigManager import ConfigManager

import PackageManager.UI.resources
from PackageManager.Packages.ProgramBase.Resources import ICON_DIR

from PySide6.QtCore import (QFileInfo, QSettings, QSize, Qt)
from PySide6.QtGui import QKeySequence, QUndoStack, QAction, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PySide6.QtWidgets import QMdiArea
from PackageManager.Packages.ProgramBase.Database import DefaultData
from PackageManager.Packages.ProgramBase.Database import dbMaster

import openai
from gpt4all import GPT4All

from PackageManager import KeyFile
key = KeyFile.getKeys()
NOMICKEY = key['NOMIC']['NOMICKEY']
WhatsAppToken = key["WhatsApp"]["WhatsaAppToken"]
WhatsAppNumber = key["WhatsApp"]["WhatsAppNumber"]
openai.organization = key["OpenAI"]["OpenAIOrg"]
openai.api_key = key["OpenAI"]["OpenAIKey"]

promptactive = True

def generateRandomString(numSymbolds=5):
    result = ""
    for i in range(numSymbolds):
        letter = random.choice(ascii_letters)
        result += letter
    return result

def getOrCreateMenu(menuBar, title):
    for child in menuBar.findChildren(QMenu):
        if child.title() == title:
            return child
    menu = QMenu(menuBar)
    menu.setObjectName(title)
    menu.setTitle(title)
    return menu

def winTitle():
    return f"Enigma Machine v{currentVersion().__str__()}"

class PackageManager(QMainWindow):
    appInstance = None
    def __init__(self, parent=None):
        super(PackageManager, self).__init__(parent=parent)
        self.PackageName = "ProgramBase"
        self.mdiArea = QMdiArea()
        '''self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)'''
        self.setCentralWidget(self.mdiArea)

        self.uuid = uuid.uuid4()

        self.mdiArea.subWindowActivated.connect(self.updateWindowsMenus)

        self.currentSoftware = "standalone"
        self.currentSoftware = ""
        self._modified = False

        self.preferencesWindow = PreferencesWindow(self)
        settings = ConfigManager().getSettings("APP_STATE")
        editableStyleSheet(self)

        self.setFocusPolicy(Qt.StrongFocus)

        self.edHistory = EditorHistory(self)
        self.edHistory.statePushed.connect(self.historyStatePushed)

        self.setWindowTitle(winTitle())
        self.undoStack = QUndoStack(self)

        self.setContentsMargins(1, 1, 1, 1)
        #self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        #self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks)

        defaultpaths = GET_DEFAULT_PATHS()
        self.packagelist = ["ProgramBase", "ProjectList", "Template",
                            "PyFlowPkg", "XFiles", "StockTrader", "TaskManager"]
        self.windowMapper = QSignalMapper()

        # Loads the packages ready to be initiated
        self.packageRegister = Register.loadPackageRegister(defaultpaths, self.packagelist)



        # Creates the base packages
        self.commandRegister = Register.LoadPackages(self, self.packageRegister)
        # The package register is now in commandRegister
        # todo create database if it does not exist
        self.sqlRegister = SQL.Register(self)

        connectiondict = {}
        connectiondict["Location1"] = {"Base": "MainBase", "Session": "Location1", "DatabaseType": "mysql+pymysql",
                                       "Login": key["MySQL"]["Login"], "Password": key["MySQL"]["Password"], "Address": "127.0.0.1",
                                       "Port": "3306", "Schema": "projectmanager", "Key": None, "SSHTunnel": None,
                                       "SyncType": "ASAP"}

        self.sqlRegister.registarInstance(connectiondict["Location1"])
        self.sqlRegister.sqlDict["Location1"].loadTables("ProgramBase")
        self.sqlRegister.connectDatabase("Location1")

        connectiondict["Location2"] = {"Base": "MainBase", "Session": "Location2", "DatabaseType": "sqlite",
                                       "Login": None, "Password": None,
                                       "Address": r"D:\Dropbox\ProjectManager\ProjectManager.db",
                                       "Port": None, "Schema": None, "Key": None, "SSHTunnel": None, "SyncType": "ASAP"}

        self.sqlRegister.registarInstance(connectiondict["Location2"])
        self.sqlRegister.sqlDict["Location2"].loadTables("ProgramBase")
        self.sqlRegister.connectDatabase("Location2")

        self.sessionList = {}
        self.baseList = {}

        # This is the table coordinator
        self.sessionList[1] = self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Location1"].session
        self.baseList[1] = self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].base
        self.sessionList[2] = self.sqlRegister.sqlDict["Location2"].session
        self.baseList[2] = self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location2"].base
        self.sqlRegister.masterTable = dbMaster.MasterTable

        self.session = self.sessionList[1]
        self.base = self.baseList[1]

        self.sqlRegister.saveSession("ProgramBase", connectiondict)
        self.sqlRegister.createMasterTableidDict("Location1")

        path = r"C:\ChatGPT"
        try:
            self.chatmodel = GPT4All(model_name="nous-hermes-llama2-13b.Q4_0.gguf", model_path=path)
        except:
            self.chatmodel = None

        # Create Base Menus
        self.InstanceDict = {}
        instance1 = self.packageRegister.createPackageInstance("ProgramBase", self, None)()
        self.InstanceDict[instance1.uuid] = self.commandRegister.registerPackageInstance("ProgramBase", instance1, None,
                                                                                         None)

        instance2 = self.packageRegister.createPackageInstance("PyFlowPkg", self.InstanceDict[instance1.uuid], None)()
        self.InstanceDict[instance2.uuid] = self.commandRegister.registerPackageInstance("PyFlowPkg", instance2,
                                                                                         self.InstanceDict[
                                                                                             instance1.uuid], None)
        self.PyFlow = self.InstanceDict[instance2.uuid]

        for package in self.packagelist:
            if package not in ["ProgramBase", "PyFlowPkg"]:
                instance = self.loadPackage(package, instance1.uuid, None)
                self.sqlRegister.sqlDict["Location1"].loadTables(package)
                self.sqlRegister.sqlDict["Location2"].loadTables(package)

        self.currentPackage = self.InstanceDict[instance1.uuid]
        self.currentinstance = instance1
        self.main = self

        self.setIcon(QtGui.QIcon(ICON_DIR + "ProgramLogo.png"))
        self.setWindowIcon(self.Icon)

        self.currentTempDir = ""

        self.setMouseTracking(True)

        self._currentFileName = ''
        self.currentFileName = None
        self.currentPackageName = None
        self.currentChildWindow = None

        self.createStatusBar()
        self.createWindowActions()

        self.refreshMenu(self.currentPackage)

        self.toolBarGroupDict = {}
        self.refreshToolBar(self.currentPackage)
        self.toolbar = ""

        # the first part is just to show that its part of the instance dict
        # the second uuid is where the information comes from.
        self.ribbonBar = None
        self.refreshRibbonBar()

        tempDirPath = ConfigManager().getPrefsValue("PREFS", "General/TempFilesDir")
        settings = ConfigManager().getSettings("APP_STATE")

        #self.setStyle(QStyleFactory.get("plastique"))
        self.setStyleSheet(editableStyleSheet().getStyleSheet())

    def updateDatabaseController(self):
        self.sqlRegister.updateDatabaseController()

    def dropTables(self):
        defaultdata = DefaultData.defaultData()

        for item, value in enumerate(defaultdata):
            table = defaultdata[value]["Table"]
            try:
                self.session.query(table).delete()
                self.session.commit()
            except:
                self.session.rollback()

    def setIcon(self, Icon):
        self.Icon = Icon

    def getIcon(self):
        return self.Icon

    def loadPackage(self, packagename, mainuuid, parent=None):
        instance = self.packageRegister.createPackageInstance(packagename, self.InstanceDict[mainuuid], parent)()
        self.InstanceDict[instance.uuid] = self.commandRegister.registerPackageInstance(packagename, instance,
                                                                                        self.InstanceDict[mainuuid],
                                                                                        parent)
        return instance
    def loadPackage2(self, PackageName):
        # Check if Loaded
        x = PackageName
        if PackageName not in self.commandRegister.instanceList:
            self.commandRegister.createPackageInstance(PackageName, self, self)
        self.currentPackage = self.commandRegister.instanceList[PackageName]
        self.currentinstance = self.commandRegister.instanceList[PackageName].instance
        self.refreshStuff(PackageName, self.commandRegister.instanceList[PackageName])

    def refreshStuff(self, package, instanceregister, uuid=None):
        # If the instance does not exist the base package information is loaded.
        if uuid:
            self.currentinstance = self.commandRegister.getInstancebyUUID(uuid)
        else:
            if instanceregister:
                self.currentinstance = instanceregister.instance
            else:
                self.currentinstance = self.commandRegister.getInstancebyPackageName(package)

        self.refreshMenu(instanceregister)
        self.refreshRibbonBar()
        self.refreshToolBar(instanceregister)

    def refreshMenu(self, instance):
        self.menuBar = QMenuBar()

        try:
            menuDict = instance.getMenuLayout()
            menuDict["Packages"] = []

            menuOrder = instance.getMenuOrder()
            if "Packages" not in menuOrder:
                menuOrder.insert(0, "Packages")
        except:
            menuDict["Packages"] = []
            menuOrder = ["Packages"]

        for menuCategory in menuOrder:
            self.menuBar.addMenu(menuCategory)
            if menuCategory == "Packages":
                self.windowMenu = getOrCreateMenu(self.menuBar, menuCategory)
                self.windowMenu.clear()
                for packagename in self.packagelist:
                    action = QAction(packagename, self, triggered=(lambda checked, x=packagename: self.loadPackage2(x)))
                    self.windowMenu.addAction(action)
            else:
                mbar = getOrCreateMenu(self.menuBar, menuCategory)
                if menuCategory in menuDict:
                    for menuItem in menuDict[menuCategory]:
                        self.addMenuItem(mbar, menuItem, self.currentinstance)

        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.setMenuBar(self.menuBar)

    def addMenuItem(self, mBar, mDict, instance):
        if mDict["Action"] == "Add Action":
            try:
                a = self.commandRegister.instanceList[mDict["Package"]]
                b = a.actionRegister
                menuAction = b.getAction(mDict["PackageGroup"], mDict["Command"])

                if menuAction:
                    menuAction.setInstance(self, instance)

                try:
                    mBar.addAction(menuAction)
                except:
                    a = mDict["Package"]
                    b = mDict["Command"]
                    c = mDict["PackageGroup"]
            except:
                pass

        if mDict["Action"] == "Add Separator":
            pass
            '''menuAction.setSeparator(True)
            mBar.addAction(menuAction)'''
        if mDict["Action"] == "Add Children":
            pass

    def refreshRibbonBar(self):
        if self.ribbonBar:
            self.ribbonBar.hide()
        self.ribbonBar = self.currentPackage.dockWindowRegister.getDocWindows("RibbonBar")
        self.ribbonBar.show()

    def refreshToolBar(self, instance):

        if instance is None:  # The Package is selected but a file has not be loaded/started

            package = "Root"
            toolDict = self.getToolBarLayout()
            toolOrder = ["Packages", "Tools"]
            # actionRegister = self.actionRegister

        else:  # There is an active instance
            package = "PyFlow"
            # toolDict = instance.getToolBarLayout()
            # actionRegister = self.actionRegister

    def updateToolBar(self, tBar, tDict, actionRegister):
        if tDict["Action"] == "Add Action":
            toolAction = self.actionRegisterDict[tDict["Package"]].getAction(tDict["PackageGroup"], tDict["Command"])
            try:
                toolAction.setInstance(tDict["Instance"])
                tBar.addAction(toolAction)
            except:
                pass

        if tDict["Action"] == "Add Separator":
            pass
            '''menuAction.setSeparator(True)
            mBar.addAction(menuAction)'''
        if tDict["Action"] == "Add Children":
            pass

    def historyStatePushed(self, state):
        if state.modifiesData():
            self.modified = True
            self.updateLabel()
        # print(state, state.modifiesData())

    @property
    def modified(self):
        return self._modified

    @modified.setter
    def modified(self, value):
        self._modified = value
        self.updateLabel()

    def updateLabel(self):
        label = "Untitled"
        if self.currentFileName is not None:
            if os.path.isfile(self.currentFileName):
                label = os.path.basename(self.currentFileName)
        if self.modified:
            label += "*"
        self.setWindowTitle("{0} - {1}".format(winTitle(), label))

    def getTempDirectory(self):
        """Returns unique temp directory for application instance.

        This folder and all its content will be removed from disc on application shutdown.
        """
        if self.currentTempDir == "":
            # create app folder in documents
            # random string used for cases when multiple instances of app are running in the same time
            tempDirPath = ConfigManager().getPrefsValue("PREFS", "General/TempFilesDir")
            if tempDirPath[-1:] in ('/', '\\'):
                tempDirPath = tempDirPath[:-1]
            self.currentTempDir = "{0}_{1}".format(tempDirPath, generateRandomString())

            if not os.path.exists(self.currentTempDir):
                os.makedirs(self.currentTempDir)
        return self.currentTempDir

    def showPreferencesWindow(self):
        self.preferencesWindow.show()

    def getToolbar(self):
        return self.toolBar

    def getRibbonbar(self):
        return self.ribbonBar

    @property
    def currentFileName(self):
        return self._currentFileName

    @currentFileName.setter
    def currentFileName(self, value):
        self._currentFileName = value
        self.updateLabel()

    def createPopupMenu(self):
        pass

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def newFile(self, MDIClass):
        child = self.createMdiChild(MDIClass)
        child.newFile()
        child.show()

    def createMdiChild(self, MDIClass):
        '''child = MdiChild()
        self.mdiArea.addSubWindow(child)'''

        child = MDIClass
        self.mdiArea.addSubWindow(child)
        self.mdiArea.setBaseSize(200, 200)
        '''child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)'''
        return child

    def newFileFromUi(self, MDIClass):
        #todo: add splash screen logo.
        pixmap = QPixmap(ICON_DIR + "/ProgramLogo - Large.png")
        splash = QSplashScreen(pixmap)
        splash.show()
        child = MDIClass.ui
        MDIClass.uuid = uuid.uuid4()
        self.commandRegister.createMDIPackageInstance(MDIClass.PackageName, self, MDIClass, None)
        self.mdiArea.addSubWindow(MDIClass) #This makes it pop out
        #self.mdiArea.addSubWindow(child) #This breaks everything
        child.show()
        #splash.finish(child)

    def newSubFormFromUi(self, MDIClass):
        child = MDIClass.ui
        MDIClass.uuid = uuid.uuid4()
        self.commandRegister.createMDIPackageInstance(MDIClass.PackageName, self, MDIClass, None)
        #self.mdiArea.addSubWindow(MDIClass) #This makes it pop out
        self.mdiArea.addSubWindow(child) #This breaks everything
        child.show()

    def createPackagebBuilder(self):
        self.newFileFromUi(PackageBuilder.PackageBuilder(self))

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()

    def about(self):
        QMessageBox.about(self, "The Enigma Machine",
                          "Welcome to the Enimga Machine.  A tool for creating programs and applications.")

    def createWindowActions(self):

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows",
                               triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self,
                                  statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                                   shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

    def updateWindowsMenus(self):

        hasMdiChild = (self.activeMdiChild() is not None)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        # self.nextAct.setEnabled(hasMdiChild)
        # self.previousAct.setEnabled(hasMdiChild)
        # self.separatorAct.setVisible(hasMdiChild)

        if self.currentChildWindow != self.mdiArea.activeSubWindow():
            self.currentChildWindow = self.mdiArea.activeSubWindow()
            # self.refreshMenu(self.mdiArea.activeSubWindow())

    def updateWindowMenu(self):
        menu = self.menuBar
        self.windowMenu = getOrCreateMenu(menu, "Windows")

        self.windowMenu.clear()

        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        # self.windowMenu.addAction(self.nextAct)
        # self.windowMenu.addAction(self.previousAct)
        # self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        # self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            try:
                text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
                if i < 9:
                    text = '&' + text
            except:
                text = "%d %s" % (i + 1, "filename")
                if i < 9:
                    text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def loadDockWindow(self, packageName, commandName, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        '''a = self.packageRegister
        commandClass = self.packageRegister'''

        if commandName == "RibbonBar":
            commandName = "Logger"

        commandClass = self.currentPackage.actionRegister.getCommandClass(packageName, commandName).commandClass
        commandClass.setAppInstance(self.main)
        commandClass.setPackageInstance(self)

        if commandClass is None:
            return
        isSingleton = commandClass.isSingleton()
        if isSingleton:
            # check if already registered
            docWindow = self.currentPackage.dockWindowRegister.getDocWindows(commandName)
            if docWindow:
                docWindow.show()
                docWindow.onShow()
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

    def writeSettings(self):
        settings = QtCore.QSettings('Enigma Design Solutions', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        # print(activeSubWindow.uuid)
        if activeSubWindow:
            try:
                packagename = activeSubWindow.PackageName

                print(packagename, activeSubWindow.uuid)
                instancedata = self.commandRegister.getInstancebyUUID(activeSubWindow.uuid)

                self.refreshStuff(packagename, instancedata)
                return activeSubWindow.widget()
            except:
                pass
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            try:
                if window.widget().currentFile() == canonicalFilePath:
                    return window
            except:
                pass
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            print("Window Set Active")
            self.registerDict = {}
            self.registerDict["Action"] = window.getActionRegister()
            self.registerDict["RibbonBar"] = window.getRibbonBarRegister()
            self.registerDict["ToolBar"] = window.getToolBarRegister()
            self.registerDict["Menu"] = window.getMenuRegister()
            self.registerDict["DockWindow"] = window.getDockBarRegister()
            self.registerDict["App"] = window
            self.refreshMenu(self.registerDict["App"])
            self.mdiArea.setActiveSubWindow(window)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = PackageManager()
    mainWin.show()
    sys.exit(app.exec_())
