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
from gpt4all import GPT4All
import openai

#PySide Imports
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QMdiSubWindow)
from PySide6 import QtGui

#Import Tables
from PackageManager.Packages.ProgramBase.Database.dbMaster import MasterTable
from PackageManager.Packages.XFiles.Resources import ICON_DIR

#Default Settings
basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"

class ChatGPT(QMdiSubWindow):
    def __init__(self, main, parent):
        super(ChatGPT, self).__init__()
        self.PackageName = "ChatGPT"
        self.setWindowTitle("ChatGPT 4 All")
        self.setWindowIcon(QtGui.QIcon(ICON_DIR + 'ChatGPT4All.jpeg'))

        self.ReferenceNumber_id = None
        self.main = main
        self.chatmodel = main.instance.chatmodel
        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmChatGPT.ui')
        self.ui = loader.load(uiFile, self)

        self. loadFormCommands()

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

        connectiondict = {}
        connectiondict["Location1"] = {"Base": "MainBase", "Session": "Location1", "DatabaseType": "mysql+pymysql",
                                       "Login": "", "Password": "", "Address": "127.0.0.1",
                                       "Port": "3306", "Schema": "PackageManager", "Key": None, "SSHTunnel": None,
                                       "SyncType": "ASAP"}

        self.sqlRegister.registarInstance(connectiondict["Location1"])
        self.sqlRegister.sqlDict["Location1"].createSession(base, name, dbtype, login, password, location, port,
                                                                   schema, key, sshTunnel)
        # This is the table coordinator
        self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Location1"].session
        self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].base
        self.session = self.sqlRegister.sqlDict["Location1"].session
        self.base = self.sqlRegister.sqlDict["Location1"].base

        self.sqlRegister.masterTable = "MasterTable"
        self.sqlRegister.masterFieldList = "MasterFieldList"

        # Database Query Test
        rows = self.session.query(MasterTable).count()

    def loadFormCommands(self):
        self.ui.cmdSubmitRequest.clicked.connect(self.on_cmdSubmitRequest_clicked)

    def loadFormData(self):
        pass

    def updateModel(self):
        path = r"C:\ChatGPT"
        self.chatmodel = GPT4All(model_name="nous-hermes-llama2-13b.Q4_0.gguf",
                             model_path=path)

    def on_cmdSubmitRequest_clicked(self):
        # Get the text from the text box
        question = self.ui.txtAskChatGPT.text()
        # Send the text to the GPT-3 API
        self.ui.txtChatReponse.appendPlainText(question)

        response = self.chatmodel.generate(question, max_tokens=255)
        # Add the response to the text box
        self.ui.txtChatReponse.appendPlainText(response)
        # Clear the request text box
        self.ui.txtAskChatGPT.clear()

    def comp(self, PROMPT, MaxToken=50, outputs=3):
        # using OpenAI's Completion module that helps execute
        # any tasks involving text
        response = openai.Completion.create(
            # model name used here is text-davinci-003
            # there are many other models available under the
            # umbrella of GPT-3
            model="text-davinci-003",
            # passing the user input
            prompt=PROMPT,
            # generated output can have "max_tokens" number of tokens
            max_tokens=MaxToken,
            # number of outputs generated in one call
            n=outputs
        )
        # creating a list to store all the outputs
        output = list()
        for k in response['choices']:
            output.append(k['text'].strip())
        return output