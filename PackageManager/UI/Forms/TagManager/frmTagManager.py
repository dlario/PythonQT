import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot, Qt, QSortFilterProxyModel, QRegularExpression
from PySide6.QtGui import QStandardItem, QStandardItemModel, QIcon

from sqlalchemy import literal_column

from qtalchemy import QueryTableModel

basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"
from PackageManager.Packages.ProjectList.Resources import ICON_DIR
from PackageManager.Core.Database import DatabaseTools
from PackageManager.Packages.ProgramBase.Database.dbMaster import *


class TagManager():
    def __init__(self, MasterData, main, Table, Record, TagList):
        self.MasterData = MasterData
        
        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmTagManager.ui')
        self.ui = loader.load(uiFile, self)

        self.PackageName = "ProjectList"
        self.setWindowTitle("Project List")
        self.setWindowIcon(QIcon(ICON_DIR + 'AMProject.png'))

        self.main = main

        # Loading The Database
        self.sqlRegister = main.instance.sqlRegister
        # This is the table coordinator
        self.sessions = {}
        self.bases = {}

        self.ReferenceNumber_id = None
        self.ProjectDict = {}
        self.ProjectDict["id"] = None

        self.registerDatabase()
        self.on_projectList_load()
        self.MasterData = DatabaseTools.DatabaseController(self.session, MasterTable, FieldInformation, self.engines,
                                                           self.bases, self.sessions,
                                                           SessionBase, SessionNames)
        
        self.initSessionList()
        self.on_commands_load()
        self.taglist = TagList
        self.on_tagList_load()

        self.dialog.exec_()

    def registerDatabase(self):
        #This is just an example of how to register a database
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

        self.sqlRegister.registarInstance("Location1", "ProgramBase", "ASAP", self)
        self.sqlRegister.sqlDict["Location1"].createSession(base, name, dbtype, login, password, location, port,
                                                                   schema, key, sshTunnel)
        # This is the table coordinator
        self.scopedSession = self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Location1"].scopedSession
        self.session = self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Location1"].session
        self.base = self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].base
        self.engines = self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].engine
        self.sqlRegister.masterTable = "MasterTable"
        self.sqlRegister.masterFieldList = "MasterFieldList"
        self.sessions["Master"] = self.session
    def on_commands_load(self):
        self.dialog.cmdAddNewPhraseName.clicked.connect(self.on_cmdAddNewPhraseName_clicked)
        self.dialog.cmdAddFavorite.clicked.connect(self.on_cmdAddFavorite_clicked)
        self.dialog.cmdAddSelectedTag.clicked.connect(self.on_cmdAddSelectedTag_clicked)
        self.dialog.cmdRemoveTag.clicked.connect(self.on_cmdRemoveTag_clicked)

    # region MasterTable 
    @Slot()
    def on_cmdUpdateMasterTable_clicked(self):
        DatabaseTools.updateMasterTable(self.session, MasterTable, FieldInformation, self.engines, self.bases, SessionBase,
                                        SessionNames)

    @Slot(str)
    def on_txtMasterTableFilter_textChanged(self, value):
        self.loadMasterTable(value)

    def on_tagList_load(self):
        tagModel = QStandardItemModel(0, 4)

        for row, Tag in enumerate(self.taglist):
            tagitem = self.MasterData.getTagInfo(Tag)
            tagModel.setItem(row, 0, QStandardItem(Tag))
            tagModel.setItem(row, 1, QStandardItem(str(tagitem[0])))
            tagModel.setItem(row, 2, QStandardItem(str(tagitem[1])))
            if tagitem[2]: tagModel.setItem(row, 3, QStandardItem("%i" % tagitem[2]))
            if tagitem[3]: tagModel.setItem(row, 4, QStandardItem("%i" % tagitem[3]))
            
            tagModel.setHeaderData(0, Qt.Horizontal, 'Tag', role=Qt.DisplayRole)
            tagModel.setHeaderData(1, Qt.Horizontal, 'Table', role=Qt.DisplayRole)
            tagModel.setHeaderData(2, Qt.Horizontal, 'Item', role=Qt.DisplayRole)
            tagModel.setHeaderData(3, Qt.Horizontal, 'Table_id', role=Qt.DisplayRole)
            tagModel.setHeaderData(4, Qt.Horizontal, 'Item_id', role=Qt.DisplayRole)
            
        self.dialog.tbltaglist.setModel(tagModel)
        self.dialog.tbltaglist.resizeColumnsToContents()

    def initSessionList(self):
        qrysessionlist = self.sessions["Master"].query(SessionNames.id, SessionNames.NameText, literal_column(str("242")))  # 139
        self.dialog.lstTagSessionFilter.setModel(QueryTableModel(qrysessionlist))
        self.dialog.lstTagSessionFilter.model().reset_content_from_session()
        self.dialog.lstTagSessionFilter.setModelColumn(1)
        self.dialog.lstTagSessionFilter.blockSignals(True)
        self.dialog.lstTagSessionFilter.selectionModel().selectionChanged.connect(self.on_lstTagSessionFilter_selectionChanged)
        self.dialog.lstTagSessionFilter.blockSignals(False)
        self.dialog.lstTagTables.clicked.connect(self.on_lstTagTables_clicked)

    #@Slot()
    def on_lstTagTables_clicked(self):
        mastertable_id = self.dialog.lstTagTables.model().index(self.dialog.lstTagTables.currentIndex().row(), 0).data()

        query1 = self.sessions["Master"].query(MasterTable).filter_by(id=int(mastertable_id)).first()
        query2 = self.sessions["Master"].query(SessionNames).filter_by(id=int(query1.Session)).first()

        self.dialog.txtMstrSelected_id.setText(str(mastertable_id))

        self.dialog.txtSQLStatement.blockSignals(True)
        self.dialog.txtSQLStatement.setText(query1.DisplayQuery)
        self.dialog.txtSQLStatement.blockSignals(False)

        self.selectedTagTableModel = self.MasterData.displayTableData(mastertable_id, query1.DisplayQuery)

        self.dialog.lstTags.setModel(self.selectedTagTableModel)
        self.dialog.lstTags.setModelColumn(1)
        #self.dialog.lstTags.selectionModel().selectionChanged.connect(self.on_lstTags_selectionChanged)

    #Slot()
    def on_cmdAddFavorite_clicked(self):
        tableid = 553 #ImageData
        item_id = self.dialog.lstTagTables.model().index(self.dialog.lstTagTables.currentIndex().row(), 0).data()
        tagitem = "(%s-%s)" % (str(tableid), item_id)
        self.MasterData.addTags(item_id, tagitem)

    def on_cmdRemoveFavorite_clicked(self):
        tableid = 553 #ImageData
        item_id = self.dialog.lstTagTables.model().index(self.dialog.lstTagTables.currentIndex().row(), 0).data()
        tagitem = "(%s-%s)" % (str(tableid), item_id)
        self.MasterData.removeTags(item_id, tagitem)

    #@Slot()
    def on_cmdAddNewPhraseName_clicked(self):

        table_id = self.dialog.lstTagTables.model().index(self.dialog.lstTagTables.currentIndex().row(), 0).data()
        returnvalue = UpdateList(self, self.bases, self.sessions, table_id)

    @Slot(str)
    def on_txtSearchMasterTableItem_textChanged(self, text):
        # self.loadDescriptorTypes(1)
        search = QRegularExpression(text,
                                    QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.sessionitemModelproxy.setFilterRegExp(search)
        self.sessionitemModelproxy.setFilterKeyColumn(1)


    @Slot()
    def on_lstMasterTableItems_clicked(self):
        mastertable_id = self.dialog.lstMasterTableItems.model().index(self.dialog.lstMasterTableItems.currentIndex().row(),
                                                                   0).data()

        query1 = self.sessions["Master"].query(MasterTable).filter_by(id=int(mastertable_id)).first()
        query2 = self.sessions["Master"].query(SessionNames).filter_by(id=int(query1.Session)).first()

        self.dialog.txtMstrSelected_id.setText(str(mastertable_id))

        self.dialog.txtSQLStatement.blockSignals(True)
        self.dialog.txtSQLStatement.setText(query1.DisplayQuery)
        self.dialog.txtSQLStatement.blockSignals(False)

        self.selectedTableModel = self.loadsampleTableData(mastertable_id, query1.DisplayQuery)

        self.dialog.lstMasterTableSample.setModel(self.selectedTableModel)
        self.dialog.lstMasterTableSample.setModelColumn(1)


    @Slot(str)
    def on_txtSQLStatement_textChanged(self, text):
        mastertable_id = int(self.dialog.txtMstrSelected_id.text())
        self.loadsampleTableData(mastertable_id, text)


    @Slot()
    def on_cmdUpdateSQL_clicked(self):
        pass


    def loadsampleTableData(self, mastertable_id, displayquery):
        query1 = self.sessions["Master"].query(MasterTable).filter_by(id=int(mastertable_id)).first()
        query2 = self.sessions["Master"].query(SessionNames).filter_by(id=int(query1.Session)).first()

        selectedTableModel = QStandardItemModel(0, 2)
        conn = self.sessions["Master"].connection()
        try:
            conn2 = self.sessions[query2.NameText].connection()

            if displayquery is not None:
                records = conn2.execute(displayquery).fetchall()

                if records != []:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name = QStandardItem(ItemName[1])

                        selectedTableModel.setItem(row, 0, Descriptor_id)
                        selectedTableModel.setItem(row, 1, Descriptor_Name)

                conn2.close()
                conn.close()
                return selectedTableModel

            else:
                print("No Records to Display")
                return None

        except:
            return None


    def on_lstMasterTableSession_selectionChanged(self):
        SQLUnion = ""
        SQLSelect = "SELECT id, NameText"
        SQLFrom = " FROM ItemTable"
        SQLOrder = " ORDER BY NameText"

        SQLUnion = ""

        selectedItems = self.dialog.lstMasterTableSession.selectedIndexes()

        for itemsselected in selectedItems:
            Session_id = self.dialog.lstMasterTableSession.model().index(itemsselected.row(), 0, None).data()
            # SQLSelect = "SELECT id, TableName, TableName, %i, Session, DisplayColumn" % (int(ItemMasterTable))
            # SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s UNION " % ("NameText", 253, "mastertable", 1, "mastertable")
            SQLUnion += "SELECT id, %s, \"%s\", %i FROM %s WHERE session = %i UNION " % (
            "TableName", "mastertable", Session_id, "mastertable", Session_id)

        strSQL = SQLUnion.rstrip('UNION ')
        print(strSQL)
        self.mastersessionmodel = self.loadSessionList(strSQL)
        # self.dialog.listItem.setModelColumn(1)
        self.sessionitemModelproxy = QSortFilterProxyModel()
        self.sessionitemModelproxy.setSourceModel(self.mastersessionmodel)
        self.dialog.lstMasterTableItems.setModel(self.sessionitemModelproxy)
        # self.dialog.lstMasterTableItems.setModel(self.sessionitemNames)
        self.dialog.lstMasterTableItems.setModelColumn(1)


    def on_lstTagSessionFilter_selectionChanged(self):
        self.on_TagSessionFilter_load()


    @Slot(int)
    def on_chkShowDisplayable_stateChanged(self):
        self.dialog.chkShowFavorites.blockSignals(True)
        self.dialog.chkShowFavorites.setChecked(False)
        self.dialog.chkShowFavorites.blockSignals(False)
        self.on_TagSessionFilter_load()


    @Slot(int)
    def on_chkShowFavorites_stateChanged(self):
        self.dialog.chkShowDisplayable.blockSignals(True)
        self.dialog.chkShowDisplayable.setChecked(False)
        self.dialog.chkShowDisplayable.blockSignals(False)
        self.on_TagSessionFilter_load()


    def on_TagSessionFilter_load(self):
        qryMasterTable = self.sessions["PackageManager"].query(MasterTable.id, SessionBase.NameText.label("Base"),
                                                          SessionNames.NameText.label("Session"), MasterTable.TableName) \
            .outerjoin(SessionBase, MasterTable.Base == SessionBase.id) \
            .outerjoin(SessionNames, MasterTable.Session == SessionNames.id)

        if self.dialog.chkShowDisplayable.isChecked():
            qryMasterTable = qryMasterTable.filter(MasterTable.DisplayColumn.isnot(None))

        if self.dialog.chkShowFavorites.isChecked():
            tableid = 553  # ImageData

            qryMasterTable = qryMasterTable.filter(MasterTable.Tags.like("%(" + str(tableid) + "%"))

        if self.dialog.chkFilterProjectRelated.isChecked():
            pass

        if not self.dialog.chkShowFavorites.isChecked():
            filterstatement = None
            filtersessionlist = []
            selectedItems = self.dialog.lstTagSessionFilter.selectedIndexes()
            for itemsselected in selectedItems:
                filtersessionlist.append(self.dialog.lstTagSessionFilter.model().index(itemsselected.row(), 0, None).data())

            '''if filtersessionlist != []:
                qryMasterTable = qryMasterTable.filter(MasterTable.sessions["PackageManager"].in_(filtersessionlist))'''

        qryMasterTable = qryMasterTable.all()

        self.sessionTTmodel = QStandardItemModel(0, 2)
        for row, record in enumerate(qryMasterTable):
            itemID = QStandardItem("%i" % record.id)
            self.sessionTTmodel.setItem(row, 0, itemID)
            self.sessionTTmodel.setItem(row, 1, QStandardItem(record.TableName))

        '''for itemsselected in selectedItems:
            Session_id = self.dialog.lstTagSessionFilter.model().index(itemsselected.row(), 0, None).data()
            #SQLSelect = "SELECT id, TableName, TableName, %i, Session, DisplayColumn" % (int(ItemMasterTable))
            #SQLUnion += "SELECT id, %s, %i, \"%s\", %i FROM %s UNION " % ("NameText", 253, "mastertable", 1, "mastertable")
            SQLUnion += "SELECT id, %s, \"%s\", %i FROM %s WHERE session = %i UNION " % ("TableName", "mastertable", Session_id, "mastertable", Session_id)
    
        strSQL = SQLUnion.rstrip('UNION ')
    
        self.sessionTTmodel = self.loadSessionList(strSQL)'''

        # self.dialog.listItem.setModelColumn(1)
        self.sessionTTModelproxy = QSortFilterProxyModel()
        self.sessionTTModelproxy.setSourceModel(self.sessionTTmodel)
        self.dialog.lstTagTables.blockSignals(True)
        self.dialog.lstTagTables.setModel(self.sessionTTModelproxy)
        # self.dialog.lstMasterTableItems.setModel(self.sessionitemNames)
        self.dialog.lstTagTables.blockSignals(False)
        self.dialog.lstTagTables.setModelColumn(1)


    def loadSessionList(self, strSQL):
        conn = sessions["Master"].connection()
        sessionModel = QStandardItemModel(0, 4)
        try:
            rowcount = 0
            for row, ItemName in enumerate(conn.execute(strSQL).fetchall()):
                rowcount += 1
                # print(ItemName[1])
                Item_id = QStandardItem("%i" % ItemName[0])
                # ItemTable_id = QStandardItem("%i" % ItemName[1])
                MasterTable_id = QStandardItem("%i" % ItemName[3])

                sessionModel.setItem(rowcount, 0, Item_id)
                sessionModel.setItem(rowcount, 1, QStandardItem(str(ItemName[1])))
                sessionModel.setItem(rowcount, 2, QStandardItem(ItemName[2]))
                sessionModel.setItem(rowcount, 3, MasterTable_id)
            conn.close()

        except:
            print("No Records Found")

        return sessionModel


    def loadDescriptor(self):
        # This will load all the tables types that are selected and then apply the filter
        # http://stackoverflow.com/questions/14546913/how-to-get-item-selected-from-qlistview-in-pyqt
        conn = self.sessions["Master"].connection()
        sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
        self.descriptorModel = QStandardItemModel(0, 2)
        itemsadded = 0

        selectedItems = self.dialog.lstDescriptorTypes.selectedIndexes()
        for itemsselected in selectedItems:
            ItemID = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 0, None).data()
            ItemName = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 1, None).data()
            ItemMasterTable = self.dialog.lstDescriptorTypes.model().index(itemsselected.row(), 2, None).data()

            if DatabaseConnect.sqlAttackCheck(self, itemsselected.data()):
                query1 = self.sessions["Master"].query(self.sessions["Master"]).filter_by(id=int(ItemMasterTable)).first()
                query2 = self.sessions["Master"].query(sessionbase1).filter_by(id=int(query1.Session)).first()

                displayquery = query1.DisplayQuery
                conn2 = self.sessionlist[query2.NameText].connection()
                records = conn2.execute(displayquery).fetchall()

                if records is not None:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name = QStandardItem(ItemName[1])
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

            self.dialog.lstDescriptors.setModel(self.descriptorModel)

            '''self.descriptorModelproxy.setSourceModel(self.descriptorModel)
            self.dialog.lstDescriptors.setModel(self.descriptorModelproxy)'''
            self.dialog.lstDescriptors.setModelColumn(1)

        conn.close()


    def loadItems(self):
        # This will load all the tables types that are selected and then apply the filter
        # http://stackoverflow.com/questions/14546913/how-to-get-item-selected-from-qlistview-in-pyqt

        conn = self.sessions["Master"].connection()
        sessionbase1 = DatabaseTools.get_class_by_tablename(self.baselist["PackageManager"], "lstsession")
        self.itemNames = QStandardItemModel(0, 2)
        itemsadded = 0

        selectedItems = self.dialog.listItemTypes.selectedIndexes()
        for itemsselected in selectedItems:
            ItemID = self.dialog.listItemTypes.model().index(itemsselected.row(), 0, None).data()
            ItemName = self.dialog.listItemTypes.model().index(itemsselected.row(), 1, None).data()
            ItemMasterTable = self.dialog.listItemTypes.model().index(itemsselected.row(), 2, None).data()

            if DatabaseConnect.sqlAttackCheck(self, itemsselected.data()):
                query1 = self.sessions["Master"].query(self.sessions["Master"]).filter_by(
                    id=int(ItemMasterTable)).first()
                query2 = self.sessions["Master"].query(sessionbase1).filter_by(
                    id=int(query1.Session)).first()

                displayquery = query1.DisplayQuery
                conn2 = self.sessionlist[query2.NameText].connection()
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

                conn2.close()

        self.itemModelproxy.setSourceModel(self.itemNames)
        self.dialog.listItem.setModel(self.itemModelproxy)
        self.dialog.listItem.setModelColumn(1)

        conn.close()


    #@Slot()
    def on_cmdAddSelectedTag_clicked(self):
        selectedItems = self.dialog.lstTags.selectionModel().selectedIndexes()

        for itemsselected in selectedItems:
            item_id = self.dialog.lstTags.model().index(itemsselected.row(), 0).data()
            table_id = self.dialog.lstTags.model().index(itemsselected.row(), 2).data()

            SelectedTag = "(%s-%s)" % (str(table_id), str(item_id))

            if SelectedTag not in self.taglist:
                self.taglist.append(SelectedTag)

        self.on_tagList_load()

    #@Slot()
    def on_cmdRemoveTag_clicked(self):
        tag_id = self.dialog.tbltaglist.model().index(self.dialog.tbltaglist.currentIndex().row(), 0).data()
        self.dialog.taglist.remove(tag_id)
        self.on_tagList_load()

    def loadMasterTable(self, FilterName=None):
        qryMasterTable = self.sessions["PackageManager"].query(MasterTable.id, SessionBase.NameText.label("Base"),
                                                          SessionNames.NameText.label("Session"), MasterTable.TableName) \
            .join(SessionBase, MasterTable.Base == SessionBase.id) \
            .join(SessionNames, MasterTable.Session == SessionNames.id)
        if FilterName is not None:
            qryMasterTable = qryMasterTable.filter(MasterTable.TableName.like("%" + str(FilterName) + "%"))

        self.dialog.tblMasterTable.setModel(QueryTableModel(qryMasterTable))
    # endregion

    @staticmethod
    def get_data(parent=None):
        dialog = UpdateList(parent)
        dialog.exec_()
        return dialog.return_strings()