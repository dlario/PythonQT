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

import datetime
import ast
import os
import shutil
#import subprocess
import inspect
import importlib
import re

from importlib_metadata import distributions
import types
import pkgutil
import openai
from heyoo import WhatsApp
import pyperclip

promptactive = True
openai.organization = ""
openai.api_key = ""

from PackageManager import Packages
from PackageManager import Functions

from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import QTreeWidgetItem, QComboBox, QFileDialog, QMdiSubWindow, QListWidgetItem, QDialog
from PySide6.QtGui import QIcon, QFontMetrics
from PySide6.QtCore import QSize  # Because Pyside hijacked from pyqt
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PackageManager.UI.Widgets.InputDialog import InputDialog
from PackageManager.UI.Widgets.PopUpWindows import RibbonBarDialog
from PackageManager.UI.Widgets import TreeView

from PackageManager.Packages.ProgramBase.Commands import RESOURCES_DIR
RESOURCES_DIR3 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UI/resources/")

#from PySide6.uic import loadUiType, loadUi
from PySide6 import QtUiTools
loader = QtUiTools.QUiLoader()

path = os.path.dirname(os.path.abspath(__file__))
packageRoot = Packages.__path__[0]

uiFile = os.path.join(path, 'PackageBuilder.ui')
#WindowTemplate, TemplateBaseClass = loadUiType(uiFile)


class TableComboModel(QComboBox):
    #Should combine with to customWidgets
    #currentIndexChanged2 = pyqtSignal([dict])

    def __init__(self, parent, *args, **kwargs):
        super(TableComboModel, self).__init__(parent)
        #super(ComboModel, self).currentIndexChanged[dict].connect(self.currentIndexChangedDictionary)

        self.setModel(kwargs['dataModel'])
        self.setModelColumn(1)
        self.column = kwargs['column']
        self.row = kwargs['row']
        self.id = kwargs['id']

        self.dataout = {}
        self.dataout['id'] = kwargs['id']
        self.dataout['column'] = kwargs['column']
        self.dataout['row'] = kwargs['row']
        self.dataout['dataModel'] = kwargs['dataModel']
        self.newItemName = ""

        #for key in kwargs:
        #    print("another keyword arg: %s: %s" % (key, kwargs[key]))

        #self.currentIndexChanged.connect(self.currentIndexChangedDictionary)
        self.currentIndexChanged.connect(self.on_currentIndexChanged)
        self.currentIndexChanged.connect(self.currentIndexChangedDictionary)
        self.editTextChanged.connect(self.on_newInformation)
        self.setEditable(True)

    def column(self):
        return self.x

    def row(self):
        return self.y

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.dbIds)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    def setValue(self, index, column=0):
        for row in range(self.model().rowCount()):
            if str(self.model().index(row, column).data()) == str(index):
                #print(self.model().index(row, 0).data(), index)
                self.setCurrentIndex(row)
                break

    def data(self, index, role=QtCore.Qt.DisplayRole):
        #print('ComboModel data')
        if not index.isValid() or (role != QtGui.Qt.DisplayRole and role != QtGui.Qt.EditRole):
            print('ComboModel return invalid QVariant')
            return QtCore.QVariant()
        if index.column() == 0:
            return QtCore.QVariant(self.dbIds[index.row()])
        if index.column() == 1:
            return QtCore.QVariant(self.dbValues[index.row()])
        print('ComboModel return invalid QVariant')
        return QtCore.QVariant()

    def currentIndexChangedDictionary(self, index):
        #print("Combo Index changed2:", index)
        #self.dataout['index'] = index
        self.dataout['value'] = self.dataout['dataModel'].index(index, 0).data()
        #self.currentIndexChanged2.emit(self.dataout)

    def on_newInformation(self, newName):
        if 1==2:
            if newName != "":
                self.newItemName = newName
            else:
                #Create a new model that has old and new data
                cmbTableModel = QStandardItemModel(0, 1, self)
                cmbTableModel.setItem(0, 1, QStandardItem(self.newItemName))

                for row in range(self.dataout['dataModel'].rowCount()):
                    cmbTableModel.setItem(row+1, 1, QStandardItem(self.dataout['dataModel'].index(row,1).data()))

                self.setModel(cmbTableModel)

    def on_currentIndexChanged(self, index):
        pass
        #print("Combo Index changed:", index) #, self.sender().x(), self.y)
        #self.currentIndexChanged2.emit(self.dataout)


class PackageBuilder(QMdiSubWindow):
    def  __init__(self, main, parent=None):
        super().__init__(None)

        self.ui = loader.load(uiFile)
        self.PackageName = "PackageBuilder"
        self.actionRegister = None
        self.main = main
        self.defaultfolderlist = ["Commands", "FunctionLibrary", "Nodes", "Pins", "PrefsWidgets", "Tools", "UI"]
        packageRoot = Packages.__path__[0]
        self.ui.txtPackageFolderLocation.setText(packageRoot)

        self.packagelistmodel = QStandardItemModel(0, 1)
        rowcount = 0
        self.packageDict = {}
        self.functiondict = {}
        self.commanddict = {}
        self.filecommandDict = {}
        self.pindefs = {}
        self.pindefs["Inputs"] = {}
        self.pindefs["Outputs"] = {}

        self.codeDict = {}
        self.codeList = []
        self.pindata = {}
        self.selectedPinName = ""
        self.selectedPinDir = ""
        self.workingFile = ""

        packageRoot = Packages.__path__[0]
        for directories in os.listdir(packageRoot):
            if directories[1] != "_":
                self.packagelistmodel.setItem(rowcount, 0, QStandardItem(directories))
                rowcount += 1

        self.packagelistModelproxy = QSortFilterProxyModel()
        self.packagelistModelproxy.setSourceModel(self.packagelistmodel)

        self.ui.lstPackages.setModel(self.packagelistModelproxy)
        self.ui.lstPackages.setModelColumn(1)
        self.ui.lstPackages.clicked.connect(self.onSelectPackage)
        self.ui.cmdUpdateInit.clicked.connect(self.on_cmdUpdateInit_clicked)

        self.ui.cmdOpenPackageFolder.clicked.connect(self.onOpenPackageFolder)
        self.ui.txtPackageFilter.textChanged.connect(self.onChangeFilterValue)
        self.ui.tvPackageItems.header().hide()

        self.ui.tvLoadedApps.clear()

        for d in distributions():
            parent = QTreeWidgetItem()
            parent.setText(0, f"{d.metadata['Name']}") #=={d.version}
            self.ui.tvLoadedApps.addTopLevelItem(parent)

        self.newfunctiondict = {}
        self.ui.tvLoadedApps.itemClicked.connect(self.on_tvLoadedApps_itemClicked)

        #self.ui.tblFInputPins.selectionModel().selectionChanged.connect(self.on_tblFInputPins_Changed)
        self.ui.tblFInputPins.clicked.connect(self.on_tblFInputPins_clicked)

        #self.ui.tblFOutputPins.selectionModel().selectionChanged.connect(self.on_tblFOutputPins_Changed)
        self.ui.tblFOutputPins.clicked.connect(self.on_tblFOutputPins_clicked)
        self.ui.tvPackageItems.itemClicked.connect(self.on_tvPackageItems_clicked)
        self.ui.cmdCreatePackage.clicked.connect(self.on_cmdCreatePackage_clicked)

        self.ui.cmdCommandAddSmallIcon.clicked.connect(self.on_cmdCommandAddSmallIcon_clicked)
        self.ui.cmdCommandAddMediumIcon.clicked.connect(self.on_cmdCommandAddMediumIcon_clicked)
        self.ui.cmdCommandAddLargeIcon.clicked.connect(self.on_cmdCommandAddLargeIcon_clicked)

        self.ui.cmdNewCommand.clicked.connect(self.on_cmdNewCommand_clicked)
        self.ui.cmdSaveCommand.clicked.connect(self.on_cmdSaveCommand_clicked)
        self.ui.cmdSaveAsCommand.clicked.connect(self.on_cmdSaveAsCommand_clicked)
        self.ui.cmdWriteCommand.clicked.connect(self.on_cmdWriteCommand_clicked)

        #self.ui.dteCommandRevisionDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.cmdAddCommandRevision.clicked.connect(self.on_cmdAddCommandRevision_clicked)
        self.onPinScan()

        self.ui.rdoCommandDT.clicked.connect(self.on_rdoCommandDT_clicked)
        self.ui.rdoCommandST.clicked.connect(self.on_rdoCommandST_clicked)
        self.ui.rdoCommandDialog.clicked.connect(self.on_rdoCommandDialog_clicked)

        self.ui.cmdCommandDTCreateUI.clicked.connect(self.on_cmdCommandDTCreateUI_clicked)
        self.ui.cmdCommandDialogCreateUI.clicked.connect(self.on_cmdCommandDialogCreateUI_clicked)
        self.ui.cmdCommandSTCreateUI.clicked.connect(self.on_cmdCommandSTCreateUI_clicked)

        self.ui.cmdLoadPackage.clicked.connect(self.on_cmdLoadPackage_clicked)
        self.ui.cmdReadFile.clicked.connect(self.on_cmdReadFile_clicked)

        self.ui.cmdCreateAppPackage.clicked.connect(self.on_cmdCreateAppPackage_clicked)
        #self.ui.cmdCreateAppFunction.clicked.connect(self.on_cmdCreateAppFunction_clicked)

        self.ui.cmdCreateCommand.clicked.connect(self.on_cmdCreateCommand_clicked)

        self.ui.cmdCreateRibbonItem.clicked.connect(self.on_cmdCreateRibbonItem_clicked)
        self.ui.tvRibbonBar.itemClicked.connect(self.on_tvRibbonBar_clicked)
        self.ui.cmdRibbonSave.clicked.connect(self.on_cmdRibbonSave_clicked)

        self.functionFileList = []

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

    def onChangeFilterValue(self, text):
        #self.packagelistModelproxy.setFilterKeyColumn(text)
        search = QRegularExpression(text,
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.packagelistModelproxy.setFilterRegExp(search)

    def onSelectPackage(self, index):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(index.row(), 0).data()
        #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex(), 0, None).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        self.ui.tvPackageItems.clear()
        self.ui.txtPackageName.setText(selectedpackage)
        self.loadInit()

        CommandList = {}
        FunctionList = {}
        PrefsWidgetsList = {}

        self.fileDict = {}
        self.fill_tree(self.ui.tvPackageItems, packagepath, selectedpackage)

    def fill_tree(self, tree, path, packagename):
        item = QTreeWidgetItem()

        item.setText(0, packagename)
        item.setExpanded(True)
        self.fill_item2(item, path)
        tree.addTopLevelItem(item)

    def fill_item2(self, item, path):
        item.setExpanded(True)
        if "Database" in path:
            baseList = ""
            tableitemlist = ""

        if os.path.isdir(path):
            for filename in sorted(os.listdir(path)):

                child_path = os.path.join(path, filename)
                if filename[-3:] != ".py":
                    child_item = QTreeWidgetItem()
                    child_item.setText(0, filename)
                    item.addChild(child_item)
                    if os.path.isdir(child_path):
                        self.fill_item2(child_item, child_path)
                else:
                    #filefullpath = Packages.__path__[0] + "\\"

                    #filefullpath = os.path.join(filefullpath, selectedpackage)
                    #filefullpath = os.path.join(filefullpath, directories)
                    if "Database" in path:
                        if "__init__.py" not in filename:
                            packagename = self.ui.txtPackageName.text()
                            tableitemlist = tableitemlist + f"from PackageManager.Packages.{packagename}.Database import {filename[:-3]} \n"

                    try:
                        with open(child_path) as f:
                            code = f.read()
                            tree = ast.parse(code)


                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    class_child = QTreeWidgetItem(item)
                                    class_child.setText(0, node.name)
                                    if "Database" in path:
                                        tableitemlist = tableitemlist + f"_TABLES[\"{node.name}\"] = {filename[:-3]}.{node.name}\n"
                                    self.fileDict[node.name] = {}
                                    for method_node in ast.iter_child_nodes(node):
                                        if isinstance(method_node, ast.FunctionDef):
                                            method_child = QTreeWidgetItem(class_child)
                                            method_child.setText(0, method_node.name)
                                            self.fileDict[node.name][method_node.name] = self.initfilecommandDict()
                                            arginput = False
                                            for arg in method_node.args.args:
                                                if "self" not in arg.arg:
                                                    if arginput == False:
                                                        grandchild = QTreeWidgetItem(method_child)
                                                        grandchild.setText(0, "Inputs")
                                                        arginput = True
                                                    greatgrandchild = QTreeWidgetItem(grandchild)
                                                    greatgrandchild.setText(0, arg.arg)

                                            if any(isinstance(inner_node, ast.Return) for inner_node in
                                                   ast.walk(method_node)):
                                                grandchild = QTreeWidgetItem(method_child)
                                                grandchild.setText(0, "Outputs")
                                                greatgrandchild = QTreeWidgetItem(grandchild)
                                                greatgrandchild.setText(0, "Return")
                        if "Database" in path:
                            tableitemlist = tableitemlist + "\n"

                            '''elif isinstance(node, ast.FunctionDef):
                                # This handles standalone functions, not methods within classes
                                child = QTreeWidgetItem(parent)
                                child.setText(0, node.name)
            
                                arginput = False
                                for arg in node.args.args:
                                    if "self" not in arg.arg:
                                        if arginput == False:
                                            grandchild = QTreeWidgetItem(child)
                                            grandchild.setText(0, "Inputs")
                                            arginput = True
                                        greatgrandchild = QTreeWidgetItem(grandchild)
                                        greatgrandchild.setText(0, arg.arg)
            
                                if any(isinstance(inner_node, ast.Return) for inner_node in ast.walk(node)):
                                    grandchild = QTreeWidgetItem(child)
                                    grandchild.setText(0, "Outputs")
                                    greatgrandchild = QTreeWidgetItem(grandchild)
                                    greatgrandchild.setText(0, "Return")'''


                    except:
                        print("Error in parsing file: " + str(child_path))

        #this is to manually add stuff
        if "Database" in path:
            pyperclip.copy(tableitemlist)
    def find_children_of_inputs(self, item, searchitem):
        children_of_inputs = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.text(0) == searchitem:
                # This child is an "Inputs" item, get its children
                for j in range(child.childCount()):
                    sub_child = child.child(j)
                    children_of_inputs.append(sub_child.text(0))
            else:
                # This child is not an "Inputs" item, check its children
                children_of_inputs.extend(self.find_children_of_inputs(child, searchitem))

        return children_of_inputs

    @QtCore.Slot(QTreeWidgetItem, int)
    def on_tvPackageItems_clicked(self, it, col):
        parents = []
        current_item = it
        current_item_value = current_item.text(col)
        current_parent = current_item.parent()

        children_of_inputs = self.find_children_of_inputs(current_item, "Inputs")
        children_inputtext = ','.join(children_of_inputs)

        children_of_outputs = self.find_children_of_inputs(current_item, "Outputs")
        children_outputtext = ','.join(children_of_outputs)

        # Walk up the tree and collect all parent items of this item
        while not current_parent is None:
            parents.insert(0, current_parent.text(col))
            current_item = current_parent
            current_parent = current_item.parent()

        filefullpath = Packages.__path__[0] + "\\"
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        selecteditem = it.text(col) + ".py"
        filefullpath = os.path.join(filefullpath, selectedpackage)

        for items in parents:
            filefullpath = os.path.join(filefullpath, items)

        self.functionlibrarypath = filefullpath + ".py"
        self.workingFile = os.path.join(filefullpath, selecteditem)

        if parents:
            if parents[0] is not None and ".py" in parents[0]:
                self.ui.txtPackageName.setText(selectedpackage)
                self.ui.txtCommandFileName.setText(selecteditem)
                self.ui.txtCommandName.setText(it.text(col))
                self.ui.rdoCommandST.setChecked(True)

                importlist = []
                importlist.append("")
                importlist.append("from PackageManager.UI.Commands.Command import ShelfTool")
                importlist.append(f"from PackageManager.Packages.{selectedpackage}.Commands import RESOURCES_DIR")
                importlist.append("from PackageManager.Core.Common import Direction")
                importlist.append("from PySide6 import QtGui")

                self.ui.lstCommandImports.clear()
                for lineitem in importlist:
                    self.ui.lstCommandImports.addItem(lineitem)

                #self.PackageInstance
                #self.ProgramManagerInstance

                self.ui.txtCommandCode.setPlainText(f"self.PackageInstance.{current_item_value}({children_inputtext})")

                #Load Nodes
                self.ui.txtNodeFileName.setText(selecteditem)
                self.ui.txtNodeCode.setPlainText(f"self.PackageInstance.{current_item_value}({children_inputtext})")
                inputnodedata = {}
                for order, value in enumerate(children_of_inputs):
                    inputnodedata[value] = {"Name": value, "DataType": "Any", "DefaultValue": "", "Order": order, "Direction": "Input"}
                outputnodedata = {}
                for order, value in enumerate(children_of_outputs):
                    outputnodedata[value] = {"Name": value, "DataType": "Any", "DefaultValue": "", "Order": order, "Direction": "Output"}

                self.selectedNodeDataName = it.text(col)
                self.selectedNodeData = {}
                self.selectedNodeData[self.selectedNodeDataName] = {}

                self.selectedNodeData[self.selectedNodeDataName]["Inputs"] = inputnodedata
                self.selectedNodeData[self.selectedNodeDataName]["Outputs"] = outputnodedata

                self.loadNodePinTable()



            if "\\Commands" in self.workingFile:
                self.initCommandForm()

                #todo: check if package level was selected
                deft = it.text(col)
                self.initCommandDict(deft)
                self.initializeFunctionForm
                self.initializePinData
                filename = self.workingFile.split("\\")[-1]
                self.ui.txtFunctionFileName.setText(filename)
                self.ui.txtFunctionName.setText(deft)
                self.ui.twPackage.setCurrentIndex(1)
                implementdata = ""
                definitiondata = ""
                codedata = ""

                if os.path.exists(self.workingFile):
                    self.ui.txtCommandFileName.setText(filename)
                    self.ui.txtCommandName.setText(deft)
                    self.readCommandData(self.workingFile)


            if "\\Function" in self.workingFile:
                self.loadAllFunctions()
                #todo: check if package level was selected
                deft = it.text(col)
                self.initializeFunctionForm
                self.initializePinData
                filename = self.functionlibrarypath.split("\\")[-1]
                self.ui.txtFunctionFileName.setText(filename)
                self.ui.txtFunctionName.setText(deft)

                #self.loadAllFunctions()
                implementdata = ""
                definitiondata = ""
                codedata = ""
                self.ui.twPackage.setCurrentIndex(2)

                try:
                    for idata in self.functiondict[deft]["Implement"]:
                        implementdata += idata
                    self.ui.txtFImplement.setText(implementdata)

                    for ddata in self.functiondict[deft]["Definition"]:
                        definitiondata += ddata
                    self.ui.txtFDef.setText(definitiondata)

                    code = ""
                    for codeline in self.functiondict[deft]["Code"]:
                        code += codeline
                    self.ui.txtCode.setText(code)

                    self.ui.chkPSDraggerSteps.setChecked(False)
                    self.ui.txtPSDraggerSteps.setText("")

                    if "CATEGORY" in self.functiondict[deft]["MetaData"]:
                        self.ui.txtMetaCategory.setText(self.functiondict[deft]["MetaData"]["CATEGORY"])
                    if "KEYWORDS" in self.functiondict[deft]["MetaData"]:
                        self.ui.txtMetaKeywords.setText(self.functiondict[deft]["MetaData"]["KEYWORDS"])
                    if "CacheEnabled" in self.functiondict[deft]["MetaData"]:
                        self.ui.chkMetaCacheEnabled.setChecked(self.functiondict[deft]["MetaData"]["CacheEnabled"])

                    self.pindefs = self.functiondict[deft]

                    if deft in self.functiondict:
                        self.loadPinTable(deft)

                except:
                    pass

            if "\\Node" in filefullpath:
                deft = it.text(col)
                self.ui.txtNodeFileName.setText(deft)
                self.selectedNodeDataName = deft.replace(".py", "")
                filefullpath = os.path.join(filefullpath, deft)
                self.loadNodeProperties(filefullpath)
                self.parseNodePins()
                self.ui.twPackage.setCurrentIndex(3)

            if "\\Pins" in filefullpath:
                self.loadPinProperties(filefullpath)
                print(self.pindict)

            if "\\SQL" in filefullpath:
                deft = it.text(col)
                self.loadTableProperties(filefullpath)
                self.ui.twPackage.setCurrentIndex(8)

    def onOpenPackageFolder(self):

        #print(Packages.__path__[0] + "\\")
        os.startfile(Packages.__path__[0])
        #subprocess.Popen(r'explorer' + Packages.__path__[0] + "\\")

#Command Code
    def initPackageDict(self, defname):
        packagedict = {}
        packagedict["Author"] = ""
        packagedict["CopyrightYear"] = ""
        packagedict["RevisionHistory"] = []
        packagedict["Import"] = []
        packagedict["Filename"] = ""
        packagedict["Name"] = ""
        packagedict["Description"] = ""
        packagedict["Category"] = ""
        packagedict["Keywords"] = ""
        packagedict["ToolTip"] = ""
        packagedict["KeyboardShortCut"] = ""
        packagedict["SmallIcon"] = ""
        packagedict["MediumIcon"] = ""
        packagedict["LargeIcon"] = ""
        packagedict["ResourceFolder"] = "{Resource Folder}"
        packagedict["PythonCode"] = ""
        packagedict["PyflowFile"] = ""

        self.packageDict[defname] = packagedict



    def initfilecommandDict(self):
        commanddict = {}
        commanddict["Author"] = ""
        commanddict["CopyrightYear"] = ""
        commanddict["RevisionHistory"] = []
        commanddict["Import"] = []
        commanddict["Filename"] = ""
        commanddict["Name"] = ""
        commanddict["Description"] = ""
        commanddict["Category"] = ""
        commanddict["Keywords"] = ""
        commanddict["ToolTip"] = ""
        commanddict["KeyboardShortCut"] = ""
        commanddict["SmallIcon"] = ""
        commanddict["MediumIcon"] = ""
        commanddict["LargeIcon"] = ""
        commanddict["ResourceFolder"] = "{Resource Folder}"
        commanddict["PythonCode"] = ""
        commanddict["PyflowFile"] = ""

        return commanddict

    def initCommandDict(self, defname):
        commanddict = {}
        commanddict["Author"] = ""
        commanddict["CopyrightYear"] = ""
        commanddict["RevisionHistory"] = []
        commanddict["Import"] = []
        commanddict["Filename"] = ""
        commanddict["Name"] = ""
        commanddict["Description"] = ""
        commanddict["Category"] = ""
        commanddict["Keywords"] = ""
        commanddict["ToolTip"] = ""
        commanddict["KeyboardShortCut"] = ""
        commanddict["SmallIcon"] = ""
        commanddict["MediumIcon"] = ""
        commanddict["LargeIcon"] = ""
        commanddict["ResourceFolder"] = "{Resource Folder}"
        commanddict["PythonCode"] = ""
        commanddict["PyflowFile"] = ""

        self.commanddict[defname] = commanddict

    def initRibbonDict(self):
        ribbondict = {}
        ribbondict["Bar"] = ""
        ribbondict["Section"] = ""
        ribbondict["Widget"] = ""
        ribbondict["Order"] = 0
        ribbondict["smallIconLocation"] = ""
        ribbondict["mediumIconLocation"] = ""
        ribbondict["largeIconLocation"] = ""
        ribbondict["Action"] = ""
        ribbondict["Package"] = ""
        ribbondict["PackageGroup"] = ""
        ribbondict["Path"] = ""
        ribbondict["ToolTip"] = ""
        ribbondict["KeyboardShortCut"] = ""
        ribbondict["StartPosX"] = 0
        ribbondict["StartPosY"] = 0
        ribbondict["Fixity"] = "Order"
        ribbondict["WidgetSize"] = (1,1)
        ribbondict["DisplayName"] = ""
        ribbondict["DisplayNameVisible"] = False
        ribbondict["ToolTip"] = ""
        ribbondict["Command"] = ""
        ribbondict["IsEnabled"] = True
        ribbondict["IsVisible"] = True
        ribbondict["MainVisible"] = True
        ribbondict["InstanceVisible"] = True

        return ribbondict

    def initRibbonForm(self):
        self.ui.txtRibbonCommand.setText(None)
        self.ui.txtRibbonPackage.setText(None)
        self.ui.txtRibbonPath.setText(None)
        self.ui.cmbRibbonBar.setCurrentText(None)
        self.ui.cmbRibbonSection.setCurrentText(None)
        self.ui.cmbRibbonWidget.setCurrentText(None)
        self.ui.cmbRibbonSmallIcon.setCurrentText(None)
        self.ui.cmbRibbonMediumIcon.setCurrentText(None)
        self.ui.cmbRibbonLargeIcon.setCurrentText(None)
        self.ui.spnRibbonOrder.setValue(0)
        self.ui.spnRibbonStartPosX.setValue(0)
        self.ui.spnRibbonStartPosY.setValue(0)
        self.ui.cmbRibbonFixitity.setCurrentText(None)
        self.ui.spnWidgetSizeX.setValue(0)
        self.ui.spnWidgetSizeY.setValue(0)
        self.ui.txtRibbonDisplayName.setText(None)
        self.ui.chkRibbonDisplayName.setChecked(False)
        self.ui.txtRibbonToolTip.setText(None)
        self.ui.chkRibbonIsEnabled.setChecked(True)
        self.ui.chkRibbonIsVisible.setChecked(True)
        self.ui.chkRibbonMainVisible.setChecked(False)
        self.ui.chkRibbonInstanceVisible.setChecked(False)

    def copyCommandDict(self, defname1, defname2):

        commanddict = {}
        commanddict["Author"] = self.commanddict[defname1]["Author"]
        commanddict["CopyrightYear"] = self.commanddict[defname1]["CopyrightYear"]
        commanddict["RevisionHistory"] = []
        commanddict["Import"] = self.commanddict[defname1]["Import"]
        commanddict["Filename"] = defname2 + ".py"
        commanddict["Name"] = defname2
        commanddict["Description"] = self.commanddict[defname1]["Description"]
        commanddict["Category"] = self.commanddict[defname1]["Category"]
        commanddict["Keywords"] = self.commanddict[defname1]["Keywords"]
        commanddict["ToolTip"] = self.commanddict[defname1]["ToolTip"]
        commanddict["KeyboardShortCut"] = self.commanddict[defname1]["KeyboardShortCut"]
        commanddict["SmallIcon"] = self.commanddict[defname1]["SmallIcon"]
        commanddict["MediumIcon"] = self.commanddict[defname1]["MediumIcon"]
        commanddict["LargeIcon"] = self.commanddict[defname1]["LargeIcon"]
        commanddict["ResourceFolder"] = self.commanddict[defname1]["ResourceFolder"]
        commanddict["PythonCode"] = self.commanddict[defname1]["PythonCode"]
        commanddict["PyflowFile"] = self.commanddict[defname1]["PyflowFile"]

        self.commanddict[defname2] = commanddict

    def initCommandForm(self):
        self.ui.txtCommandName.setText("")
        self.ui.txtCommandDescription.setText("")
        self.ui.txtCommandCategory.setText("")
        self.ui.txtCommandKeyWords.setText("")
        self.ui.txtCommandToolTip.setText("")
        self.ui.txtCommandKeyBoardShortcut.setText("")
        self.ui.txtCommandSmallIcon.setText("")
        self.ui.txtCommandMediumIcon.setText("")
        self.ui.txtCommandLargeIcon.setText("")
        self.ui.txtCommandResourceFolder.setText("")
        self.ui.txtCommandCode.setText("")
        self.ui.lstCommandRevisionHistory.clear()
        self.ui.lstCommandImports.clear()

    def loadCommandFormFromDict(self, defname):
        #self.commanddict[defname1]["Author"]
        self.ui.txtCommandName.setText(self.commanddict[defname]["Name"])
        self.ui.txtCommandDescription.setText(self.commanddict[defname]["Description"])
        self.ui.txtCommandCategory.setText(self.commanddict[defname]["Category"])
        self.ui.txtCommandKeyWords.setText(self.commanddict[defname]["Keywords"])
        self.ui.txtCommandToolTip.setText(self.commanddict[defname]["ToolTip"])
        self.ui.txtCommandKeyBoardShortcut.setText(self.commanddict[defname]["KeyboardShortCut"])
        self.ui.txtCommandSmallIcon.setText(self.commanddict[defname]["SmallIcon"])
        self.ui.txtCommandMediumIcon.setText(self.commanddict[defname]["MediumIcon"])
        self.ui.txtCommandLargeIcon.setText(self.commanddict[defname]["LargeIcon"])
        self.ui.txtCommandResourceFolder.setText(self.commanddict[defname]["ResourceFolder"])
        self.ui.txtCommandCode.setText(self.commanddict[defname]["PythonCode"])

        for item in self.commanddict[defname]["Import"]:
            self.ui.lstCommandImport.addItem(item)

        for item in self.commanddict[defname]["RevisionHistory"]:
            self.ui.lstCommandRevisionHistory.addItem(item)


    def on_cmdAddCommandRevision_clicked(self):

        commandName = self.ui.txtCommandName.text()
        revisionstatement = self.ui.dteCommandRevisionDate.date().toString(
            "yyyy-MM-dd") + " " + self.ui.txtCommandAuthor.text() + ":  " + self.ui.txtCommandRevision.text()

        if revisionstatement not in self.commanddict[commandName]["RevisionHistory"]:
            self.commanddict[commandName]["RevisionHistory"].append(revisionstatement)
            self.ui.lstCommandRevisionHistory.addItem(revisionstatement)

    def addCopyright(self, f):
        Filename = self.ui.txtCommandName.text()
        now = datetime.datetime.now()
        year = now.year
        author = self.ui.cmbCommandAuthor.currentText()
        copyright = self.ui.txtCopyright.toPlainText()

        f.write(f"## Copyright {year} {author}\n\n{copyright}\n\n")

        f.write("## Revision History\n")
        revisionstatement = now.strftime("%Y-%m-%d") + " " + self.ui.txtCommandAuthor.text() + ":  " + "File Created"

        f.write(f"#{revisionstatement}\n")
        f.write("\n")

    def readCommandData(self, filefullpath):
        codenotes = 0
        importlist = []
        importstart = 0
        classstart = 0
        super = 0
        staticmethod = []
        definitionlist = []
        codedata = []

        filefullpath2 = Packages.__path__[0] + "\\"
        filename = self.ui.txtCommandFileName.text()
        defname = filename[:-3]

        filefullpath2 = os.path.join(filefullpath2, self.ui.txtPackageName.text())
        filefullpath2 = os.path.join(filefullpath2, "Commands")

        self.initCommandDict(defname)

        self.commanddict[defname]["Filename"] = defname
        self.commanddict[defname]["Description"] = ""
        self.commanddict[defname]["Category"] = ""
        self.commanddict[defname]["Keywords"] = ""
        self.commanddict[defname]["KeyboardShortCut"] = ""
        self.commanddict[defname]["ResourceFolder"] = ""

        self.ui.cmdCommandAddSmallIcon.setIcon(QIcon())
        self.ui.txtCommandSmallIcon.setText("")
        self.ui.cmdCommandAddMediumIcon.setIcon(QIcon())
        self.ui.cmdCommandAddMediumIcon.setText("")
        self.ui.cmdCommandAddLargeIcon.setIcon(QIcon())
        self.ui.txtCommandLargeIcon.setText("")

        filesize = len(open(filefullpath).readlines())
        f = open(filefullpath, "r")
        importlistmodel = QStandardItemModel(0, 0)
        revisionflag = -1
        descriptionflag = -1
        description = ""
        doflag = -1

        for index, lineitem in enumerate(f):
            # Reading the parts of the code (Implement, Def, Code)
            codedata.append(lineitem)

            if revisionflag == 1:
                if lineitem != "\n":
                    revisionlist.append(lineitem)
                    self.ui.lstCommandRevisionHistory.addItem(lineitem)
                else:
                    revisionflag = 0
                    self.commanddict[defname]["RevisionHistory"] = revisionlist

            if "Revision History" in lineitem:
                revisionflag = 1
                revisionlist = []

            if lineitem.find("import") != -1:
                self.ui.lstCommandImports.addItem(lineitem.rstrip())

            if lineitem.find("class") != -1:
                if lineitem.find("DockTool") != -1:
                    self.ui.rdoCommandDT.setChecked(True)
                    self.ui.stkCommandClassType.setCurrentIndex(0)
                if lineitem.find("ShelfTool") != -1:
                    self.ui.rdoCommandST.setChecked(True)
                    self.ui.stkCommandClassType.setCurrentIndex(1)
                if lineitem.find("Dialog") != -1:
                    self.ui.rdoCommandDialog.setChecked(True)
                    self.ui.stkCommandClassType.setCurrentIndex(2)

            if lineitem.find("__init__") != -1:
                descriptionflag = 0  # Stop reading the description
                description = description.strip()
                if description.startswith('"""') and description.endswith('"""'):
                    description = description[3:-3]

                self.commanddict[defname]["Description"] = description
                self.ui.txtCommandDescription.setText(description)

            if descriptionflag == 1:
                description = description + lineitem

            if lineitem.find("class") != -1:
                descriptionflag = 1  # Start reading the description

            if lineitem.find("def") != -1:
                definitionlist.append(index)

        self.commanddict[defname]["Import"] = importlist

        defCount = len(definitionlist)
        for count, defitem in enumerate(definitionlist):
            line = codedata[defitem]
            if count == defCount - 1:
                endCodeBlock = len(codedata)
            else:
                endCodeBlock = definitionlist[count + 1] - 1

            if codedata[defitem - 1].find("@staticmethod") != -1:
                staticmethod = True
            else:
                staticmethod = False

            if codedata[defitem].find("__init__") != -1:
                if codedata[defitem].find("super") != -1:
                    pass

            if codedata[defitem].find("toolTip") != -1:
                for row in range(defitem, endCodeBlock):
                    line2 = codedata[row]
                    if codedata[row].find("return") != -1:
                        tooltip = codedata[row][15:]
                        pattern = 'str\("(.*)"\)'
                        match = re.search(pattern, tooltip)
                        if match:
                            tooltip = match.group(1)
                        else:
                            tooltip = tooltip[1:-2]

                        self.ui.txtCommandToolTip.setText(tooltip)
                        self.commanddict[defname]["ToolTip"] = tooltip

            if codedata[defitem].find("getIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    a = codedata[row]
                    if codedata[row].find("return") != -1:
                        getIcon = codedata[row][15:]
                        # Todo: Load Icon Image to Button
                        parts = getIcon.split("(")
                        icon_path = parts[1][:-1]
                        parts = icon_path.split('"')
                        filename = parts[1]
                        RESOURCES_DIR2 = os.path.join(filefullpath2, "res")
                        fullpath = os.path.join(RESOURCES_DIR2, filename)
                        self.ui.cmdCommandAddSmallIcon.setIcon(QtGui.QIcon(fullpath))

                        if RESOURCES_DIR2:
                            self.ui.chkCommandResourceFolder.setChecked(True)
                        else:
                            self.ui.chkCommandResourceFolder.setChecked(False)

                        self.ui.txtCommandResourceFolder.setText(RESOURCES_DIR2)

                        self.ui.txtCommandSmallIcon.setText(filename)
                        iconpath = os.path.join(RESOURCES_DIR2, filename)
                        self.commanddict[defname]["SmallIcon"] = getIcon

            if codedata[defitem].find("getSmallIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getSmallIcon = codedata[row][15:]
                        self.ui.txtCommandSmallIcon.setText(getSmallIcon)
                        self.ui.cmdCommandAddSmallIcon.setIcon(QtGui.QIcon(getIcon))
                        self.commanddict[defname]["SmallIcon"] = getSmallIcon

            if codedata[defitem].find("getMediumIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getMediumIcon = codedata[row][15:]
                        self.ui.txtCommandMediumIcon.setText(getMediumIcon)
                        self.ui.cmdCommandAddMediumIcon.setIcon(QtGui.QIcon(getIcon))
                        self.commanddict[defname]["MediumIcon"] = getMediumIcon

            if codedata[defitem].find("getLargeIcon") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        getLargeIcon = codedata[row][15:]
                        self.ui.txtCommandLargeIcon.setText(getLargeIcon)
                        self.ui.cmdCommandAddLargeIcon.setIcon(QtGui.QIcon(getIcon))
                        self.commanddict[defname]["LargeIcon"] = getLargeIcon

            if codedata[defitem].find("category") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        category = codedata[row][15:]
                        pattern = 'str\("(.*)"\)'
                        match = re.search(pattern, category)
                        if match:
                            category = match.group(1)

                        self.ui.txtCommandCategory.setText(category)
                        self.commanddict[defname]["Category"] = category

            if codedata[defitem].find("keywords") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        keywords = codedata[row][15:]
                        pattern = 'str\("(.*)"\)'
                        match = re.search(pattern, keywords)
                        if match:
                            keywords = match.group(1)
                        self.ui.txtCommandKeyWords.setText(keywords)
                        self.commanddict[defname]["Keywords"] = keywords

            if codedata[defitem].find("keyboardShortcut") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        keywordboardshortcut = codedata[row][15:]
                        pattern = 'str\("(.*)"\)'
                        match = re.search(pattern, keywordboardshortcut)
                        if match:
                            keywordboardshortcut = match.group(1)
                        self.ui.txtKeyBoardShortcut.setText(keywordboardshortcut)
                        self.commanddict[defname]["Keyboardshortcut"] = keywordboardshortcut

            if codedata[defitem].find("name") != -1:
                for row in range(defitem, endCodeBlock):
                    if codedata[row].find("return") != -1:
                        name = codedata[row][15:]
                        pattern = 'str\("(.*)"\)'
                        match = re.search(pattern, name)
                        if match:
                            name = match.group(1)
                        self.ui.txtCommandName.setText(name)

            if codedata[defitem].find("do") != -1:
                code = ""
                for codeline in codedata[defitem:endCodeBlock]:
                    if codeline.startswith('        '):
                        codeline = codeline[8:]

                    if "def do(self):" not in codeline:
                        code += codeline

                self.commanddict[defname]["PythonCode"] = code
                #This will only work if it matches exactly
                code2 = code.replace("self.PackageManagerInstance.instance.newFile(", "")
                code2 = code2.replace(".MdiChild(self.PackageManagerInstance.instance, None))", "")
                #self.ui.txtCommandDiUIPyFile.setText(code2)
                self.ui.txtCommandCode.setPlainText(code)

    @QtCore.Slot()
    def on_cmdNewCommand_clicked(self):
        inputData = {"label": "Enter Command Name", "default": "New Command Name", "button": "Create",
                   "title": "Create New Command", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = InputDialog(inputData)
        defname = dialog.get_value()
        self.createNewCommand(defname)

    def createNewCommand(self, defname):
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        if defname is not None:
            #self.initCommandDict(defname)
            #self.loadCommandFormFromDict(defname)
            self.ui.txtCommandFileName.setText(defname + ".py")
            self.commanddict[defname]["Import"].append("")
            self.commanddict[defname]["Import"].append("from PackageManager.UI.Commands.Command import ShelfTool")
            self.commanddict[defname]["Import"].append(f"from PackageManager.Packages.{selectedpackage}.Commands import RESOURCES_DIR")
            self.commanddict[defname]["Import"].append("from PySide6 import QtGui")

            self.commanddict[defname]["Name"] = defname
            self.commanddict[defname]["Author"] = self.ui.cmbCommandAuthor.currentText()
            # self.commanddict[defname]["CopyrightYear"] = self.ui.dteCopyrightYear.date().year()
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y-%m-%d")

            self.commanddict[defname]["RevisionHistory"].append("# " + formatted_date + " - " +
                                                                self.ui.cmbCommandAuthor.currentText() + " - Created")

            self.on_cmdWriteCommand_clicked()

    @QtCore.Slot()
    def on_cmdSaveAsCommand_clicked(self):
        inputData = {"label": "Enter Command Name", "default": "New Command Name", "button": "Create",
                   "title": "Create New Command", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = InputDialog(inputData)
        defname = dialog.get_value()

        if defname != "":
            filename = self.ui.txtCommandFileName.text()
            # Copy the current command to the new command then set the name in the form
            self.copyCommandDict(defname, filename)
            self.initCommandForm()
            self.loadCommandFormFromDict(defname)
            self.ui.textCommandFileName.setText(defname)

    @QtCore.Slot()
    def on_cmdSaveCommand_clicked(self):
        filename = self.ui.txtCommandFileName.text()
        defname = filename.replace(".py", "")
        self.initCommandDict(defname)
        #defname = self.ui.txtCommandName.text()
        self.commanddict[defname]["Author"] = self.ui.cmbCommandAuthor.currentText()
        # self.commanddict[defname]["CopyrightYear"] = self.ui.dteCopyrightYear.date().year()

        for index in range(self.ui.lstCommandRevisionHistory.count()):
            self.commanddict[defname]["RevisionHistory"].append(self.ui.lstCommandRevisionHistory.item(index).text())

        self.commanddict[defname]["Filename"] = self.ui.txtCommandFileName.text()

        for index in range(self.ui.lstCommandImports.count()):
            self.commanddict[defname]["Import"].append(self.ui.lstCommandImports.item(index).text())

        self.commanddict[defname]["Name"] = self.ui.txtCommandName.text()
        self.commanddict[defname]["Description"] = self.ui.txtCommandDescription.toPlainText()
        self.commanddict[defname]["Category"] = self.ui.txtCommandCategory.text()
        self.commanddict[defname]["Keywords"] = self.ui.txtCommandKeyWords.text()
        self.commanddict[defname]["ToolTip"] = self.ui.txtCommandToolTip.text()
        self.commanddict[defname]["KeyboardShortCut"] = self.ui.txtCommandKeyBoardShortcut.text()
        self.commanddict[defname]["SmallIcon"] = self.ui.txtCommandSmallIcon.text()
        self.commanddict[defname]["MediumIcon"] = self.ui.txtCommandMediumIcon.text()
        self.commanddict[defname]["LargeIcon"] = self.ui.txtCommandLargeIcon.text()

        if self.ui.chkCommandResourceFolder.isChecked():
            self.commanddict[defname]["ResourceFolder"] = "{Resource Folder}"
        else:
            self.commanddict[defname]["ResourceFolder"] = self.ui.txtCommandResourceFolder.text()

        self.commanddict[defname]["PythonCode"] = self.ui.txtCommandCode.toPlainText()
        self.commanddict[defname]["PyflowFile"] = ""

    @QtCore.Slot()
    def on_cmdWriteCommand_clicked(self):
        filename = self.ui.txtCommandFileName.text()
        # Write File
        fname = filename
        filefullpath = Packages.__path__[0] + "\\"
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        filefullpath = os.path.join(filefullpath, selectedpackage)
        filefullpath = os.path.join(filefullpath, "Commands")
        filefullpath = os.path.join(filefullpath, fname)

        classline = ""
        Filename = filename.split(".")[0]


        if self.ui.rdoCommandDT.isChecked():
            classline = f"class {Filename}(DockTool):\n"
        if self.ui.rdoCommandST.isChecked():
            classline = f"class {Filename}(ShelfTool):\n"
        if self.ui.rdoCommandDialog.isChecked():
            classline = f"class {Filename}(Dialog):\n"

        classline += "    \"\"\"" + self.commanddict[Filename]["Description"] + "\"\"\"\n\n"
        classline += "    def __init__(self):\n"
        classline += f"        super({Filename}, self).__init__()\n\n"

        variablelist = ["ToolTip", "getIcon", "SmallIcon",
                        "MediumIcon", "LargeIcon", "Name", "Category", "Keywords", "KeyboardShortCut", "PythonCode"]

        with open(filefullpath, 'w') as f:
            now = datetime.datetime.now()
            year = now.year
            author = self.ui.cmbCommandAuthor.currentText()
            copyright = self.ui.txtCopyright.toPlainText()

            f.write(f"## Copyright {year} {author}\n\n{copyright}\n\n")

            if len(self.commanddict[Filename]["RevisionHistory"]):
                f.write("## Revision History\n")
                for revisionHistory in self.commanddict[Filename]["RevisionHistory"]:
                    f.write(f"#{revisionHistory}\n")
                f.write("\n")

            for importitem in self.commanddict[Filename]["Import"]:
                f.write(importitem + "\n")

            f.write("\n")
            # f.write("from PackageManager.Packages.%s.Commands import RESOURCES_DIR\n\n" % (selectedpackage))

            f.write(classline)
            for variable, code in self.commanddict[Filename].items():
                if variable in variablelist:
                    if code != {}:
                        if variable != "PythonCode":
                            f.write("    @staticmethod\n")
                            newvariable = variable[0].lower() + variable[1:]
                            f.write("    " + "def " + newvariable + "():\n")
                            if len(code):
                                if "icon" in variable.lower():
                                    if self.ui.chkCommandResourceFolder.isChecked():
                                        f.write("        " + "return QtGui.QIcon(RESOURCES_DIR + \"" + code + "\")\n\n")
                                    else:
                                        f.write("        " + "return " + QtGui.QIcon(code) + "\n\n")
                                else:
                                    f.write("        " + "return str(\"" + code + "\")\n\n")
                            else:
                                f.write("        " + "return None\n\n")
                        else:
                            #Python Code
                            #code = code.replace("    ", "        ")
                            f.write("    " + "def do(self):\n")
                            for line in code:
                                f.write("        " + line + "\n\n")

    @QtCore.Slot()
    def on_rdoCommandDT_clicked(self):
        self.ui.stkCommandClassType.setCurrentIndex(0)

    @QtCore.Slot()
    def on_rdoCommandST_clicked(self):
        self.ui.stkCommandClassType.setCurrentIndex(1)

    @QtCore.Slot()
    def on_rdoCommandDialog_clicked(self):
        self.ui.stkCommandClassType.setCurrentIndex(2)

    @QtCore.Slot()
    def on_cmdCommandSTCreateUI_clicked(self):
        #Add Command Code
        #Add Command to Init
        #Copy UI Template to Folder
        #Add PythonFile
        print("Create Shelf Tool UI")

    @QtCore.Slot()
    def on_cmdCommandDTCreateUI_clicked(self):
        #Add Command Code
        #Add Command to Init
        #Copy UI Template to Folder
        #Add PythonFile
        print("Create Dialog UI")

    @QtCore.Slot()
    def on_cmdCommandDialogCreateUI_clicked(self):
        filename = self.ui.txtCommandFileName.text()
        defname = filename.replace(".py", "")

        packagepath = Packages.__path__[0]
        parent_dir = os.path.dirname(os.path.dirname(packagepath))
        source_dir = os.path.join(parent_dir, "PackageManager\\Template\\UI\\Forms\\Dialog\\")
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        target_dir = os.path.join(os.path.join(packageRoot, selectedpackage),"UI\\Forms\\")
        source_file = 'dialog.ui'
        inputData = {"label": "Dialog Name", "default": "Dialog", "button": "Create",
                   "title": "Create New Dialog", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = InputDialog(inputData)
        target_file = str(dialog.get_value()) + ".ui"
        self.ui.txtCommandDiUIFile.setText(dialog.get_value())

        # Make sure target_dir exist, if not, create it
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Construct full file path
        source = os.path.join(source_dir, source_file)
        target = os.path.join(target_dir, target_file)

        # Copy the file
        shutil.copyfile(source, target)

        source_file = 'dialog.py'
        target_file = str(dialog.get_value()) + ".py"
        source = os.path.join(source_dir, source_file)
        target = os.path.join(target_dir, target_file)
        shutil.copyfile(source, target)
        self.ui.txtCommandDiUIPyFile.setText(dialog.get_value())

        PackageName = self.ui.txtPackageName.text()
        FileName = target_file.replace(".py", "")
        capitalized_letters = [char for char in FileName if char.isupper()]
        capitalized_letters.join(capitalized_letters)

        importfile = f"from PackageManager.Packages.{PackageName}.UI.Forms.{FileName} import {FileName} as {capitalized_letters}"
        self.commanddict[defname]["Import"].append(importfile)
        self.commanddict[defname]["Do"] = f"self.PackageManagerInstance.instance.newFile({capitalized_letters}.MdiChild(self.PackageManagerInstance.instance, None))"

    @QtCore.Slot()
    def on_cmdCreateMenuItem_clicked(self):
        self.initDict["MenuOrder"] = {}
        self.initDict["MenuLayout"] = {}

        itemList = {"Action": "Add Action",
                         "Package": "PyFlow",
                         "PackageGroup": "PyFlow",
                         "Command": "NewFile"}

        self.initDict["MenuLayout"]["File"].append(itemList)


    @QtCore.Slot()
    def on_cmdRibbonSave_clicked(self):
        Bar = self.ui.cmbRibbonBar.currentText()
        Section = self.ui.cmbRibbonSection.currentText()
        Command = self.ui.txtRibbonCommand.text()

        self.initDict["RibbonLayout"][Bar][Section][Command]["Bar"] = self.ui.cmbRibbonBar.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Section"] = self.ui.cmbRibbonSection.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Widget"] = self.ui.cmbRibbonWidget.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Order"] = self.ui.spnRibbonOrder.value()
        self.initDict["RibbonLayout"][Bar][Section][Command]["smallIconLocation"] = self.ui.cmbRibbonSmallIcon.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["mediumIconLocation"] = self.ui.cmbRibbonMediumIcon.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["largeIconLocation"] = self.ui.cmbRibbonLargeIcon.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Action"] = "Add Action"
        self.initDict["RibbonLayout"][Bar][Section][Command]["Package"] = self.ui.txtRibbonPackage.text()
        self.initDict["RibbonLayout"][Bar][Section][Command]["PackageGroup"] = ""
        self.initDict["RibbonLayout"][Bar][Section][Command]["Path"] = self.ui.txtRibbonPath.text()
        self.initDict["RibbonLayout"][Bar][Section][Command]["KeyboardShortCut"] = ""
        self.initDict["RibbonLayout"][Bar][Section][Command]["StartPosX"] = self.ui.spnRibbonStartPosX.value()
        self.initDict["RibbonLayout"][Bar][Section][Command]["StartPosY"] = self.ui.spnRibbonStartPosY.value()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Fixity"] = self.ui.cmbRibbonFixitity.currentText()
        self.initDict["RibbonLayout"][Bar][Section][Command]["WidgetSize"] = (self.ui.spnWidgetSizeX.value(), self.ui.spnWidgetSizeY.value())
        self.initDict["RibbonLayout"][Bar][Section][Command]["WidgetSizeX"] = self.ui.spnWidgetSizeX.value()
        self.initDict["RibbonLayout"][Bar][Section][Command]["WidgetSizeY"] = self.ui.spnWidgetSizeY.value()
        self.initDict["RibbonLayout"][Bar][Section][Command]["DisplayName"] = self.ui.txtRibbonDisplayName.text()
        self.initDict["RibbonLayout"][Bar][Section][Command]["DisplayNameVisible"] = self.ui.chkRibbonDisplayName.isChecked()
        self.initDict["RibbonLayout"][Bar][Section][Command]["ToolTip"] = self.ui.txtRibbonToolTip.text()
        self.initDict["RibbonLayout"][Bar][Section][Command]["Command"] = self.ui.txtRibbonCommand.text()
        self.initDict["RibbonLayout"][Bar][Section][Command]["IsEnabled"] = self.ui.chkRibbonIsEnabled.isChecked()
        self.initDict["RibbonLayout"][Bar][Section][Command]["IsVisible"] = self.ui.chkRibbonIsVisible.isChecked()
        self.initDict["RibbonLayout"][Bar][Section][Command]["MainVisible"] = self.ui.chkRibbonMainVisible.isChecked()
        self.initDict["RibbonLayout"][Bar][Section][Command]["InstanceVisible"] = self.ui.chkRibbonInstanceVisible.isChecked()

    @QtCore.Slot()
    def on_cmdCreateRibbonItem_clicked(self):
        bars = ['File', 'Edit', 'View', 'Help']
        bar_name = 'File'
        sections = ['File', 'Edit']
        section_name = "File"
        elements = ['Small Button', 'Medium Button', 'Large Button', "Combobox"]
        element_name = "Medium Button"

        dialog = RibbonBarDialog(bars, bar_name, sections, section_name, elements, element_name)
        result = dialog.exec()

        if result == QDialog.Accepted:
            bar_name, section, Widget, main_checked, instance_checked = dialog.get_inputs()
        else:
            section = "File"
            Widget = "Large Button"
            main_checked = True
            instance_checked = True

        smallIconLocation = "ICON_DIR + construction - Small.png"
        mediumIconLocation = "ICON_DIR + construction - Medium.png"
        largeIconLocation = "ICON_DIR + construction - Large.png"
        Action = "Add Action"

        Package = self.ui.txtPackageName.text()
        PackageGroup = self.ui.txtPackageName.text()
        Command = self.ui.txtCommandName.text()

        if not section in self.initDict["RibbonOrder"]:
            self.initDict["RibbonOrder"].append(section)

        if bar_name not in self.initDict["RibbonLayout"]:
            self.initDict["RibbonLayout"][bar_name] = {}

        if section not in self.initDict["RibbonLayout"][bar_name]:
            self.initDict["RibbonLayout"][bar_name][section] = {}

        itemList = {"Bar": bar_name, "Section": section, "Widget": Widget,
                    "smallIconLocation": smallIconLocation,
                    "mediumIconLocation": mediumIconLocation,
                    "largeIconLocation": largeIconLocation,
                    "Action": Action, "Package": Package,
                    "Order": 1, "StartPosition": (1, 1), "Fixity": "Order", "Size": (1, 1),
                    "DisplayName": "Save", "ShowName": False, "ToolTip": "Save",
                    "PackageGroup": PackageGroup, "Command": Command,
                    "IsEnabled": True, "IsVisible": True, "MainVisible": main_checked,
                    "InstanceVisible": instance_checked}

        self.initDict["RibbonLayout"][bar_name][section][Command] = itemList
        TreeView.dict2TreeWidget(self.ui.tvRibbonBar, self.initDict["RibbonLayout"])
    @QtCore.Slot(QTreeWidgetItem, int)
    def on_tvRibbonBar_clicked(self, it, col):
        parents = []
        current_item = it
        current_item_value = current_item.text(col)
        current_parent = current_item.parent()
        ribbonpathlist = TreeView.treewidgetpath(it)
        try:
            selectedRibbonItem = self.initDict["RibbonLayout"][ribbonpathlist[0]][ribbonpathlist[1]][ribbonpathlist[2]]
            self.initRibbonForm()

            self.ui.txtRibbonCommand.setText(selectedRibbonItem["Command"])
            self.ui.txtRibbonPackage.setText(selectedRibbonItem["Package"])
            self.ui.txtRibbonPath.setText(selectedRibbonItem["PackageGroup"])
            self.ui.cmbRibbonBar.setCurrentText(selectedRibbonItem["Bar"])
            self.ui.cmbRibbonSection.setCurrentText(selectedRibbonItem["Section"])
            self.ui.cmbRibbonWidget.setCurrentText(selectedRibbonItem["Widget"])
            self.ui.cmbRibbonSmallIcon.setCurrentText(selectedRibbonItem["smallIconLocation"])
            self.ui.cmbRibbonMediumIcon.setCurrentText(selectedRibbonItem["mediumIconLocation"])
            self.ui.cmbRibbonLargeIcon.setCurrentText(selectedRibbonItem["largeIconLocation"])
            self.ui.spnRibbonOrder.setValue(int(selectedRibbonItem["Order"]))
            self.ui.spnRibbonStartPosX.setValue(int(selectedRibbonItem["StartPosition"][0]))
            self.ui.spnRibbonStartPosY.setValue(int(selectedRibbonItem["StartPosition"][1]))
            self.ui.cmbRibbonFixitity.setCurrentText(selectedRibbonItem["Fixity"])
            self.ui.spnWidgetSizeX.setValue(int(selectedRibbonItem["WidgetSize"][0]))
            self.ui.spnWidgetSizeY.setValue(int(selectedRibbonItem["WidgetSize"][1]))
            self.ui.txtRibbonDisplayName.setText(selectedRibbonItem["Action"])
            self.ui.chkRibbonDisplayName.setChecked(selectedRibbonItem["ShowName"])
            self.ui.txtRibbonToolTip.setText(selectedRibbonItem["ToolTip"])
            self.ui.chkRibbonIsEnabled.setChecked(selectedRibbonItem["IsEnabled"])
            self.ui.chkRibbonIsVisible.setChecked(selectedRibbonItem["IsVisible"])
            self.ui.chkRibbonMainVisible.setChecked(selectedRibbonItem["MainVisible"])
            self.ui.chkRibbonInstanceVisible.setChecked(selectedRibbonItem["InstanceVisible"])
        except:
            pass

    @QtCore.Slot()
    def on_cmdCreateToolItem_clicked(self):

        itemList = {"Action": "Add Action",
                    "Package": "PyFlow",
                    "PackageGroup": "PyFlow",
                    "Command": "NewFile"}

        self.initDict["ToolBarLayout"]["File"].append(itemList)


    @QtCore.Slot()
    def on_cmdCommandAddSmallIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddSmallIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandSmallIcon.setText(os.path.basename(file_path))

    @QtCore.Slot()
    def on_cmdCommandAddMediumIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddMediumIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandMediumIcon.setText(os.path.basename(file_path))

    @QtCore.Slot()
    def on_cmdCommandAddLargeIcon_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        self.ui.cmdCommandAddLargeIcon.setIcon(QtGui.QIcon(file_path))
        self.ui.txtCommandLargeIcon.setText(os.path.basename(file_path))
    
    
## Function Code
    def loadFunctionCode(self, filefullpath, functionname):

        previousitem = ""
        implementdata = ""
        readingimplementdata = -1
        readingdefdata = 0
        defdata = ""
        codedata = []
        eof = 0
        defname = ""
        code = ""
        codedescription = ""
        NestDict = {}
        try:
            filesize = len(open(filefullpath).readlines())
            f = open(filefullpath, "r")

            for index, lineitem in enumerate(f):
                #Reading the parts of the code (Implement, Def, Code)
                if lineitem.find("class") != -1:
                    self.intro = code
                precode = code
                code += lineitem
                codedata.append(lineitem)
                #print(lineitem)
                if lineitem.find("super") != -1:
                    code = ""
                    codedata = []

                if lineitem.find("@staticmethod") != -1 or index == filesize-1:
                    readingdefdata = 0
                    if defname == functionname:
                        if precode.find("@staticmethod") != -1:
                            NestDict = {}
                            implement2 = implementdata
                            NestDict["Implement"] = implement2.replace("@staticmethod", "")
                            NestDict["Definition"] = defdata
                            NestDict["CodeDescription"] = codedescription
                            NestDict["Code"] = codedata[:-1]
                            self.functiondict[functionname] = NestDict

                            self.parseFunctionFile(functionname)
                        break
                    else:
                        implementdata = ""

                if lineitem.find("def ") != -1 and lineitem.find(" " + functionname) != -1:
                    defnamestart = 7
                    defnameend = lineitem.find("(")
                    defname = lineitem[defnamestart + 1:defnameend]
                    readingdefdata = 1

                if readingdefdata == 1:
                    if lineitem.find("def ") != -1:
                        lineitem = lineitem[defnameend+1:]
                    readingimplementdata = 0
                    defdata += lineitem.strip()
                    if defdata[-1] == ":":
                        readingdefdata = 0
                        codedata = []

                if (lineitem.find("@IMPLEMENT_NODE") != -1) or readingimplementdata == 1:
                    implementdata += lineitem.strip()
                    readingimplementdata = 1

                '''if "\'\'\'" in lineitem or "\"\"\"" in lineitem and readingdefdata == 0:
                    codedescription += lineitem[8:]
                else:
                    codedata.append(lineitem[8:])'''
        except:
            pass
        pass
    def parseFunctionFile(self, defname):
            #https://nedbatchelder.com/text/python-parsers.html
            #Maybe use Code Parser

            '''     Function Dictionary Structure
                    ["Name"]                    - Function Name
                    ["Order"]                   - Order in Appearance
                    ["Meta"]                    - Meta Data
                    ["Inputs"]                  - Pin Input List
                        ["Variable"]            - Input Pin Name
                            ["DataType"]        - Input Pin Data Type
                            ["DefaultValue"]    - Input Pin Default Value
                            ["PinSpecifiers"]   - Input Pin Options
                    ["Outputs"]
                        ["Variable"]            - Output Pin Name
                            ["DataType"]        - Output Pin Data Type
                            ["DefaultValue"]    - Output Pin Default Value
                            ["PinSpecifiers"]   - Output Pin Options
                '''

            implementdata = self.functiondict[defname]["Implement"]

            '''IMPLEMENT_NODE( func=None, returns=(DataType, DefaultValue, PinSpecficiers), meta={NodeMeta.CATEGORY: 'Default', NodeMeta.KEYWORDS: []}, nodeType=NodeTypes.Pure):'''
            istyle = "kwarg"
            ikeywords = ["func", "returns", "meta"]

            '''PinSpecifires = {PinSpecifires.List: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported, PinSpecifires.Value: "1"}'''
            parseparameters = {"start":"{", "end": "}", "delimination": ","}
            valuetype = {"\"": "Value", "|": "List"}

            '''meta = {NodeMeta.CATEGORY: 'Utils', NodeMeta.KEYWORDS: ['id'], NodeMeta.CACHE_ENABLED: False}'''
            parseparameters = {"start": "{", "end": "}", "delimination": ","}
            valuetype = {"\"": "Value", "[]": "List"}

            defdata = self.functiondict[defname]["Definition"]
            style = "csv"
            pos = ["DataType", "DefaultValue", "PinSpecifiers"]

            codedata = self.functiondict[defname]["Code"]

            implementdata2 = []
            defdata2 = []

            code = ""
            for line, linedata in enumerate(codedata):
                if "staticmethod" not in linedata:
                    if line == 0:
                        output = linedata.replace("\"", "").replace("\'","")[8:]
                        self.ui.txtCodeDescription.setText(output)
                    else:
                        code += linedata[8:]

            self.functiondict[defname]["Code"] = codedata

            #Extracting Information from Implement
            itemdict = {}
            itemdict["FunctionName"] = defname

            idata = {}
            pos = 1

            while pos <= len(implementdata)-1:
                if implementdata[pos] == "=":
                    pos2 = pos
                    while implementdata[pos2] != "(" and implementdata[pos2] != ",":
                        pos2 -= 1
                    variable = implementdata[pos2 + 1:pos].strip()
                    pos3 = pos + 1
                    while implementdata[pos3] != "=" and pos3 != len(implementdata) - 1:
                        pos3 += 1
                    if pos3 != len(implementdata) - 1:
                        pos4 = pos3
                        while implementdata[pos4] != ",":
                            pos4 -= 1
                        settings = implementdata[pos + 1:pos4].strip()
                    else:
                        settings = implementdata[pos + 1:len(implementdata) - 1].strip()
                        pos4 = len(implementdata) - 1
                    idata[variable] = settings.strip()
                    pos = pos4
                pos += 1

            bracketstart = implementdata.find("returns") + len("returns") + 2
            bracketend = bracketstart
            bracketcount = 1
            while bracketend < len(implementdata) and bracketcount != 0:
                if implementdata[bracketend:bracketend + 1] == "(":
                    bracketcount += 1
                if implementdata[bracketend:bracketend + 1] == ")":
                    bracketcount -= 1
                bracketend += 1
            bracketstuff = implementdata[bracketstart:bracketend-1]
            #implementdata = implementdata.replace(bracketstuff,"bracketstuff")

            curlbracketstart = implementdata.find("meta") + len("meta") + 2
            curlbracketend = curlbracketstart
            bracketcount = 1
            metadata = {}

            if curlbracketstart != -1:
                while curlbracketend < len(implementdata) and bracketcount != 0:
                    if implementdata[curlbracketend:curlbracketend + 1] == "{":
                        bracketcount += 1
                    if implementdata[curlbracketend:curlbracketend + 1] == "}":
                        bracketcount -= 1
                    curlbracketend += 1

                metalist = implementdata[curlbracketstart:curlbracketend-1]
                for y in metalist.split(","):
                    itemdata = y.strip().split(":")
                    if itemdata[0] == "NodeMeta.CATEGORY":
                        metadata["CATEGORY"] = itemdata[1].replace("/'", "").strip()
                        #self.ui.txtMetaCategory.setText(itemdata[1])
                    if itemdata[0] == "NodeMeta.KEYWORDS":
                        metadata["KEYWORDS"] = itemdata[1].strip()
                        #self.ui.txtMetaKeywords.setText(itemdata[1])
                    if itemdata[0] == "NodeMeta.CACHE_ENABLED":
                        metadata["CACHE_ENABLED"] = itemdata[1].strip()
                        #self.ui.chkMetaCacheEnabled.setChecked(itemdata[1])


            self.functiondict[defname]["MetaData"] = metadata
            implementdata2.append(implementdata[:curlbracketstart-6])
            implementdata2.append(implementdata[curlbracketstart-6:curlbracketend - 1] + "})")

            #Definition Item
            defs = {}
            pos = 1
            while pos <= len(defdata)-1:
                if defdata[pos] == "=":
                    pos2 = pos
                    while pos2 != -1 and defdata[pos2] != ",":
                        pos2 -= 1
                    variable = defdata[pos2 + 1:pos].strip()
                    pos3 = pos + 1
                    while defdata[pos3] != "=" and pos3 != len(defdata) - 1:
                        pos3 += 1
                    if pos3 != len(defdata) - 1:
                        pos4 = pos3
                        while defdata[pos4] != ",":
                            pos4 -= 1
                        settings = defdata[pos + 1:pos4].strip()
                    else:
                        settings = defdata[pos + 1:len(defdata) - 1].strip()
                        pos4 = len(defdata) - 1
                    defs[variable] = settings.strip()
                    pos = pos4
                pos += 1

            #Output Pin

            outputpinlistmodel = QStandardItemModel(0, 2)
            rowcount = 0
            pinOutCounter = 0
            pindefs = {}
            pindefs["Inputs"] = {}
            pindefs["Outputs"] = {}
            pindata = {}
            data = idata["returns"]

            if data is not None:
                pinOutCounter += 1
                curlbracketstart = data.find("{") + 1
                curlbracketend = curlbracketstart
                bracketcount = 1
                if curlbracketstart != 0:
                    while curlbracketend < len(data) and bracketcount != 0:
                        if data[curlbracketend:curlbracketend + 1] == "{":
                            bracketcount += 1
                        if data[curlbracketend:curlbracketend + 1] == "}":
                            bracketcount -= 1
                        curlbracketend += 1

                    curlystuff3 = data[curlbracketstart:curlbracketend - 1]
                    #data = data.replace(curlystuff3, "curlystuff")
                    pindata = {}
                    for y in curlystuff3.split(","):
                        itemdata = y.strip().split(":")
                        if itemdata[0] == "PinSpecifires.SUPPORTED_DATA_TYPES":
                            pindata["SUPPORTED_DATA_TYPES"] = itemdata[1][1:].strip()
                        if itemdata[0] == "PinSpecifires.CONSTRAINT":
                            pindata["CONSTRAINT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.STRUCT_CONSTRAINT":
                            pindata["STRUCT_CONSTRAINT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.ENABLED_OPTIONS":
                            pindata["ENABLED_OPTIONS"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DISABLED_OPTIONS":
                            pindata["DISABLED_OPTIONS"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.INPUT_WIDGET_VARIANT":
                            pindata["INPUT_WIDGET_VARIANT"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DESCRIPTION":
                            pindata["DESCRIPTION"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.VALUE_LIST":
                            pindata["VALUE_LIST"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.VALUE_RANGE":
                            pindata["VALUE_RANGE"] = itemdata[1].strip()
                        if itemdata[0] == "PinSpecifires.DRAGGER_STEPS":
                            pindata["DRAGGER_STEPS"] = itemdata[1].strip()

                listdata = data.split(",")
                pindata["Name"] = "out"
                pindata["Direction"] = "Out"
                pindata["Order"] = pinOutCounter
                pindata["DataType"] = listdata[0][1:].strip().replace("\"", "").replace("\'", "")
                pindata["DefaultValue"] = listdata[1].strip().replace("))","")
                pindefs["Outputs"]["out"] = pindata

            #InputPin

            rowcount2 = 0

            pindata = {}
            curlystuff3 = None
            PinCounter = 0

            for variable, data in defs.items():
                #print(variable, data)
                PinCounter += 1
                if data.find("REF") == -1:
                    curlbracketstart = data.find("{") + 1
                    curlbracketend = curlbracketstart
                    bracketcount = 1
                    if curlbracketstart != 0:
                        while curlbracketend < len(data) and bracketcount != 0:
                            if data[curlbracketend:curlbracketend + 1] == "{":
                                bracketcount += 1
                            if data[curlbracketend:curlbracketend + 1] == "}":
                                bracketcount -= 1
                            curlbracketend += 1

                        curlystuff3 = data[curlbracketstart:curlbracketend - 1]

                    if curlystuff3 != None: data = data.replace(curlystuff3, "curlystuff")
                    listdata = data.split(",")
                    pindata = {}
                    pindata["Name"] = variable
                    pindata["Direction"] = "In"
                    pindata["Order"] = PinCounter
                    pindata["DataType"] = listdata[0][1:].strip().replace("\"", "").replace("\'", "")
                    if len(listdata) >= 2:
                        pindata["DefaultValue"] = listdata[1].strip()

                    if curlystuff3 is not None:
                        for y in curlystuff3.split(","):
                            itemdata = y.strip().split(":")
                            if itemdata[0] == "PinSpecifires.SUPPORTED_DATA_TYPES":
                                pindata["SUPPORTED_DATA_TYPES"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.CONSTRAINT":
                                pindata["CONSTRAINT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.STRUCT_CONSTRAINT":
                                pindata["STRUCT_CONSTRAINT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.ENABLED_OPTIONS":
                                pindata["ENABLED_OPTIONS"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DISABLED_OPTIONS":
                                pindata["DISABLED_OPTIONS"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.INPUT_WIDGET_VARIANT":
                                pindata["INPUT_WIDGET_VARIANT"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DESCRIPTION":
                                pindata["DESCRIPTION"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.VALUE_LIST":
                                pindata["VALUE_LIST"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.VALUE_RANGE":
                                pindata["VALUE_RANGE"] = itemdata[1].strip()
                            if itemdata[0] == "PinSpecifires.DRAGGER_STEPS":
                                pindata["DRAGGER_STEPS"] = itemdata[1].strip()

                    pindefs["Inputs"][variable] = pindata

                    rowcount2 += 1
                else:
                    pinOutCounter += 1
                    startvalue = data.find("\"")
                    if startvalue == -1:
                        startvalue = data.find("\'")

                    endvalue = data.find(")")
                    pindata = {}
                    pindata["Name"] = variable
                    pindata["Direction"] = "Out"
                    pindata["Order"] = pinOutCounter

                    listdata = data[startvalue:endvalue].split(",")
                    pindata["DataType"] = listdata[0].strip().replace("\"", "").replace("\'", "")

                    if len(listdata) >= 2:
                        pindata["DefaultValue"] = listdata[1].strip().replace(")","")

                    pindefs["Outputs"][variable] = pindata

                    rowcount += 1

            self.functiondict[defname] = pindefs

            self.functiondict[defname]["Implement"] = implementdata2

            for variable, data in defs.items():
                defdata2.append(variable + "=" + data)

            self.functiondict[defname]["Definition"] = defdata2

    def onPinScan(self):
        packageRoot = Packages.__path__[0]
        self.pinDict = {}
        for root, dirs, files in os.walk(packageRoot, topdown=False):
            for name in files:
                directories = os.path.join(root, name)
                if "Pin.py" in name:
                    PinName = name.replace(".py", "")
                    self.pinDict[PinName] = directories
    def loadPinTable(self, defname):
        # InputPin
        pinTransDict = {"ArrayPin": "Array", "ExecPin": "Execution", "AnyPin": "Anything",
                        "BoolPin": "Boolean", "IntPin": "Integer",
                        "FloatPin": "Float", "StringPin": "String"}

        pindatatypemodel = QStandardItemModel(0, 2)
        for index, key in enumerate(self.pinDict):
            pindatatypemodel.setItem(index, 0, QtGui.QStandardItem(str(index)))
            pindatatypemodel.setItem(index, 1, QtGui.QStandardItem(pinTransDict[key]))

        if "PinDefs" in self.functiondict[defname]:
            inputpinlistmodel = QStandardItemModel(0, 2)
            inputPinList = []
            if "Inputs" in self.functiondict[defname]:
                row2 = 0
                for pindata in self.functiondict[defname]["Inputs"]:
                    row = int(self.functiondict[defname]["Inputs"][pindata]["Order"]) - 1
                    if row == -1:
                        row = row2
                    inputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))
                    DataTypeValue = ""
                    inputvalue = self.functiondict[defname]["Inputs"][pindata]["DataType"]
                    if "DataType" in self.functiondict[defname]["Inputs"][pindata]:
                        DataTypeValue = self.findPinType(
                            self.functiondict[defname]["Inputs"][pindata]["DataType"])
                        inputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(DataTypeValue))
                        if DataTypeValue is None:
                            a = self.functiondict[defname]["Inputs"][pindata]["DataType"]

                    inputPinList.append(DataTypeValue)
                    if "DefaultValue" in self.functiondict[defname]["Inputs"][pindata]:
                        inputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(str(self.functiondict[defname]["Inputs"][pindata]["DefaultValue"])))
                    row2 += 1

                inputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                inputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            outputPinList = []
            if "Outputs" in self.functiondict[defname]:
                outputpinlistmodel = QStandardItemModel(0, 2)
                row2 = 0
                for rowcount2, pindata in enumerate(self.functiondict[defname]["Outputs"]):
                    row = int(self.functiondict[defname]["Outputs"][pindata]["Order"]) - 1
                    if row == -1:
                        row = row2
                    DataTypeValue = ""
                    inputvalue = self.functiondict[defname]["Outputs"][pindata]["DataType"]
                    if rowcount2 == 0:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem("out"))
                    else:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))

                    if "DataType" in self.functiondict[defname]["Outputs"][pindata]:
                        DataTypeValue = self.findPinType(self.functiondict[defname]["Outputs"][pindata]["DataType"])
                        if DataTypeValue is None:
                            a = self.functiondict[defname]["Outputs"][pindata]["DataType"]
                        outputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(DataTypeValue))

                    outputPinList.append(DataTypeValue)

                    if "DefaultValue" in self.functiondict[defname]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(str(self.functiondict[defname]["Outputs"][pindata]["DefaultValue"])))
                    row2 += 1

                outputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            self.ui.tblFInputPins.setModel(inputpinlistmodel)
            self.ui.tblFOutputPins.setModel(outputpinlistmodel)

        if "Inputs" in self.functiondict[defname]:
            for row, data in enumerate(self.functiondict[defname]["Inputs"]):
                self.ui.tblFInputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                c.setValue(self.functiondict[defname]["Inputs"][data]["DataType"], 1)
                i = self.ui.tblFInputPins.model().index(row, 1)
                #c.currentIndexChanged2[dict].connect(self.on_lstPinSettings_cmbTableChanged)
                self.ui.tblFInputPins.setIndexWidget(i, c)

        if "Outputs" in self.functiondict[defname]:
            for row, data in enumerate(self.functiondict[defname]["Outputs"]):
                self.ui.tblFOutputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                c.setValue(self.functiondict[defname]["Outputs"][data]["DataType"], 1)
                i = self.ui.tblFOutputPins.model().index(row, 1)
                #c.currentIndexChanged2[dict].connect(self.on_lstTableSettings_cmbTableChanged)
                self.ui.tblFOutputPins.setIndexWidget(i, c)

            #self.ui.tblFInputPins.resizeColumnsToContents()
            #self.ui.tblFOutputPins.resizeColumnsToContents()

            #self.ui.tblFInputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))
            #self.ui.tblFOutputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))

            self.initializePinData()

            '''for z in curlystuff2.split(","):
                itemdata = z.strip().split(":")
                #print(itemdata[0], itemdata[1].strip())'''

    def findPinType(self, pinname):
        pinTransDict2 = {"Execution": ["execpin", "exec", "execution", "exec"],
                         "Anything": ["anypin", "anything", "any"],
                         "Array": ["arraypin", "array", "arr"],
                         "Boolean": ["boolpin", "boolean", "bool"],
                         "Integer": ["intpin", "integer", "int"],
                         "Float": ["floatpin", "float", "double", "number", "num", "real", "decimal", "doub", "numeric"],
                         "String": ["stringpin", "string", "str"]}

        for pinType in pinTransDict2:
            if pinname.lower() in pinTransDict2[pinType]:
                return pinType

    def on_lstPinSettings_cmbTableChanged(self, int):
        print(int)

    def get_function_signature(self, function_obj, parent, name, package_name, packagedict):
        child = QTreeWidgetItem(parent)
        child.setText(0, name)

        if "." in name:
            func = name.split(".")
            if func[0] not in self.functionFileList:
                packagedict.append(func[0])
        try:
            # Create Functions
            functionGroup = parent.text(0)
            if len(functionGroup) <= 1:
                print("No Function Group")
            else:
                functionName = name

                '''if "." in name:
                    namesplit = name.split(".")
                    functionGroup = namesplit[-2]
                    functionName = namesplit[-1]'''

                if functionGroup not in packagedict:
                    packagedict[functionGroup] = {}
                if functionName not in packagedict[functionGroup]:
                    packagedict[functionGroup][functionName] = {}

                descriptionlist = "Not put into effect yet"
                '''PROMPT = f"With the Python Package {package_name} please describe the function {functionName}."
                descriptionlist = self.comp(PROMPT, 250, 1)
                inputData = {"label": "Description", "default": "Dialog", "button": "Accept",
                             "title": f"Create Description for {functionName}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
                dialog = ListSelectionDialog(inputData, descriptionlist)
    
                if dialog.exec_() == QDialog.Accepted:
                    descriptionselected = dialog.selected_item()'''

                packagedict[functionGroup][functionName]["Description"] = descriptionlist
                categoryselected = []
                categoryselected.append(package_name)
                if functionGroup not in categoryselected:
                    categoryselected.append(functionGroup)
                if functionName not in categoryselected:
                    categoryselected.append(functionName)

                packagedict[functionGroup][functionName]["Category"] = categoryselected

                PROMPT = f"With the Python Package {package_name} please list keywords for the function {functionName}.  Please list in single words separated by a comma."
                #keywordselection = self.comp(PROMPT, 15, 1)
                inputData = {"label": "Dialog Name", "default": "Dialog", "button": "Create",
                             "title": "Create New Dialog", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
                keywordselection = "Test"
                keywords = []
                for keywordlist in keywordselection:
                    keywordlist2 = keywordlist.split(",")
                    for keyword in keywordlist2:
                        keyword = keyword.strip()
                        keyword = keyword.title()
                        keyword = keyword.replace(".", "")

                        if keyword not in keywords and keyword != "":
                            keywords.append(keyword)
                '''dialog = ListItemSelectionDialog(inputData, keywords)
    
                if dialog.exec_() == QDialog.Accepted:
                    keywordselected = dialog.selected_items()'''

                packagedict[functionGroup][functionName]["Keywords"] = keywords

                PROMPT = f"With the Python Package {package_name} please write a tooltip for the function {functionName}"
                tooltiplist = "Test"
                '''tooltiplist = self.comp(PROMPT, 250, 1)
                inputData = {"label": "Tooltip", "default": "Dialog", "button": "Create",
                             "title": "Create Tooltip", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
                dialog = ListItemSelectionDialog(inputData, tooltiplist)
                if dialog.exec_() == QDialog.Accepted:
                    tooltipselected = dialog.selected_items()
                    packagedict[functionGroup][functionName]["ToolTip"] = tooltipselected'''

                packagedict[functionGroup][functionName]["KeyboardShortCut"] = ""

                '''inputData = {"label": "Logo", "default": "Dialog", "button": "Create",
                             "title": "Logo", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
                dialog = IconSelectionDialog(inputData, RESOURCES_DIR)
                if dialog.exec_() == QDialog.Accepted and dialog.selected_icon() is not None:
                    print('You selected an icon.')
                else:
                    print('Operation cancelled.')'''

                packagedict[functionGroup][functionName]["SmallIcon"] = ""
                packagedict[functionGroup][functionName]["MediumIcon"] = ""
                packagedict[functionGroup][functionName]["LargeIcon"] = ""

                packagedict[functionGroup][functionName] = {}
                packagedict[functionGroup][functionName]["MetaData"] = {}
                packagedict[functionGroup][functionName]["MetaData"]["CATEGORY"] = categoryselected
                packagedict[functionGroup][functionName]["MetaData"]["KEYWORDS"] = keywords
                packagedict[functionGroup][functionName]["MetaData"]["DESCRIPTION"] = descriptionlist[0]
                packagedict[functionGroup][functionName]["MetaData"]["TOOLTIP"] = tooltiplist[0]
                packagedict[functionGroup][functionName]["MetaData"]["CACHE_ENABLED"] = False

                packagedict[functionGroup][functionName]["Inputs"] = {}
                packagedict[functionGroup][functionName]["Outputs"] = {}

                sig = inspect.signature(function_obj)

                pinDict2 = {"Array": {"Name": "ArrayPin", "DefaultValue": None},
                            "Boolean": {"Name": "BooleanPin", "DefaultValue": False},
                            "Integer": {"Name": "IntegerPin", "DefaultValue": 0},
                            "Float": {"Name": "FloatPin", "DefaultValue": 0.0},
                            "String": {"Name": "StringPin", "DefaultValue": ""},
                            "File": {"Name": "FilePin", "DefaultValue": None},
                            "Folder": {"Name": "FolderPin", "DefaultValue": None},
                            "Point": {"Name": "PointPin", "DefaultValue": None}}
                pinlist = list(pinDict2.keys())

                inputcount = 0
                inputlist = []
                for paramname, param in sig.parameters.items():
                    inputlist.append(paramname)
                    descriptionselected = "This value would be activated in the code at line 1635"
                    '''PROMPT = f"Python Package {package_name} and function {functionName}, what is the description for the parameter {paramname}?"
                    description = self.comp(PROMPT, 255, 1)
                    inputData = {"label": "Description", "default": "Dialog", "button": "Accept",
                                 "title": f"Create Description for {paramname} in {functionName}",
                                 "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
                    dialog = ListSelectionDialog(inputData, descriptionlist)
                    if dialog.exec_() == QDialog.Accepted:
                        descriptionselected = dialog.selected_item()'''

                    packagedict[functionGroup][functionName]["Description"] = descriptionselected

                    '''defaultvalue1 = param.default
                    PROMPT = f"In a single word, with the Python Package {package_name} and function {functionName}, what is the default value for the parameter {paramname}?  Say None if there is no default value"
                    defaultvalue = self.comp(PROMPT, 255, 1)[0]'''

                    PROMPT = f"With the Python Package {package_name} and function {functionName} what are the acceptable datatypes for the parameter {paramname} that would " \
                             f"best match this this list: {pinlist}?" \
                             f"Please return values as comma separated list.  If there are no matches, please say None"
                    #datatype = self.comp(PROMPT, 15, 1)[0]
                    datatype = "Test"

                    datatype2 = []
                    defaultlist = []

                    if datatype is not None:
                        for datatype1 in datatype.split(","):
                            datatype1 = datatype1.strip()
                            if datatype1 in pinlist:
                                datatype2.append(pinDict2[datatype1]["Name"])
                                defaultlist.append(pinDict2[datatype1]["DefaultValue"])

                    if datatype2 == []:
                        datatype2 = ['AnyType']
                        defaultlist = [None]

                    data = {}

                    data["DefaultValue"] = defaultlist[0]
                    data["Order"] = inputcount
                    data["Parent"] = parent.text(0)
                    data["DataType"] = datatype2

                    data["SUPPORTED_DATA_TYPES"] = datatype2
                    data["CONSTRAINT"] = None
                    data["STRUCT_CONSTRAINT"] = None
                    data["ENABLED_OPTIONS"] = None
                    data["DISABLED_OPTIONS"] = None
                    data["INPUT_WIDGET_VARIANT"] = None
                    data["DESCRIPTION"] = descriptionselected[0]
                    data["VALUE_LIST"] = None
                    data["VALUE_RANGE"] = None
                    data["DRAGGER_STEPS"] = None

                    packagedict[functionGroup][functionName]["Inputs"][paramname] = data
                    inputcount += 1

                data = {}
                PROMPT = f"With the Python Package {package_name} and function {functionName} what is the datatype for return that would " \
                         f"best match this this list: {pinlist}?" \
                         f"Please return values as comma separated list.  If there are no matches, please say None"

                #datatype = self.comp(PROMPT, 15, 1)[0]
                datatype = "Test"
                datatypeb = sig.return_annotation

                datatype2 = []
                defaultlist = []

                if datatype is not None:
                    for datatype1 in datatype.split(","):
                        datatype1 = datatype1.strip()
                        if datatype1 in pinlist:
                            datatype2.append(pinDict2[datatype1]["Name"])
                            defaultlist.append(pinDict2[datatype1]["DefaultValue"])

                if datatype2 == []:
                    datatype2 = ['AnyType']
                    defaultlist = [None]

                data["DefaultValue"] = defaultlist[0]
                data["Order"] = 1
                data["DataType"] = datatype2[0]
                data["SUPPORTED_DATA_TYPES"] = datatype2
                data["CONSTRAINT"] = None
                data["STRUCT_CONSTRAINT"] = None
                data["ENABLED_OPTIONS"] = None
                data["DISABLED_OPTIONS"] = None
                data["OUTPUT_WIDGET_VARIANT"] = None
                data["DESCRIPTION"] = None
                data["VALUE_LIST"] = None
                data["VALUE_RANGE"] = None
                data["DRAGGER_STEPS"] = None
                packagedict[functionGroup][functionName]["Outputs"]["out"] = data
                self.writeFunction(functionGroup, functionName)

                inputstring = ", ".join(inputlist)

                packagedict[functionGroup][functionName]["Code"] = [f"        return {functionName}({inputstring})"]
                packagedict[functionGroup][functionName]["DocString"] = ""
                packagedict[functionGroup][functionName]["ExampleCode"] = ""

        except ValueError:
            pass  # Some built-in functions, C functions, or functions with *args, **kwargs can cause inspect.signature to raise ValueError

    def get_module_functions(self, parent, module, package_name, packagedict):

        for f in dir(module):
            if f.startswith('_'):  # Skip internal functions
                continue
            function_obj = getattr(module, f)
            if isinstance(function_obj, types.FunctionType):
                self.get_signature(function_obj, parent, f, package_name, packagedict)
            elif inspect.isclass(function_obj):
                for name, member in inspect.getmembers(function_obj):
                    if isinstance(member, (types.MethodType, types.FunctionType)):
                        if name[0] != '_':
                            self.get_signature(member, parent, f'{f}.{name}', package_name, packagedict)

    def try_import(self, function_name, package_name, packagedict):
        try:
            if function_name == "Any":
                pass
            else:
                try:
                    a = importlib.import_module(function_name)
                    return a
                except:
                    print(f"Error loading Function {function_name}")
                    #todo: add a dialog box here

        except ImportError:
            try:
                return importlib.import_module(function_name.lower())
            except ImportError:
                if False:
                    inputData = {
                        "label": f"Error Loading Package {function_name}",
                        "default": "",
                        "button": "Load",
                        "title": "Import Error",
                        "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")
                    }
                    dialog = InputDialog(inputData)
                    defname = dialog.get_value()
                    try:
                        if defname:
                            return importlib.import_module(defname)
                        else:
                            pass
                    except ImportError:
                        pass  # Handle failed imports how you wish here

    def get_package_functions(self, parent, function_name, package_name, packagedict):
        package = self.try_import(function_name, package_name, packagedict)
        if package is not None:
            self.get_module_functions(parent, package, package_name, packagedict)
            if hasattr(package, '__path__'):
                for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                    full_name = function_name + '.' + name
                    child = QTreeWidgetItem(parent)
                    child.setText(0, name)
                    if is_pkg:
                        self.get_package_functions(child, full_name, package_name, packagedict)
                    else:
                        if "._" not in full_name:
                            module = self.try_import(full_name, package_name, packagedict)
                            if module is not None:
                                self.get_module_functions(child, module, package_name, packagedict)

    @QtCore.Slot()
    def on_cmdLoadPackage_clicked(self):
        self.ui.tvLoadedApps.clear()
        for d in distributions():
            parent = QTreeWidgetItem(self.ui.tvLoadedApps)
            parent.setText(0, f"{d.metadata['Name']}") #=={d.version}
        self.newfunctiondict = {}
        self.ui.tvLoadedApps.itemClicked.connect(self.on_tvLoadedApps_itemClicked)


    def on_cmdReadFile_clicked(self):
        item = self.ui.tvPackageItems.currentItem()
        packagename = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        filename = item.text(0).replace(".py", "")
        column = self.ui.tvLoadedApps.currentColumn()

        filefullpath = Packages.__path__[0] + "\\"

        filefullpath = os.path.join(filefullpath, packagename)
        filefullpath = os.path.join(filefullpath, item.text(0))

        #self.initfilecommandDict(packagename)

        with open(filefullpath) as f:
            code = f.read()
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    child = QTreeWidgetItem(item)
                    child.setText(0, node.name)
                    grandchild = QTreeWidgetItem(child)
                    grandchild.setText(0, "Inputs")
                    for arg in node.args.args:
                        if "self" not in arg.arg:
                            greatgrandchild = QTreeWidgetItem(grandchild)
                            greatgrandchild.setText(0, arg.arg)
                    if node.returns:
                        grandchild = QTreeWidgetItem(child)
                        grandchild.setText(0, "Output")
                        greatgrandchild = QTreeWidgetItem(grandchild)
                        greatgrandchild.setText(0, node.returns.id)

    @QtCore.Slot()
    def on_tvLoadedApps_itemClicked(self, item, column):
        if column == 0:
            pass

    def on_cmdCUpdateAppFunction_clicked(self):
        item = self.ui.tvLoadedApps.currentItem()
        packagename = item.text(0)

        column = self.ui.tvLoadedApps.currentColumn()

        self.commandFileList = []
        self.functionFileList = []

        self.get_package_functions(item, item.text(column), item.text(column), self.commanddict)

        for functionGroup in self.functiondict:
            self.writeFunctionFile(packagename, functionGroup)

        self.updateFunctionInit(packagename)

    def on_cmdCreateAppPackage_clicked(self):
        item = self.ui.tvLoadedApps.currentItem()
        packagename = item.text(0)

        column = self.ui.tvLoadedApps.currentColumn()
        self.functionFileList = []
        self.createPackage(packagename.title())
        self.get_package_functions(item, item.text(column), item.text(column))

        for functionGroup in self.functiondict:
                self.writeFile(packagename, functionGroup)

        self.updateInit(packagename)

    def on_cmdReadPackage_clicked(self):
        item = self.ui.tvLoadedApps.currentItem()
        column = self.ui.tvLoadedApps.currentColumn()
        self.get_package_functions(item, item.text(column), item.text(column), self.commanddict)

    def on_cmdCreateCommand_clicked(self):
        item = self.ui.tvLoadedApps.currentItem()
        column = self.ui.tvLoadedApps.currentColumn()
        #self.get_command_signature()
        #self.get_package_functions(item, item.text(column), item.text(column))

        item2 = self.ui.tvPackageItems.currentItem()
        column2 = self.ui.tvPackageItems.currentColumn()
        classname = item2.parent().text(0)
        defname = item2.text(column2)
        if defname not in self.commanddict:
            self.commanddict[defname] = self.fileDict[classname][defname]
        #self.commanddict[defname] = self.fileDict[classname][defname]
        if self.commanddict[defname]["PythonCode"] == "":
            codelist = []
            codelist.append("newClass = self.PackageInstance.instance.instance(self.ProgramManagerInstance)")
            codelist.append(f"self.ProgramManagerInstance.instance.{defname}()")
        self.commanddict[defname]["PythonCode"] = codelist

        self.createNewCommand(defname)

    def initializeFunctionForm(self):

        self.ui.txtFunctionFileName.setText("")
        self.ui.txtFunctionName.setText("")
        #self.ui.tblFInputPins
        #self.ui.tblFOutputPins
        self.ui.txtFImplement.setText("")
        self.ui.txtFDef.setText("")
        self.ui.txtCodeDescription.setText("")
        self.ui.txtCode.setText("")

        self.ui.txtMetaCategory.setText("")
        self.ui.txtMetaKeywords.setText("")
        self.ui.chkMetaCacheEnabled.setChecked(False)

    def blockPinSignals(self):
        self.ui.chkPSSupportedDataTypes.blockSignals(True)
        self.ui.chkPSSupportedDataTypes.blockSignals(True)
        self.ui.txtPSSupportedDataTypes.blockSignals(True)
        self.ui.chkPSConstraint.blockSignals(True)
        self.ui.txtPSConstraint.blockSignals(True)
        self.ui.chkPSStructConstraint.blockSignals(True)
        self.ui.txtPSStructConstraint.blockSignals(True)
        #self.ui.chkPSEnableOptions.blockSignals(True)
        #self.ui.txtPSEnableOptions.blockSignals(True)
        self.ui.chkPSDisableOptions.blockSignals(True)
        self.ui.txtPSDisableOptions.blockSignals(True)
        self.ui.chkPSInputWidget.blockSignals(True)
        self.ui.txtPSInputWidget.blockSignals(True)
        self.ui.chkPSDescription.blockSignals(True)
        self.ui.txtPSDescription.blockSignals(True)
        self.ui.chkPSValueList.blockSignals(True)
        self.ui.txtPSValueList.blockSignals(True)
        self.ui.chkPSValueRange.blockSignals(True)
        self.ui.txtPSValueRange.blockSignals(True)
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.blockSignals(True)

        self.ui.chkArraySupported.blockSignals(True)
        self.ui.chkDictionarySupported.blockSignals(True)
        self.ui.chkSupportOnlyArrays.blockSignals(True)
        self.ui.chkAllowMultipleConnections.blockSignals(True)
        self.ui.chkChangeTypeOnConnection.blockSignals(True)
        self.ui.chkRenamingEnabled.blockSignals(True)
        self.ui.chkDynamic.blockSignals(True)
        self.ui.chkAlwaysPushDirty.blockSignals(True)
        self.ui.chkStorable.blockSignals(True)
        self.ui.chkAllowAny.blockSignals(True)
        self.ui.chkDictionaryElementSupported.blockSignals(True)

    def unblockPinSignals(self):
        self.ui.chkPSSupportedDataTypes.blockSignals(False)
        self.ui.txtPSSupportedDataTypes.blockSignals(False)
        self.ui.chkPSConstraint.blockSignals(False)
        self.ui.txtPSConstraint.blockSignals(False)
        self.ui.chkPSStructConstraint.blockSignals(False)
        self.ui.txtPSStructConstraint.blockSignals(False)
        #self.ui.chkPSEnableOptions.blockSignals(False)
        #self.ui.txtPSEnableOptions.blockSignals(False)
        self.ui.chkPSDisableOptions.blockSignals(False)
        self.ui.txtPSDisableOptions.blockSignals(False)
        self.ui.chkPSInputWidget.blockSignals(False)
        self.ui.txtPSInputWidget.blockSignals(False)
        self.ui.chkPSDescription.blockSignals(False)
        self.ui.txtPSDescription.blockSignals(False)
        self.ui.chkPSValueList.blockSignals(False)
        self.ui.txtPSValueList.blockSignals(False)
        self.ui.chkPSValueRange.blockSignals(False)
        self.ui.txtPSValueRange.blockSignals(False)
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.blockSignals(False)

        self.ui.chkArraySupported.blockSignals(False)
        self.ui.chkDictionarySupported.blockSignals(False)
        self.ui.chkSupportOnlyArrays.blockSignals(False)
        self.ui.chkAllowMultipleConnections.blockSignals(False)
        self.ui.chkChangeTypeOnConnection.blockSignals(False)
        self.ui.chkRenamingEnabled.blockSignals(False)
        self.ui.chkDynamic.blockSignals(False)
        self.ui.chkAlwaysPushDirty.blockSignals(False)
        self.ui.chkStorable.blockSignals(False)
        self.ui.chkAllowAny.blockSignals(False)
        self.ui.chkDictionaryElementSupported.blockSignals(False)

    def initializePinData(self):
        self.blockPinSignals()
        self.ui.chkPSSupportedDataTypes.setChecked(False)
        self.ui.txtPSSupportedDataTypes.setText("")
        self.ui.chkPSConstraint.setChecked(False)
        self.ui.txtPSConstraint.setText("")
        self.ui.chkPSStructConstraint.setChecked(False)
        self.ui.txtPSStructConstraint.setText("")
        #self.ui.chkPSEnableOptions.setChecked(False)
        #self.ui.txtPSEnableOptions.setText("")
        self.ui.chkPSDisableOptions.setChecked(False)
        self.ui.txtPSDisableOptions.setText("")
        self.ui.chkPSInputWidget.setChecked(False)
        self.ui.txtPSInputWidget.setText("")
        self.ui.chkPSDescription.setChecked(False)
        self.ui.txtPSDescription.setText("")
        self.ui.chkPSValueList.setChecked(False)
        self.ui.txtPSValueList.setText("")
        self.ui.chkPSValueRange.setChecked(False)
        self.ui.txtPSValueRange.setText("")
        self.ui.chkPSDraggerSteps.setChecked(False)
        self.ui.txtPSDraggerSteps.setText("")

        self.ui.chkArraySupported.setChecked(False)
        self.ui.chkDictionarySupported.setChecked(False)
        self.ui.chkSupportOnlyArrays.setChecked(False)
        self.ui.chkAllowMultipleConnections.setChecked(False)
        self.ui.chkChangeTypeOnConnection.setChecked(False)
        self.ui.chkRenamingEnabled.setChecked(False)
        self.ui.chkDynamic.setChecked(False)
        self.ui.chkAlwaysPushDirty.setChecked(False)
        self.ui.chkStorable.setChecked(False)
        self.ui.chkAllowAny.setChecked(False)
        self.ui.chkDictionaryElementSupported.setChecked(False)
        self.unblockPinSignals()

    def writepindata(self):
        self.functiondict = {}

    @QtCore.Slot(int)
    def on_chkPSSupportedDataTypes_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SUPPORTED_DATA_TYPES"] = self.ui.txtPSSupportedDataTypes.text()

    @QtCore.Slot(str)
    def on_txtPSSupportedDataTypes_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SUPPORTED_DATA_TYPES"] = self.ui.txtPSSupportedDataTypes.text()

    @QtCore.Slot(int)
    def on_chkPSConstraint_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["CONSTRAINT"] = self.ui.txtPSConstraint.text()

    @QtCore.Slot(str)
    def on_txtPSConstraint_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["CONSTRAINT"] = self.ui.txtPSConstraint.text()

    @QtCore.Slot(int)
    def on_chkPSStructConstraint_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["STRUCT_CONSTRAINT"] = self.ui.txtPSStructConstraint.text()

    @QtCore.Slot(str)
    def on_txtPSStructConstraint_stateChanged(self):
        a = self.ui.txtPSStructConstraint.text()
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["STRUCT_CONSTRAINT"] = self.ui.txtPSStructConstraint.text()

    @QtCore.Slot(int)
    def on_chkPSDisableOptions_stateChanged(self):
        a = self.ui.chkPSDisableOptions.isChecked()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.setFunctionDirty()

    @QtCore.Slot(str)
    def on_txtPSDisableOptions_textChanged(self):
        b = self.ui.txtPSDisableOptions.text()
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)

    @QtCore.Slot(int)
    def on_chkPSInputWidget_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["INPUT_WIDGET_VARIANT"] = self.ui.txtPSInputWidget.text()

    @QtCore.Slot(str)
    def on_txtPSInputWidget_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["INPUT_WIDGET_VARIANT"] = self.ui.txtPSInputWidget.text()

    @QtCore.Slot(int)
    def on_chkPSDescription_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DESCRIPTION"] = self.ui.txtPSDescription.text()

    @QtCore.Slot(str)
    def on_txtPSDescription_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DESCRIPTION"] = self.ui.txtPSDescription.text()

    @QtCore.Slot(int)
    def on_chkPSValueList_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_LIST"] = self.ui.txtPSValueList.text()

    @QtCore.Slot(str)
    def on_txtPSValueList_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_LIST"] = self.ui.txtPSValueList.text()

    @QtCore.Slot(int)
    def on_chkPSValueRange_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_RANGE"] = self.ui.txtPSValueRange.text()

    @QtCore.Slot(str)
    def on_txtPSValueRange_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["VALUE_RANGE"] = self.ui.txtPSValueRange.text()

    @QtCore.Slot(int)
    def on_chkPSDraggerSteps_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DRAGGER_STEPS"] = self.ui.txtPSDraggerSteps.text()

    @QtCore.Slot(str)
    def on_txtPSDraggerSteps_textChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DRAGGER_STEPS"] = self.ui.txtPSDraggerSteps.text()

    @QtCore.Slot(int)
    def on_chkArraySupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["ArraySupported"] = self.ui.chkArraySupported.isChecked()

    @QtCore.Slot(int)
    def on_chkDictionarySupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DictSupported"] = self.ui.chkDictionarySupported.isChecked()

    @QtCore.Slot(int)
    def on_chkSupportOnlyArrays_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["SupportsOnlyArrays"] = self.ui.chkSupportOnlyArrays.isChecked()

    @QtCore.Slot(int)
    def on_chkAllowMultipleConnections_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AllowMultipleConnections"] = self.ui.chkAllowMultipleConnections.isChecked()

    @QtCore.Slot(int)
    def on_chkChangeTypeOnConnection_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["ChangeTypeOnConnection"] = self.ui.chkChangeTypeOnConnection.isChecked()

    @QtCore.Slot(int)
    def on_chkRenamingEnabled_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["RenamingEnabled"] = self.ui.chkRenamingEnabled.isChecked()

    @QtCore.Slot(int)
    def on_chkDynamic_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["Dynamic"] = self.ui.chkDynamic.isChecked()

    @QtCore.Slot(int)
    def on_chkAlwaysPushDirty_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AlwaysPushDirty"] = self.ui.chkAlwaysPushDirty.isChecked()

    @QtCore.Slot(int)
    def on_chkStorable_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["Storable"] = self.ui.chkStorable.isChecked()

    @QtCore.Slot(int)
    def on_chkAllowAny_stateChanged(self, value):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["AllowAny"] = self.ui.chkAllowAny.isChecked()

    @QtCore.Slot(int)
    def on_chkDictionaryElementSupported_stateChanged(self):
        self.setFunctionDirty()
        self.pinDictCheck(self.selectedPinDir, self.selectedPinName)
        self.pindefs[self.selectedPinDir][self.selectedPinName]["DictElementSupported"] = self.ui.chkDictionaryElementSupported.isChecked()

    def pinDictCheck(self, Direction, PinName):
        if Direction not in self.pindefs:
            self.pindefs[Direction] = {}

        if PinName not in self.pindefs["Inputs"] and PinName not in self.pindefs["Outputs"]:
            self.pindefs[Direction][PinName] = {}
            return(True)
        else:
            return(False)

    @QtCore.Slot()
    def on_cmdUpOrderFInputPin_clicked(self):
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]

        if order > 1:
            for key, data in self.pindefs["Inputs"].items():
                if data["Order"] == order - 1:
                    data["Order"] += 1
                    self.pindefs["Inputs"][self.selectedPinName]["Order"] -= 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdDownOrderFInputPin_clicked(self):
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]

        if order < len(self.pindefs["Inputs"]):
            for key, data in self.pindefs["Inputs"].items():
                if data["Order"] == order + 1:
                    data["Order"] -= 1
                    self.pindefs["Inputs"][self.selectedPinName]["Order"] += 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdAddFInputPin_clicked(self):
        self.setFunctionDirty()
        if self.ui.txtFunctionName.text() != "":

            newPinName = "NewPinName"
            pinnum = ""
            counter = 0
            while not self.pinDictCheck("Inputs", newPinName + pinnum):
                counter += 1
                pinnum = "_" + str(counter)

            newPinName = newPinName + pinnum

            self.pindefs["Inputs"][newPinName]["DataType"] = 'AnyPin'
            self.pindefs["Inputs"][newPinName]["DefaultValue"] = 'None'
            self.pindefs["Inputs"][newPinName]["Order"] = len(self.pindefs["Inputs"])
            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdRemoveFInputPin_clicked(self):
        self.setFunctionDirty()
        order = self.pindefs["Inputs"][self.selectedPinName]["Order"]
        self.pindefs["Inputs"].pop(self.selectedPinName)
        for key, data in self.pindefs["Inputs"].items():
            if data["Order"] > order:
                data["Order"] -= 1
        self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdUpOrderFOutputPin_clicked(self):
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]

        if order > 1:
            for key, data in self.pindefs["Outputs"].items():
                if data["Order"] == order - 1:
                    data["Order"] += 1
                    self.pindefs["Outputs"][self.selectedPinName]["Order"] -= 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdDownOrderFOutputPin_clicked(self):
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]

        if order < len(self.pindefs["Outputs"]):
            for key, data in self.pindefs["Outputs"].items():
                if data["Order"] == order + 1:
                    data["Order"] -= 1
                    self.pindefs["Outputs"][self.selectedPinName]["Order"] += 1
                    break

            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdAddFOutputPin_clicked(self):
        self.setFunctionDirty()
        if self.ui.txtFunctionName.text() != "":
            newPinName = "NewPinName"
            pinnum = ""
            counter = 0
            while not self.pinDictCheck("Outputs", newPinName + pinnum):
                counter += 1
                pinnum = "_" + str(counter)

            newPinName = newPinName + pinnum

            self.pinDictCheck("Outputs", "NewPinName")
            self.pindefs["Outputs"][newPinName]["DataType"] = 'AnyPin'
            self.pindefs["Outputs"][newPinName]["DefaultValue"] = 'None'
            self.pindefs["Outputs"][newPinName]["Order"] = len(self.pindefs["Outputs"])
            self.loadPinTable(self.ui.txtFunctionName.text())

    @QtCore.Slot()
    def on_cmdRemoveFOutputPin_clicked(self):
        self.setFunctionDirty()
        order = self.pindefs["Outputs"][self.selectedPinName]["Order"]
        self.pindefs["Outputs"].pop(self.selectedPinName)
        for key, data in self.pindefs["Outputs"].items():
            if data["Order"] > order:
                data["Order"] -= 1
        self.loadPinTable(self.ui.txtFunctionName.text())

    def setFunctionDirty(self):
        self.ui.cmdSaveFunction.setEnabled(True)
        self.ui.cmdSaveFunction.setVisible(True)
        self.ui.cmdSaveFunction.setStyleSheet("background-color: red")

    @QtCore.Slot()
    def on_cmdSaveFunction_clicked(self):
        self.ui.cmdSaveFunction.setEnabled(False)
        self.ui.cmdSaveFunction.setVisible(False)
        functiongroup = ""
        defname = self.ui.txtFunctionName.text()
        self.writeFunction(functiongroup, defname)
        filename = self.ui.txtFunctionFileName.text()
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        self.writeFile(selectedpackage, filename)

    @QtCore.Slot()
    def on_cmdCreateNewFunction_clicked(self):
        functionName = self.ui.txtFunctionName.text()
        if functionName not in self.functiondict:

            self.setFunctionDirty()
            self.functiondict[functionName] = {}

            self.functiondict[functionName] = {}
            self.functiondict[functionName]["Implement"] = {}
            self.functiondict[functionName]["Definition"] = {}
            self.functiondict[functionName]["MetaData"] = {}
            self.functiondict[functionName]["Code"] = ["Pass"]

            #self.initializeFunctionForm
            self.initializePinData

            #self.loadAllFunctions()
            #self.loadPinTable(deft)
        else:
            print("Function Name Taken")

    def renamePin(self, mydict, old_key, new_key):
        mydict[new_key] = mydict.pop(old_key)

    def loadAllFunctions(self):
        try:
            f = open(self.functionlibrarypath, "r")
            for lineitem in f:
                if lineitem.find("def ") != -1:
                    if lineitem[8] != "_":
                        classnamestart = 7
                        classnameend = lineitem.find("(")
                        classname = lineitem[classnamestart+1:classnameend]
                        if classname in self.workingFile:
                            functionname = lineitem[classnamestart+1:classnameend]
                            self.functiondict[functionname] = {}
                            self.loadFunctionCode(self.functionlibrarypath, functionname)
        except:
            pass

    def writeFunction(self, functiongroup, defname):

        implementdata = []
        defindata = []
        defoutdata = []

        print(functiongroup, defname)
        idata = "@IMPLEMENT_NODE(returns=("
        # @IMPLEMENT_NODE(returns=('AnyPin', None, {
        outCounter = 0
        if "out" in self.functiondict[functiongroup][defname]["Outputs"]:
            data = self.functiondict[functiongroup][defname]["Outputs"]["out"]
            dataout = str(data["DataType"])
            idata += f"\'{dataout}\'"

            if data["DefaultValue"] is not None and data["DefaultValue"] != "":
                idata += ", " + str(data["DefaultValue"])
            else:
                idata += ", None"

            pinspecifiers = ""
            if "SUPPORTED_DATA_TYPES" in data and data["SUPPORTED_DATA_TYPES"] != [] and data["SUPPORTED_DATA_TYPES"] is not None:
                pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + str(data["SUPPORTED_DATA_TYPES"]) + ", "

            if "CONSTRAINT" in data and data["CONSTRAINT"] != "" and data["CONSTRAINT"] is not None:
                pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
            if "STRUCT_CONSTRAINT" in data and data["STRUCT_CONSTRAINT"] != "" and data["STRUCT_CONSTRAINT"] is not None:
                pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
            if "ENABLED_OPTIONS" in data and data["ENABLED_OPTIONS"] != "" and data["ENABLED_OPTIONS"] is not None:
                pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
            if "DISABLED_OPTIONS" in data and data["DISABLED_OPTIONS"] != "" and data["DISABLED_OPTIONS"] is not None:
                pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
            if "INPUT_WIDGET_VARIANT" in data and data["INPUT_WIDGET_VARIANT"] != "" and data["INPUT_WIDGET_VARIANT"] is not None:
                pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
            #if "DESCRIPTION" in data and data["DESCRIPTION"] != "" and data["DESCRIPTION"] is not None:
            #    pinspecifiers += "PinSpecifires.DESCRIPTION: \'" + data["DESCRIPTION"] + "\', "
            if "VALUE_LIST" in data and data["VALUE_LIST"] != "" and data["VALUE_LIST"] is not None:
                pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
            if "VALUE_RANGE" in data and data["VALUE_RANGE"] != "" and data["VALUE_RANGE"] is not None:
                pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
            if "DRAGGER_STEPS" in data and data["DRAGGER_STEPS"] != "" and data["DRAGGER_STEPS"] is not None:
                pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
            if pinspecifiers != "":
                idata += ", {" + pinspecifiers[:-2] + "})"

            idata += ", "

        implementdata.append(idata)
        mdata = ""
        category = '|'.join(self.functiondict[functiongroup][defname]["MetaData"]["CATEGORY"])
        CacheEnabeled = str(self.functiondict[functiongroup][defname]["MetaData"]["CACHE_ENABLED"])
        if CacheEnabeled is None:
            CacheEnabeled = "False"

        if "CATEGORY" in self.functiondict[functiongroup][defname]["MetaData"]:
            mdata += "NodeMeta.CATEGORY: \'{category}\', "
        if "KEYWORDS" in self.functiondict[functiongroup][defname]["MetaData"]:
            mdata += "NodeMeta.KEYWORDS: " + str(self.functiondict[functiongroup][defname]["MetaData"]["KEYWORDS"]) + ", "
        if "CACHE_ENABLED" in self.functiondict[functiongroup][defname]["MetaData"]:
            mdata += "NodeMeta.CACHE_ENABLED: " + CacheEnabeled + ", "

        implementdata.append("meta={" + mdata[:-2] + "})")

        for pin, data in self.functiondict[functiongroup][defname]["Inputs"].items():

            didata = pin + "=("
            datatype = str(data["DataType"])[1:-1]
            didata += f"{datatype}"
            if data["DefaultValue"] is not None:
                didata += ", " + str(data["DefaultValue"])
            else:
                didata += ", None"

            pinspecifiers = ""
            if "SUPPORTED_DATA_TYPES" in data and data["SUPPORTED_DATA_TYPES"] != "" and data["SUPPORTED_DATA_TYPES"] is not None:
                pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + str(data["SUPPORTED_DATA_TYPES"]) + ", "
            if "CONSTRAINT" in data and data["CONSTRAINT"] != "" and data["CONSTRAINT"] is not None:
                pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
            if "STRUCT_CONSTRAINT" in data and data["STRUCT_CONSTRAINT"] != "" and data["STRUCT_CONSTRAINT"] is not None:
                pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
            if "ENABLED_OPTIONS" in data and data["ENABLED_OPTIONS"] != "" and data["ENABLED_OPTIONS"] is not None:
                pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
            if "DISABLED_OPTIONS" in data and data["DISABLED_OPTIONS"] != "" and data["DISABLED_OPTIONS"] is not None:
                pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
            if "INPUT_WIDGET_VARIANT" in data and data["INPUT_WIDGET_VARIANT"] != "" and data["INPUT_WIDGET_VARIANT"] is not None:
                pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
            #if "DESCRIPTION" in data and data["DESCRIPTION"] != "" and data["DESCRIPTION"] is not None:
            #    pinspecifiers += "PinSpecifires.DESCRIPTION: " + data["DESCRIPTION"] + ", "
            if "VALUE_LIST" in data and data["VALUE_LIST"] != "" and data["VALUE_LIST"] is not None:
                pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
            if "VALUE_RANGE" in data and data["VALUE_RANGE"] != "" and data["VALUE_RANGE"] is not None:
                pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
            if "DRAGGER_STEPS" in data and data["DRAGGER_STEPS"] != "" and data["DRAGGER_STEPS"] is not None:
                pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
            if pinspecifiers != "":
                didata += ", {" + pinspecifiers[:-2] + "}"

            didata += ")"
            defindata.append(didata)

        outCounter = -1
        for pin, data in self.functiondict[functiongroup][defname]["Inputs"].items():
            ddata = ""
            outCounter += 1
            if outCounter != 0:
                ddata += pin + "=("
                ddata += "REF, ("

                ddata += str(data["DataType"])[1:-1]
                if data["DefaultValue"] is not None:
                    ddata += ", " + str(data["DefaultValue"])
                else:
                    ddata += ", None"

                pinspecifiers = ""
                if "SUPPORTED_DATA_TYPES" in data and data["SUPPORTED_DATA_TYPES"] != "" and data["SUPPORTED_DATA_TYPES"] is not None:
                    pinspecifiers += "PinSpecifires.SUPPORTED_DATA_TYPES: " + str(data["SUPPORTED_DATA_TYPES"]) + ", "
                if "CONSTRAINT" in data and data["CONSTRAINT"] != "" and data["CONSTRAINT"] is not None:
                    pinspecifiers += "PinSpecifires.CONSTRAINT: " + data["CONSTRAINT"] + ", "
                if "STRUCT_CONSTRAINT" in data and data["STRUCT_CONSTRAINT"] != "" and data["STRUCT_CONSTRAINT"] is not None:
                    pinspecifiers += "PinSpecifires.STRUCT_CONSTRAINT: " + data["STRUCT_CONSTRAINT"] + ", "
                if "ENABLED_OPTIONS" in data and data["ENABLED_OPTIONS"] != "" and data["ENABLED_OPTIONS"] is not None:
                    pinspecifiers += "PinSpecifires.ENABLED_OPTIONS: " + data["ENABLED_OPTIONS"] + ", "
                if "DISABLED_OPTIONS" in data and data["DISABLED_OPTIONS"] != "" and data["DISABLED_OPTIONS"] is not None:
                    pinspecifiers += "PinSpecifires.DISABLED_OPTIONS: " + data["DISABLED_OPTIONS"] + ", "
                if "INPUT_WIDGET_VARIANT" in data and data["INPUT_WIDGET_VARIANT"] != "" and data["INPUT_WIDGET_VARIANT"] is not None:
                    pinspecifiers += "PinSpecifires.INPUT_WIDGET_VARIANT: " + data["INPUT_WIDGET_VARIANT"] + ", "
                #if "DESCRIPTION" in data and data["DESCRIPTION"] != "" and data["DESCRIPTION"] is not None:
                #    pinspecifiers += "PinSpecifires.DESCRIPTION: " + "\'" + data["DESCRIPTION"] + "\', "
                if "VALUE_LIST" in data and data["VALUE_LIST"] != "" and data["VALUE_LIST"] is not None:
                    pinspecifiers += "PinSpecifires.VALUE_LIST: " + data["VALUE_LIST"] + ", "
                if "VALUE_RANGE" in data and data["VALUE_RANGE"] != "" and data["VALUE_RANGE"] is not None:
                    pinspecifiers += "PinSpecifires.VALUE_RANGE: " + data["VALUE_RANGE"] + ", "
                if "DRAGGER_STEPS" in data and data["DRAGGER_STEPS"] != "" and data["DRAGGER_STEPS"] is not None:
                    pinspecifiers += "PinSpecifires.DRAGGER_STEPS: " + data["DRAGGER_STEPS"] + ", "
                if pinspecifiers != "":
                    ddata += ", {" + pinspecifiers[:-2] + "}"

                if outCounter == len(self.pindefs["Outputs"]) - 1:
                    ddata = ddata + ")))"
                else:
                    ddata += "))"

                defoutdata.append(ddata)

        self.functiondict[functiongroup]
        self.functiondict[functiongroup][defname]["Implement"] = implementdata
        self.functiondict[functiongroup][defname]["Definition"] = defindata # + defoutdata
        self.functiondict[functiongroup][defname]["Code"] = []

    def writeFunctionFile(self, package, functiongroup):
        # Write Code
        Filename = functiongroup

        filefullpath = Functions.__path__[0] + "\\"

        filefullpath = os.path.join(filefullpath, package)
        filefullpath = os.path.join(filefullpath, "Functions")
        filefullpath = os.path.join(filefullpath, package)

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        year = now.year
        author = self.ui.cmbCommandAuthor.currentText()
        copyright = self.ui.txtCopyright.toPlainText()
        imports = []
        importfunctionlist = self.functionFileList
        importfunctionlist.append(functiongroup)

        importfunction = str(importfunctionlist)[1:-1].replace("'", "")
        imports.append(f"from {package} import *")
        imports.append("from PyFlow.Core import FunctionLibraryBase")
        imports.append("from PyFlow.Core import (")
        imports.append("    FunctionLibraryBase,")
        imports.append("    IMPLEMENT_NODE)")
        imports.append("from PyFlow import getHashableDataTypes")
        imports.append("from PyFlow.Core.Common import *")
        imports.append("from PackageManager.Core.PathsRegistry import PathsRegistry")

        revisionhistory = [f"# {formatted_date} - {author} - Created"]

        classline = f"class {Filename}(FunctionLibraryBase):\n"
        classline += "#doc string\n\n"
        classline += "    def __init__(self, packageName):\n"
        classline += f"        super({Filename}, self).__init__(packageName)\n"

        with open(filefullpath + ".py", 'w') as f:
            f.write(f"## Copyright {year} {author}\n\n{copyright}\n\n")

            if len(revisionhistory):
                f.write("## Revision History\n")
                for revisionHistory in revisionhistory:
                    f.write(f"#{revisionHistory}\n")
                f.write("\n")

            for importitem in imports:
                f.write(f"{importitem}\n")
            f.write("\n")

            f.write(classline)
            for variable, code in self.functiondict[functiongroup].items():
                variable2 = variable.replace(".", "_")
                # f.write(f"    def {variable2}():\n")
                if code != {}:
                    f.write("\n")
                    f.write("    @staticmethod\n")
                    if "Implement" in code:
                        for iitems in code["Implement"]:

                            if "meta" in iitems:
                                f.write(f"                    {iitems}\n")
                            else:
                                f.write(f"    {iitems}\n")
                    if "Definition" in code:
                        if code["Definition"] == []:
                            variable2 = variable.replace(".", "_")
                            f.write(f"    def {variable}():\n")
                        else:
                            for row, ditems in enumerate(code["Definition"]):
                                if row == len(code["Definition"]) - 1:
                                    defend = "):"
                                else:
                                    defend = ", "

                                if row == 0:
                                    f.write(f"    def {variable2} ({ditems}{defend}\n")
                                else:
                                    f.write(f"                 {ditems}{defend}\n")

                    # f.write(code["CodeDescription"])
                    if "Code" in code:
                        for codeline in code["Code"]:
                            f.write(codeline)
                    f.write("\n")

        print("Done")


    def writeFile(self, package, functiongroup):
        # Write Code
        Filename = functiongroup

        filefullpath = Packages.__path__[0] + "\\"

        filefullpath = os.path.join(filefullpath, package)
        filefullpath = os.path.join(filefullpath, "Functions")
        filefullpath = os.path.join(filefullpath, functiongroup)

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        year = now.year
        author = self.ui.cmbCommandAuthor.currentText()
        copyright = self.ui.txtCopyright.toPlainText()
        imports = []
        importfunctionlist = self.functionFileList
        importfunctionlist.append(functiongroup)

        importfunction = str(importfunctionlist)[1:-1].replace("'", "")
        imports.append(f"from {package} import *")
        imports.append("from PyFlow.Core import FunctionLibraryBase")
        imports.append("from PyFlow.Core import (")
        imports.append("    FunctionLibraryBase,")
        imports.append("    IMPLEMENT_NODE)")
        imports.append("from PyFlow import getHashableDataTypes")
        imports.append("from PyFlow.Core.Common import *")
        imports.append("from PackageManager.Core.PathsRegistry import PathsRegistry")


        revisionhistory = [f"# {formatted_date} - {author} - Created"]

        classline = f"class {Filename}(FunctionLibraryBase):\n"
        classline += "#doc string\n\n"
        classline += "    def __init__(self, packageName):\n"
        classline += f"        super({Filename}, self).__init__(packageName)\n"

        with open(filefullpath + ".py", 'w') as f:
            f.write(f"## Copyright {year} {author}\n\n{copyright}\n\n")

            if len(revisionhistory):
                f.write("## Revision History\n")
                for revisionHistory in revisionhistory:
                    f.write(f"#{revisionHistory}\n")
                f.write("\n")

            for importitem in imports:
                f.write(f"{importitem}\n")
            f.write("\n")

            f.write(classline)
            for variable, code in self.functiondict[functiongroup].items():
                variable2 = variable.replace(".", "_")
                #f.write(f"    def {variable2}():\n")
                if code != {}:
                    f.write("\n")
                    f.write("    @staticmethod\n")
                    if "Implement" in code:
                        for iitems in code["Implement"]:

                            if "meta" in iitems:
                                f.write(f"                    {iitems}\n")
                            else:
                                f.write(f"    {iitems}\n")
                    if "Definition" in code:
                        if code["Definition"] == []:
                            variable2 = variable.replace(".","_")
                            f.write(f"    def {variable}():\n")
                        else:
                            for row, ditems in enumerate(code["Definition"]):
                                if row == len(code["Definition"])-1:
                                    defend = "):"
                                else:
                                    defend = ", "

                                if row == 0:
                                    f.write(f"    def {variable2} ({ditems}{defend}\n")
                                else:
                                    f.write(f"                 {ditems}{defend}\n")

                    #f.write(code["CodeDescription"])
                    if "Code" in code:
                        for codeline in code["Code"]:
                            f.write(codeline)
                    f.write("\n")

        print("Done")

    def on_tblFInputPins_Changed(self, index):
        print("changed")
        row = self.ui.tblFInputPins.selectionModel().currentIndex().row()
        column = self.ui.tblFInputPins.selectionModel().currentIndex().column()
        value = self.ui.tblFInputPins.selectionModel().currentIndex().data(0)
        print("IP On Change", row, column, value)

    def on_tblFInputPins_clicked(self, index):
        '''print(index)
        print("Click", self.ui.tblFInputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFInputPins.model().data(index, QtCore.Qt.UserRole))'''
        #self.ReferenceNumber_id = self.ui.tblFInputPins.model().index(index.row(), 0).data()

        self.selectedPinDir = "Inputs"
        self.selectedPinName = self.ui.tblFInputPins.model().index(index.row(), 0).data()

        if self.selectedPinName in self.pindefs[self.selectedPinDir]:
            self.selectedPinData = self.pindefs[self.selectedPinDir][self.selectedPinName]
            self.loadPinData(self.selectedPinData)

    def on_tblFInputPins_doubleclicked(self, index):
        print("Double Click", self.ui.tblFInputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFInputPins.model().data(index, QtCore.Qt.UserRole))

    def on_tblFOutputPins_Changed(self, index):
        row = self.ui.tblFOutputPins.selectionModel().currentIndex().row()
        column = self.ui.tblFOutputPins.selectionModel().currentIndex().column()
        value = self.ui.tblFOutputPins.selectionModel().currentIndex().data(0)
        print("IP On Change", row, column, value)

    def on_tblFOutputPins_clicked(self, index):
        print("Click", self.ui.tblFOutputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.ui.tblFOutputPins.model().data(index, QtCore.Qt.UserRole))
        self.ReferenceNumber_id = self.ui.tblFOutputPins.model().index(index.row(), 0).data()
        #self.loadProjectdata()

        self.selectedPinDir = "Outputs"
        self.selectedPinName = self.ui.tblFOutputPins.model().index(index.row(), 0).data()

        if self.selectedPinName in self.pindefs[self.selectedPinDir]:
            self.selectedPinData = self.pindefs[self.selectedPinDir][self.selectedPinName]
            self.loadPinData(self.selectedPinData)

    def on_tblFOutputPins_doubleclicked(self, index):
        print("Double Click", self.tblFOutputPins.model().index(index.row(), 0).data())
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.tblFOutputPins.model().data(index, QtCore.Qt.UserRole))

    def loadPinData(self, data):
        self.initializePinData()
        self.blockPinSignals()
        if "SUPPORTED_DATA_TYPES" in data:
            self.ui.chkPSSupportedDataTypes.setChecked(True)
            self.ui.txtPSSupportedDataTypes.setText(data["SUPPORTED_DATA_TYPES"])
        if "CONSTRAINT" in data:
            self.ui.chkPSConstraint.setChecked(True)
            self.ui.txtPSConstraint.setText(data["CONSTRAINT"])
        if "STRUCT_CONSTRAINT" in data:
            self.ui.chkPSStructConstraint.setChecked(True)
            self.ui.txtPSStructConstraint.setText(data["STRUCT_CONSTRAINT"])
        if "ENABLED_OPTIONS" in data:
            options = data["ENABLED_OPTIONS"].split("|")
            for option in options:
                if "ArraySupported" in option:  #: Pin can hold array data structure
                    self.ui.chkArraySupported.setChecked(True)
                if "DictSupported" in option:  #: Pin can hold dict data structure
                    self.ui.chkDictionarySupported.setChecked(True)
                if "SupportsOnlyArrays" in option:   #: Pin will only support other pins with array data structure
                    self.ui.chkSupportOnlyArrays.setChecked(True)
                if "AllowMultipleConnections" in option:   #: This enables pin to allow more that one input connection. See :func:`~PyFlow.Core.Common.connectPins`
                    self.ui.chkAllowMultipleConnections.setChecked(True)
                if "ChangeTypeOnConnection" in option:  #: Used by :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` to determine if it can change its data type on new connection.
                    self.ui.chkChangeTypeOnConnection.setChecked(True)
                if "RenamingEnabled" in option:  #: Determines if pin can be renamed
                    self.ui.chkRenamingEnabled.setChecked(True)
                if "Dynamic" in option:  #: Specifies if pin was created dynamically (during program runtime)
                    self.ui.chkDynamic.setChecked(True)
                if "AlwaysPushDirty" in option:  #: Pin will always be seen as dirty (computation needed)
                    self.ui.chkAlwaysPushDirty.setChecked(True)
                if "Storable" in option:  #: Determines if pin data can be stored when pin serialized
                    self.ui.chkStorable.setChecked(True)
                if "AllowAny" in option:  #: Special flag that allow a pin to be :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin`, which means non typed without been marked as error. By default a :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` need to be initialized with some data type, other defined pin. This flag overrides that. Used in lists and non typed nodes
                    self.ui.chkAllowAny.setChecked(True)
                if "DictElementSupported" in option:  #: Dicts are constructed with :class:`DictElement` objects. So dict pins will only allow other dicts until this flag enabled. Used in :class:`~PyFlow.Packages.PyFlowBase.Nodes.makeDict` node
                    self.ui.chkDictionaryElementSupported.setChecked(True)

        if "DISABLED_OPTIONS" in data:
            self.ui.chkPSDisableOptions.setChecked(True)
            self.ui.txtPSDisableOptions.setText(data["DISABLED_OPTIONS"])
        if "INPUT_WIDGET_VARIANT" in data:
            self.ui.chkPSInputWidget.setChecked(True)
            self.ui.txtPSInputWidget.setText(data["INPUT_WIDGET_VARIANT"])
        if "DESCRIPTION" in data:
            self.ui.chkPSDescription.setChecked(True)
            self.ui.txtPSDescription.setText(data["DESCRIPTION"])
        if "VALUE_LIST" in data:
            self.ui.chkPSValueList.setChecked(True)
            self.ui.txtPSValueList.setText(data["VALUE_LIST"])
        if "VALUE_RANGE" in data:
            self.ui.chkPSValueRange.setChecked(True)
            self.ui.txtPSValueRange.setText(data["VALUE_RANGE"])
        if "DRAGGER_STEPS" in data:
            self.ui.chkPSDraggerSteps.setChecked(True)
            self.ui.txtPSDraggerSteps.setText(data["DRAGGER_STEPS"])
        self.unblockPinSignals()


    def loadNodeProperties(self, filefullpath):
            preamble = ""
            precode = ""
            readingimplementdata = -1
            readingdefdata = 0
            defdata = ""
            codedata = []
            eof = 0
            defname = ""
            code = ""
            self.selectedNodeData = {}
            self.selectedNodeData[self.selectedNodeDataName] = {}

            addDecorator = ""

            try:
                filesize = len(open(filefullpath).readlines())
                f = open(filefullpath, "r")

                for index, lineitem in enumerate(f):
                    # Reading the parts of the code (Implement, Def, Code)
                    if lineitem.find("def ") != -1 or index == filesize:
                        if lineitem.find("_init_") != -1:
                            defname = "init"

                        else:
                            defnamestart = 7
                            defnameend = lineitem.find("(")

                            if "@" in codedata[-1]:
                                addDecorator = codedata[-1].replace("    ", "")
                                codedata.pop()
                                self.selectedNodeData[self.selectedNodeDataName][defname] = codedata
                                #Starts the Next Group of code
                                codedata = [addDecorator]
                            else:
                                addDecorator = ""
                                self.selectedNodeData[self.selectedNodeDataName][defname] = codedata
                                codedata = []

                            defname = lineitem[defnamestart + 1:defnameend]

                    if lineitem.find("class ") != -1:
                        preamble = precode
                        base = ""
                        codedata = []
                    else:
                        codedata.append(lineitem.replace("    ","").replace("\n",""))
            except:
                pass


    def loadTableProperties(self, filefullpath):
            className = None
            tableName = None
            baseName = None

            fieldName = None
            fieldDataType = None
            fieldSize = None
            fieldOptions = None

            try:
                filesize = len(open(filefullpath).readlines())
                f = open(filefullpath, "r")

                for index, lineitem in enumerate(f):
                    if lineitem.find("__tablename__") != -1:
                        print(lineitem)
                    if lineitem.find("class ") != -1:
                        print(lineitem)
                        codedata = []
                        if className:
                            pass
                    else:
                        codedata.append(lineitem.replace("    ","").replace("\n",""))

                    if className:
                        fieldName = None
                        fieldDataType = None
                        fieldSize = None
                        fieldOptions = None
            except:
                pass

    def parseNodePins(self):
        defname = self.selectedNodeDataName
        self.selectedNodeData[defname] = {}
        self.selectedNodeData[defname]["Inputs"] = {}
        self.selectedNodeData[defname]["Outputs"] = {}
        inputPinOrder = 0
        outputPinOrder = 0
        try:
            for item in self.selectedNodeData[defname]["init"]:
                if "=" in item:
                    phrase = item.split("=")
                    pinName = phrase[0].replace("self.", "")

                    pinOptionsStart = phrase[1].find("(")
                    pinOptionEnd = phrase[1].find(")")
                    if pinOptionsStart != -1:
                        pinOptions = phrase[1][pinOptionsStart:pinOptionEnd]

                        '''def createInputPin(self, pinName, dataType, defaultValue=None, foo=None,
                                           structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):'''

                        '''createOutputPin(self, pinName, dataType, defaultValue=None, structure=StructureType.Single, constraint=None,
                                        structConstraint=None, supportedPinDataTypes=[], group=""):'''
                        pinOptionList = pinOptions.split(",")

                        pinData = {}

                        pinName = pinOptionList[0].replace("\"","").replace("\'","").replace("(","").replace(")","").replace(" ","").strip()
                        pinData["DataType"] = pinOptionList[1][2:-1].replace("\"","").replace("\'","").strip()

                        for row, options in enumerate(pinOptionList):
                            if row > 2:
                                if "=" not in options:
                                    if row == 2:
                                        pinData["DefaultValue"] = options.replace(")", "")\
                                            .replace("\"","")\
                                            .replace("\'","")\
                                            .strip()

                                    if row == 3:
                                        pinData["foo"] = options.replace("\"","").replace("\'","").strip()
                                else:
                                    moreoptions = options.split("=")
                                    pinData[moreoptions[0]] = moreoptions[0]
                    else:
                        if "headerColor" in phrase[0]:
                            self.selectedNodeData[defname]["HeaderColor"] = phrase[1].strip()
                            self.ui.txtNodeHeaderColor.setText(self.selectedNodeData[defname]["HeaderColor"])

                    if 'createOutputPin' in phrase[1]:
                        outputPinOrder += 1
                        self.selectedNodeData[defname]
                        self.selectedNodeData[defname]["Outputs"][pinName] = {}
                        pinData["Order"] = outputPinOrder

                        self.selectedNodeData[defname]["Outputs"][pinName] = pinData
                    if 'createInputPin' in phrase[1]:
                        inputPinOrder += 1
                        self.selectedNodeData[defname]["Inputs"][pinName] = {}
                        pinData["Order"] = inputPinOrder

                        self.selectedNodeData[defname]["Inputs"][pinName] = pinData

        except:
            print(self.selectedNodeDataName, "Fail")

        print(self.selectedNodeData[defname])
        value = ""
        if "description" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["description"]:
                if "return" in items or len(value):
                    value += items.replace("return","").replace("\'","").strip()

                self.ui.txtNodeDescription.setText(value)

        if "category" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["category"]:
                if "return" in items:
                    value = items.replace("return","").replace("\'","").strip()
                    self.ui.txtNodeCategory.setText(value)

        if "keywords" in self.selectedNodeData[defname]:
            for items in self.selectedNodeData[defname]["keywords"]:
                if "return" in items:
                    value = items.replace("return","").replace("\'","").replace(")","").replace("[","").replace("]","").strip()
                    self.ui.txtNodeKeyWords.setText(value)

        self.loadNodePinTable()

    def loadNodePinTable(self):
        # InputPin
        defname = self.selectedNodeDataName
        pindatatypemodel = QStandardItemModel(0, 2)

        for index, key in enumerate(self.pinDict):
            pindatatypemodel.setItem(index, 0, QtGui.QStandardItem(str(index)))
            pindatatypemodel.setItem(index, 1, QtGui.QStandardItem(key))
        pindatatypemodel.setItem(index+1, 0, QtGui.QStandardItem(str(index+1)))
        pindatatypemodel.setItem(index+1, 1, QtGui.QStandardItem('ExecPin'))

        inputpinlistmodel = QStandardItemModel(0, 2)
        inputPinList = []
        if "Inputs" in self.selectedNodeData[defname]:
            for rowcount1, pindata in enumerate(self.selectedNodeData[defname]["Inputs"]):
                row = int(self.selectedNodeData[defname]["Inputs"][pindata]["Order"])
                inputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))
                DataTypeValue = ""
                if "DataType" in self.selectedNodeData[defname]["Inputs"][pindata]:
                    inputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(
                        self.selectedNodeData[defname]["Inputs"][pindata]["DataType"]))
                    DataTypeValue = self.selectedNodeData[defname]["Inputs"][pindata]["DataType"]
                inputPinList.append(DataTypeValue)
                if "DefaultValue" in self.selectedNodeData[defname]["Inputs"][pindata]:
                    inputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(
                        self.selectedNodeData[defname]["Inputs"][pindata]["DefaultValue"]))

            inputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
            inputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
            inputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            outputPinList = []
            outputpinlistmodel = QStandardItemModel(0, 2)
            if "Outputs" in self.selectedNodeData[defname]:
                for rowcount2, pindata in enumerate(self.selectedNodeData[defname]["Outputs"]):
                    row = int(self.selectedNodeData[defname]["Outputs"][pindata]["Order"])
                    DataTypeValue = ""
                    if rowcount2 == 0:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem("out"))
                    else:
                        outputpinlistmodel.setItem(row, 0, QtGui.QStandardItem(pindata))

                    if "DataType" in self.selectedNodeData[defname]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 1, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["Outputs"][pindata]["DataType"]))
                        DataTypeValue = self.selectedNodeData[defname]["Outputs"][pindata]["DataType"]
                    outputPinList.append(DataTypeValue)

                    if "DefaultValue" in self.selectedNodeData[defname]["Outputs"][pindata]:
                        outputpinlistmodel.setItem(row, 2, QtGui.QStandardItem(
                            self.selectedNodeData[defname]["Outputs"][pindata]["DefaultValue"]))

                outputpinlistmodel.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data Type', role=QtCore.Qt.DisplayRole)
                outputpinlistmodel.setHeaderData(2, QtCore.Qt.Horizontal, 'Default Value', role=QtCore.Qt.DisplayRole)

            self.ui.tblNInputPins.setModel(inputpinlistmodel)
            self.ui.tblNOutputPins.setModel(outputpinlistmodel)

            if "Inputs" in self.selectedNodeData[defname]:
                for row, data in enumerate(self.selectedNodeData[defname]["Inputs"]):
                    self.ui.tblNInputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)

                    c.setValue(self.selectedNodeData[defname]["Inputs"][data]["DataType"], 1)
                    i = self.ui.tblNInputPins.model().index(row, 1)
                    # c.currentIndexChanged2[dict].connect(self.on_lstPinSettings_cmbTableChanged)
                    self.ui.tblNInputPins.setIndexWidget(i, c)

            if "Outputs" in self.selectedNodeData[defname]:
                for row,  data in enumerate(self.selectedNodeData[defname]["Outputs"]):
                    self.ui.tblNOutputPins.openPersistentEditor(pindatatypemodel.index(row, 1))
                    c = TableComboModel(self, dataModel=pindatatypemodel, id=row, row=row, column=1)
                    c.setValue(self.selectedNodeData[defname]["Outputs"][data]["DataType"], 1)
                    i = self.ui.tblNOutputPins.model().index(row, 1)
                    # c.currentIndexChanged2[dict].connect(self.on_lstTableSettings_cmbTableChanged)
                    self.ui.tblNOutputPins.setIndexWidget(i, c)

            # self.ui.tblNInputPins.resizeColumnsToContents()
            # self.ui.tblNOutputPins.resizeColumnsToContents()

            # self.ui.tblNInputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))
            # self.ui.tblNOutputPins.setItemDelegateForColumn(1, ComboDelegate(self, inputpinlistmodel))

            #self.initializePinData()

            '''for z in curlystuff2.split(","):
                itemdata = z.strip().split(":")
                #print(itemdata[0], itemdata[1].strip())'''

    @QtCore.Slot()
    def on_cmdCreatePackage_clicked(self):
        inputData = {"label": "Enter Package Name", "default": "New Package Name", "button": "Create",
                   "title": "Create New Package", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = InputDialog(inputData)
        packagename = dialog.get_value()
        if packagename != "":
            self.createPackage(packagename)


    def createFunctionPackage(self, packagename):
        packageRoot = Functions.__path__[0]

        self.initPackageDict(packagename)

        PROMPT = f"With the Python Package {packagename} please describe this package."
        descriptionlist = "Test"
        '''descriptionlist = self.comp(PROMPT, 250, 3)
        inputData = {"label": "Package Description", "default": "Dialog", "button": "Accept",
                     "title": f"Describing package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListSelectionDialog(inputData, descriptionlist)
        if dialog.exec_() == QDialog.Accepted:
            descriptionselected = dialog.selected_item()'''
        self.packageDict[packagename]["Description"] = descriptionlist[0]

        category = []
        category.append(packagename)
        self.packageDict[packagename]["Category"] = category

        PROMPT = f"With the Python Package {packagename} please list keywords for this package.  Please list in single words separated by a comma."
        # keywordlist = self.comp(PROMPT, 15, 3)
        keywordlist = "Test"
        keywords = []
        for keywords2 in keywordlist:
            keywords3 = keywords2.split(",")
            for keyword in keywords3:
                keyword = keyword.strip()
                keyword = keyword.title()
                keyword = keyword.replace(".", "")

                if keyword not in keywords and keyword != "":
                    keywords.append(keyword.strip())

        '''inputData = {"label": "Package Keywords", "default": "Dialog", "button": "Accept",
                     "title": f"Keywords for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListItemSelectionDialog(inputData, keywords)
        if dialog.exec_() == QDialog.Accepted:
            keywordselected = dialog.selected_items()'''

        self.packageDict[packagename]["Keywords"] = keywords

        PROMPT = f"With the Python Package {packagename} please write a tooltip describing {packagename}."
        '''tooltiplist = self.comp(PROMPT, 250, 3)
        inputData = {"label": "Package Tooltip", "default": "Dialog", "button": "Accept",
                     "title": f"Tooltip for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListSelectionDialog(inputData, tooltiplist)
        if dialog.exec_() == QDialog.Accepted:
            tooltipselected = dialog.selected_item()'''
        tooltiplist = "Test"
        self.packageDict[packagename]["ToolTip"] = tooltiplist[0]

        self.packageDict[packagename]["KeyboardShortCut"] = ""

        '''inputData = {"label": "Icon", "default": "Dialog", "button": "Accept",
                     "title": f"Icon for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = IconSelectionDialog(inputData, RESOURCES_DIR)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_icon() is not None:
            print('You selected an icon.')
        else:
            print('Operation cancelled.')'''

        self.packageDict[packagename]["SmallIcon"] = ""
        self.packageDict[packagename]["MediumIcon"] = ""
        self.packageDict[packagename]["LargeIcon"] = ""

        self.ui.txtPackageName.setText(packagename)
        if packagename == "":
            return
        packageFolderPath = os.path.join(packageRoot, packagename)
        filepath = self.createfolder(packageFolderPath)
        self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageFunctions.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Functions"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackagePins.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Pins"))
            self.createfile(os.path.join(filepath, "__init__.py"))


        packagelistmodel = QStandardItemModel(0, 1)
        rowcount = 0

    def createPackage(self, packagename):
        packageRoot = Packages.__path__[0]

        self.initCommandDict(packagename)

        PROMPT = f"With the Python Package {packagename} please describe this package."
        descriptionlist = "Test"
        '''descriptionlist = self.comp(PROMPT, 250, 3)
        inputData = {"label": "Package Description", "default": "Dialog", "button": "Accept",
                     "title": f"Describing package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListSelectionDialog(inputData, descriptionlist)
        if dialog.exec_() == QDialog.Accepted:
            descriptionselected = dialog.selected_item()'''
        self.commanddict[packagename]["Description"] = descriptionlist[0]

        category = []
        category.append(packagename)
        self.commanddict[packagename]["Category"] = category

        PROMPT =  f"With the Python Package {packagename} please list keywords for this package.  Please list in single words separated by a comma."
        #keywordlist = self.comp(PROMPT, 15, 3)
        keywordlist = "Test"
        keywords = []
        for keywords2 in keywordlist:
            keywords3 = keywords2.split(",")
            for keyword in keywords3:
                keyword = keyword.strip()
                keyword = keyword.title()
                keyword = keyword.replace(".", "")

                if keyword not in keywords and keyword != "":
                    keywords.append(keyword.strip())

        '''inputData = {"label": "Package Keywords", "default": "Dialog", "button": "Accept",
                     "title": f"Keywords for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListItemSelectionDialog(inputData, keywords)
        if dialog.exec_() == QDialog.Accepted:
            keywordselected = dialog.selected_items()'''

        self.commanddict[packagename]["Keywords"] = keywords

        PROMPT = f"With the Python Package {packagename} please write a tooltip describing {packagename}."
        '''tooltiplist = self.comp(PROMPT, 250, 3)
        inputData = {"label": "Package Tooltip", "default": "Dialog", "button": "Accept",
                     "title": f"Tooltip for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = ListSelectionDialog(inputData, tooltiplist)
        if dialog.exec_() == QDialog.Accepted:
            tooltipselected = dialog.selected_item()'''
        tooltiplist = "Test"
        self.commanddict[packagename]["ToolTip"] = tooltiplist[0]

        self.commanddict[packagename]["KeyboardShortCut"] = ""

        '''inputData = {"label": "Icon", "default": "Dialog", "button": "Accept",
                     "title": f"Icon for package {packagename}", "icon": os.path.join(RESOURCES_DIR, "ProgramLogo.png")}
        dialog = IconSelectionDialog(inputData, RESOURCES_DIR)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_icon() is not None:
            print('You selected an icon.')
        else:
            print('Operation cancelled.')'''

        self.commanddict[packagename]["SmallIcon"] = ""
        self.commanddict[packagename]["MediumIcon"] = ""
        self.commanddict[packagename]["LargeIcon"] = ""

        self.ui.txtPackageName.setText(packagename)
        if packagename == "":
            return
        packageFolderPath = os.path.join(packageRoot, packagename)
        filepath = self.createfolder(packageFolderPath)
        self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageResource.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Resource"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageCommands.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Commands"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageFunctions.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Functions"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageWidgets.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Widgets"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageUI.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "UI"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackagePins.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Pins"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageNodes.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Nodes"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageTools.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Commands"))
            self.createfolder(os.path.join(filepath, "res"))
            filepath2 = os.path.join(filepath, "__init__.py")
            with open(filepath2, "w") as f:
                self.addCopyright(f)
                f.write("import os\n")
                f.write("RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + \"/RESOURCES_DIR/\"\n")

        if self.ui.chkPackageExporters.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Exporters"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        if self.ui.chkPackageFactories.isChecked():
            filepath = self.createfolder(os.path.join(packageFolderPath, "Factories"))
            self.createfile(os.path.join(filepath, "__init__.py"))

        packagelistmodel = QStandardItemModel(0, 1)
        rowcount = 0

        for directories in os.listdir(packageRoot):
            if directories[1] != "_":
                packagelistmodel.setItem(rowcount, 0, QtGui.QStandardItem(directories))
                rowcount += 1

        self.packagelistModelproxy = QtCore.QSortFilterProxyModel(self)
        self.packagelistModelproxy.setSourceModel(packagelistmodel)

        self.ui.lstPackages.setModel(self.packagelistModelproxy)

    def createfolder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def createfile(self, file_name):
        if not os.path.exists(file_name):
            open(file_name, 'a').close()

    @QtCore.Slot()
    def on_cmdUpdateInit_clicked(self):
        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        self.updateInit(selectedpackage, packagepath)

    def updateFunctionInit(self, selectedpackage):
        packageRoot = Functions.__path__[0]
        packagepath = os.path.join(packageRoot, selectedpackage)
        filefullpath = os.path.join(packagepath, "__init__.py")

        fileList = []
        for file in os.listdir(packagepath):
            fileList.append(file)

        with open(filefullpath, 'w') as f:
            self.addIntro(f, selectedpackage)
            self.defineFiles(f, selectedpackage, "FunctionLibrary")
            self.createFunctionBasePackage(f, selectedpackage)

    def updateInit(self, selectedpackage, packagepath):
        packageRoot = Packages.__path__[0]
        #packagepath = os.path.join(packageRoot, selectedpackage)
        filefullpath = os.path.join(packagepath, "__init__2.py")

        s = self.initDict

        fileList = []
        for file in os.listdir(packagepath):
            fileList.append(file)

        with open(filefullpath, 'w') as f:
            self.addIntro(f, selectedpackage)

            f.write("# [Class Imports]\n")
            self.importClasses(f, selectedpackage, packagepath, "Pins")
            self.importClasses(f, selectedpackage, packagepath, "FunctionLibrary")
            #self.importClasses(f, selectedpackage, packagepath, "FooLibs")
            self.importClasses(f, selectedpackage, packagepath, "Nodes")
            self.importClasses(f, selectedpackage, packagepath, "Commands", ["res"])
            self.importClasses(f, selectedpackage, packagepath, "Exporters")

            self.defineFiles2(f, selectedpackage, packagepath, "def ", "Factories")
            self.defineFiles2(f, selectedpackage, packagepath, "class ", "PrefsWidgets")
            #self.defineFoo(f, selectedpackage, "FunctionLibrary", "_FOO_LIBS"
            self.defineDict(f, selectedpackage, "Nodes", "_NODES")
            self.defineDict(f, selectedpackage, "Pins", "_PINS")

            self.defineOrderedDict(f, selectedpackage, "Commands", "_COMMANDS", ["res"])

            f.write("_COMMANDS[RibbonBar.__name__] = RibbonBar\n")
            f.write("_COMMANDS[HistoryTool.__name__] = HistoryTool\n")
            f.write("_COMMANDS[PropertiesTool.__name__] = PropertiesTool\n")
            f.write("_COMMANDS[Preferences.__name__] = Preferences\n")
            f.write("#_COMMANDS[SearchResultsTool.__name__] = SearchResultsTool\n\n")

            self.defineOrderedDict(f, selectedpackage, "Exporters", "_EXPORTERS")

            self.defineOrderedDict3(f, self.ui.lstpkgBases, "Bases")
            self.defineOrderedDict3(f, self.ui.lstpkgTables, "Tables")

            self.defineOrderedDict2(f, selectedpackage, "PrefsWidgets", "_PREFS_WIDGETS")

            self.createBasePackage(f, selectedpackage)
            self.createMenus(f, selectedpackage)

    def loadInit(self):
        '''["Class Imports", "Pins", "Functions", "Nodes", "Factories", "Prefs widgets",
                          "Foo Dict", "Node Dict", "Pin Dict", "Toolbar Dict", "Export", "Preferred Widgets",
                          "Base Package"]'''

        packageRoot = Packages.__path__[0]
        selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
        #selectedpackage = self.ui.lstPackages.model().index(self.ui.listPackages.row(), 0).data()
        packagepath = os.path.join(packageRoot, selectedpackage)
        initfile = "__init__.py"
        filename = os.path.join(packagepath, initfile)

        category = "Introduction"
        self.initDict = {}
        self.initDict[category] = []

        self.initDict["MenuOrder"] = {}
        self.initDict["MenuLayout"] = {}
        self.initDict["RibbonOrder"] = {}
        self.initDict["RibbonLayout"] = {}
        self.initDict["ToolBarLayout"] = {}

        categoryDict = {"Imports": self.ui.lstpkgImports, "Commands": self.ui.lstpkgCommands,
                        "Functions": self.ui.lstpkgFunctions, "Nodes": self.ui.lstpackageNodes,
                        "Widgets": self.ui.lstpkgWidgets, "UI": self.ui.lstpkgUI,
                        "Bases": self.ui.lstpkgBases,
                        "Tables": self.ui.lstpkgTables, "Export": self.ui.lstpkgExport,
                        "Node Dict": self.ui.lstpkgImports, "Factories": self.ui.lstPackageFactories,
                        "MenuOrder": self.ui.lstpkgMenuOrder, "MenuLayout": self.ui.tvpkgMenu,
                        "RibbonOrder": self.ui.lstpkgRibbonOrder, "RibbonLayout": self.ui.tvpkgRibbonItems,
                        "ToolBarLayout": self.ui.tvpkgToolbar}

        try:
            f = open(filename, "r")
            currentCategory = "Start"
            self.initDict[currentCategory] = []
            preitem = ""
            beforeCode = True

            for index, lineitem in enumerate(f):

                category = None
                #item = lineitem.replace("\n", "")
                lineitem = lineitem.strip()
                print(lineitem)

                if "@staticmethod" in lineitem:
                    preitem = "@staticmethod"

                if "import RESOURCES_DIR" in lineitem:
                    self.ui.txtpkgResourceFolder.setText(lineitem)

                if lineitem != "":
                    if "class" in lineitem:
                        category = "Code"
                        beforeCode = False
                        self.initDict[category] = []

                    if "# [" in lineitem:
                        start = lineitem.find("[")
                        stop = lineitem.find("]")
                        category = lineitem[start+1:stop]
                        self.initDict[category] = []

                    if "GetSmallIcon" in lineitem:
                        category = "SmallIcon"
                        self.initDict[category] = []

                    if "GetMediumIcon" in lineitem:
                        category = "MediumIcon"
                        self.initDict[category] = []

                    if "GetLargeIcon" in lineitem:
                        category = "LargeIcon"
                        self.initDict[category] = []

                    if "GetDefaultMenuOrder" in lineitem:
                        category = "MenuOrder"
                        self.initDict[category] = []

                    if "GetDefaultMenuLayout" in lineitem:
                        category = "MenuLayout"
                        self.initDict[category] = []

                    if "GetDefaultRibbonOrder" in lineitem:
                        category = "RibbonOrder"
                        self.initDict[category] = []

                    if "GetDefaultRibbonLayout" in lineitem:
                        category = "RibbonLayout"
                        self.initDict[category] = []

                    if "GetDefaultToolBarLayout" in lineitem:
                        category = "ToolBarLayout"
                        self.initDict[category] = []

                    if category is None and preitem == "":
                        if currentCategory is not None:
                            self.initDict[currentCategory].append(lineitem)
                            if currentCategory in categoryDict:
                                item = QListWidgetItem(f"{lineitem}")
                                font_metrics = QFontMetrics(item.font())
                                text_height = font_metrics.height()
                                a = categoryDict[currentCategory].sizeHint().width()
                                item.setSizeHint(QSize(a, text_height))
                                if beforeCode:
                                    categoryDict[currentCategory].addItem(item)
                    else:
                        currentCategory = category
                        if preitem == "@staticmethod" and category is not None:
                            item = QListWidgetItem(f"{preitem}")
                            font_metrics = QFontMetrics(item.font())
                            text_height = font_metrics.height()
                            a = categoryDict[currentCategory].sizeHint().width()
                            item.setSizeHint(QSize(a, text_height))
                            if beforeCode:
                                categoryDict[currentCategory].addItem(item)
                        preitem = ""
            f.close()
        except:
            pass

        self.initDict["MenuOrder"] = self.setItemOrder(self.initDict["MenuOrder"], self.ui.lstpkgMenuOrder)
        self.initDict["MenuLayout"] = self.parseDefinition(self.initDict["MenuLayout"], None)
        model = QStandardItemModel()
        self.fill_model(model, self.initDict["MenuLayout"])
        self.ui.tvpkgMenu.setModel(model)

        self.initDict["RibbonOrder"] = self.setItemOrder(self.initDict["RibbonOrder"], self.ui.lstpkgRibbonOrder)
        #self.initDict["RibbonLayout"] = self.parseDefinition(self.initDict["RibbonLayout"], self.initDict["RibbonOrder"])
        TreeView.dict2TreeWidget(self.ui.tvRibbonBar, self.initDict["RibbonLayout"])

        model = QStandardItemModel()
        self.fill_model(model, self.initDict["RibbonLayout"])
        self.ui.tvpkgRibbonItems.setModel(model)

        self.initDict["ToolBarLayout"] = self.parseDefinition(self.initDict["ToolBarLayout"], None)
        model = QStandardItemModel()
        self.fill_model(model, self.initDict["ToolBarLayout"])
        self.ui.tvpkgToolbar.setModel(model)

    def fill_item(self, item, value):
        item.setRowCount(0)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child_item = QStandardItem(str(key))
                item.appendRow([child_item, QStandardItem(str(val))])
                self.fill_item(child_item, val)
        elif type(value) is list:
            for val in value:
                child_item = QStandardItem()
                item.appendRow([child_item, QStandardItem(str(val))])
                self.fill_item(child_item, val)

    def fill_model(self, model, data):
        model.setHorizontalHeaderLabels(['Key', 'Value'])
        root_item = model.invisibleRootItem()
        self.fill_item(root_item, data)


    def setItemOrder(self, itemlist, listwidget):
        itemstatement = ""
        returnlist = []
        for lineitem in itemlist:
            if "[" in lineitem:
                itemstatement = lineitem

            if "]" in lineitem:
                start = lineitem.find("[")
                stop = lineitem.find("]")
                liststring = lineitem[start + 1:stop]
                newitemlist = liststring.split(",")

                for item in newitemlist:
                    item = item.strip()[1:-1]
                    if item != "":
                        witem = QListWidgetItem(f"{item}")
                        font_metrics = QFontMetrics(witem.font())
                        text_height = font_metrics.height()
                        a = listwidget.sizeHint().width()
                        witem.setSizeHint(QSize(a, text_height))
                        listwidget.addItem(witem)
                        returnlist.append(item)
                break
            else:
                itemstatement += lineitem
        return returnlist

    def parseDefinition(self, fileList, barList):
        searchlist = ["itemDict", "itemList"]

        newDict = {}
        if barList is not None:
            barDict = {item: {} for item in barList}

        dictstring = ""
        for lineitem in fileList:
            if lineitem[0] != "#":
                if "itemList = []" in lineitem:
                    dictstring = ""
                    localdict = {}
                if all(item in lineitem for item in searchlist):
                    #itemList = []
                    start = lineitem.find("[")
                    stop = lineitem.find("]")
                    category = lineitem[start + 1:stop][1:-1]
                    newDict[category] = localdict

                elif "barDict" in lineitem or 'itemDict' in lineitem:
                    start = lineitem.find("[")
                    stop = lineitem.find("]")
                    if start != -1:
                        bar_name = lineitem[start + 1:stop][1:-1]
                        barDict[bar_name] = newDict
                        newDict = {}
                else:
                    if "append" in lineitem:
                        if dictstring != "":
                            dictstring = dictstring.replace("itemList.append(", "")[:-1]
                            dictstring = dictstring.replace("RESOURCES_DIR +", "\"RESOURCES_DIR +\"")
                            stringDict = ast.literal_eval(dictstring)
                            localdict[stringDict["Command"]] = stringDict
                        dictstring = lineitem
                    elif "itemList = []" not in lineitem:
                        dictstring += lineitem

        if barList is not None:
            return barDict
        else:
            return newDict


    def addIntro(self,f, selectedpackage):
        if self.initDict["Start"] is None:
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            selectedpackage = selectedpackage.title()

            f.write(f"PACKAGE_NAME = \'{selectedpackage}\'\n")
            f.write(f"\'\'\'{selectedpackage}\n")
            f.write("\'\'\'\n")
            f.write("from collections import OrderedDict\n")
            f.write("from PackageManager.UI.UIInterfaces import IPackage\n")
            f.write(f"from PackageManager.Packages.{selectedpackage}.Commands import RESOURCES_DIR")
            f.write(f"from PackageManager.Packages.ProgramBase.Commands.Preferences import Preferences")
            f.write(f"from PackageManager.Packages.ProgramBase.UI.DockWindows.RibbonBar import RibbonBar")
            f.write(f"from PackageManager.Packages.ProgramBase.UI.DockWindows.HistoryTool import HistoryTool")
            f.write(f"from PackageManager.Packages.ProgramBase.UI.DockWindows.PropertiesTool import PropertiesTool")

            f.write("\n")
        else:
            for item in self.initDict["Start"]:
                f.write(f"{item}\n")

        f.write("\n")

    def importClasses(self, f, selectedpackage, packagepath, foldername, ignorelist=[]):
        if ignorelist is None:
            ignorelist = []
        try:
            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            #packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)

            #f.write(f"# [{foldername}]\n")
            #f.write("%s = {" % (category))
            for file in os.listdir(filepath):
                if file[1] != "_":
                    file2 = file.replace(".py","")
                    if file2 not in ignorelist:
                        #from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin
                        a = f"from PackageManager.Packages.{selectedpackage}.{foldername}.{file2} import {file2}"
                        f.write(f"from PackageManager.Packages.{selectedpackage}.{foldername}.{file2} import {file2}\n")
            #f.write("\n")
        except:
            pass


    def defineFiles2(self, f, selectedpackage, packagepath, search, foldername, ignorelist=[]):
        try:
            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)

            f.write(f"# [{foldername}]\n")
            for file in os.listdir(filepath):
                if file[1] != "_":
                    file2 = file.replace(".py","")
                    if file2 not in ignorelist:
                        f2 = open(os.path.join(filepath, file), "r")
                        for index, lineitem in enumerate(f2):

                            if lineitem[:len(search)] == search:
                                classnamestart = len(search)
                                classnameend = lineitem.find("(")
                                if self.workingFile.find(lineitem[classnamestart + 1:classnameend]) == -1:
                                    functionname = lineitem[classnamestart :classnameend]
                                    f.write(f"from PackageManager.Packages.{selectedpackage}.{foldername}.{file2} import {functionname}\n")
                                break
                                #from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin

            f.write("\n")
        except:
            pass

    def defineFoo(self, f, selectedpackage, foldername, category):

        try:
            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)

            f.write(f"# [{foldername}]\n" % (foldername))
            f.write(f"{category} = {{\n")
            for file in os.listdir(filepath):
                if file[1] != "_":
                    file2 = file.replace(".py","")
                    f.write(f"    {file}.__name__: {file2}(PACKAGE_NAME),\n")
            f.write("}\n")
            f.write("\n")
        except:
            pass
    def defineDict(self, f, selectedpackage, foldername, category):
        try:
            "_FOO_LIBS, _NODES, _PINS"
            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)

            f.write(f"# [{foldername}]\n")
            f.write(f"{category} = {{\n")
            if os.path.isdir(filepath):
                for file in os.listdir(filepath):
                    if file[1] != "_":
                        file2 = file.replace(".py","")
                        f.write(f"    {file2}.__name__: {file2},\n")
            f.write("}\n\n")
        except:
            pass

    def defineOrderedDict(self, f, selectedpackage, foldername, category, ignorelist=[]):
        try:
            "_TOOLS, _EXPORTERS, _PREFS_WIDGETS"
            '''_TOOLS = OrderedDict()
               _TOOLS[CompileTool.__name__] = CompileTool'''

            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)

            f.write(f"# [{foldername}]\n")
            f.write(f"{category} = OrderedDict()\n")
            for file in os.listdir(filepath):
                if file[1] != "_":
                    file2 = file.replace(".py","")
                    if file2 not in ignorelist:
                        f.write(f"{category}[{file2}.__name__] = {file2}\n")
            f.write("\n")
        except:
            f.write("\n")

    def defineOrderedDict2(self, f, selectedpackage, foldername, category):
        try:
            packageRoot = Packages.__path__[0]
            #selectedpackage = self.ui.lstPackages.model().index(self.ui.lstPackages.currentIndex().row(), 0).data()
            packagepath = os.path.join(packageRoot, selectedpackage)
            filepath = os.path.join(packagepath, foldername)
            search = "class "
            f.write(f"# [{foldername}]\n")
            f.write(f"{category} = OrderedDict()\n")
            for file in os.listdir(filepath):
                if file[1] != "_":
                    file2 = file.replace(".py","")
                    f2 = open(os.path.join(filepath, file), "r")
                    for index, lineitem in enumerate(f2):

                        if lineitem[:len(search)] == search:
                            classnamestart = len(search)
                            classnameend = lineitem.find("(")
                            if self.workingFile.find(lineitem[classnamestart + 1:classnameend]) == -1:
                                functionname = lineitem[classnamestart:classnameend]

                                f.write(f"{category}[\"{file2}\"] = {functionname}\n")
                                break
            f.write("\n")
        except:
            pass

    def defineOrderedDict3(self, f, list_widget, category):
        try:
            f.write(f"# [{category}]\n")
            for i in range(list_widget.count()):
                f.write(list_widget.item(i).text())
                f.write("\n")
        except:
            pass
        f.write("\n")
    def createFunctionBasePackage(self, f, selectedpackage):

        f.write(f"# [{selectedpackage} Package]\n")
        f.write(f"class {selectedpackage.title()} (IPackage):\n")
        f.write(f"    \"\"\"{selectedpackage}  package\n")
        f.write("    \"\"\"\n\n")

        f.write("    def __init__(self, Parent):\n")
        f.write(f"        super({selectedpackage.title()} , self).__init__()\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetPinClasses():\n")
        f.write("        return _PINS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetIcon():\n")
        f.write("        return RESOURCES_DIR + \"ProgramLogo.png\"\n\n")

    def createBasePackage(self, f, selectedpackage):

        f.write(f"# [{selectedpackage} Package]\n")
        f.write(f"class {selectedpackage} (IPackage):\n")
        f.write(f"    \"\"\"{selectedpackage}  package\n")
        f.write("    \"\"\"\n\n")

        f.write("    def __init__(self, Parent):\n")
        f.write(f"        super({selectedpackage}, self).__init__()\n\n")
        f.write(f"        self.parent = Parent")
        f.write("\n")
        f.write("    @staticmethod\n")
        f.write("    def CreateInstance(main, parent=None):\n")
        f.write("        return AppMDI.MDIMain.NewInstance(main, parent)\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetExporters():\n")
        f.write("        return _EXPORTERS\n\n")

        #f.write("    @staticmethod\n")
        #f.write("    def GetFunctionLibrary():\n")
        #f.write("        return _FOO_LIBS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetBases():\n")
        f.write("        return _BASES\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetTables():\n")
        f.write("        return _TABLES\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetNodeClasses():\n")
        f.write("        return _NODES\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetPinClasses():\n")
        f.write("        return _PINS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetCommandClasses():\n")
        f.write("        return _COMMANDS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def PrefsWidgets():\n")
        f.write("        return _PREFS_WIDGETS\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetIcon():\n")
        a = str(self.initDict["SmallIcon"][0])
        f.write(f"        {a}\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetSmallIcon():\n")
        b = str(self.initDict["SmallIcon"][0])
        f.write(f"        {b}\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetMediumIcon():\n")
        c = str(self.initDict["MediumIcon"][0])
        f.write(f"        {c}\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetLargeIcon():\n")
        d = str(self.initDict["LargeIcon"][0])
        f.write(f"        {d}\n\n")

    def createMenus(self, f, selectedpackage):

        f.write("    @staticmethod\n")
        f.write("    def GetDefaultMenuOrder():\n")
        a = str(self.initDict["MenuOrder"])
        f.write(f"        itemOrder = {a}\n")
        f.write("        return itemOrder\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetDefaultMenuLayout():\n")
        f.write("        itemDict = {}\n")
        for category in self.initDict["MenuLayout"]:
            f.write(f"        itemList = []\n")
            for key, item in enumerate(self.initDict["MenuLayout"][category]):
                value = str(self.initDict["MenuLayout"][category][item])
                value = value.replace("\'RESOURCES_DIR +", "RESOURCES_DIR + \'")
                f.write(f"        itemList.append({value})\n")
            f.write(f"        itemDict[\'{category}\'] = itemList\n\n")
        f.write("        return itemDict\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetDefaultRibbonOrder():\n")
        a = str(self.initDict["RibbonOrder"])
        f.write(f"        itemOrder = {a}\n")
        f.write("        return itemOrder\n\n")

        f.write("    @staticmethod\n")
        f.write("    def GetDefaultRibbonLayout():\n")
        f.write("        itemDict = {}\n")

        for bar in self.initDict["RibbonLayout"]:
            for category in self.initDict["RibbonLayout"][bar]:
                f.write("        itemList = []\n")
                for key, item in enumerate(self.initDict["RibbonLayout"][bar][category]):
                    value = str(self.initDict["RibbonLayout"][bar][category][item])
                    value = value.replace("\'RESOURCES_DIR +", "RESOURCES_DIR + \'")
                    f.write(f"        itemList.append({value})\n")
                f.write(f"        itemDict[\'{category}\'] = itemList\n\n")
            f.write(f"        itemDict[\'{bar}\'] = itemDict\n")
            f.write("        itemDict = {}\n\n")
        f.write("        return itemDict\n\n")


        f.write("    @staticmethod\n")
        f.write("    def GetDefaultToolBarLayout():\n")
        f.write("        itemDict = {}\n")

        for category in self.initDict["ToolBarLayout"]:
            f.write(f"        itemList = []\n")
            for key, item in enumerate( self.initDict["ToolBarLayout"][category]):
                value = str(self.initDict["ToolBarLayout"][category][item])
                value = value.replace("\'RESOURCES_DIR +", "RESOURCES_DIR + \'")
                f.write(f"        itemList.append({value})\n")
            f.write(f"        itemDict[\'{category}\'] = itemList\n\n")
        f.write("        return itemDict\n\n")

        '''formlist = []
        for forms in formlist:
            f.write(f"        packageToolList.append({{\"Action\": \"Add Action\", \"Package\": \"{selectedpackage}\", "
                    f"\"PackageGroup\": \"{selectedpackage}\", \"Command\": \"{forms}\"}})\n")

        f.write("        menuDict[\"Tools\"] = packageToolList\n\n")
        f.write("        windowMenuList = []\n")
        f.write("        menuDict[\"Windows\"] = windowMenuList\n\n")
        f.write("        helpMenuList = []\n")'''


    def onDone(self):
        # if we are here, everything is correct
        self.accept()

# Scanning Folders
    def scanfolder(filelocation, folderlist):
        packageRoot = Packages.__path__[0]
        templatesRoot = os.path.join(packageRoot, "../../../../PackageManager/UI/Forms/PackageWizard/Templates")
        packageRoot = QFileDialog.getExistingDirectory(None, "Choose folder", "Choose folder",
                                                       QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        defaultfolderlist = ["Exporters", "Factories", "FunctionLibrary", "Nodes", "Pins", "PrefsWidgets", "Tools",
                             "UI"]
        folderdict = {i: [] for i in defaultfolderlist}

        fullpathname = ""
        for path, dirs, files in os.walk(packageRoot):
            for filename in files:
                print(path, dirs, files)
                module_info = pyclbr.readmodule(filename)
                print(module_info)
                for item in module_info.values():
                    print(item.name)

    def packageScan(self):
        print(f"Class name: {cls.__name__}")
        print("Methods:")
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        for _, method in methods:
            print(method)

    def analyze_package(package_name):
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            print(f"Error: Package '{package_name}' not found.")
            return

        classes = inspect.getmembers(package, predicate=inspect.isclass)
        functions = inspect.getmembers(package, predicate=inspect.isfunction)

        print(f"Package name: {package_name}\n")
        '''print("Classes:")
        for _, cls in classes:
            print_class_info(cls)

        print("Functions:")
        for _, function in functions:
            print_function_info(function)'''

    @staticmethod
    def run():
        instance = PackageBuilder(None, None)
        return instance

