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

import os
import json
import uuid

from string import ascii_letters
import random

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import (QSize, Qt, QPoint)
from PySide6.QtCore import (QFile, QFileInfo, QTextStream)
from PySide6.QtWidgets import (QApplication, QFileDialog, QMdiSubWindow, QMessageBox)

from PackageManager.Core.MDIDocument import MDIMain, MDIChild
from PackageManager.Core.PathsRegistry import PathsRegistry
from Temp.version import *
from PackageManager.UI.EditorHistory import EditorHistory

try:
    from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool
except:
    pass

from PackageManager.ConfigManager import ConfigManager
from PackageManager.Packages.ProgramBase.Database.dbMaster import *
from PackageManager.Packages.ProjectList.Database.dbFinance import Currency
from PackageManager.Packages.StockTrader.Database import DefaultData

#Database Import

def winTitle():
    return "Project List v{0}".format(currentVersion().__str__())
def generateRandomString(numSymbolds=5):
    result = ""
    for i in range(numSymbolds):
        letter = random.choice(ascii_letters)
        result += letter
    return result

class MDIMain(MDIMain):
    appInstance = None
    def __init__(self, main, parent=None):
        super(MDIMain, self).__init__(parent=parent)

        self.uuid = uuid.uuid4()
        self.parent = parent
        self.main = main
        settings = ConfigManager().getSettings("APP_STATE")
        self.currentFileName = None
        self.initDatabase()

    def about(self):
        QMessageBox.about(self, "About Template",
                          "The <b>Template</b> is a template for making packages "
                          "change this accordingly.")

    def newFile(self):
        pass

    def CreateInstance(self, main, parent):
        instance = MDIChild(main, parent)
        return instance

    def close(self):
        pass

    def closeAll(self):
        pass

    def open(self):
        pass

    def initDefaultData(self):
        class Market(MainBase):
            __tablename__ = 'lstmarket'
            id = Column(Integer, primary_key=True)
            NameText = Column(String(50))

        listCurrency = ["CAD", "USD", "EUR", "GBP", "AUD", "NZD", "JPY", "CHF"]
        for currency in listCurrency:
            newCurrency = Currency(NameText=currency)
            self.session.add(newCurrency)
            self.session.commit()

    def load(self):
        name_filter = "Graph files (*.pygraph)"
        savepath = QFileDialog.getOpenFileName(filter=name_filter)

    def loadFile(self, filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)
            self.loadFromData(data, clearHistory=True)
            self.currentFileName = filePath
            EditorHistory().saveState("Open {}".format(os.path.basename(self.currentFileName)))

    def save(self, save_as=False):
        if self.parent.activeMdiChild():
            self.parent.statusBar().showMessage("File saved", 2000)

            if save_as:
                name_filter = "Graph files (*.pygraph)"
                savepath = QFileDialog.getSaveFileName(filter=name_filter)
                if type(savepath) in [tuple, list]:
                    pth = savepath[0]
                else:
                    pth = savepath
                if not pth == '':
                    self.currentFileName = pth
                else:
                    self.currentFileName = None
            else:
                if self.currentFileName is None:
                    name_filter = "Graph files (*.pygraph)"
                    savepath = QFileDialog.getSaveFileName(filter=name_filter)
                    if type(savepath) in [tuple, list]:
                        pth = savepath[0]
                    else:
                        pth = savepath
                    if not pth == '':
                        self.currentFileName = pth
                    else:
                        self.currentFileName = None

            if not self.currentFileName:
                return False

            if not self.currentFileName.endswith(".pygraph"):
                self.currentFileName += ".pygraph"

            if not self.currentFileName == '':
                with open(self.currentFileName, 'w') as f:
                    saveData = self.MDIChild.graphManager.get().serialize()
                    json.dump(saveData, f, indent=4)
                print(str("// saved: '{0}'".format(self.currentFileName)))
                self.modified = False
                self.updateLabel()
                return True

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def initDatabase(self):
        # Loading The Database
        self.sqlRegister = self.main.instance.sqlRegister
        # This is just an example of how to register a database
        base = "MainBase"
        name = "self.session"
        dbtype = "mysql+pymysql"
        login = ""
        password = ""
        location = "127.0.0.1"
        port = "3306"
        schema = "PackageManager"
        key = None,
        sshTunnel = None

        self.sqlRegister.registarInstance("Location1", "StockMarket", "ASAP", self)
        self.sqlRegister.sqlDict["Location1"].createSession(base, name, dbtype, login, password, location, port,
                                                                   schema, key, sshTunnel)
        # This is the table coordinator
        self.sqlRegister.masterself.session = self.sqlRegister.sqlDict["Location1"].self.session
        self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].base
        self.session = self.sqlRegister.sqlDict["Location1"].self.session
        self.base = self.sqlRegister.sqlDict["Location1"].base

        self.sqlRegister.masterTable = "MasterTable"
        self.sqlRegister.masterFieldList = "MasterFieldList"

    def updateDatabaseController(self):
        self.sqlRegister.updateDatabaseController(self)

    def dropTables(self):
        defaultdata = dbAllListsDefaultData.defaultData()

        for item, value in enumerate(defaultdata):
            table = defaultdata[value]["Table"]
            try:
                self.session.query(table).delete()
                self.session.commit()
            except:
                self.session.rollback()

    def updateDatabaseController(self):
        self.sqlRegister.updateDatabaseController(self)

    def dropTables(self):
        defaultdata = dbAllListsDefaultData.defaultData()

        for item, value in enumerate(defaultdata):
            table = defaultdata[value]["Table"]
            try:
                self.session.query(table).delete()
                self.session.commit()
            except:
                self.session.rollback()

class MDIChild(QMdiSubWindow):
    sequenceNumber = 1
    newFileExecuted = QtCore.Signal(bool)
    fileBeenLoaded = QtCore.Signal()

    def __init__(self, main, parent):
        super(MDIChild, self).__init__()
        settings = ConfigManager().getSettings("APP_STATE")
        self.PackageName = "Template-MDIChild"
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        #self.instance = instance
        self.main = main
        self.parent = parent

        self._modified = False
        self.currentFileName = "David"
        self.edHistory = EditorHistory(self)
        self.edHistory.statePushed.connect(self.historyStatePushed)
        self.undoStack = QtGui.QUndoStack(self)

        self.canvasWidget.setObjectName("canvasWidget")
        self.setWidget(self.canvasWidget)

    def CreateInstance(main, parent):
        instance = MDIChild(main, parent)
        return instance

    def newFile(self, keepRoot=True):
        #this does not belong here.  only in the parent
        self.isUntitled = True
        self.curFile = "document%d.txt" % MDIChild.sequenceNumber
        MDIChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')
        # broadcast
        try:
            self.newFileExecuted.emit(keepRoot)
            self.onRequestClearProperties()
        except:
            pass

        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "MDI","Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.document().contentsChanged.connect(self.documentWasModified)

        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                                "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def closeEvent(self, event):
        pass
        '''if self.maybeSave():
            event.accept()
        else:
            event.ignore()'''

    def maybeSave(self):
        if self.document().isModified():
            ret = QMessageBox.warning(self, "MDI",
                                      "'%s' has been modified.\nDo you want to save your "
                                      "changes?" % self.userFriendlyCurrentFile(),
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

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

        This folder and all it's content will be removed from disc on application shutdown.
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


    def loadFromFileChecked(self, filePath):
        shouldSave = self.shouldSave()
        if shouldSave == QMessageBox.Yes:
            self.save()
        elif shouldSave == QMessageBox.Discard:
            return
        self.loadFromFile(filePath)
        self.modified = False
        self.updateLabel()

    def loadFromData(self, data, clearHistory=False):

        # check first if all packages we are trying to load are legal
        missedPackages = set()

        if clearHistory:
            EditorHistory().clear()
            historyTools = self.getRegisteredTools(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()

        self.newFile(keepRoot=False)
        # load raw data
        self.fileBeenLoaded.emit()
        self.updateLabel()
        PathsRegistry().rebuild()

    @property
    def currentFileName(self):
        return self._currentFileName

    def loadFromFile(self, filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)
            self.loadFromData(data, clearHistory=True)
            self.currentFileName = filePath
            EditorHistory().saveState("Open {}".format(os.path.basename(self.currentFileName)))
        return True

    def load(self):
        name_filter = "Graph files (*.pygraph)"
        savepath = QFileDialog.getOpenFileName(filter=name_filter)
        if type(savepath) in [tuple, list]:
            fpath = savepath[0]
        else:
            fpath = savepath
        if not fpath == '':
            self.loadFromFile(fpath)

    def closeEvent(self, event):

        shouldSave = self.shouldSave()
        if shouldSave == QMessageBox.Yes:
            if not self.save():
                event.ignore()
                return
        elif shouldSave == QMessageBox.Discard:
            event.ignore()
            return

        EditorHistory().shutdown()

        settings = ConfigManager().getSettings("APP_STATE")

        # clear file each time to capture opened dock tools
        settings.clear()
        settings.sync()

        settings.beginGroup('Editor')
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.endGroup()


        #PyFlow.appInstance = None

        QMainWindow.closeEvent(self, event)

    @currentFileName.setter
    def currentFileName(self, value):
        self._currentFileName = value
        self.updateLabel()

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QtCore.QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QtCore.QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())