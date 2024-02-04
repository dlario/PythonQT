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

#PySide Imports
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QMdiSubWindow)

#Other Programs

#Scripts

#Database

#Import Tables
from PackageManager.Packages.ProgramBase.Database.dbMaster import MasterTable

#Addon Programs

#Default Settings
basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"


from PackageManager.Packages.XFiles.Resources import ICON_DIR

class frmTemplate(QMdiSubWindow):
    def __init__(self, main, parent):
        super(frmTemplate, self).__init__()
        self.PackageName = "Template"
        self.setWindowTitle("Template")
        self.setWindowIcon(ICON_DIR + 'ProgramLogo.png')

        self.ReferenceNumber_id = None
        self.main = main

        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmTemplate.ui')
        self.ui = loader.load(uiFile, self)

        self.initDatabase()
        self.loadFormCommands()
        self.loadFormData()

        self.initCommands()

    def initCommands(self):
        pass

    def initDatabase(self):
        # Loading The Database
        self.sqlRegister = self.main.instance.sqlRegister
        # This is just an example of how to register a database
        base = "MainBase"
        name = "Session"
        dbtype = "mysql+pymysql"
        login = ""
        password = ""
        location = "127.0.0.1"
        port = "3306"
        schema = "PackageManager"
        key = None,
        sshTunnel = None

        self.sqlRegister.registarInstance("Template", "ProjectList", "ASAP", self)
        self.sqlRegister.sqlDict["Template"].createSession(base, name, dbtype, login, password, location, port,
                                                                   schema, key, sshTunnel)
        # This is the table coordinator
        self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Template"].session
        self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Template"].base
        self.session = self.sqlRegister.sqlDict["Template"].session
        self.base = self.sqlRegister.sqlDict["Template"].base

        self.sqlRegister.masterTable = "MasterTable"
        self.sqlRegister.masterFieldList = "MasterFieldList"

        # Database Query Test
        rows = self.session.query(MasterTable).count()

    def setSessions(self, Location):
        self.session = self.sqlRegister.sqlDict[Location].session
        self.base = self.sqlRegister.sqlDict[Location].base

        self.sessions["Master"] = self.sqlRegister.sqlDict[Location].session

    def loadFormCommands(self):
        pass
        #self.ui.cmdAddNewActivity.clicked.connect(self.AddNewActivity)
        #self.ui.cmdLoadExcel.clicked.connect(self.on_cmdLoadExcel_clicked)
        #self.ui.cmdLoadCurrentProject.clicked.connect(self.on_cmdLoadCurrentProject_clicked)
        #self.ui.cmdSyncExcel.clicked.connect(self.on_cmdSyncExcel_clicked)

    def loadFormData(self):
        pass