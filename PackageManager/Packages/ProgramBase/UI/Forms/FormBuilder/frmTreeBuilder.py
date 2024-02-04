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

from PackageManager.Packages.ProgramBase.Database import *
import frmBase
from PackageManager.Core.Common import strToMyList, myListToStr
from PackageManager.UI.Widgets import customTree
from sqlalchemy import func
HORIZONTAL_HEADERS = ("Category", "Description")

from sqlalchemy import literal_column, literal, or_
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression

class TreeBuilderEntity(frmBase):

    def loadSettingForm(self):

        SQLSelect = "SELECT *"
        SQLFrom = " FROM %s" % self.settingTable
        SQLWhere = ""
        SQLOrder = " ORDER BY section, title"

        self.tvSettingsModel = customTree.treeCategoryModel(fileLocation=self.settingDatabase, tableName=self.settingTable,
                                                            DisplayItems=['title', 'key', 'desc'],
                                                            headers=("Item", "Value", "Description"),
                                                            sqlStr=SQLSelect + SQLFrom + SQLWhere + SQLOrder)

        self.tvSettingsModel.setupModelData()
        self.dialog.tvSettings.setModel(self.tvSettingsModel)

        self.dialog.tvSettings.clicked.connect(self.on_tvSettings_Clicked)
        self.dialog.tvSettings.setColumnWidth(0, 250)
        self.dialog.tvSettings.setColumnWidth(1, 250)
        self.dialog.tvSettings.setColumnWidth(2, 50)

        settingdatatypes = ProgramSettings.loadDataTypes(self.settingDatabase, "tblDataTypes")
        self.settingtypemodel = QStandardItemModel(0, 1)
        self.optioncategorymodel = QStandardItemModel(0, 1)

        for row, ItemName in enumerate(self.tvSettingsModel.listCategories()):
            #print(row)
            self.optioncategorymodel.setItem(row, 0, QStandardItem(ItemName))
        self.dialog.cmbOptionCategory.setModel(self.optioncategorymodel)

        for row, ItemName in enumerate(settingdatatypes):
            typeID = QStandardItem("%i" % ItemName[0])
            # typeID.setTextAlignment( Qt.AlignCenter )
            self.settingtypemodel.setItem(row, 0, typeID)
            self.settingtypemodel.setItem(row, 1, QStandardItem(ItemName[1]))

        self.dialog.cmbDataType.setModel(self.settingtypemodel)
        self.dialog.cmbDataType.setModelColumn(1)

        optiontypes = ProgramSettings.loadOptionsTypes(self.settingDatabase, "tblOptionTypes")
        self.settingoptionModel = QStandardItemModel(0, 2)

        for row, ItemName in enumerate(optiontypes):
            optionID = QStandardItem("%i" % ItemName[0])
            # optionID.setTextAlignment( Qt.AlignCenter )
            self.settingoptionModel.setItem(row, 0, optionID)
            self.settingoptionModel.setItem(row, 1, QStandardItem(ItemName[1]))
            self.settingoptionModel.setItem(row, 2, QStandardItem(ItemName[2]))

        self.dialog.cmbOptionLink.setModel(self.settingoptionModel)
        self.dialog.cmbOptionLink.setModelColumn(1)

        # Settings
        self.roottreeitem = None

    def ClearSettingData(self):
        self.dialog.txtSettingID.setText(None)
        self.dialog.cmbOptionCategory.setCurrentIndex(0)
        self.dialog.txtSettingName.setText(None)
        self.dialog.txtSettingValue.setText(None)
        self.dialog.txtSettingDescription.setText(None)
        self.dialog.cmbDataType.setCurrentIndex(0)
        self.dialog.txtSettingOption.setText(None)
        self.dialog.cmbOptionLink.setCurrentIndex(0)

    def CreateOptionDictionary(self):
        self.UpdatedItem = ProgramSettings.dictSettings(ID=self.dialog.txtSettingID.text(),
                                                              location=1,
                                                              section=self.dialog.cmbOptionCategory.currentText(),
                                                              title=self.dialog.txtSettingName.text(),
                                                              key=self.dialog.txtSettingValue.text(),
                                                              desc=self.dialog.txtSettingDescription.text(),
                                                              dataType=self.dialog.cmbDataType.currentText(),
                                                              optionType=self.dialog.txtSettingOption.text(),
                                                              options=self.dialog.cmbOptionLink.currentText())

    def on_tvSettings_Clicked(self, index):
        self.ClearSettingData()
        try:
            itemselected = index.internalPointer()
            if str(itemselected.TreeClassItem.treeID) != None:
                self.UpdatedItem = ProgramSettings.loadSettings(self.settingDatabase, self.settingTable,
                                                                      itemselected.TreeClassItem.treeID)
                self.dialog.txtSettingID.setText(str(itemselected.TreeClassItem.treeID))
                # self.dialog.txtSettingCategory.setText(self.UpdatedItem['section'])
                index = self.dialog.cmbOptionCategory.findText(self.UpdatedItem['section'], Qt.MatchFixedString)
                if index >= 0:
                    self.dialog.cmbOptionCategory.setCurrentIndex(index)

                self.dialog.txtSettingName.setText(self.UpdatedItem['title'])
                self.dialog.txtSettingValue.setText(self.UpdatedItem['key'])
                self.dialog.txtSettingDescription.setText(self.UpdatedItem['desc'])

                index = self.dialog.cmbDataType.findText(self.UpdatedItem['dataType'], Qt.MatchFixedString)
                if index >= 0:
                    self.dialog.cmbDataType.setCurrentIndex(index)

                index = self.dialog.cmbOptionLink.findText(self.UpdatedItem['optionType'], Qt.MatchFixedString)
                # index = self.dialog.cmbOptionLink.currentIndex()
                #print(index)
                self.dialog.cmbOptionLink.setCurrentIndex(index)

                if index == 0:
                    self.dialog.txtSettingOption.setText(self.UpdatedItem['options'])
                else:
                    OptionLinkID = self.dialog.cmbOptionLink.currentIndex()
                    #print(self.settingoptionModel.data(self.settingoptionModel.index(OptionLinkID, 2)))
                    self.dialog.txtSettingOption.setText(
                        self.settingoptionModel.data(self.settingoptionModel.index(OptionLinkID, 2)))
                    # self.dialog.txtSettingOption.setText(self.UpdatedItem['linkedoptions'])

                    # self.dialog.txtSettingName.setText(str(itemselected.TreeClassItem.Header))
                    # self.dialog.cmbOptionLink

                    # self.dialog.txtSettingValue.setText(str(itemselected.TreeClassItem.Display[1]))
                    # self.dialog.txtSettingDescription.setText(str(itemselected.TreeClassItem.Display[2]))
                    # self.dialog.txtSettingID.setText(str(itemselected.TreeClassItem.treeID))

        except:
            self.dialog.txtSettingValue.setText("")
            # saveDefaultValue(treeID,itemselected.TreeClassItem.Display[1])

    @QtCore.pyqtSlot()
    def on_cmdSettingSave_clicked(self):
        self.CreateOptionDictionary()
        idcolumn = 0
        dataColumn = 1
        cmbDataTyperow = self.cmbDataType.currentIndex()
        DataTyperowID = self.settingtypemodel.data(self.settingtypemodel.index(cmbDataTyperow, idcolumn))
        # DataTyperow = self.settingtypemodel.data(self.settingtypemodel.index(cmbDataTyperow, dataColumn))
        # self.tblItemInformation.model().index(index.row(),0).data()

        cmbOptionLinkrow = self.cmbOptionLink.currentIndex()
        OptionLinkrowID = self.cmbOptionLink.model().index(cmbOptionLinkrow, idcolumn).data()
        # OptionLinkrow = self.settingoptionModel.data(self.settingoptionModel.index(cmbOptionLinkrow, dataColumn))
        # OptionLinkrow2 = self.settingoptionModel.data(self.settingoptionModel.index(cmbOptionLinkrow, 2))

        ProgramSettings.saveSettings(Database=self.settingDatabase, Datatable=self.settingTable,
                                           Location=1,
                                           SettingDict=self.UpdatedItem,
                                           Datatype=DataTyperowID,
                                           OptionType=OptionLinkrowID)

        # self.tvSettingsModel.setData(self.tvSettingsModel.currentIndex,8,None)

    @QtCore.pyqtSlot()
    def on_cmdSettingAdd_clicked(self):
        self.CreateOptionDictionary()
        idcolumn = 0
        dataColumn = 1
        cmbDataTyperow = self.cmbDataType.currentIndex()
        DataTyperowID = self.settingtypemodel.data(self.settingtypemodel.index(cmbDataTyperow, idcolumn))
        # DataTyperow = self.settingtypemodel.data(self.settingtypemodel.index(cmbDataTyperow, dataColumn))
        # self.tblItemInformation.model().index(index.row(),0).data()

        cmbOptionLinkrow = self.cmbOptionLink.currentIndex()
        OptionLinkrowID = self.cmbOptionLink.model().index(cmbOptionLinkrow, idcolumn).data()
        # OptionLinkrow = self.settingoptionModel.data(self.settingoptionModel.index(cmbOptionLinkrow, dataColumn))
        # OptionLinkrow2 = self.settingoptionModel.data(self.settingoptionModel.index(cmbOptionLinkrow, 2))

        NewID = ProgramSettings.addSettings(Database=self.settingDatabase, Datatable=self.settingTable,
                                                  Location=1,
                                                  SettingDict=self.UpdatedItem,
                                                  Datatype=DataTyperowID,
                                                  OptionType=OptionLinkrowID)

        # self.tvSettingsModel.setData(self.tvSettingsModel.currentIndex,8,None)
        self.dialog.txtSettingID.setText(str(NewID))
        self.on_cmdSettingSave_clicked()
        self.loadSettingForm()

    @QtCore.pyqtSlot()
    def on_cmdSettingRemove_clicked(self):
        SQLDelete = "DELETE FROM %s" % self.settingTable
        SQLWhere = " WHERE ID = %s" % self.dialog.txtSettingID.text()

        conn = sqlite3.connect(self.settingDatabase)
        cursor = conn.cursor()
        cursor.execute(SQLDelete + SQLWhere)
        conn.commit()
        cursor.close()
        conn.close()
        self.loadSettingForm()

    def __init__(self, TD1, tablesettings, MasterData, parent = None, widget = None):
        frmBase.__init__(self)

        self.settingTable = tablesettings
        self.settingDatabase = "DSSettings.db"

        self.dialog = loadUi('frmTreeBuilder.ui')

        self.treedict = TD1
        self.treedict2 = self.treedict.copy()
        self.componenttreedict = TD1.copy()
        self.componenttreedict["TreeItems"] = self.treedict["ComponentTable"]

        self.MasterData = MasterData
        self.sessionlist = MasterData.sessiondict
        self.baselist = MasterData.basedict
        self.header = "Header"

        self.dialog.txtTableItemID.setText(str(0))
        self.dialog.txtPrimaryGroupID.setText(str(0))
        self.dialog.txtSecondaryGroupID.setText(str(0))
        self.dialog.txtTreeItemID.setText(str("(0)"))
        self.dialog.txtTreeParentItemID.setText(str(0))
        self.dialog.txtParentItemID.setText(str("(0)"))
        self.dialog.txtTreeItemLevel.setText(str(0))
        self.dialog.txtTreeItemOrder.setValue(int(0))
        self.dialog.txtTreePath.setText(str("(0)"))

        self.loadSettingForm()
        self.loadTreeSettingForm()
        self.loadBBTable()

        self.dialog.exec_()

    def loadTreeSettingForm(self):

        self.treeitemdata={}
        self.treeitemdata['PrimaryGroup_id'] = None
        self.treeitemdata['Tree_id'] = None
        self.treeitemdata['ParentTree_id'] = None
        self.treeitemdata['DescriptorMaster'] = None
        self.treeitemdata['DescriptorMasterTable'] = None
        self.treeitemdata['DescriptorTable'] = None
        self.treeitemdata['Descriptor_id'] = None
        self.treeitemdata['ItemMaster'] = None
        self.treeitemdata['ItemTable'] = None
        self.treeitemdata['Item_id'] = None
        self.treeitemdata['DisplayName'] = None
        self.treeitemdata['ItemOrder'] = 0
        self.treeitemdata['FlattenedOrder'] = None
        self.treeitemdata['ItemLevel'] = -1
        self.treeitemdata['ForeColor'] = None
        self.treeitemdata['Expanded'] = False
        self.treeitemdata['Header'] = None

        self.datatable = 'treeitems'

        qrysessionlist = self.treedict["MasterSession"].query(SessionNames.id, SessionNames.NameText, literal_column(str("242"))) #139
        self.dialog.lstMasterTableSession.setModel(QueryTableModel(qrysessionlist))
        self.dialog.lstMasterTableSession.model().reset_content_from_session()
        self.dialog.lstMasterTableSession.setModelColumn(1)
        self.dialog.lstMasterTableSession.selectionModel().selectionChanged.connect(self.loadSessionList)

        self.dialog.cmbDestinationSession.setModel(QueryTableModel(qrysessionlist))
        self.dialog.cmbDestinationSession.model().reset_content_from_session()
        self.dialog.cmbDestinationSession.setModelColumn(1)


        self.dialog.lstMasterTableItems.clicked.connect(self.loadsampleTableData)

#Master Tree Table
        qrymastertree = self.treedict["Session"].query(self.treedict["TreeSettings"].id, self.treedict["TreeSettings"].NameText)
        self.dialog.cmbTreeSettings.setModel(QueryTableModel(qrymastertree))
        self.dialog.cmbTreeSettings.model().reset_content_from_session()
        self.dialog.cmbTreeSettings.setModelColumn(1)

        self.dialog.cmbTreeSettings.currentIndexChanged.connect(self.on_cmbTreeSettings_currentIndexChanged)

        qrymastertable = Session.query(self.treedict["MasterTable"].id, self.treedict["MasterTable"].TableName)

#Tree Group
        #self.loadtreelist()
        Master = self.dialog.cmbTreeSettings.model().index(self.dialog.cmbTreeSettings.currentIndex(), 0, None).data()

        qrytreegroup = self.treedict["Session"].query(self.treedict["PrimaryGroup"].id, self.treedict["PrimaryGroup"].NameText)
        self.dialog.cmbPrimaryGroup.setModel(QueryTableModel(qrytreegroup))
        self.dialog.cmbPrimaryGroup.model().reset_content_from_session()
        self.dialog.cmbPrimaryGroup.setModelColumn(1)

        self.dialog.cmbPrimaryGroup_2.setModel(QueryTableModel(qrytreegroup))
        self.dialog.cmbPrimaryGroup_2.model().reset_content_from_session()
        self.dialog.cmbPrimaryGroup_2.setModelColumn(1)


        defaulttreegroup = 1

        for row in range(self.dialog.cmbPrimaryGroup.model().rowCount(None)):
            if str(self.dialog.cmbPrimaryGroup.model().index(row, 0, None).data()) == str(defaulttreegroup):
                self.dialog.cmbPrimaryGroup.setCurrentIndex(row)
                break

        self.dialog.cmbPrimaryGroup.currentIndexChanged.connect(self.on_cmbPrimaryGroup_currentIndexChanged)


        qrymastergroup = self.treedict["MasterSession"].query(self.treedict["MasterTable"].id, self.treedict["MasterTable"].NameText)
        self.dialog.cmbPrimaryGroup.setModel(QueryTableModel(qrytreegroup))
        self.dialog.cmbPrimaryGroup.model().reset_content_from_session()
        self.dialog.cmbPrimaryGroup.setModelColumn(1)

        self.dialog.rdoInternal.toggled.connect(self.on_rdoInternal_toggled)
        self.dialog.rdoExternal.toggled.connect(self.on_rdoExternal_toggled)

        self.dialog.cmbDestinationSession.currentIndexChanged.connect(self.on_cmbDestinationSession_currentIndexChanged)
        self.dialog.cmbPrimaryGroup_2.currentIndexChanged.connect(self.on_cmbPrimaryGroup_2_currentIndexChanged)
        self.dialog.tblBranchCreator.clicked.connect(self.on_tblActivityGroups_clicked)
        self.dialog.cmdRemoveBranch.clicked.connect(self.on_cmdRemoveBranch_clicked)
        self.dialog.cmdCreateBranch.clicked.connect(self.on_cmdCreateBranch_clicked)
        self.dialog.cmdCreateBranch_2.clicked.connect(self.on_cmdCreateBranch_2_clicked)
        self.dialog.cmdCreateFullBranch.clicked.connect(self.on_cmdCreateFullBranch_clicked)


        self.dialog.cmdSaveBranch.clicked.connect(self.on_cmdSaveBranch_clicked)

#Tree Table
        #self.tvAttributes, itemcount = DatabaseTools.tvitemAttributes(connt, data["AttributeTable_id"])
        #SQLQuery = 'select * from %s' % ("treeItems")
        #self.treeData = TreeView.treeModel(fileLocation="ControlTree.db", sqlStr=SQLQuery)

        #self.treeData = TreeViewAlchemy.sqlStandardItemModel(session=self.treedict["Session"], tableclass=TreeItems)
        #self.treeData.setupModelData()

        #self.dialog.tblTreeItems.setModel(self.treeData)

        self.dialog.treeView.setAlternatingRowColors(bool(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Show Alternating Row Colors")))

        self.dialog.treeView.setColumnWidth(0,250)
        self.dialog.treeView.setColumnWidth(1,50)
        self.dialog.treeView.setColumnWidth(2,50)
        self.dialog.treeView.clicked.connect(self.on_treeView_Clicked)
        self.dialog.treeView.doubleClicked.connect(self.on_treeView_DoubleClicked)
        self.dialog.cmdTreeViewRefresh.clicked.connect(self.on_cmdTreeViewRefresh_Clicked)
        self.dialog.treeView.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")

        # hide grid
        self.dialog.tblTreeItems.setShowGrid(bool(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1,"Show Grid")))

        # set the font
        if ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable,1,"Font Size") is not None:
            font = QFont(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1,"Font"), int(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable,1,"Font Size")))
            self.dialog.tblTreeItems.setFont(font)

        # hide vertical Header
        vh = self.dialog.tblTreeItems.verticalHeader()
        vh.setVisible(bool(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Show Vertical Header")))

        # set horizontal Header properties
        hh = self.dialog.tblTreeItems.horizontalHeader()
        hh.setStretchLastSection(bool(ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Horizontal Header")))

        # set column width to fit contents
        self.dialog.tblTreeItems.resizeColumnsToContents()

        self.dialog.tblTreeItems.setSortingEnabled(True)

        self.dialog.tblTreeItems.setColumnWidth(0,50)
        self.dialog.tblTreeItems.setColumnWidth(1,50)
        self.dialog.tblTreeItems.setColumnWidth(2,50)
        self.dialog.tblTreeItems.setColumnWidth(3,50)
        self.dialog.tblTreeItems.setColumnWidth(4,200)
        self.dialog.tblTreeItems.setColumnWidth(5,50)

        self.dialog.tblTreeItems.clicked.connect(self.cell_was_clicked)
        self.dialog.tblTreeItems.doubleClicked.connect(self.cell_was_dblclicked)
        self.dialog.tblTreeItems.pressed.connect(self.cell_was_pressed)
        #self.dialog.tblTreeItems.released.connect(self.cell_was_clicked)

        #self.loadDescriptorTypes(self.treemodel.recordCount())

#lstDescriptor
        self.descriptorModelproxy = QSortFilterProxyModel()
        #self.loadDescriptor()

#listItemTypes
        #self.loadItemTypes(self.treemodel.recordCount())
#items
        self.itemModelproxy = QSortFilterProxyModel()
        #self.loadItems()

        self.dialog.AddTreeSettings.clicked.connect(self.on_AddTreeSettings_clicked)
        self.dialog.cmdCreatePrimaryGroup.clicked.connect(self.on_cmdCreatePrimaryGroup_clicked)
        self.dialog.cmdCreateSecondaryGroup.clicked.connect(self.on_cmdCreateSecondaryGroup_clicked)

        self.dialog.cmdAddDescriptorTable2.clicked.connect(self.on_cmbAddDescriptorTable_clicked)

        self.dialog.cmdAddItemTable.clicked.connect(self.on_AddItemTable_clicked)

        self.dialog.txtSearchMasterTableItem.textChanged.connect(self.on_txtSearchMasterTableItem_textChanged)
        self.dialog.txtSearchDescriptor.textChanged.connect(self.on_txtSearchDescriptor_textChanged)
        self.dialog.cmdAddDescriptorItem.clicked.connect(self.on_cmdAddDescriptorItem_clicked)

        self.dialog.cmdAddItem.pressed.connect(self.on_cmdAddItem_clicked)
        self.dialog.txtSearchItem.textChanged.connect(self.on_txtSearchItem_textChanged)

        self.dialog.cmdAddSubDescription.pressed.connect(self.on_cmdAddSubDescription_clicked)
        self.dialog.cmdAddAdjDescription.pressed.connect(self.on_cmdAddAdjDescription_clicked)
        self.dialog.cmdAddRootDescription.pressed.connect(self.on_cmdAddRootDescription_clicked)

        self.dialog.cmdAddSubItem.pressed.connect(self.on_cmdAddSubItem_clicked)
        self.dialog.cmdAddAdjItem.pressed.connect(self.on_cmdAddAdjacent_clicked)

        self.dialog.cmbTreeItemTable_id_3.setModel(QueryTableModel(qrymastertable))
        self.dialog.cmbTreeItemTable_id_3.model().reset_content_from_session()
        self.dialog.cmbTreeItemTable_id_3.setModelColumn(1)

        self.dialog.tblBranchCreator.clicked.connect(self.on_tblBranchCreator_clicked)


        self.dialog.txtDisplay.textEdited.connect(self.on_txtDisplay_textEdited)
        #self.dialog.txtDisplay.editingFinished.connect(self.on_txtDisplay_editingFinished)
        self.dialog.cmdAddTitleTag.clicked.connect(self.on_cmdAddTitleTag_clicked)

        self.dialog.cmdRemoveTreeItem.clicked.connect(self.on_cmdRemoveTreeItem_clicked)

        self.loadDescriptorTypes()
        self.loadItemTypes()

    def ClearSettingData(self):
        self.dialog.txtSettingID.setText(None)
        self.dialog.cmbOptionCategory.setCurrentIndex(0)
        self.dialog.txtSettingName.setText(None)
        self.dialog.txtSettingValue.setText(None)
        self.dialog.txtSettingDescription.setText(None)
        self.dialog.cmbDataType.setCurrentIndex(0)
        self.dialog.txtSettingOption.setText(None)
        self.dialog.cmbOptionLink.setCurrentIndex(0)

    def LoadTreeModel(self):
        self.dialog.treeView.setModel(None)
        self.treemodel = TreeViewAlchemy2.linkedtreemodel(self.MasterData, self.treedict, header=self.header)
        mrilist = []
        selectedItems = self.dialog.lstSecondaryGroup.selectedIndexes()
        for itemsselected in selectedItems:
            SecondaryGroup_id = self.dialog.lstSecondaryGroup.model().index(itemsselected.row(), 3, None).data()
            ItemName = self.dialog.lstSecondaryGroup.model().index(itemsselected.row(), 1, None).data()
            PrimaryGroup_id = self.dialog.lstSecondaryGroup.model().index(itemsselected.row(), 2, None).data()
            if ItemName != "":
                modelrootitem = self.treedict["Session"].query(self.treedict["TreeItems"]).filter_by(ParentTree_id="(0)") \
                                                                                            .filter_by(PrimaryGroup_id=PrimaryGroup_id) \
                                                                                            .filter_by(SecondaryGroup_id=SecondaryGroup_id)\
                                                                                            .order_by(self.treedict["TreeItems"].ItemOrder)\
                                                                                            .order_by(self.treedict["TreeItems"].DisplayName).first()

                if modelrootitem is not None:
                    data = {}
                    data["root_id"] = modelrootitem.id
                    data["SourcePG"] = PrimaryGroup_id
                    data["SourceSG"] = modelrootitem.SecondaryGroup_id
                    data["DestinationPG"] = None
                    data["DestinationSG"] = None

                    mrilist.append(data)

        if mrilist != []:
            self.treemodel.createLinkedTree(mrilist)
            self.dialog.treeView.setModel(self.treemodel)

            self.dialog.treeView.expandToDepth(2)

    def on_treeView_Clicked(self, index):
        itemselected = index.internalPointer()
        self.createItemTable(itemselected.TreeClassItem.TreePath)
        #print(itemselected.TreeClassItem.Tree_id, itemselected.TreeClassItem.TreePath)

    def on_cmdTreeViewRefresh_Clicked(self):
        self.LoadTreeModel()

    def on_cmdRemoveTreeItem_clicked(self):
        txttreepath = self.dialog.txtTreePath.text()
        TreeRecord = self.treedict["Session"].query(self.treedict["TreeItems"]).filter_by(TreePath=txttreepath)
        if TreeRecord:
            self.treedict["Session"].begin()
            TreeRecord.delete(synchronize_session=False)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()
        self.LoadTreeModel()

    def on_AddTreeSettings_clicked(self):
        NewName = self.dialog.cmbTreeSettings.currentText()

        newitem = self.treedict["Session"].query(self.treedict["TreeSettings"]).filter_by(NameText=NewName).first()

        if newitem is None:
            self.treedict["Session"].begin()
            newitem = self.treedict["TreeSettings"](NameText=NewName)
            self.treedict["Session"].add(newitem)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()

        MTTModel = self.treedict["Session"].query(self.treedict["TreeSettings"]).order_by(self.treedict["TreeSettings"].NameText)

        self.dialog.cmbTreeSettings.setModel(QueryTableModel(MTTModel))

        for row in range(self.dialog.cmbTreeSettings.model().rowCount()):
            if int(self.dialog.cmbTreeSettings.model().index(row, 0).data()) == newitem.id:
                self.dialog.cmbTreeSettings.setCurrentIndex(row)
                break

        self.loadDescriptorTypes()
        self.loadItemTypes()

    #@QtCore.pyqtSlot()
    def on_cmdCreatePrimaryGroup_clicked(self):
        #Add Blank Zero Record
        NewTreeGroup = self.treedict["Session"].query(self.treedict["PrimaryGroup"]).first()
        if NewTreeGroup is None:
            self.treedict["Session"].begin()
            NewTreeGroup = self.treedict["PrimaryGroup"](NameText="")
            self.treedict["Session"].add(NewTreeGroup)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()

        NewName = self.dialog.cmbPrimaryGroup.currentText()

        NewTreeGroup = self.treedict["Session"].query(self.treedict["PrimaryGroup"]).filter_by(NameText=NewName).first()

        if NewTreeGroup is None:
            self.treedict["Session"].begin()
            NewTreeGroup = self.treedict["PrimaryGroup"](NameText=NewName)
            self.treedict["Session"].add(NewTreeGroup)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()

        GroupModel = self.treedict["Session"].query(self.treedict["PrimaryGroup"].id, self.treedict["PrimaryGroup"].NameText)

        self.dialog.cmbPrimaryGroup.setModel(QueryTableModel(GroupModel))

        for row in range(self.dialog.cmbPrimaryGroup.model().rowCount()):
            if int(self.dialog.cmbPrimaryGroup.model().index(row, 0).data()) == NewTreeGroup.id:
                self.dialog.cmbPrimaryGroup.setCurrentIndex(row)
                break

    #@QtCore.pyqtSlot()
    def on_cmdCreateSecondaryGroup_clicked(self):
      print("Use Create Root Item Now")

    #@QtCore.pyqtSlot(int)
    def on_cmbTreeSettings_currentIndexChanged(self, index):
        self.loadDescriptorTypes()
        self.loadItemTypes()

    #@QtCore.pyqtSlot(int)
    def on_cmbPrimaryGroup_currentIndexChanged(self, index):
        PrimaryGroup_id = self.dialog.cmbPrimaryGroup.model().index(index, 0).data()

        GroupModel = self.treedict["Session"].query(self.treedict["SecondaryGroup"].id,
                                                      self.treedict["SecondaryGroup"].NameText,
                                                      self.treedict["SecondaryGroup"].PrimaryGroup_id,
                                                      self.treedict["SecondaryGroup"].SecondaryGroup_id) \
                                                        .filter(self.treedict["SecondaryGroup"].PrimaryGroup_id==PrimaryGroup_id)

        self.dialog.lstSecondaryGroup.setModel(QueryTableModel(GroupModel))
        self.dialog.lstSecondaryGroup.setModelColumn(1)
        self.dialog.lstSecondaryGroup.model().reset_content_from_session()


        self.dialog.treeView.setModel(None)

        #ix = self.dialog.lstSecondaryGroup.model().index(whichrowyouwantct, 0)
        #self.list.selectionModel().setCurrentIndex(ix, QtGui.QItemSelectionModel.SelectCurrent)

        model = self.dialog.lstSecondaryGroup.model()
        for rowIndex in range(model.rowCount()):
            sindex = model.index(rowIndex, 1, None)
            #self.dialog.lstSecondaryGroup.selectionModel().select(sindex, QItemSelectionModel.Select)

        self.dialog.lstSecondaryGroup.selectionModel().selectionChanged.connect(self.LoadTreeModel)

        self.LoadTreeModel()

    def loadsampleTableData(self):
        mastertable_id = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(), 0).data()

        conn = self.treedict["MasterSession"].connection()
        sessionbase1 = lario.DatabaseTools.get_class_by_tablename(self.baselist["Master"], "lstsession")
        self.selectedTableModel = QStandardItemModel(0, 2)

        query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(mastertable_id)).first()

        query2 = self.treedict["MasterSession"].query(sessionbase1).filter_by(id=int(query1.Session)).first()

        displayquery = query1.DisplayQuery
        conn2 = self.sessionlist[query2.NameText].connection()
        try:
            if displayquery is not None:
                records = conn2.execute(displayquery).fetchall()

                if records != []:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name = QStandardItem(ItemName[1])

                        self.selectedTableModel.setItem(row, 0, Descriptor_id)
                        self.selectedTableModel.setItem(row, 1, Descriptor_Name)

                conn2.close()

                self.dialog.lstMasterTableSample.setModel(self.selectedTableModel)
                self.dialog.lstMasterTableSample.setModelColumn(1)

                conn.close()
            else:
                print("No Records to Display")
        except:
            print("record display error")

    def on_cmbAddDescriptorTable_clicked(self):
        Master = self.dialog.cmbTreeSettings.model().index(self.dialog.cmbTreeSettings.currentIndex(), 0, None).data()

        mastertable_id = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(), 0).data()
        mastertable_name = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(), 1).data()

        self.treedict["Session"].begin()
        newdescriptor = self.treedict["DescriptorTable"](NameText = mastertable_name, MasterTable_id = mastertable_id, MTTT_id = Master)
        self.treedict["Session"].add(newdescriptor)
        self.treedict["Session"].commit()

        self.loadDescriptorTypes()

    def on_AddDescriptorTable_clicked(self):
        tableName = "taskdescriptortable"
        AddNewItem = UpdateList(self, tableName, self.treedict["Session"], Reference, session)
        NewData = AddNewItem.GetItemData()

        self.dialog.lstDescriptorTypes.setModel(AddNewItem.GetItemModel())

    def on_AddItemTable_clicked(self):

        Master = self.dialog.cmbTreeSettings.model().index(self.dialog.cmbTreeSettings.currentIndex(), 0, None).data()

        mastertable_id = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(), 0).data()
        mastertable_name = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(), 1).data()

        self.treedict["Session"].begin()
        newitem = self.treedict["ItemTable"](NameText=mastertable_name, MasterTable_id=mastertable_id, MTTT_id = Master)
        self.treedict["Session"].add(newitem)
        self.treedict["Session"].commit()

        self.loadItemTypes()

    def on_AddItemTable_clicked2(self):
        tableName = "taskitemtable"
        AddNewItem = UpdateList(self, tableName, self.treedict["Session"], Reference, session)
        NewData = AddNewItem.GetItemData()

        self.dialog.listItemTypes.setModel(AddNewItem.GetItemModel())

    #@QtCore.pyqtSlot(str)
    def on_txtSearchMasterTableItem_textChanged(self, text):
        #self.loadDescriptorTypes(1)
        search = QRegularExpression(text,
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.sessionitemModelproxy.setFilterRegExp(search)
        self.sessionitemModelproxy.setFilterKeyColumn(1)

    #@QtCore.pyqtSlot(str)
    def on_txtSearchDescriptor_textChanged(self, text):
        #self.loadDescriptorTypes(1)
        search = QRegularExpression(text,
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.descriptorModelproxy.setFilterRegExp(search)
        self.descriptorModelproxy.setFilterKeyColumn(1)

    #@QtCore.pyqtSlot(str)
    def on_txtSearchItem_textChanged(self, text):
        #self.loadItemTypes(1)
        search = QRegularExpression(text,
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.itemModelproxy.setFilterRegExp(search)
        self.itemModelproxy.setFilterKeyColumn(1)

    #@QtCore.pyqtSlot()
    def on_lstDescriptorTypes_selectionChanged(self,selected, deselected):
        print(selected,deselected)

    #@QtCore.pyqtSlot()
    def on_listItem_selectionChanged(self,selected, deselected):
        print(selected,deselected)

    #@QtCore.pyqtSlot()
    def on_cmdAddDescriptorItem_clicked(self):

        popup = True

        if popup == True:
            selectedItems = self.dialog.lstDescriptorTypes.selectedIndexes()
            descriptorcount = len(selectedItems)
            descriptortable = None
            if descriptorcount == 1:
                for itemsselected in selectedItems:
                    DescriptorMasterTable = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 2, None).data()

                self.listeditor = UpdateList(self, bases, sessions, DescriptorMasterTable)

            NewItemName = "New Name"

            AddEvent = "%s was added to table %s" % (NewItemName, descriptortable)
            self.addHistoryEvent(AddEvent)

        #self.loadDescriptor()

    #@QtCore.pyqtSlot()
    def on_cmdAddItem_clicked(self):
        print("Adding Item")
        selectedItems = self.dialog.listItemTypes.selectedIndexes()
        itemcount = len(selectedItems)
        itemtable = None
        if itemcount == 1:
            for itemsselected in selectedItems:
                itemtable = self.dialog.listItemTypes.model().index(itemsselected.row(), 2, None).data()

            table_id = 194
            self.listeditor = UpdateList(self, bases, sessions, table_id)

            NewItemName = "New Name"

            AddEvent = "%s was added to table %s" % (NewItemName, itemtable)
            self.addHistoryEvent(AddEvent)

            self.loadItems()

    #@QtCore.pyqtSlot()
    def on_cmdAddRootDescription_clicked(self):

        treedict = self.treedict

        AddLevel = None

        PrimaryGroup_id = self.dialog.cmbPrimaryGroup.model().index(self.dialog.cmbPrimaryGroup.currentIndex(), 0).data()
        Secondary_id = self.treedict["Session"].query(self.treedict["SecondaryGroup"]).filter_by(PrimaryGroup_id=PrimaryGroup_id).count()

        # Add Blank Zero Record
        NewTreeGroup = self.treedict["Session"].query(self.treedict["SecondaryGroup"]).filter_by(PrimaryGroup_id=PrimaryGroup_id).first()
        if NewTreeGroup is None:
            self.treedict["Session"].begin()
            NewTreeGroup = self.treedict["SecondaryGroup"](NameText="", PrimaryGroup_id=PrimaryGroup_id, SecondaryGroup_id=Secondary_id+1)
            self.treedict["Session"].add(NewTreeGroup)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()
            Secondary_id = Secondary_id + 1

        NameText = ("%s-%s") % (PrimaryGroup_id, Secondary_id + 1)

        self.treedict["Session"].begin()
        NewSecondaryGroup = self.treedict["SecondaryGroup"](NameText = NameText, PrimaryGroup_id=PrimaryGroup_id, SecondaryGroup_id=Secondary_id+1)
        self.treedict["Session"].add(NewSecondaryGroup)
        self.treedict["Session"].commit()
        self.treedict["Session"].flush()

        SecondaryGroup_id = NewSecondaryGroup.SecondaryGroup_id

        ItemList = []

        for itemsselected in self.dialog.lstDescriptors.selectionModel().selectedIndexes():
            data = {}

            data['Item_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(), 0).data()
            data['Name'] = self.dialog.lstDescriptors.model().index(itemsselected.row(), 1).data()
            data['MasterTable_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),2).data()
            data['Table'] = self.dialog.lstDescriptors.model().index(itemsselected.row(), 3).data()
            data['PrimaryGroup_id'] = self.dialog.cmbPrimaryGroup.model().index(self.dialog.cmbPrimaryGroup.currentIndex(), 0).data()
            data['SecondaryGroup_id'] = SecondaryGroup_id

            ItemList.append(data)

        treeid = self.AddTreeItem(AddLevel, ItemList, treedict)
        #self.treemodel.setupModelData(MasterTable_id, treeid)
        #self.dialog.treeView.setModel(self.treemodel)

        TagName = treeid["Tags"][0]
        NameCount = self.treedict["Session"].query(self.treedict["TreeItems"]).filter_by(Tags=TagName).filter_by(PrimaryGroup_id=PrimaryGroup_id).count()

        NewName = ("%s-%s") % (data['Name'], str(NameCount))

        self.treedict["Session"].begin()
        NewSecondaryGroup.NameText = NewName
        self.treedict["Session"].commit()
        self.treedict["Session"].flush()

        self.roottreeitem = treeid
        self.LoadTreeModel()

        GroupModel = self.treedict["Session"].query(self.treedict["SecondaryGroup"].id,
                                                    self.treedict["SecondaryGroup"].NameText,
                                                    self.treedict["SecondaryGroup"].PrimaryGroup_id) \
            .filter_by(PrimaryGroup_id=PrimaryGroup_id)

        self.dialog.lstSecondaryGroup.setModel(QueryTableModel(GroupModel))
        #self.dialog.lstSecondaryGroup.selectionModel().selectionChanged.connect(self.LoadTreeModel)

    #@QtCore.pyqtSlot()
    def on_cmdAddAdjDescription_clicked(self):
        treedict = self.treedict

        ItemList = []

        for itemsselected in self.dialog.lstDescriptors.selectionModel().selectedIndexes():

            data = {}
            data['Table'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),3).data()
            data['MasterTable_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),2).data()
            data['Name'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),1).data()
            data['Item_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),0).data()
            data['PrimaryGroup_id'] = int(self.dialog.txtPrimaryGroupID.text())
            data['SecondaryGroup_id'] = int(self.dialog.txtSecondaryGroupID.text())

            ItemList.append(data)

        self.AddTreeItem(0, ItemList, treedict)

        self.LoadTreeModel()


    #@QtCore.pyqtSlot()
    def on_cmdAddSubDescription_clicked(self):

        treedict = self.treedict

        AddLevel = 1

        ItemList = []

        for itemsselected in self.dialog.lstDescriptors.selectionModel().selectedIndexes():

            data = {}
            data['Table'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),3).data()
            data['MasterTable_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),2).data()
            data['Name'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),1).data()
            data['Item_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),0).data()
            data['PrimaryGroup_id'] = int(self.dialog.txtPrimaryGroupID.text())
            data['SecondaryGroup_id'] = int(self.dialog.txtSecondaryGroupID.text())

            ItemList.append(data)

        treeid = self.AddTreeItem(AddLevel, ItemList, treedict)


        #self.treemodel.setupModelData(treedict["Session"], treedict["TreeItems"], ItemList)
        #self.dialog.treeView.setModel(self.treemodel)

        self.LoadTreeModel()
        #self.LoadTreeModel()




    #@QtCore.pyqtSlot()
    def on_cmdAddSubItem_clicked(self):

        treedict = self.treedict

        AddLevel = 1

        ItemList = []

        for itemsselected in self.dialog.listItem.selectionModel().selectedIndexes():
            data = {}
            data['Table'] = self.dialog.listItem.model().index(itemsselected.row(), 3).data()
            data['MasterTable_id'] = self.dialog.listItem.model().index(itemsselected.row(), 2).data()
            data['Name'] = self.dialog.listItem.model().index(itemsselected.row(), 1).data()
            data['Item_id'] = self.dialog.listItem.model().index(itemsselected.row(), 0).data()
            data['PrimaryGroup_id'] = int(self.dialog.txtPrimaryGroupID.text())
            data['SecondaryGroup_id'] = int(self.dialog.txtSecondaryGroupID.text())
            ItemList.append(data)

        treeid = self.AddTreeItem(AddLevel, ItemList, treedict)


        self.LoadTreeModel()

    #@QtCore.pyqtSlot()
    def on_cmdAddAdjacent_clicked(self):
        pass

    def AddTreeRoot(self, RootName):

        indexlist = self.dialog.treeView.selectedIndexes()
        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        newtreeitemdata = self.treemodel.defaultTreeItem()
        newtreeitemdata['DisplayName'] = RootName

        ActivityTypeParentID = self.addTreeItem(treeviewindex, newtreeitemdata)

    def AddTreeItem(self, AddLevel, ItemList, TreeDict):
        # 0 puts item on same level
        # 1 puts item on one level below (sub item)

        treedict = self.treedict
        treemodel = self.treemodel
        indexlist = self.dialog.treeView.selectedIndexes()
        Record_id = self.dialog.txtTableItemID.text()
        Tree_id = self.dialog.txtTreeItemID.text()
        TreeParentItem_id = self.dialog.txtTreeParentItemID.text()
        ParentItem_id = self.dialog.txtParentItemID.text()
        ItemLevel = self.dialog.txtTreeItemLevel.text()
        ItemOrder = self.dialog.txtTreeItemOrder.value()
        ItemMasterTable = -1
        Item_id = -1
        ItemTable_id = -1
        if AddLevel == 0:
            TreePath = ""
            TagPath = "None"
        else:
            TreePath = self.dialog.txtTreePath.text()
            TagPath = self.dialog.txtTagPath.text()

        treeviewindex = None
        for index in indexlist:
            treeviewindex = index

        newtreeitemdata = treemodel.defaultTreeItem()
        #newtreeitemdata['ItemMaster_id'] = ItemMasterTable
        newtreeitemdata['MasterTable_id'] = treedict["MasterTable_id"]

        newtreeitemdata['ItemTable_id'] = -1
        ParentTree_id = 0

        if AddLevel is None:
            newtreeitemdata['ParentTree_id'] = "(0)"
            newtreeitemdata['ItemLevel'] = 0
        elif AddLevel == 1:
            if Tree_id == "-":
                ParentTree_id = 0
            else:
                ParentTree_id = str(Tree_id)

            newtreeitemdata['ParentTree_id'] = ParentTree_id
            newtreeitemdata['ItemLevel'] = int(ItemLevel) + int(AddLevel)
        else:
            treeviewindex = index.parent()
            if self.dialog.txtParentItemID.text() == "-":
                ParentTree_id = 0
            else:
                ParentTree_id = str(ParentItem_id)

            newtreeitemdata['ParentTree_id'] = ParentTree_id
            newtreeitemdata['ItemLevel'] = int(ItemLevel)

        selectedItems = self.dialog.listItem.selectedIndexes()
        itemcount = len(selectedItems)

        treeid = 0

        newtreeitemdata['Tags'] = []
        newtreeitemdata['TreePath'] = strToMyList(TreePath)
        if TagPath != "None":
            newtreeitemdata['Tags'] = strToMyList(TagPath)

        parenttreepath = newtreeitemdata['TreePath']
        partenttag = newtreeitemdata['Tags']

        for itemsselected in ItemList:

            newtreeitemdata["Item_id"] = int(itemsselected['Item_id'])
            newtreeitemdata["ItemTable_id"] = int(itemsselected['MasterTable_id'])
            newtreeitemdata['PrimaryGroup_id'] = itemsselected['PrimaryGroup_id']
            newtreeitemdata['SecondaryGroup_id'] = itemsselected['SecondaryGroup_id']

            mastertabledata = self.treedict["MasterSession"].query(TreeDict["MasterTable"]).filter_by(id=int(itemsselected['MasterTable_id'])).first()
            #if mastertabledata.ItemTableType_id is not None: newtreeitemdata['ItemTableType_id'] = mastertabledata.ItemTableType_id

            #print(mastertabledata.Base)

            SessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=mastertabledata.Session).first()
            BaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=mastertabledata.Base).first()

            if mastertabledata.TableType_id is not None: newtreeitemdata['ItemTableType_id'] = mastertabledata.TableType_id

            tableclass = DatabaseTools.get_class_by_tablename(self.baselist[BaseName.NameText], mastertabledata.TableName)

            itemcount = TreeDict["Session"].query(TreeDict["TreeItems"]).filter_by(ParentTree_id=ParentTree_id).count()
            newtreeitemdata['ItemOrder'] = itemcount

            fielditem = self.sessionlist[SessionName.NameText].query(tableclass).filter_by(id=int(itemsselected['Item_id'])).first()

            newtreeitemdata['TreePath'] = parenttreepath.copy()
            newtreeitemdata['Tags'] = partenttag.copy()
            newtreeitemdata['ItemTable_id'] = itemsselected['MasterTable_id']
            newtreeitemdata['DestinationPG'] = itemsselected['PrimaryGroup_id']
            newtreeitemdata['DestinationSG'] = itemsselected['SecondaryGroup_id']

            if mastertabledata.DisplayColumn == "NameText":
                newtreeitemdata['DisplayName'] = fielditem.NameText
                newtreeitemdata['ItemName'] = fielditem.NameText
            if mastertabledata.DisplayColumn == "Title":
                newtreeitemdata['DisplayName'] = fielditem.Title
                newtreeitemdata['ItemName'] = fielditem.Title

            newtreeitemdata['id'] = None

            if treeviewindex is not None:
                treemodel.beginInsertRows(treeviewindex, 0, 0)
                newtreeitemdata['Tree_id'] = None
                print("Adding", newtreeitemdata)
                treeid = treemodel.addTreeItem(TreeDict["TreeItems"], newtreeitemdata)
                treemodel.endInsertRows()
            else:
                newtreeitemdata['Tree_id'] = None
                RootName = "Need to change this to proper title"
                print("Root Data", newtreeitemdata)
                PrimaryGroup_id = None
                treeid = treemodel.AddTreeRoot(RootName, indexlist, newtreeitemdata, LinkedTable=TreeDict["TreeItems"])

        #self.addTreeTag(newtreeitemdata)
        return treeid

    def on_cmdAddTitleTag_clicked(self):

        txttreepath_id = self.dialog.txtTreePath.text()
        treedict = self.treedict
        treedict["Session"].begin()
        treerecordcount = treedict["Session"].query(treedict["TreeItems"]).filter_by(TreePath=txttreepath_id).count()
        if treerecordcount == 1:
            treerecord = treedict["Session"].query(treedict["TreeItems"]).filter_by(TreePath=txttreepath_id).first()
            if treerecord:
                tagstring = treerecord.Tags
                taglist = strToMyList(tagstring)

                for itemsselected in self.dialog.listItem.selectionModel().selectedIndexes():
                    data = {}
                    data['Table'] = self.dialog.listItem.model().index(itemsselected.row(),3).data()
                    data['MasterTable_id'] = self.dialog.listItem.model().index(itemsselected.row(),2).data()
                    data['Item_id'] = self.dialog.listItem.model().index(itemsselected.row(),0).data()
                    NewTag = "(%s-%s)" % (str(data['MasterTable_id']), str(data['Item_id']))
                    taglist.append(NewTag)
                newtagstring = myListToStr(taglist)
                treerecord.Tags = newtagstring
                self.dialog.txtTagPath.setText(newtagstring)
            treedict["Session"].commit()
            treedict["Session"].flush()
            self.LoadTreeModel()

    def addTreeTag(self, newtreeitemdata):
        tagid = "%s-%s" % (str(newtreeitemdata['ItemMaster_id']), str(newtreeitemdata["Item_id"]))
        taglistquery = tsession.query(TagList).filter_by(Tag_id=tagid).first()
        tagName = newtreeitemdata['ItemName']

        if taglistquery is None:
            tsession.begin()
            taglistquery = TagList(Tag_id=tagid,
                                   NameText=tagName)
            tsession.add(taglistquery)
            tsession.commit()

        Taglist = newtreeitemdata['Tags']

        if len(Taglist) != 1:
            taggroupname = ""
            for count, eachtagitem in enumerate(Taglist):
                TagListQuery = tsession.query(TagList).filter_by(Tag_id=eachtagitem).first()
                if TagListQuery is not None:
                    if count == 0:
                        taggroupname = TagListQuery.NameText
                    else:
                        taggroupname += ", " + TagListQuery.NameText

            tsession.begin()
            taglistquery = TagList(Tag_id=myListToStr(newtreeitemdata['Tags']),
                                   NameText=taggroupname, Levels=count + 1)
            tsession.add(taglistquery)
            tsession.commit()

    def on_cmdCreateBranch_Clicked(self):
        primaryGroup_id = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0, None).data()

        treedict = self.settingTable

        #treedict["MasterSession"] = sessions["PackageManager"]
        #treedict["MasterTable"] = MasterTable
        #treedict["DescriptorTable"] = TaskDescriptorTable
        #treedict["ItemTable"] = TaskItemTable
        #treedict["Session"] = sessions["TaskManager"]
        #treedict["SessionName"] = "TaskManager"
        #treedict["TreeItems"] = TaskTree

        treedict["Header"] = "Tree Header"
        treedict["GeneratedSession"] = sessions["PackageManager"]
        treedict["GeneratedTree"] = ActivityTaskTree
        treedict["ComponentTable"] = TaskComponents

        treedict["PrimaryGroup"] = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0, None).data()
        treedict["MasterTable_id"] = 360

        TreeViewAlchemy2.createbranch(treedict)


    def on_cmbEventGroupExtension_currentIndexChanged(self, index):
        self.dialog.txtExtensionGroupList.setText(str(self.dialog.cmbEventGroupExtension.model().index(self.dialog.cmbEventGroupExtension.currentIndex(), 2, None).data()))


    def AddTreeItem2(self, AddLevel=None):
        #0 puts item on same level
        #1 puts item on one level below (sub item)
        indexlist = self.dialog.treeView.selectedIndexes()

        treeviewindex = None
        for index in indexlist:
            treeviewindex = index

        newtreeitemdata = {}
        newtreeitemdata['Tree_id'] = None #Will be added when record is made
        newtreeitemdata['PrimaryGroup_id'] = self.dialog.cmbPrimaryGroup.model().index(self.dialog.cmbPrimaryGroup.currentIndex(), 0, None).data()
        treeGroup = self.dialog.cmbPrimaryGroup.model().index(self.dialog.cmbPrimaryGroup.currentIndex(), 1, None).data()

        if AddLevel is None:
            newtreeitemdata['ParentTree_id'] = "(0)"
            newtreeitemdata['ItemLevel'] = 0
        elif AddLevel == 1:
            newtreeitemdata['ParentTree_id'] = self.dialog.txtTreeItemID.text()
            newtreeitemdata['ItemLevel'] = int(self.dialog.txtTreeItemLevel.text()) + int(AddLevel)
        else:
            newtreeitemdata['ParentTree_id'] = self.dialog.txtTreeParentItemID.text()
            newtreeitemdata['ItemLevel'] = int(self.dialog.txtTreeItemLevel.text()) + int(AddLevel)

        newtreeitemdata['DescriptorMasterTable'] = self.dialog.cmbMasterDescriptor.model().index(self.dialog.cmbMasterDescriptor.currentIndex(), 1, None).data()
        newtreeitemdata['DescriptorMaster_id'] = self.dialog.cmbMasterDescriptor.model().index(self.dialog.cmbMasterDescriptor.currentIndex(), 0, None).data()
        newtreeitemdata['DescriptorTable'] = None
        newtreeitemdata['DescriptorTable_id'] = None
        newtreeitemdata['DescriptorName'] = None
        newtreeitemdata['Descriptor_id'] = None

        newtreeitemdata['ItemMasterTable'] = self.dialog.cmbMasterItem.model().index(self.dialog.cmbMasterItem.currentIndex(), 1, None).data()
        newtreeitemdata['ItemMaster_id'] = self.dialog.cmbMasterItem.model().index(self.dialog.cmbMasterItem.currentIndex(), 0, None).data()
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['Item_id'] = 0

        newtreeitemdata['TreePath'] = self.dialog.txtTreeParentItemID.text()
        newtreeitemdata['DisplayName'] = None
        newtreeitemdata['FlattenedOrder'] = 0
        newtreeitemdata['ItemOrder'] = 0
        #print(int(self.txtTreeItemLevel.text()))
        #Program will fail here if nothing is selected!


        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = False
        newtreeitemdata['Header'] = None

        #txtLoadTreeViewrow = self.dialog.txtLoadTreeView.currentIndex()
        #FileLocationID = self.dialog.txtLoadTreeView.model().index(txtLoadTreeViewrow, 0).data()

        #The original table could be a multiselect so use the other table that will have the value in it as well

        selectedDescriptors = self.dialog.lstDescriptors.selectedIndexes()
        descriptorcount = len(selectedDescriptors)
        selectedItems = self.dialog.listItem.selectedIndexes()
        itemcount = len(selectedItems)

        for itemsselected in selectedDescriptors:
            id = self.dialog.lstDescriptors.model().index(itemsselected.row(),0).data()
            value = self.dialog.lstDescriptors.model().index(itemsselected.row(),1).data()
            table = self.dialog.lstDescriptors.model().index(itemsselected.row(),2).data()
            table2 = self.dialog.lstDescriptors.model().index(itemsselected.row(),3).data()
            #print(id, value, table, table2)

            newtreeitemdata['DescriptorTable'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),3).data()
            newtreeitemdata['DescriptorTable_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),2).data()
            newtreeitemdata['DescriptorName'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),1).data()
            newtreeitemdata['Descriptor_id'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),0).data()

            newtreeitemdata['DisplayName'] = self.dialog.lstDescriptors.model().index(itemsselected.row(),1).data()

            #if multiselect is selected then each item is processed individually


            if (descriptorcount != 1) or (itemcount == 0):
                #Just to be cautious this data is going to be removed.  Incase function gets called two times and data from first call is not removed.
                newtreeitemdata['ItemTable'] = None
                newtreeitemdata['ItemTable_id'] = 0
                newtreeitemdata['ItemName'] = None
                newtreeitemdata['Item_id'] = 0

                if treeviewindex is not None:
                    self.treemodel.beginInsertRows(treeviewindex, 0, 0)
                treeid = self.treemodel.addTreeItem(TreeItems, newtreeitemdata)
                if treeviewindex is not None:
                    self.treemodel.endInsertRows()
                HistoryEvent = "Added Descriptor %s from table %s to %s" % (newtreeitemdata['DescriptorName'], newtreeitemdata['DescriptorTable'], treeGroup)
                self.addHistoryEvent(HistoryEvent)

        for itemsselected in selectedItems:
            id = self.dialog.listItem.model().index(itemsselected.row(),0).data()
            value = self.dialog.listItem.model().index(itemsselected.row(),1).data()
            table = self.dialog.listItem.model().index(itemsselected.row(),2).data()
            #print(id, value, table)
            newtreeitemdata['ItemTable'] = self.dialog.listItem.model().index(itemsselected.row(),3).data()
            newtreeitemdata['ItemTable_id'] = self.dialog.listItem.model().index(itemsselected.row(),2).data()
            newtreeitemdata['ItemName'] = self.dialog.listItem.model().index(itemsselected.row(),1).data()
            newtreeitemdata['Item_id'] = self.dialog.listItem.model().index(itemsselected.row(),0).data()

            newtreeitemdata['DisplayName'] = self.dialog.listItem.model().index(itemsselected.row(),1).data()
            #self.treeView.addTreeItem(self.treeitemdata)
            if itemcount != 1 or descriptorcount == 0:
                newtreeitemdata['DescriptorTable'] = None
                newtreeitemdata['DescriptorTable_id'] = 0
                newtreeitemdata['DescriptorName'] = None
                newtreeitemdata['Descriptor_id'] = 0

                #print(self.treeitemdata)
                self.treemodel.beginInsertRows(treeviewindex, 0, 0)
                treeid = self.treemodel.addTreeItem(TreeItems, newtreeitemdata)
                self.treemodel.endInsertRows()

                HistoryEvent = "Added Descriptor %s from table %s to %s" % (newtreeitemdata['ItemName'], newtreeitemdata['ItemTable'],treeGroup)
                self.addHistoryEvent(HistoryEvent)

        if itemcount == 1 and descriptorcount == 1:
            treeid = self.treemodel.addTreeItem(TreeItems, newtreeitemdata)

            newtreeitemdata['DisplayName'] = newtreeitemdata['DescriptorName'] + "(" + newtreeitemdata['ItemName'] + ")"
            HistoryEvent = "Added Descriptor %s (%s) from table %s (%s) to %s" % (newtreeitemdata['DescriptorName'],
                                                                                  newtreeitemdata['ItemName'],
                                                                                  newtreeitemdata['ItemTable'],
                                                                                  newtreeitemdata['DescriptorName'],treeGroup)
            self.addHistoryEvent(HistoryEvent)

        self.treemodel.layoutChanged.emit()

        #self.treemodel.endInsertRows()

        #self.dialog.treeView.reset()

        return treeid

    @QtCore.pyqtSlot()
    def on_cmdAddActivityCategory_clicked(self):
        MasterTable_id = 28
        Item_id = self.dialog.cmbActivityCategory.model().index(self.dialog.cmbActivityCategory.currentIndex(), 0).data()
        ParentTree_id = self.dialog.txtTreeItemID_2.text()
        self.AddEventItem(MasterTable_id, Item_id, ParentTree_id)

    def AddEventItem(self, MasterTable_id, Item_id, ParentTree_id=None):

        MasterTableData = tsession.query(ItemMasterTable).filter_by(id=MasterTable_id).first()

        print(MasterTableData.ReferenceTable)
        TableClass = DatabaseTools.get_class_by_tablename(bases[MasterTableData.ReferenceTablself.treedict["Session"]],
                                                          MasterTableData.ReferenceTable)
        listquery = sessions[MasterTableData.ReferenceTablself.treedict["Session"]].query(TableClass.id,
                                                                          TableClass.NameText).filter_by(
            id=Item_id).first()

        newtreeitemdata = self.ComputerGroupItemsmodel.defaultTreeItem()

        newtreeitemdata['ItemMasterTable'] = MasterTableData.NameText
        newtreeitemdata['ItemMaster_id'] = MasterTable_id

        newtreeitemdata['DisplayName'] = listquery.NameText
        newtreeitemdata['ItemName'] = listquery.NameText
        newtreeitemdata['Item_id'] = Item_id
        newtreeitemdata['ItemTableType_id'] = 0
        newtreeitemdata['ParentTree_id'] = "(0)"  # int(self.dialog.txtTreeItemID_2.text())
        newtreeitemdata['TreePath'] = strToMyList(self.dialog.txtTreePath_2.text())
        newtreeitemdata['Tags'] = strToMyList(self.dialog.txtTagPath_2.text())
        newtreeitemdata['id'] = None
        parenttreeid = 0  # int(self.dialog.txtTreeItemID.text())
        itemlevel = 0  # int(self.dialog.txtTreeItemLevel.text())
        currentIndex = self.dialog.tvComputerGroupItems.selectedIndexes()

        if ParentTree_id is None:
            print(listquery.NameText, currentIndex, 0, newtreeitemdata)

            ParentTree = self.ComputerGroupItemsmodel.AddTreeRoot(listquery.NameText, currentIndex, 0,
                                                                  newtreeitemdata,
                                                                  LinkedTable=self.tvtrackinggroupdict["TreeItems"])
        else:
            tableclass = self.tvtrackinggroupdict["TreeItems"]
            ParentTree = self.AddTreeTrackingItem(self.ComputerGroupItemsmodel, tableclass,
                                                  self.dialog.tvComputerGroupItems, ParentTree_id, newtreeitemdata,
                                                  itemlevel + 1)


            self.AddTreeTrackingItem(self.ComputerGroupItemsmodel, tableclass, self.dialog.tvComputerGroupItems,
                                     ParentTree, newtreeitemdata, itemlevel + 2)


        self.dialog.tvComputerGroupItems.expandToDepth(1)

    def AddTreeTrackingItem(self, treemodel, treeclass, treewidget, parenttreeid, newtreeitemdata, itemlevel):
        # 0 puts item on same level
        # 1 puts item on one level below (sub item)
        #todo: Some files like solidworks drawings dont show the extension in the tracker

        indexlist = treewidget.selectedIndexes()

        treeviewindex = None
        for index in indexlist:
            treeviewindex = index
        #newtreeitemdata['PrimaryGroup_id'] = 0
        #treeGroup = self.dialog.cmbPrimaryGroup.model().index(self.dialog.cmbPrimaryGroup.currentIndex(), 1, None).data()

        newtreeitemdata['ParentTree_id'] = parenttreeid
        newtreeitemdata['ItemLevel'] = itemlevel

        selecteditemtable = self.dialog.lstItemTables.selectedIndexes()
        selecteditemtablecount = len(selecteditemtable)

        newtreeitemdata['ItemTableType_id'] = self.dialog.cmbItemTableType.model().index(
            self.dialog.cmbItemTableType.currentIndex(), 0, None).data()
        newtreeitemdata['ItemTable'] = "Computer"
        newtreeitemdata['ItemTable_id'] = 4
        newtreeitemdata['id'] = None

        if treeviewindex is not None:
            treemodel.beginInsertRows(treeviewindex, 0, 0)
            treeid = treemodel.addTreeItem(treeclass, newtreeitemdata)
            treemodel.endInsertRows()
            self.addTreeTag(newtreeitemdata)
        else:
            treeid = treemodel.addTreeItem(treeclass, newtreeitemdata)

        return treeid

    @QtCore.pyqtSlot(int)
    def on_cmbMasterDescriptor_currentIndexChanged(self, index):
        pass

    @QtCore.pyqtSlot(int)
    def on_cmbMasterItem_currentIndexChanged(self, index):
        pass

    def on_treeView_DoubleClicked(self, index):
        print("Double Click!")

    def cell_was_clicked(self, index):
        #index is qmodelindex
        print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        print(self.treeData.data(index, Qt.UserRole))

    def cell_was_dblclicked(self, index):
        print("Row %d and Column %d was double clicked" % (index.row(), index.column()))
        print(self.treeData.data(index, Qt.UserRole))

    def cell_was_pressed(self, index):
        print("Row %d and Column %d was pressed" % (index.row(), index.column()))
        print(self.treeData.data(index, Qt.UserRole))

    def createItemTable(self, TreePath):
        if TreePath != None:
            #Tree Table

            #self.treeData = TreeViewAlchemy.sqlStandardItemModel(session=self.treedict["Session"], tableclass=TreeItems)
            #self.ItemTableTreeID = Tree_id
            #self.treeData.setupModelData()
            #print(self.datatable)

            self.tableData = QStandardItemModel(0, 2)
            sTreePath = myListToStr(TreePath)
            #print(sTreePath)
            record = self.treedict["Session"].query(self.treedict["GeneratedTree"]).filter(self.treedict["GeneratedTree"].TreePath==sTreePath).first()
            orecord = self.treedict["Session"].query(self.treedict["TreeItems"]).filter(self.treedict["TreeItems"].TreePath==sTreePath).first()

            #print(record)
            if record is not None:
                self.dialog.txtTableItemID.setText(str(record.id))
                self.dialog.txtPrimaryGroupID.setText(str(record.PrimaryGroup_id))
                self.dialog.txtSecondaryGroupID.setText(str(record.SecondaryGroup_id))

                self.dialog.txtTreeItemID.setText(str(record.Tree_id))
                self.dialog.txtTreeParentItemID.setText(str("-"))
                self.dialog.txtParentItemID.setText(str(record.ParentTree_id))
                self.dialog.txtTreeItemLevel.setText(str(record.ItemLevel))
                self.dialog.txtTreeItemOrder.setValue(int(record.ItemOrder))
                self.dialog.txtTreeItemMasterTable_2.setText(str(record.ItemMaster_id))
                self.dialog.txtTreeItem_id_2.setText(str(record.Item_id))
                self.dialog.txtTreeItemTable_id_3.setText(str(record.ItemTable_id))
                self.dialog.txtTreeTableType_id_2.setText(str(record.ItemTableType_id))
                self.dialog.txtTreePath.setText(str(record.TreePath))


             #self.dialog.txtTreePath_2.setText(str(record.TreePath))
                if record.Tags == "None":
                    self.dialog.txtTagPath.setText("")
                else:
                    pass
                    #@self.dialog.txtTagPath_2.setText(str(record.Tag))

                if self.dialog.cmbTreeSetting.model() is not None:
                    for row in range(self.dialog.cmbTreeSetting.model().rowCount()):
                        if int(self.dialog.cmbTreeSetting.model().index(row, 0, None).data()) == int(record.ItemTable_id):
                            self.dialog.cmbTreeSetting.setCurrentIndex(row)
                            break

                itemquery = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=record.ItemTable_id).first()
                #Newtable = DatabaseTools.get_class_by_tablename(bases(itemquery.Referencself.treedict["Session"]), itemquery.ReferenceTable)
                SessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=itemquery.Session).first()
                BaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=itemquery.Base).first()

                if itemquery is not None:
                    SQLString = itemquery.DisplayQuery
                    conn = sessions[SessionName.NameText].connection()
                    self.itemNames2 = QStandardItemModel(0, 3)
                    try:
                        rowcount = 0
                        for row, ItemName in enumerate(conn.execute(SQLString).fetchall()):
                            if ItemName[1] != "" and ItemName[1] != None:
                                rowcount += 1
                                itemID = QStandardItem("%i" % ItemName[0])
                                self.itemNames2.setItem(rowcount, 0, itemID)
                                self.itemNames2.setItem(rowcount, 1, QStandardItem(ItemName[1]))
                    except: pass
                    conn.close()

                    self.dialog.cmbTreeItem_id_2.setModel(self.itemNames2)
                    self.dialog.cmbTreeItem_id_2.setModelColumn(1)

                    if record.Item_id is not None:
                        for row in range(self.dialog.cmbTreeItem_id_2.model().rowCount()):
                            if self.dialog.cmbTreeItem_id_2.model().index(row, 0).data() is not None:
                                if int(self.dialog.cmbTreeItem_id_2.model().index(row, 0).data()) == int(record.Item_id):
                                    self.dialog.cmbTreeItem_id_2.setCurrentIndex(row)
                                    break

                if self.dialog.cmbTreeItemTable_id_3.model() is not None:
                    for row in range(self.dialog.cmbTreeItemTable_id_3.model().rowCount()):
                        if int(self.dialog.cmbTreeItemTable_id_3.model().index(row, 0, None).data()) == int(record.ItemTable_id):
                            self.dialog.cmbTreeItemTable_id_3.setCurrentIndex(row)
                            break

                if self.dialog.cmbTreeSetting.model() is not None:
                    for row in range(self.dialog.cmbTreeSetting.model().rowCount()):
                        if int(self.dialog.cmbTreeSetting.model().index(row, 0).data()) == int(record.ItemTableType_id):
                            self.dialog.cmbTreeSetting.setCurrentIndex(row)
                            break

                if self.dialog.cmbParentItemID_2.model() is not None:
                    for row in range(self.dialog.cmbParentItemID_2.model().rowCount()):
                        if int(self.dialog.cmbParentItemID_2.model().index(row, 0).data()) == int(record.ParentTree_id):
                            self.dialog.cmbParentItemID_2.setCurrentIndex(row)
                            break

                if record.ChartColor is not None:
                    self.dialog.cmdEventGroupColor_2.setStyleSheet("background-color:rgb(" + record.ChartColor + ")");
                else:
                    self.dialog.cmdEventGroupColor_2.setStyleSheet("background-color:rgb(" + str("0,0,0") + ")");
            else:
                self.dialog.txtTableItemID.setText("")
                self.dialog.txtTreeParentItemID.setText("")
                self.dialog.txtParentItemID.setText("")
                self.dialog.txtTreeItemLevel.setText("")
                self.dialog.txtTreeItemOrder.setValue(0)
                self.dialog.txtTreeItemMasterTable_2.setText("")
                self.dialog.txtTreeItem_id_2.setText("")
                self.dialog.txtTreeItemTable_id_3.setText("")
                self.dialog.txtTreeTableType_id_2.setText("")
                self.dialog.txtTreePath.setText("")
                self.dialog.txtTagPath.setText("")


            #TitleTag = "(%s-%s)" % (str(record.ItemTable_id), str(record.Item_id))

            if orecord:
                treelistcount = len(strToMyList(orecord.TreePath))

                TreeRecordCount = self.treedict["Session"].query(self.treedict["TreeItems"]).filter_by(TreePath=sTreePath).count()
                TreeTagList = strToMyList(orecord.Tags)

                if TreeRecordCount == 1:
                    self.dialog.txtDisplay.setEnabled(True)
                else:
                    self.dialog.txtDisplay.setEnabled(False)

                #self.dialog.lstDisplayTags.setModel(None)
                tagmodel = QStandardItemModel(0, 4)
                for row, tagitem in enumerate(TreeTagList[treelistcount-1:]):
                    tagdata = self.MasterData.getTagInfo(tagitem)
                    tagmodel.setItem(row, 0, QStandardItem(tagitem))
                    tagmodel.setItem(row, 1, QStandardItem(tagdata[1]))

                self.dialog.lstDisplayTags.setModel(tagmodel)
                self.dialog.lstDisplayTags.setModelColumn(1)
                self.dialog.txtDisplay.setText(str(orecord.DisplayName))
                self.dialog.txtTagPath.setText(str(orecord.Tags))
            else:
                self.dialog.txtDisplay.setText(str(record.DisplayName))
                self.dialog.txtTagPath.setText(str(record.Tags))
            #self.dialog.tblItemInformation.setModel(self.tableData)
            self.dialog.tblItemInformation.setColumnWidth(0,100)
            self.dialog.tblItemInformation.setColumnWidth(1,100)

            self.dialog.tblItemInformation.clicked.connect(self.cell_was_clicked2)
            self.dialog.tblItemInformation.pressed.connect(self.cell_was_pressed2)

   #@pyqtSlot()
    def on_txtDisplay_textEdited(self):

        txttreepath = self.dialog.txtTreePath.text()
        TreeRecord = self.treedict["Session"].query(self.treedict["TreeItems"]).filter_by(TreePath=txttreepath).first()
        if TreeRecord:
            self.treedict["Session"].begin()
            TreeRecord.DisplayName = self.dialog.txtDisplay.text()
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()
        
    def cell_was_clicked2(self, index):
        #index is qmodelindex
        #print("Row %d and Column %d was clicked" % (index.row(), index.column()))
        #print(self.tableData.data(index, Qt.UserRole))
        print(self.tblItemInformation.model().index(index.row(),0).data())
        print(self.tblItemInformation.model().index(index.row(),1).data())
        self.dialog.txtTreeItemLabel.setText(self.tblItemInformation.model().index(index.row(),0).data())
        self.dialog.txtTreeItemValue.setText(self.tblItemInformation.model().index(index.row(),1).data())

    def cell_was_pressed2(self, index):
        #print("Row %d and Column %d was pressed" % (index.row(), index.column()))
        #print(self.tableData.data(index, Qt.UserRole))

        SQLWhere = " WHERE \"TreeID\" = %i" % self.ItemTableTreeID
        #conn = DatabaseConnect.dbConnect(self.fileLocation)
        #cursor = conn.cursor()
        #strSQL = self.SQLSelect + self.SQLFrom + SQLWhere
        #cursor.execute(strSQL)

        #self.tableData = QStandardItemModel(0, 2)
        #record = cursor.fetchone()

        recordrow = 0
        #index2 = self.tblItemInformation.model().index(index.row(),1)
        #print(self.tblItemInformation.model().index(index.row(),1).data())
        #print(self.tblItemInformation.model().index(index.row(),2).data())
        #self.dialog.txtTreeItemLabel = self.tblItemInformation.model().index(index.row(),1).data()
        #self.dialog.txtTreeItemValue = self.tblItemInformation.model().index(index.row(),2).data()

    #@QtCore.pyqtSlot(int)
    def on_rdoInternal_toggled(self, index):
        self.loadLinkToggle()

    #@QtCore.pyqtSlot(int)
    def on_rdoExternal_toggled(self, index):
        self.loadLinkToggle()

    def loadLinkToggle(self):
        if self.dialog.rdoExternal.isChecked():
            self.dialog.cmbDestinationSession.setVisible(True)
            self.dialog.lblDestinationSession.show()
            self.dialog.lblDestinationTable.show()
            self.dialog.cmbDestinationTable.setVisible(True)

            self.dialog.txtTBLocal.setVisible(False)
            self.dialog.cmbPrimaryGroup_2.setVisible(True)

            qrysessionlist = self.treedict["MasterSession"].query(SessionNames.id, SessionNames.NameText, literal_column(str("242"))) #139
            self.dialog.cmbDestinationSession.setModel(QueryTableModel(qrysessionlist))
            self.dialog.cmbDestinationSession.model().reset_content_from_session()
            self.dialog.cmbDestinationSession.setModelColumn(1)
            self.dialog.cmbDestinationSession.currentIndexChanged.connect(self.on_cmbDestinationSession_currentIndexChanged)

            self.exportprimarykey = self.dialog.cmbPrimaryGroup.model().index(
                self.dialog.cmbPrimaryGroup.currentIndex(), 0, None).data()

        else:

            qrytreegroup = self.treedict["Session"].query(self.treedict["PrimaryGroup"].id,
                                                          self.treedict["PrimaryGroup"].NameText)

            self.dialog.cmbPrimaryGroup_3.setModel(QueryTableModel(qrytreegroup))
            self.dialog.cmbPrimaryGroup_3.model().reset_content_from_session()
            self.dialog.cmbPrimaryGroup_3.setModelColumn(1)

            self.dialog.cmbDestinationSession.setVisible(False)
            self.dialog.cmbDestinationTable.setVisible(False)
            self.dialog.lblDestinationSession.hide()
            self.dialog.lblDestinationTable.hide()
            self.dialog.txtTBLocal.setVisible(True)
            self.dialog.cmbPrimaryGroup_2.setVisible(False)

    #@QtCore.pyqtSlot(int)
    def on_cmbDestinationSession_currentIndexChanged(self, index):
        DestinationSession_id = self.dialog.cmbDestinationSession.model().index(index, 0).data()
        self.loadDestinationData(DestinationSession_id)

    def loadDestinationData(self, DestinationSession_id):
        SQLUnion = ""
        conn = self.treedict["MasterSession"].connection()

        SQLSelect = "SELECT id, NameText"
        SQLFrom = " FROM ItemTable"
        SQLOrder = " ORDER BY NameText"

        SQLUnion = ""

        #SQLSelect = "SELECT id, TableName, TableName, %i, Session, DisplayColumn" % (int(ItemMasterTable))
        #SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s UNION " % ("NameText", 253, "mastertable", 1, "mastertable")
        SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s WHERE session = %i UNION " % ("TableName", 253, "mastertable", DestinationSession_id, "mastertable", DestinationSession_id)

        strSQL = SQLUnion.rstrip('UNION ')

        #if len(strSQL) != 0:
         #   strSQL += " ORDER BY NameText"

        self.sessionitemNames = QStandardItemModel(0, 4)
        try:
            rowcount = 0
            for row, ItemName in enumerate(conn.execute(strSQL).fetchall()):
                if ItemName[1] != "" and ItemName[1] != None:
                    rowcount += 1
                    #print(ItemName[1])
                    Item_id = QStandardItem("%i" % ItemName[0])
                    ItemTable_id = QStandardItem("%i" % ItemName[2])
                    MasterTable_id = QStandardItem("%i" % ItemName[4])

                    self.sessionitemNames.setItem(rowcount, 0, Item_id)
                    self.sessionitemNames.setItem(rowcount, 1, QStandardItem(ItemName[1]))
                    self.sessionitemNames.setItem(rowcount, 2, ItemTable_id)
                    self.sessionitemNames.setItem(rowcount, 3, QStandardItem(ItemName[3]))
                    self.sessionitemNames.setItem(rowcount, 4, MasterTable_id)
            conn.close()

        except:
            print("No Records Found")

        self.dialog.cmbPrimaryGroup_2.setModel(self.sessionitemNames)
        self.dialog.cmbPrimaryGroup_2.setModelColumn(1)

        self.destinationProxyModel = QSortFilterProxyModel(self.dialog.cmbDestinationTable)
        self.destinationProxyModel.setSourceModel(self.sessionitemNames)
        self.dialog.cmbDestinationTable.setModel(self.destinationProxyModel)

        #self.dialog.cmbDestinationTable.setModel(self.sessionitemNames)
        self.dialog.cmbDestinationTable.setModelColumn(1)
        
        self.destinationProxyModel.setFilterKeyColumn(1)
        search = QRegularExpression("*%s*" % str("tree"),
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.destinationProxyModel.setFilterRegExp(search)

    #@QtCore.pyqtSlot(int)
    def on_cmbPrimaryGroup_2_currentIndexChanged(self, index):

        if self.dialog.rdoExternal.isChecked():
            DestinationSession_id = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            DestinationSession_id2 = self.dialog.cmbPrimaryGroup_2.model().index(index, 0).data()

            if DestinationSession_id:
                destinationquery = self.treedict["MasterSession"].query(MasterTable).filter_by(id=int(DestinationSession_id)).first()
                # Newtable = DatabaseTools.get_class_by_tablename(bases(itemquery.Referencself.treedict["Session"]), itemquery.ReferenceTable)
                destinationSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=destinationquery.Session).first()
                destinationBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=destinationquery.Base).first()

                mastertable_id = int(DestinationSession_id)

                conn = self.treedict["MasterSession"].connection()
                sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
                self.selectedTableModel = QStandardItemModel(0, 2)

                query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(mastertable_id)).first()
                query2 = self.treedict["MasterSession"].query(sessionbase1).filter_by(id=int(query1.Session)).first()

                displayquery = query1.DisplayQuery
                conn2 = self.sessionlist[query2.NameText].connection()
                records = conn2.execute(displayquery).fetchall()

                if records != []:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name = QStandardItem(ItemName[1])

                        self.selectedTableModel.setItem(row, 0, Descriptor_id)
                        self.selectedTableModel.setItem(row, 1, Descriptor_Name)

                conn2.close()

                self.dialog.cmbPrimaryGroup_3.setModel(self.selectedTableModel)
                self.dialog.cmbPrimaryGroup_3.setModelColumn(1)

                conn.close()

            else:
                pass


    #@QtCore.pyqtSlot(int)
    def on_tblActivityGroups_clicked(self):
        pass

    #@QtCore.pyqtSlot()
    def on_cmdRemoveBranch_clicked(self):
        pass

    #@QtCore.pyqtSlot()
    def on_cmdCreateBranch_clicked(self):
        sourcetable = self.treedict["MasterTable_id"]

        if self.dialog.rdoExternal.isChecked():
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data()
            destinationtable = self.dialog.cmbDestinationTable.model().index(self.dialog.cmbDestinationTable.currentIndex(), 0).data()
        else:
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data()
            destinationtable = sourcetable
        Tags = self.dialog.txtTBTags.text()

        self.treedict["Session"].begin()
        NewBB = self.treedict["TreeBuilder"](PrimaryGroupTable_id=exportprimarytable,
                                             Description=self.dialog.txtTBDescription.text(),
                                             PrimaryGroup_id=exportprimarykey,
                                             SourceTable_id=sourcetable,
                                             DestinationTable_id=destinationtable,
                                             Tags=Tags)
        self.treedict["Session"].add(NewBB)
        self.treedict["Session"].commit()
        self.treedict["Session"].flush()

        self.loadBBTable()

    #@QtCore.pyqtSlot()
    def on_cmdCreateBranch_2_clicked(self):
        sourcetable = self.treedict["MasterTable_id"]

        if self.dialog.rdoExternal.isChecked():
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(
                self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(),
                                                                           0).data()
            destinationtable = self.dialog.cmbDestinationTable.model().index(
                self.dialog.cmbDestinationTable.currentIndex(), 0).data()
        else:
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(
                self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(),
                                                                           0).data()
            destinationtable = sourcetable

        record_id = self.dialog.txtTBRecord.text()
        sourcequery = self.treedict["MasterSession"].query(MasterTable).filter_by(
            id=self.treedict["MasterTable_id"]).first()
        sourceSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=sourcequery.Session).first()
        sourceBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=sourcequery.Base).first()
        sourcetable = DatabaseTools.get_class_by_tablename(bases[sourceSessionName.NameText], sourcequery.TableName)

        destinationquery = self.treedict["MasterSession"].query(MasterTable).filter_by(id=int(destinationtable)).first()

        destinationSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(
            id=destinationquery.Session).first()
        destinationBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(
            id=destinationquery.Base).first()
        destinationtable = DatabaseTools.get_class_by_tablename(bases[destinationSessionName.NameText],
                                                                destinationquery.TableName)

        OTree_id = self.dialog.txtTableItemID.text()
        OTree_id = self.dialog.txtTreeItemID.text()

        if destinationtable:
            itemcount = sessions[destinationSessionName.NameText].query(destinationtable).filter_by(
                PrimaryGroup_id=exportprimarykey, ParentTree_id="(0)").count()
            Secondary_id = self.treedict["Session"].query(self.treedict["SecondaryGroup"]).filter_by(
                PrimaryGroup_id=exportprimarykey).count()
            # sourceid = "(%s-%s-%s-%s)" % (newtreeitemdata['SourcePG'], newtreeitemdata['SourceSG'], SourceTable_id, itemlistdata["id"])
            NameText = ("%s-%s") % (exportprimarykey, Secondary_id + 1)

            self.treedict["Session"].begin()
            NewSecondaryGroup = self.treedict["SecondaryGroup"](NameText=NameText, PrimaryGroup_id=exportprimarykey,
                                                                SecondaryGroup_id=Secondary_id + 1)
            self.treedict["Session"].add(NewSecondaryGroup)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()

            TreeViewAlchemy2.clonebranch(sessions[sourceSessionName.NameText], sourcetable, OTree_id,
                                         sessions[destinationSessionName.NameText], destinationtable, "(0)",
                                         DPG_id=exportprimarykey, DSG_id=Secondary_id + 1)

            sourceparentitem = sessions[sourceSessionName.NameText].query(sourcetable).filter_by(
                Tree_id=OTree_id).first()

            TagList = sourceparentitem.Tags.split(" ")[-1]

            NameCount = sessions[destinationSessionName.NameText].query(destinationtable).filter_by(
                PrimaryGroup_id=exportprimarykey, ParentTree_id="(0)", Tags=TagList).count()

            NewName = ("%s - %s") % (sourceparentitem.DisplayName, str(NameCount))

            self.treedict["Session"].begin()
            NewSecondaryGroup.NameText = NewName
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()
        else:
            print("Table Not Found, check title case")

    #@QtCore.pyqtSlot()
    def on_cmdCreateFullBranch_clicked(self):

        if self.dialog.rdoExternal.isChecked():
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = int(self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data())
            destinationtable = self.dialog.cmbDestinationTable.model().index(self.dialog.cmbDestinationTable.currentIndex(), 0).data()
        else:
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(
                self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = int(self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data())
            destinationtable = self.treedict["MasterTable_id"]

        record_id = self.dialog.txtTBRecord.text()
        sourcequery = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=self.treedict["MasterTable_id"]).first()
        sourceSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=sourcequery.Session).first()
        sourceBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=sourcequery.Base).first()
        sourcetable = DatabaseTools.get_class_by_tablename(bases[sourceSessionName.NameText], sourcequery.TableName)

        destinationquery = self.treedict["MasterSession"].query(MasterTable).filter_by(id=int(destinationtable)).first()

        destinationSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=destinationquery.Session).first()
        destinationBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=destinationquery.Base).first()
        destinationtable = DatabaseTools.get_class_by_tablename(bases[destinationSessionName.NameText],destinationquery.TableName)

        OTree_id1 = self.dialog.txtTableItemID.text()
        OTree_id = self.dialog.txtTreeItemID.text()

        if destinationtable:
            itemcount = sessions[destinationSessionName.NameText].query(destinationtable).filter_by(PrimaryGroup_id=exportprimarykey, ParentTree_id="(0)").count()
            Secondary_id = self.treedict["Session"].query(self.treedict["SecondaryGroup"]).filter_by(PrimaryGroup_id=exportprimarykey).count()
            # sourceid = "(%s-%s-%s-%s)" % (newtreeitemdata['SourcePG'], newtreeitemdata['SourceSG'], SourceTable_id, itemlistdata["id"])
            NameText = ("%s-%s") % (exportprimarykey, Secondary_id + 1)

            self.treedict["Session"].begin()
            NewSecondaryGroup = self.treedict["SecondaryGroup"](NameText=NameText, PrimaryGroup_id=exportprimarykey, SecondaryGroup_id=Secondary_id + 1)
            self.treedict["Session"].add(NewSecondaryGroup)
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()

            #parentstuff = SParent_id[1:-1]
            #parentstufflist = parentstuff.split("-")  # last item, remove brackets split by the -

            sourceparentitem = sessions[sourceSessionName.NameText].query(sourcetable).filter_by(Tree_id=OTree_id).first()

            TreeViewAlchemy2.clonefullbranch(self.treedict, bases, sessions, sessions[sourceSessionName.NameText], sourcetable, OTree_id, sourceparentitem.PrimaryGroup_id, sourceparentitem.SecondaryGroup_id, sessions[destinationSessionName.NameText], destinationtable, "(0)", exportprimarykey, Secondary_id + 1)

            TagList = sourceparentitem.Tags.split(" ")[-1]

            NameCount = sessions[destinationSessionName.NameText].query(destinationtable).filter_by(PrimaryGroup_id=exportprimarykey, ParentTree_id="(0)", Tags=TagList).count()

            NewName = ("%s - %s") % (sourceparentitem.DisplayName, str(NameCount))

            self.treedict["Session"].begin()
            NewSecondaryGroup.NameText = NewName
            self.treedict["Session"].commit()
            self.treedict["Session"].flush()
        else:
            print("Table Not Found, check title case")

    #@QtCore.pyqtSlot()
    def on_cmdSaveBranch_clicked(self):
        sourcetable = self.treedict["MasterTable_id"]

        if self.dialog.rdoExternal.isChecked():
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data()
            destinationtable = self.dialog.cmbDestinationTable.model().index(self.dialog.cmbDestinationTable.currentIndex(), 0).data()
        else:
            exportprimarytable = self.dialog.cmbPrimaryGroup_2.model().index(self.dialog.cmbPrimaryGroup_2.currentIndex(), 0).data()
            exportprimarykey = self.dialog.cmbPrimaryGroup_3.model().index(self.dialog.cmbPrimaryGroup_3.currentIndex(), 0).data()
            destinationtable = sourcetable
        Tags = self.dialog.txtTBTags.text()

        record_id = self.dialog.txtTBRecord.text()

        if record_id:
            NewBB = self.treedict["Session"].query(self.treedict["TreeBuilder"]).filter_by(id=int(record_id)).first()

            self.treedict["Session"].begin()
            NewBB.PrimaryGroupTable_id=exportprimarytable
            NewBB.Description=self.dialog.txtTBDescription.text()
            NewBB.PrimaryGroup_id=exportprimarykey
            NewBB.SourceTable_id=sourcetable
            NewBB.DestinationTable_id=destinationtable
            NewBB.Tags=Tags

            self.treedict["Session"].add(NewBB)
            self.treedict["Session"].commit()

            self.loadBBTable()
        else:
            print("Nothing Selected")


    def loadBBTable(self):
        BBList = self.treedict["Session"].query(self.treedict["TreeBuilder"]).all()
        sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
        #exportprimarytable

        self.ProjectListModel = QStandardItemModel(0, 4)
        if BBList:
            for row, BBItem in enumerate(BBList):
                Item_id = QStandardItem("%i" % BBItem.id)
                self.ProjectListModel.setItem(row, 0, Item_id)

                if BBItem.SourceTable_id == BBItem.DestinationTable_id:
                    self.ProjectListModel.setItem(row, 1, QStandardItem("Internal"))
                    self.ProjectListModel.setItem(row, 2, QStandardItem(BBItem.Description))
                    query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(BBItem.SourceTable_id)).first()
                    self.ProjectListModel.setItem(row, 3, QStandardItem(query1.TableName))
                    query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(BBItem.DestinationTable_id)).first()
                    self.ProjectListModel.setItem(row, 4, QStandardItem(query1.TableName))
                    query1 = self.treedict["Session"].query(self.treedict["PrimaryGroup"]).filter_by(id=int(BBItem.PrimaryGroup_id)).first()
                    self.ProjectListModel.setItem(row, 5, QStandardItem(query1.NameText))
                    self.ProjectListModel.setItem(row, 6, QStandardItem(BBItem.Tags))
                else:
                    self.ProjectListModel.setItem(row, 1, QStandardItem("External"))
                    self.ProjectListModel.setItem(row, 2, QStandardItem(BBItem.Description))
                    if BBItem.SourceTable_id is not None:
                        query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(BBItem.SourceTable_id)).first()
                        self.ProjectListModel.setItem(row, 3, QStandardItem(query1.TableName))
                    if BBItem.DestinationTable_id is not None:
                        query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(BBItem.DestinationTable_id)).first()
                        self.ProjectListModel.setItem(row, 4, QStandardItem(query1.TableName))

                    if BBItem.PrimaryGroup_id is not None:
                        query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id=int(BBItem.PrimaryGroup_id)).first()
                        self.ProjectListModel.setItem(row, 5, QStandardItem(query1.TableName))

                    self.ProjectListModel.setItem(row, 6, QStandardItem(BBItem.Tags))

        self.ProjectListModel.setHeaderData(0, Qt.Horizontal, 'ID', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(1, Qt.Horizontal, 'Location', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(2, Qt.Horizontal, 'Description', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(3, Qt.Horizontal, 'Source Table', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(4, Qt.Horizontal, 'Destination Table', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(5, Qt.Horizontal, 'Primary Group', role=Qt.DisplayRole)
        self.ProjectListModel.setHeaderData(6, Qt.Horizontal, 'Tags', role=Qt.DisplayRole)

        #
        self.sessionitemModelproxy = QSortFilterProxyModel()
        self.sessionitemModelproxy.setSourceModel(self.ProjectListModel)
        self.dialog.tblBranchCreator.setModel(self.sessionitemModelproxy)
        #self.dialog.tblBranchCreator.setModel(self.ProjectListModel)
        self.dialog.listItem.setModelColumn(1)

    def on_tblBranchCreator_clicked(self, index):
        data = {}
        data["row"] = self.dialog.tblBranchCreator.selectionModel().currentIndex().row()
        data["column"] = self.dialog.tblBranchCreator.selectionModel().currentIndex().column()
        data["Value"] = self.dialog.tblBranchCreator.model().index(data["row"], data["column"]).data()
        data["id"] = self.dialog.tblBranchCreator.model().index(data["row"], 0).data()
        self.dialog.txtTBRecord.setText(str(data["id"]))
        BBItem = self.treedict["Session"].query(self.treedict["TreeBuilder"]).filter_by(id = data["id"]).first()
        destinationquery = None

        if BBItem.SourceTable_id == BBItem.DestinationTable_id:
            self.dialog.rdoInternal.setChecked(True)
        else:
            self.dialog.rdoExternal.setChecked(True)
            if BBItem and BBItem.DestinationTable_id:
                destinationquery = self.treedict["MasterSession"].query(MasterTable).filter_by(id=int(BBItem.DestinationTable_id)).first()
                # Newtable = DatabaseTools.get_class_by_tablename(bases(itemquery.Referencself.treedict["Session"]), itemquery.ReferenceTable)
                destinationSessionName = self.treedict["MasterSession"].query(SessionNames).filter_by(id=destinationquery.Session).first()
                destinationBaseName = self.treedict["MasterSession"].query(SessionBase).filter_by(id=destinationquery.Base).first()
                self.loadDestinationData(destinationquery.Session)

        self.dialog.txtTBDescription.setText(BBItem.Description)

        if destinationquery:
            for row in range(self.dialog.cmbDestinationSession.model().rowCount(None)):
               if self.dialog.cmbDestinationSession.model().index(row, 0, None).data() == int(destinationquery.Session):
                    self.dialog.cmbDestinationSession.setCurrentIndex(row)
                    break

        if BBItem.PrimaryGroupTable_id:
            for row in range(self.dialog.cmbPrimaryGroup_2.model().rowCount()):
                if self.dialog.cmbPrimaryGroup_2.model().index(row, 0).data() is not None:
                    numb = self.dialog.cmbPrimaryGroup_2.model().index(row, 0).data()
                    if int(self.dialog.cmbPrimaryGroup_2.model().index(row, 0).data()) == int(BBItem.PrimaryGroupTable_id):
                        self.dialog.cmbPrimaryGroup_2.setCurrentIndex(row)
                        break

        if BBItem.PrimaryGroup_id:
            for row in range(self.dialog.cmbPrimaryGroup_3.model().rowCount()):
                if self.dialog.cmbPrimaryGroup_3.model().index(row, 0).data() == int(BBItem.PrimaryGroup_id):
                    self.dialog.cmbPrimaryGroup_3.setCurrentIndex(row)
                    break

        if BBItem.DestinationTable_id:
            for row in range(self.dialog.cmbDestinationTable.model().rowCount()):
                if self.dialog.cmbDestinationTable.model().index(row, 0).data() is not None:
                    if int(self.dialog.cmbDestinationTable.model().index(row, 0).data()) == int(BBItem.DestinationTable_id):
                        self.dialog.cmbDestinationTable.setCurrentIndex(row)
                        break

        self.dialog.txtTBTags.setText(BBItem.Tags)

    def loadSessionList(self):

        SQLUnion = ""
        conn = self.treedict["MasterSession"].connection()

        SQLSelect = "SELECT id, NameText"
        SQLFrom = " FROM ItemTable"
        SQLOrder = " ORDER BY NameText"

        SQLUnion = ""

        selectedItems = self.dialog.lstMasterTableSession.selectedIndexes()

        for itemsselected in selectedItems:
            Session_id = self.dialog.lstMasterTableSession.model().index(itemsselected.row(), 0, None).data()
            #SQLSelect = "SELECT id, TableName, TableName, %i, Session, DisplayColumn" % (int(ItemMasterTable))
            #SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s UNION " % ("NameText", 253, "mastertable", 1, "mastertable")
            SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s WHERE session = %i UNION " % ("TableName", 253, "mastertable", Session_id, "mastertable", Session_id)

        strSQL = SQLUnion.rstrip('UNION ')

        #if len(strSQL) != 0:
         #   strSQL += " ORDER BY NameText"

        self.sessionitemNames = QStandardItemModel(0, 4)
        try:
            rowcount = 0
            for row, ItemName in enumerate(conn.execute(strSQL).fetchall()):
                if ItemName[1] != "" and ItemName[1] != None:
                    rowcount += 1
                    #print(ItemName[1])
                    Item_id = QStandardItem("%i" % ItemName[0])
                    ItemTable_id = QStandardItem("%i" % ItemName[2])
                    MasterTable_id = QStandardItem("%i" % ItemName[4])

                    self.sessionitemNames.setItem(rowcount, 0, Item_id)
                    self.sessionitemNames.setItem(rowcount, 1, QStandardItem(ItemName[1]))
                    self.sessionitemNames.setItem(rowcount, 2, ItemTable_id)
                    self.sessionitemNames.setItem(rowcount, 3, QStandardItem(ItemName[3]))
                    self.sessionitemNames.setItem(rowcount, 4, MasterTable_id)
            conn.close()

        except:
            print("No Records Found")

        #self.dialog.listItem.setModelColumn(1)
        self.sessionitemModelproxy = QSortFilterProxyModel()
        self.sessionitemModelproxy.setSourceModel(self.sessionitemNames)
        self.dialog.lstMasterTableItems.setModel(self.sessionitemModelproxy)
        #self.dialog.lstMasterTableItems.setModel(self.sessionitemNames)
        self.dialog.lstMasterTableItems.setModelColumn(1)

    def loadDescriptor(self):
        #This will load all the tables types that are selected and then apply the filter
        #http://stackoverflow.com/questions/14546913/how-to-get-item-selected-from-qlistview-in-pyqt
        conn = self.treedict["MasterSession"].connection()
        sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
        self.descriptorModel = QStandardItemModel(0, 2)
        itemsadded = 0

        selectedItems = self.dialog.lstDescriptorTypes.selectedIndexes()
        for itemsselected in selectedItems:
            ItemID = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 0, None).data()
            ItemName = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 1, None).data()
            ItemMasterTable = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 2, None).data()

            if DatabaseConnect.sqlAttackCheck(self, itemsselected.data()):
                query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(id = int(ItemMasterTable)).first()
                query2 = self.treedict["MasterSession"].query(sessionbase1).filter_by(id=int(query1.Session)).first()

                displayquery = query1.DisplayQuery
                conn2 = self.sessionlist[query2.NameText].connection()
                records = conn2.execute(displayquery).fetchall()

                if records is not None:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name =  QStandardItem(ItemName[1])
                        MasterTable_id = QStandardItem("%i" % ItemMasterTable)
                        Table_Name = QStandardItem(query1.TableName)
                        Session_Name = QStandardItem(query1.TableName)

                        itemsadded += 1
                        self.descriptorModel.setItem(itemsadded, 0, Descriptor_id)
                        self.descriptorModel.setItem(itemsadded, 1, Descriptor_Name)
                        self.descriptorModel.setItem(itemsadded, 2, MasterTable_id)
                        self.descriptorModel.setItem(itemsadded, 3, Table_Name)
                        self.descriptorModel.setItem(itemsadded, 4, Session_Name)

                conn2.close()

            #self.dialog.lstDescriptors.setModel(self.descriptorModel)

            self.descriptorModelproxy.setSourceModel(self.descriptorModel)
            self.dialog.lstDescriptors.setModel(self.descriptorModelproxy)
            self.dialog.lstDescriptors.setModelColumn(1)

        conn.close()

    def loadItems(self):
        #This will load all the tables types that are selected and then apply the filter
        #http://stackoverflow.com/questions/14546913/how-to-get-item-selected-from-qlistview-in-pyqt

        conn = self.treedict["MasterSession"].connection()
        sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
        self.itemNames = QStandardItemModel(0, 2)
        itemsadded = 0

        selectedItems = self.dialog.listItemTypes.selectedIndexes()
        for itemsselected in selectedItems:
            ItemID = self.dialog.listItemTypes.model().index(itemsselected.row(), 0, None).data()
            ItemName = self.dialog.listItemTypes.model().index(itemsselected.row(), 1, None).data()
            ItemMasterTable = self.dialog.listItemTypes.model().index(itemsselected.row(), 2, None).data()

            if DatabaseConnect.sqlAttackCheck(self, itemsselected.data()):
                query1 = self.treedict["MasterSession"].query(self.treedict["MasterTable"]).filter_by(
                    id=int(ItemMasterTable)).first()
                query2 = self.treedict["MasterSession"].query(sessionbase1).filter_by(
                    id=int(query1.Session)).first()

                displayquery = query1.DisplayQuery
                conn2 = self.sessionlist[query2.NameText].connection()
                if displayquery is not None:
                    records = conn2.execute(displayquery).fetchall()

                    if records is not None:
                        for row, ItemName in enumerate(records):
                            Item_id = QStandardItem("%i" % ItemName[0])
                            Item_Name = QStandardItem(ItemName[1])
                            MasterTable_id = QStandardItem("%i" % ItemMasterTable)
                            Table_Name = QStandardItem(query1.TableName)
                            Session_Name = QStandardItem(query1.TableName)

                            itemsadded += 1
                            self.itemNames.setItem(itemsadded, 0, Item_id)
                            self.itemNames.setItem(itemsadded, 1, Item_Name)
                            self.itemNames.setItem(itemsadded, 2, MasterTable_id)
                            self.itemNames.setItem(itemsadded, 3, Table_Name)
                            self.itemNames.setItem(itemsadded, 4, Session_Name)

                        self.itemModelproxy.setSourceModel(self.itemNames)
                        self.dialog.listItem.setModel(self.itemModelproxy)
                        self.dialog.listItem.setModelColumn(1)

                conn2.close()
        conn.close()

    def loadDescriptorTypes(self, RecordCount = 0):
        Master = self.dialog.cmbTreeSettings.model().index(self.dialog.cmbTreeSettings.currentIndex(), 0, None).data()
        recordquery = self.treedict["Session"].query(self.treedict["DescriptorTable"].id, self.treedict["DescriptorTable"].NameText, self.treedict["DescriptorTable"].MasterTable_id).filter_by(MTTT_id=Master)

        self.dialog.lstDescriptorTypes.setModel(QueryTableModel(recordquery))
        self.dialog.lstDescriptorTypes.model().reset_content_from_session()
        self.dialog.lstDescriptorTypes.setModelColumn(1)

        self.dialog.lstDescriptorTypes.selectionModel().selectionChanged.connect(self.loadDescriptor)

    def loadItemTypes(self, recordcount=0):
        Master = self.dialog.cmbTreeSettings.model().index(self.dialog.cmbTreeSettings.currentIndex(), 0, None).data()
        recordquery = self.treedict["Session"].query(self.treedict["ItemTable"].id, self.treedict["ItemTable"].NameText, self.treedict["ItemTable"].MasterTable_id).filter_by(MTTT_id=Master)

        self.dialog.listItemTypes.setModel(QueryTableModel(recordquery))
        self.dialog.listItemTypes.model().reset_content_from_session()
        self.dialog.listItemTypes.setModelColumn(1)

        self.dialog.listItemTypes.selectionModel().selectionChanged.connect(self.loadItems)

    def loadtreelist(self):
        #self.dialog.txtLoadTreeView.addItem(self.fileLocation)
        conn2 = DatabaseConnect.dbConnect(self.fileLocation)

        cmbLoadTreeView = self.dialog.txtLoadTreeView.currentIndex()
        FileLocationID = self.txtLoadTreeView.model().index(cmbLoadTreeView, 0).data()

        SQLSelect = "SELECT treeGroup.id," \
                    "treeGroup.name," \
                    "treeGroup.fileLocation," \
                    "treeGroup.DescriptorMaster AS DescriptorMaster_id," \
                    "treeGroup.ItemMaster AS ItemMaster_id," \
                    "DescriptorMasterTable.name AS DescriptorMasterTable," \
                    "ItemMasterTable.name AS ItemMasterTable"
        SQLFrom = " FROM treeGroup" \
                  " LEFT JOIN DescriptorMasterTable ON (treeGroup.DescriptorMaster = DescriptorMasterTable.id)" \
                  " LEFT JOIN ItemMasterTable ON (treeGroup.ItemMaster = ItemMasterTable.id)"
        SQLWhere = " WHERE treeGroup.fileLocation = %s" % (FileLocationID)
        SQLOrder = " ORDER BY treeGroup.name"

        strSQL = SQLSelect + SQLFrom + SQLWhere + SQLOrder

        cursor = conn2.cursor()
        cursor.execute(strSQL)

        self.treeModel = QStandardItemModel(0, 6)

        for row, ItemName in enumerate(cursor.fetchall()):
            #print(ItemName[0],ItemName[1],ItemName[2],ItemName[3],ItemName[4],ItemName[5],ItemName[6])
            itemID = QStandardItem("%i" % ItemName[0])
            #typeID.setTextAlignment( Qt.AlignCenter )
            self.treeModel.setItem(row, 0, itemID)
            self.treeModel.setItem(row, 1, QStandardItem(ItemName[1]))
            self.treeModel.setItem(row, 2, QStandardItem(ItemName[2]))
            self.treeModel.setItem(row, 3, QStandardItem(ItemName[3]))
            self.treeModel.setItem(row, 4, QStandardItem(ItemName[4]))
            self.treeModel.setItem(row, 5, QStandardItem(ItemName[5]))
            self.treeModel.setItem(row, 6, QStandardItem(ItemName[6]))

        self.dialog.cmbPrimaryGroup.setModel(self.treeModel)
        self.dialog.cmbPrimaryGroup.setModelColumn(1)

        cursor.close()
        conn2.close()

    @QtCore.pyqtSlot()
    def on_cmdCloneBranch_clicked(self):
        OSession = self.treedict["Session"]
        OTree = EquipmentTree
        OTree_id = self.dialog.txtTreeItemID.model().index(self.dialog.txtTreeItemID.currentIndex,0).data()
        DSession = self.treedict["Session"]
        DModel = None
        DTree = EquipmentComponents
        DTree_id = 0

        DatabaseTools.clonebranch(OSession, OTree, OTree_id, DSession, DModel, DTree, DTree_id)

    @QtCore.pyqtSlot(int)
    def on_cmbTreeSetting_currentIndexChanged(self, index):
        ItemMaster_id = self.dialog.cmbTreeSetting.model().index(index, 0, None).data()
        itemquery = self.treedict["Session"].query(MasterTable).filter_by(id=ItemMaster_id).first()
        # Newtable = DatabaseTools.get_class_by_tablename(bases(itemquery.Referencself.treedict["Session"]), itemquery.ReferenceTable)
        if itemquery is not None:
            SQLString = itemquery.DisplayQuery
            if itemquery.ReferenceTablself.treedict["Session"] is not None:
                conn = sessions[itemquery.ReferenceTablself.treedict["Session"]].connection()
                self.itemNames3 = QStandardItemModel(0, 3)
                try:
                    rowcount = 0
                    for row, ItemName in enumerate(conn.execute(SQLString).fetchall()):
                        if ItemName[1] != "" and ItemName[1] != None:
                            rowcount += 1
                            itemID = QStandardItem("%i" % ItemName[0])
                            self.itemNames3.setItem(rowcount, 0, itemID)
                            self.itemNames3.setItem(rowcount, 1, QStandardItem(ItemName[1]))
                except:
                    pass
                conn.close()

                self.dialog.cmbTreeItem_id_2.setModel(self.itemNames3)
                self.dialog.cmbTreeItem_id_2.setModelColumn(1)

    @QtCore.pyqtSlot(int)
    def on_cmbECTreeItemMaster_currentIndexChanged(self, index):
        ItemMaster_id = self.dialog.cmbECTreeItemMaster.model().index(index, 0, None).data()
        itemquery = self.treedict["Session"].query(MasterTable).filter_by(id=ItemMaster_id).first()
        # Newtable = DatabaseTools.get_class_by_tablename(bases(itemquery.Referencself.treedict["Session"]), itemquery.ReferenceTable)
        if itemquery is not None:
            SQLString = itemquery.DisplayQuery
            if itemquery.ReferenceTablself.treedict["Session"] is not None:
                conn = sessions[itemquery.ReferenceTablself.treedict["Session"]].connection()
                self.itemNames3 = QStandardItemModel(0, 3)
                try:
                    rowcount = 0
                    for row, ItemName in enumerate(conn.execute(SQLString).fetchall()):
                        if ItemName[1] != "" and ItemName[1] != None:
                            rowcount += 1
                            itemID = QStandardItem("%i" % ItemName[0])
                            self.itemNames3.setItem(rowcount, 0, itemID)
                            self.itemNames3.setItem(rowcount, 1, QStandardItem(ItemName[1]))
                except:
                    pass
                conn.close()

                self.dialog.cmbECTreeItem_id.setModel(self.itemNames3)
                self.dialog.cmbECTreeItem_id.setModelColumn(1)

    def loadMasterTable(self):
        self.sessions
        self.bases

    def addHistoryEvent(self, EventName):
        datetimenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #conn = DatabaseConnect.dbConnect(self.fileLocation)
        #cursor = conn.cursor()

        statement = "INSERT INTO actionHistory (entrydatetime, actionItem) VALUES(?, ?)"
        #cursor.execute(statement, (datetimenow, EventName))

        #conn.commit()

        #self.lstHistoryModel.appendRow([QStandardItem(str(datetimenow)), QStandardItem(str(EventName))])
        #self.dialog.tblEventHistory.setModel(self.lstHistoryModel)

    def closeEvent(self, *args, **kwargs):
        print("Closing Time!!")

        self.cursor = None
        self.conn = None
