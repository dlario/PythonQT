import os

from PySide6.QtCore import QSortFilterProxyModel, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QRegularExpression

from PackageManager.Core.Database import DatabaseTools

#Import Tables
from PackageManager.Packages.ProgramBase.Database.dbMaster import MasterTable

#from dbAllTables import FormData, FormObjectMapping

basepath = os.path.dirname(os.path.abspath(__file__))

class UpdateList(object):
    def __init__(self, parent, bases, sessions, table_id):
        self.parent = parent

        masterrecord = sessions["PackageManager"].query(MasterTable).filter_by(id = int(table_id)).first()
        self.SessionName = sessions["PackageManager"].query(SessionNames).filter_by(id=masterrecord.Session).first()
        self.RecordSession = sessions[self.SessionName.NameText]
        self.RecordBase = sessions["PackageManager"].query(SessionBase).filter_by(id=masterrecord.Base).first().NameText
        a = masterrecord.TableName.lower()
        self.RecordTable = DatabaseTools.get_class_by_tablename(bases[self.RecordBase], masterrecord.TableName.lower())

        referencetable_id=260
        masterreferencerecord = sessions["PackageManager"].query(MasterTable).filter_by(id = referencetable_id).first()
        ReferenceSessionQuery = sessions["PackageManager"].query(SessionNames).filter_by(id=masterreferencerecord.Session).first().NameText
        self.ReferenceSession = sessions[ReferenceSessionQuery]

        self.ReferenceBase = sessions["PackageManager"].query(SessionBase).filter_by(id=masterreferencerecord.Base).first().NameText

        self.ReferenceTable = DatabaseTools.get_class_by_tablename(bases[self.ReferenceBase], masterreferencerecord.TableName.lower())

        # Loading the Treeview Data

        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmListEditor.ui')
        self.dialog = loader.load(uiFile, self)


        self.loadData()

        self.ItemDict = {}
        self.ItemDict["id"] = 0
        self.ItemDict["NameText"] = ""

        self.dialog.buttonBox.accepted.connect(self.accept)
        self.dialog.buttonBox.rejected.connect(self.reject)
        self.dialog.lineEdit.textChanged.connect(self.textChanged)
        self.dialog.cmdAddItem.clicked.connect(self.AddItem)
        self.dialog.tblItemTable.clicked.connect(self.on_tblItemTable_clicked)
        self.dialog.exec_()


    def GetItemData(self):
        return self.ItemDict

    def GetItemModel(self):
        return self.listDataModel2


    def loadData(self):

        tableData = self.RecordSession.query(self.RecordTable).order_by(self.RecordTable.NameText)

        self.listDataModel2 = QStandardItemModel(0, 2)

        for row, record in enumerate(tableData):
            self.listDataModel2.setItem(row, 0, QStandardItem("%i" % int(record.id)))
            self.listDataModel2.setItem(row, 1, QStandardItem(record.NameText))

        self.listItemproxy = QSortFilterProxyModel()
        self.listItemproxy.setSourceModel(self.listDataModel2)
        self.dialog.tblItemTable.setModel(self.listItemproxy)

    @Slot()
    def on_tblItemTable_clicked(self, index):

        self.ItemDict["id"] = self.dialog.tblItemTable.model().index(index.row(), 0).data()
        self.ItemDict["NameText"] = self.dialog.tblItemTable.model().index(index.row(), 1).data()

        self.dialog.lineEdit.setText(self.ItemDict["NameText"])


    @Slot()
    def AddItem(self):
        self.ReferenceSession.begin(subtransactions=True)
        ItemReferenceID = DatabaseTools.GetReferenceID(self.ReferenceTable, self.ReferenceSession, self.dialog.lineEdit.text())
        self.ReferenceSession.commit()

        self.RecordSession.begin(subtransactions=True)
        CreateUpdateAttribute = self.RecordTable(Name_id=ItemReferenceID, NameText=self.dialog.lineEdit.text())
        self.RecordSession.add(CreateUpdateAttribute)
        self.RecordSession.commit()
        self.RecordSession.flush()

        '''self.ItemDict["id"] = CreateUpdateAttribute.id
        self.ItemDict["Name_id"] =  lario.DatabaseTools.GetReferenceID(self.ReferenceTable, self.ReferenceSession, CreateUpdateAttribute.NameText)
        self.ItemDict["NameText"] = CreateUpdateAttribute.NameText'''

        self.loadData()
        self.textChanged()


    def textChanged(self):
        pattern = self.dialog.lineEdit.text()
        search = QRegularExpression(pattern,
                                   QRegularExpression.CaseInsensitiveOption | QRegularExpression.WildcardOption)
        self.listItemproxy.setFilterRegExp(search)
        self.listItemproxy.setFilterKeyColumn(1)


    def accept(self):
        print(self.dialog.lineEdit.text())
        return(self.ItemDict)

    def reject(self):
        print("Rejected")

    @staticmethod
    def get_data(parent=None):
        dialog = UpdateList(parent)
        dialog.exec_()
        return dialog.return_strings()
