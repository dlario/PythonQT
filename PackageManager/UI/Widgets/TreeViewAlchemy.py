# http://pyqt.sourceforge.net/Docs/PyQt4/qtreeview.html

from copy import *
from pickle import dumps, load, loads
from io import *

import os
import datetime
from PackageManager.Core.Common import myListToStr, strToMyList
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

basepath = os.path.dirname(os.path.abspath(__file__))


class PyMimeData(QMimeData):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = "application/x-ets-qt4-instance"

    def __init__(self, data=None):
        """ Initialise the instance.
        """
        QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if data is not None:
            # We may not be able to pickle the data.
            try:
                pdata = dumps(data)
            except:
                return

                # This format (as opposed to using a single sequence) allows the
                # type to be extracted without unpickling the data itself.
        self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)

    @classmethod
    def coerce(cls, md):
        """ Coerce a QMimeData instance to a PyMimeData instance if
        possible.
        """
        # See if the data is already of the right type.  If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # See if the data type is supported.
        if not md.hasFormat(cls.MIME_TYPE):
            return None

        nmd = cls()
        nmd.setData(cls.MIME_TYPE, md.data())

        return nmd

    def instance(self):
        """ Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            load(io)
            # Recreate the instance.
            return load(io)
        except:
            pass

        return None

    def instanceType(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            return loads(str(self.data(self.MIME_TYPE)))
        except:
            pass

        return None


class treeItem_class(object):
    '''
    A Specialized SubClass of the TreeItemBaseClass
    '''

    def __init__(self, treeDict):

        # self.treeDict = treeDict
        # the first should replace everything else in the future.
        # treemodel.currentTreeItem(self, ID=None) would load the dictionary
        self.Tree_id = int(treeDict['Tree_id'])
        self.TreePath = treeDict['TreePath']

        self.TreeGroup_id = int(treeDict['TreeGroup_id'])
        self.ParentTree_id = int(treeDict['ParentTree_id'])
        # self.DescriptorMaster = treeDict['DescriptorMasterTable']
        self.DescriptorMaster_id = int(treeDict['DescriptorMaster_id'])
        # self.DescriptorTable = treeDict['DescriptorTable']
        self.DescriptorTable_id = int(treeDict['DescriptorTable_id'])
        self.Descriptor = treeDict['Descriptor_id']
        # self.DescriptorName = treeDict['DescriptorName']
        # self.ItemMaster = treeDict['ItemMasterTable']
        self.ItemMaster = treeDict['ItemMaster_id']
        # self.ItemTable = treeDict['ItemTable']
        self.ItemTable_id = int(treeDict['ItemTable_id'])
        self.Item = treeDict['Item_id']
        # self.ItemName = treeDict['ItemName']
        self.Display = []

        if treeDict['DisplayName'] != None:
            DisplayValue = treeDict['DisplayName']
        else:
            DisplayValue = ""
            if self.DescriptorName != None:
                DisplayValue += str(self.DescriptorName)
            if self.ItemName != None:
                DisplayValue += str(self.ItemName)
            if self.DisplayName != None:
                DisplayValue += str(self.DisplayName)

        self.Display.append(DisplayValue)
        self.Order = treeDict['ItemOrder']
        self.FlattenedOrder = treeDict['FlattenedOrder']
        self.Level = treeDict['ItemLevel']
        self.ForeColor = treeDict['ForeColor']
        self.Expanded = treeDict['Expanded']
        self.Header = treeDict['Header']


class treeCategory_class(object):
    '''
    A Specialized SubClass of the TreeItemBaseClass
    '''

    def __init__(self, Tree_id=None, Category=None, Header=None, Display=None):
        self.Tree_id = Tree_id
        self.Category = Category
        self.Header = Header
        self.Display = Display


class sqlStandardItemModel(QStandardItemModel):
    def __init__(self, Parent=None, session=None, tableclass=None, **kwargs):
        super(sqlStandardItemModel, self).__init__(**kwargs)

        self.session = session
        self.TreeGeneratedClass = tableclass
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None

        # self.setupModelData()

    def setupModelData2(self):

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        for record in records:  # cursors are iterable
            for key, value in self.fieldDict:
                self.setItem(recordrow, key, QStandardItem(str(value)))
            recordrow += 1

    def setupModelData(self):

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0

        for record in records:  # cursors are iterable]
            self.fieldDict = DatabaseTools.row2dict(record)
            for key, value in enumerate(self.fieldDict):
                if value == "Display":
                    Display = []
                    Display.append(str(record[6]))
                    self.setItem(recordrow, key, QStandardItem(Display[0]))
                else:
                    self.setItem(recordrow, key, QStandardItem(str(value)))
            recordrow += 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.setItem[index.row()][index.column()])

    def headerCount(self):
        return self.fieldNameCount

    def headerData(self, column=0, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if len(self.fieldNames) !=0:
                data = QVariant(self.fieldNames[column])
            else:
                data = QVariant("-")
        else:
            data = QAbstractTableModel.headerData(self, column, orientation, role)
        return data

    def CloneBranch(self, ParentID, ParentLevel, CloneID):
        pass


class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''

    def __init__(self, TreeClassItem, Header, parentItem):
        self.TreeClassItem = TreeClassItem
        self.parentItem = parentItem
        self.Header = Header  # This is the display in tree value
        self.Display = []  # These are the additional column items
        self.childItems = []
        self.__colors = None
        self.ColumnsViewed = 1
        self.settingDatabase = "DSSettings.db"
        self.settingTable = "tblProgramSettings"

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        # This will have to be updated with the length of the display list
        return self.ColumnsViewed

    def data(self, column):

        FileLocation = ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Icon Location")
        Filelocation = FileLocation + "Excel.bmp"
        iconQPixmap = QPixmap(FileLocation)

        # This Allows a sub class to be put in that can store additional information
        if self.TreeClassItem == None:
            try:
                if column == 0:
                    return QVariant(self.Header)
                if column == 1:
                    # return QVariant("")

                    return QVariant(self.Display[column])
            except:
                pass
        else:
            try:
                return QVariant(self.TreeClassItem.Display[column])
            except:
                pass
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            ch = (value)

            self.__colors[row][column] = ch
            self.dataChanged.emit(index, index)
            return True

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class treeModel(QAbstractItemModel):
    def __init__(self, session, treeviewdict, inParent=None, header="", groupid=0, **kwargs):
        super(treeModel, self).__init__(inParent, **kwargs)

        '''TreeItems.id
            TreeItems.TreeGroup_id
            TreeItems.Tree_id
            TreeItems.ParentTree_id
            TreeItems.DescriptorMaster_id
            TreeItems.DescriptorTable_id
            TreeItems.Descriptor_id
            TreeItems.ItemMaster_id
            TreeItems.ItemTable_id
            TreeItems.Item_id
            TreeItems.DisplayName
            TreeItems.ItemOrder
            TreeItems.FlattenedOrder
            TreeItems.ItemLevel
            TreeItems.ForeColor
            TreeItems.Expanded
            TreeItems.Header'''

        self.Display = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.session = session

        self.treeviewdict = treeviewdict
        self.TreeGroup_id = groupid
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None
        # self.Headers =  ("Category", "Item", "Description")
        self.Headers = []
        self.Headers.append(header)

        self.RecordCount = 0

    def defaultTreeItem(self):
        newtreeitemdata = {}
        newtreeitemdata['TreeID'] = None  # Will be added when record is made
        newtreeitemdata['TreePath'] = ""

        newtreeitemdata['TreeGroup_id'] = 1
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = 1  # Follows the top item
        newtreeitemdata['DescriptorMaster'] = 0  # Level One Grouping
        newtreeitemdata['DescriptorMaster_id'] = 0
        newtreeitemdata['DescriptorMasterTable'] = 0  # Projects
        newtreeitemdata['DescriptorTable'] = 0  # Projects - eventgroupsliceditem
        newtreeitemdata['DescriptorTable_id'] = 0
        newtreeitemdata['DescriptorName'] = None
        newtreeitemdata['Descriptor_id'] = 0
        newtreeitemdata['ItemMaster'] = None
        newtreeitemdata['ItemMasterTable'] = None
        newtreeitemdata['ItemMaster_id'] = 0
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['DisplayName'] = None
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 0
        newtreeitemdata['ItemLevel'] = 1
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None

        # newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        # treepath = []
        # treepath.append(Tree_id)
        # newtreeitemdata['TreePath'] = str(myListToStr(treepath))
        itemlevel = 0
        # newtreeitemdata['ItemLevel'] = len(treepath) - 1

        return newtreeitemdata

    def currentTreeItem(self, ID=None):
        treeItemDict = []
        record = {}
        conn = self.session.connection()

        TreeItems = self.treeviewdict["TreeItems"]
        ItemMasterTable = self.treeviewdict["ItemMasterTable"]
        ItemTable = self.treeviewdict["ItemTable"]

        # Need to find out the custom database table name

        SelectedTreeItem = self.session.query(TreeItems.id,
                                              DescriptorMasterTable.NameText.label("DescriptorMasterTable"),
                                              ItemMasterTable.NameText.label("ItemMasterTable"),
                                              DescriptorTable.ReferenceTable.label("DescriptorTable"),
                                              ItemTable.ReferenceTable.label("ItemTable")) \
            .join(DescriptorMasterTable, TreeItems.DescriptorMaster_id == DescriptorMasterTable.id) \
            .join(ItemMasterTable, TreeItems.ItemMaster_id == ItemMasterTable.id) \
            .join(DescriptorTable, TreeItems.DescriptorTable_id == DescriptorTable.id) \
            .join(ItemTable, TreeItems.ItemTable_id == ItemTable.id) \
            .filter(TreeItems.id == ID).first()

        SQLSelect = "SELECT treeitems.id, " \
                    "treeitems.TreeGroup_id, " \
                    "treeitems.Tree_id, " \
                    "treeitems.ParentTree_id, " \
                    "treeitems.DescriptorMaster_id, " \
                    "treeitems.DescriptorTable_id, " \
                    "treeitems.Descriptor_id, " \
                    "treeitems.ItemMaster_id, " \
                    "treeitems.ItemTable_id, " \
                    "treeitems.Item_id, " \
                    "treeitems.DisplayName, " \
                    "treeitems.ItemOrder, " \
                    "treeitems.FlattenedOrder, " \
                    "treeitems.ItemLevel, " \
                    "treeitems.ForeColor, " \
                    "treeitems.Expanded, " \
                    "treeitems.Header" \

        AddNone = []

        SQLFrom = " FROM treeitems "
        if SelectedTreeItem is not None:
            SQLSelect = SQLSelect + ", lstdescriptormastertable.NameText AS DescriptorMasterTable, " \
                                    "lstitemmastertable.NameText AS ItemMasterTable "
            if SelectedTreeItem.DescriptorMasterTable is not None and SelectedTreeItem.DescriptorMasterTable is not "":
                SQLSelect += ", %s.ReferenceTable AS DescriptorTable " % SelectedTreeItem.DescriptorMasterTable
            else:
                AddNone.append("DescriptorTable")

            if SelectedTreeItem.ItemMasterTable is not None and SelectedTreeItem.ItemMasterTable is not "":
                SQLSelect += ", %s.ReferenceTable AS ItemTable " % SelectedTreeItem.ItemMasterTable
            else:
                AddNone.append("ItemTable")

            if SelectedTreeItem.DescriptorTable is not None and SelectedTreeItem.DescriptorTable is not "":
                SQLSelect += ", %s.NameText AS DescriptorName " % SelectedTreeItem.DescriptorTable
            else:
                AddNone.append("DescriptorName")

            if SelectedTreeItem.ItemTable != None and SelectedTreeItem.ItemTable is not "":
                SQLSelect += ", %s.NameText AS ItemName" % SelectedTreeItem.ItemTable
            else:
                AddNone.append("ItemName")

            SQLFrom = " FROM treeitems " \
                      "LEFT JOIN lstdescriptormastertable ON (treeitems.DescriptorMaster_id = lstdescriptormastertable.id) " \
                      "LEFT JOIN lstitemmastertable ON (treeitems.ItemMaster_id = lstitemmastertable.id) "

            if SelectedTreeItem.DescriptorMasterTable is not None and SelectedTreeItem.DescriptorMasterTable is not "":
                SQLFrom += "LEFT JOIN %s ON (treeitems.%s_id = %s.id) " % \
                           (SelectedTreeItem.DescriptorMasterTable, SelectedTreeItem.DescriptorMasterTable,
                            SelectedTreeItem.DescriptorMasterTable)

            if SelectedTreeItem.ItemMasterTable is not None and SelectedTreeItem.ItemMasterTable is not "":
                SQLFrom += "LEFT JOIN %s ON (treeitems.%s_id = %s.id) " % \
                           (SelectedTreeItem.ItemMasterTable, SelectedTreeItem.ItemMasterTable,
                            SelectedTreeItem.ItemMasterTable)

            if SelectedTreeItem.DescriptorTable is not None and SelectedTreeItem.DescriptorTable is not "":
                SQLFrom += "LEFT JOIN %s ON (treeitems.Descriptor_id = %s.id) " % \
                           (SelectedTreeItem.DescriptorTable, SelectedTreeItem.DescriptorTable)

            if SelectedTreeItem.ItemTable is not None and SelectedTreeItem.ItemTable is not "":
                SQLFrom += "LEFT JOIN %s ON (treeitems.Item_id = %s.id)" % \
                           (SelectedTreeItem.ItemTable, SelectedTreeItem.ItemTable)

        SQLWhere = " WHERE treeitems.Tree_id = %i" % (int(ID))

        SQLQuery = SQLSelect + SQLFrom + SQLWhere
        #print(SQLQuery)
        record = conn.execute(SQLQuery).fetchone()

        return dict(record)


    def AddTreeRoot(self, RootName, indexlist):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        newtreeitemdata = {}
        newtreeitemdata['TreeID'] = None  # Will be added when record is made
        newtreeitemdata['TreePath'] = ""

        newtreeitemdata['TreeGroup_id'] = 1
        newtreeitemdata['Tree_id'] = 1  #todo update treeid
        newtreeitemdata['ParentTree_id'] = 0
        newtreeitemdata['DescriptorMaster'] = None
        newtreeitemdata['DescriptorMaster_id'] = 1
        newtreeitemdata['DescriptorMasterTable'] = None
        newtreeitemdata['DescriptorTable'] = None
        newtreeitemdata['DescriptorTable_id'] = 1
        newtreeitemdata['DescriptorName'] = None
        newtreeitemdata['Descriptor_id'] = 1
        newtreeitemdata['ItemMaster'] = None
        newtreeitemdata['ItemMasterTable'] = 0
        newtreeitemdata['ItemMaster_id'] = 1
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['DisplayName'] = RootName
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 1
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Date_Created'] = str(currentdatetime)
        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        ActivityTypeParentID = self.addTreeItem(self.treeviewdict["TreeItems"], newtreeitemdata)

    def addTreeItem(self, tableclass, treeItemDict):
        currentdatetime = datetime.datetime.now()
        self.session.begin(subtransactions=True)
        #print("AttributeTableTypeID", tableDict["AttributeTableType_id"])
        # CreateUpdateAttribute = self.session.query(self.TreeItems).filter(self.TreeItems.id==tableDict["Item_id"]).first()
        CreateUpdateAttribute = None
        #print("Adding Tree Items", treeItemDict)
        if CreateUpdateAttribute is None:
            CreateUpdateAttribute = tableclass(TreeGroup_id=int(treeItemDict["TreeGroup_id"]),
                                               ParentTree_id=int(treeItemDict["ParentTree_id"]),
                                               TreePath=treeItemDict["TreePath"],
                                               DescriptorMaster_id=int(treeItemDict["DescriptorMaster_id"]),
                                               DescriptorTable_id=int(treeItemDict["DescriptorTable_id"]),
                                               Descriptor_id=int(treeItemDict["Descriptor_id"]),
                                               ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                               ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                               Item_id=int(treeItemDict["Item_id"]),
                                               DisplayName=treeItemDict["DisplayName"],
                                               ItemOrder=int(treeItemDict["ItemOrder"]),
                                               FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                               ItemLevel=int(treeItemDict["ItemLevel"]),
                                               ForeColor=treeItemDict["ForeColor"],
                                               Expanded=int(treeItemDict["Expanded"]),
                                               Header=treeItemDict["Header"],
                                               Date_Created=str(currentdatetime),
                                               Date_Modified=str(currentdatetime),
                                               Date_Accessed=str(currentdatetime))
            self.session.add(CreateUpdateAttribute)
            self.session.commit()
        else:
            #print("Updating")
            CreateUpdateAttribute.FieldName = treeItemDict["FieldName"]
            CreateUpdateAttribute.AttributeValue = treeItemDict["Value"],
            CreateUpdateAttribute.AttributeOrder = 0
            # Will Make this generic when we make generic attribute case

        self.session.begin()
        if treeItemDict["Tree_id"] is not None:
            CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
        else:
            treeItemDict["Tree_id"] = CreateUpdateAttribute.id
            CreateUpdateAttribute.Tree_id = CreateUpdateAttribute.id

        self.session.commit()
        #print(treeItemDict)
        TIC = treeItem_class(treeItemDict)
        #print("level", treeItemDict['ItemLevel'])

        if treeItemDict['ItemLevel'] == 0:
            # Root Level Entries
            newparent = TreeItem(TIC, treeItemDict['Header'], self.rootItem)
            self.rootItem.appendChild(newparent)
            # Create the Dictonary Linking Values
            self.parents[CreateUpdateAttribute.Tree_id] = newparent
        else:
            #print("parent", treeItemDict['ParentTree_id'])
            #print(self.parents)
            parentItem = self.parents[int(treeItemDict['ParentTree_id'])]
            newItem = TreeItem(TIC, treeItemDict['Header'], parentItem)

            parentItem.appendChild(newItem)
            self.parents[CreateUpdateAttribute.Tree_id] = newItem

            # self.insertRow(0, currentSelectedIndex)
        return CreateUpdateAttribute.Tree_id

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def setupModelData(self, Tree_id, Group_id=None):

        newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        if self.treeviewdict["GeneratedTree"] != self.treeviewdict["TreeItems"]:
            self.session.begin()
            treerecords = self.session.query(self.treeviewdict["GeneratedTree"])
            if treerecords is not None:
                treerecords.delete(synchronize_session=False)
            self.session.commit()

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = str(myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1

        DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, ParentID)

    def tvtreebranch(self, treepath, ParentID):

        # Load the table data that have parents that match the ParentID
        records2 = self.session.query(self.treeviewdict["TreeItems"]).filter_by(ParentTree_id=int(ParentID)).\
            order_by("DisplayName").all()

        rowcount = 0
        treeviewindex = 1  # todo... or this

        for row, record2 in enumerate(records2):
            self.RecordCount += 1
            # Initialize the Data

            newtreeitemdata = self.currentTreeItem(ID=record2.Tree_id)

            treepath2 = treepath.copy()
            treepath2.append(str(newtreeitemdata['Tree_id']))
            newtreeitemdata['TreePath'] = myListToStr(treepath2)
            newtreeitemdata['ItemLevel'] = len(treepath2) - 1
            newtreeitemdata['ItemOrder'] = self.RecordCount
            #y = newtreeitemdata['Tree_id']
            #z = newtreeitemdata['ParentTree_id']
            #print(y, z)

            DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)

            # Checking for presence of child items.
            records3 = self.session.query(self.treeviewdict["TreeItems"]).filter_by(
                ParentTree_id=int(newtreeitemdata['Tree_id'])).all()
            if records3 is not None:
                self.tvtreebranch(treepath2, newtreeitemdata['Tree_id'])

    def mimeTypes(self):
        types = QListWidget
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode) - 1, parentIndex)
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),parentIndex, parentIndex)
        return True

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def recordCount(self):
        return self.RecordCount

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            try:
                return item.data(index.column())
            except:
                pass

        if role == Qt.UserRole:
            if item:
                return item.Header
        return QVariant()

    def returnHeaderData(self):
        SQLQuery = 'select * from %s' % (self.datatable)

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                    role == Qt.DisplayRole):
            try:
                return QVariant(self.Headers[column])
            except IndexError:
                pass

        return QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self, SWhere=None, Orientation="Vertical"):
        modelData = QAbstractItemModel

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        if Orientation == "Vertical":
            recordrow = 0
            for record in records:  # cursors are iterable
                for key in self.fieldDict:
                    modelData.setItem(recordrow, key, QStandardItem(str(record[key])))
                recordrow += 1

            # Header Data
            modelData.sort(3, Qt.AscendingOrder)

            fieldColumn = 0
            for key, value in self.fieldDict:
                #print(headerName[0])
                modelData.setHeaderData(key, Qt.Horizontal, value, role=Qt.DisplayRole)
                fieldColumn += 1
        else:
            recordcolumn = 0
            for record in records:  # cursors are iterable
                for key, value in self.fieldDict:
                    modelData.setItem(key, recordcolumn, QStandardItem(str(record[key])))
                recordcolumn += 1
        return modelData

    def searchModel(self, treepath):
        '''
        get the modelIndex for a given appointment
        '''
        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if treepath == child.TreeClassItem.TreePath:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        return retarg

    def find_Tree_Branch(self, cname):
        app = None
        for category in self.categories:
            if category.cname == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

    def paintEvent(self, event):
        painter = QPainter(
            self.viewport())  # See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        painter.drawEllipse(self.center, 10, 10)
        QTableWidget.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        sellst = self.selectedList()
        if index.isValid():
            target_node = index.internalPointer().node
            dragged_nodes, drag_type, qdrag = self.drag
            # I don't think we need qdrag for anything, but it can't hurt.
            if target_node.drop_on_ok(drag_type, dragged_nodes):
                self.selectNodes(sellst, but_not=dragged_nodes)
                target_node.drop_on(drag_type, dragged_nodes)
                event.acceptProposedAction()
                self.mt_update()
                self.drag = None
                return
        event.ignore()
        self.mt_update()
        self.drag = None

    def mouseMoveEvent(self, event):
        if self.drag is not None:
            pass  # QTreeView.mouseMoveEvent(self, event)
            return
        if ((event.globalPos() - self.mouse_press_qpoint).manhattanLength()
                < QApplication.startDragDistance()):
            return
        #
        # starting a drag
        # [logic bug, after bruce change 070507: should not do this
        #  if we already started dragging out a selection. How can we tell?
        #  Only by whether the initial press had eventInRect, I think
        #  (not yet recorded), or at least, the initial move (#e could record here).]
        #
        index = self.indexAt(event.pos())

        sellst = self.selectedList()  # bruce 070507 move earlier

        DEBUG2 = True

        if index.isValid():
            thisnode = index.internalPointer().node

            # bruce 070507 bring in some code from modelTreeGui.py
            alreadySelected = (thisnode in sellst)

            item = index.internalPointer()
            rect = self.visualRect(index)
            if DEBUG2:
                print("visualRect coords", rect.left(), rect.right(), rect.top(), rect.bottom())
            # qfm = QFontMetrics(QLineEdit(self).font())
            # rect.setWidth(qfm.width(item.node.NameText) + _ICONSIZE[0] + 4)
            if DEBUG2:
                print("visualRect coords, modified:", rect.left(), rect.right(), rect.top(), rect.bottom())
                # looks like icon and text, a bit taller than text (guesses)
            eventInRect = rect.contains(event.pos())
            if DEBUG2:
                print("valid index: eventInRect = %r, item = %r, index = %r, alreadySelected = %r" % \
                      (eventInRect, item, index, alreadySelected))  #######
        else:
            thisnode = item = None
            alreadySelected = eventInRect = False

        if not eventInRect:
            # nothing to drag, but [bruce 070507] let super handle it (for dragging over nodes to select)
            self.drag_is_not_DND = True  ### not yet used
            # QTreeView.mouseMoveEvent(self, event)
            return

        if thisnode in sellst:
            # if dragging something selected, drag along all other selected ones
            dragged_nodes = sellst
        else:
            # if dragging something unselected, ignore any selected ones
            dragged_nodes = [thisnode]
        qdrag = QDrag(self)
        drag_type = 'move'  # how do I decide between 'move' and 'copy'?
        self.drag = (dragged_nodes, drag_type, qdrag)
        mimedata = QMimeData()
        mimedata.setText("need a string here for a valid mimetype")
        qdrag.setMimeData(mimedata)
        display_prefs = {}
        pixmap = dragged_nodes[0].node_icon(display_prefs)
        qdrag.setPixmap(pixmap)
        qdrag.setHotSpot(QPoint(-8, 8))
        qdrag.start()

    def mousePressEvent(self, event):
        self.drag_is_not_DND = False  # don't know yet
        qp = event.globalPos()  # clone the point to keep it constant
        self.mouse_press_qpoint = QPoint(qp.x(), qp.y())
        self.mouse_press_event = QMouseEvent(event.type(),
                                             QPoint(event.x(), event.y()),
                                             event.button(), event.buttons(),
                                             event.modifiers())

    def mouseReleaseEvent(self, event):
        self.drag_is_not_DND = False
        if self.drag is None:
            pass
            # QTreeView.mousePressEvent(self, self.mouse_press_event)
        self.drag = None
        # QTreeView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        # menu = QMenu(self)
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            item = self.indexAt(pos).internalPointer()
            node = self.item_to_node_dict[item]
            nodeset = [node]  # ? ? ? ?
            optflag = False  # ? ? ? ?
            cmenu_spec = self.treemodel.make_cmenuspec_for_set(nodeset, optflag)
            for x in cmenu_spec:
                if x is not None:
                    str, thunk = x[:2]
                    # act = QAction(str, self)
                    # act.setEnabled("disabled" not in x[2:])
                    # self.connect(act, SIGNAL("triggered()"), thunk)
                    # menu.addAction(act)
                    pass
                else:
                    pass
                    # menu.addSeparator()
                    # menu.exec_(event.globalPos())

    def flags(self, index):
        # Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class treeCategoryModel(QAbstractItemModel):
    def __init__(self, fileLocation=None, headers=("Item", "Value", "Description"),
                 DisplayItems=['title', 'key', 'desc'], sqlStr=None, inParent=None):
        super(treeCategoryModel, self).__init__(inParent)

        self.fileLocation = fileLocation

        self.categories = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.strSQL = sqlStr
        self.Headers = headers
        self.fieldNameCount = None
        self.fieldNames = None
        self.fieldDict = None
        self.DisplayItems = DisplayItems
        self.ColumnsViewed = len(self.DisplayItems)
        self.categorylist = []

    def setFileLocation(self, FileLocation):
        self.fileLocation = FileLocation

    def listCategories(self):
        return self.categorylist

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def data(self, index, role):

        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(index.column())
        if role == Qt.UserRole:
            if item:
                return item.Header
        else:
            pass
        return QVariant()

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                    role == Qt.DisplayRole):
            try:
                return QVariant(self.Headers[column])
            except IndexError:
                pass

        return QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self):

        modelData = QAbstractItemModel()
        conn = self.session.connection()
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount

        recordrow = 0
        for record in cursor.fetchall():  # cursors are iterable
            for column in range(self.fieldNameCount):
                modelData.setItem(recordrow, column, QStandardItem(str(record[column])))
                recordrow += 1

        # Header Data
        modelData.sort(3, Qt.AscendingOrder)

        fieldColumn = 0
        for headerName in cursor.description:
            #print(headerName[0])
            modelData.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
            fieldColumn += 1

        cursor.close()
        conn.close()

        return modelData

    def setupModelData(self):
        # 0- TreeID
        # 1 - Category
        # 2 - Data in list format set by ColumnCount

        conn = self.session.connection()
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        for treeRecords in cursor.fetchall():
            # Tree_id, Category, Display
            Display = []

            for item in self.DisplayItems:
                Display.append(treeRecords[self.fieldDict[item]])

            TIC = treeCategory_class(Tree_id=treeRecords[self.fieldDict['id']],
                                     Category=treeRecords[self.fieldDict['section']],
                                     Display=Display)
            CatExist = False
            for category in self.categories:
                if category.Category == treeRecords[self.fieldDict['section']]:
                    CatExist = True
                    break

            if not CatExist:
                # Root Level Entries
                self.categorylist.append(treeRecords[self.fieldDict['section']])
                self.categories.append(TIC)
                newparent = TreeItem(None, treeRecords[self.fieldDict['section']], self.rootItem)
                newparent.ColumnsViewed = self.ColumnsViewed
                self.rootItem.appendChild(newparent)
                self.parents[treeRecords[self.fieldDict['section']]] = newparent
            try:
                parentItem = self.parents[treeRecords[self.fieldDict['section']]]
                #print(Display)
                newItem = TreeItem(TIC, Display, parentItem)
                newItem.ColumnsViewed = self.ColumnsViewed
                # Need to figure how Header is involved
                TIC.Header = treeRecords[self.fieldDict['title']]
                parentItem.appendChild(newItem)
            except:
                pass

    def searchModel(self, person):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if person == child.ItemName:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])

        return retarg

    def find_GivenName(self, cname):
        app = None
        for category in self.categories:
            if category.Category == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)


class customStyledTable(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)

    def paintEvent(self, event):
        super(customStyledTable, self).paintEvent(event)

        # set the pen
        pen = QPen(Qt.white, 4)

        # Create the painter
        painter = QPainter(self.viewport())

        # Shortcuts to vertical and horizontal headers
        vh = self.verticalHeader()
        hh = self.horizontalHeader()

        # Get the first and last rows that are visible in the view and if the
        # last visiable row returns -1 set it to the row count
        firstVisualRow = max([vh.visualIndexAt(0), 0])
        lastVisualRow = vh.visualIndexAt(vh.viewport().height())
        if lastVisualRow == -1:
            lastVisualRow = self.model().rowCount(self.rootIndex()) - 1

        # Get the first and last columns that are visible in the view and if
        # if the last visible column is -1 set it to the column count.
        firstVisualColumn = max([hh.visualIndexAt(0), 0])
        lastVisualColumn = hh.visualIndexAt(hh.viewport().width())
        if lastVisualColumn == -1:
            lastVisualColumn = hh.count() - 1

        # Iterate through each row and column drawing only the
        # bottom and left side lines for each cell. Skipping rows and columns
        # that are hidden
        for vrow in range(firstVisualRow, lastVisualRow + 1, 2):
            row = vh.logicalIndex(vrow)
            FirstRow = (vrow == 0)
            if vh.isSectionHidden(row):
                continue
            # Get top left Y coordinate and row height
            rowY = self.rowViewportPosition(row)
            rowh = self.rowHeight(row)
            for vcol in range(firstVisualColumn, lastVisualColumn + 1):
                col = hh.logicalIndex(vcol)
                FirstColumn = (vcol == 0)
                if hh.isSectionHidden(col):
                    continue
                # Get top left X coordinate and column width
                colX = self.columnViewportPosition(col)
                colw = self.columnWidth(col)

                # Get the model index
                index = self.model().createIndex(row, col)

                # Specify top, bottom, left and right of the cell
                top = rowY
                bottom = rowY
                left = colX
                right = colX + colw

                # Save the painter and set the pen
                painter.save()
                painter.setPen(pen)

                # Draw Horizontal Lines
                painter.drawLine(left, bottom, right, bottom)

                # Restore painter
                painter.restore()


def cloneBranch(self, conn, cursor, SQLBranchParent, DestinationTable, GroupID, ParentID, optionalLevels):
    # This is used to put the entire contents of a branch into another branch.  It can be the same table or another table.
    #print(treeItemDict)

    SQLSelect = "SELECT tblEquipmentList.TreeID, " \
                "tblEquipmentList.ParentTreeID, " \
                "tblEquipmentList.Level, " \
                "tblEquipmentList.Order, " \
                "tblEquipmentList.Display, " \
                "tblEquipmentList.Icon, " \
                "tblEquipmentList.ForeColor, " \
                "tblEquipmentList.Tag, " \
                "tblEquipmentList.Expanded, " \
                "tblEquipmentList.Highlighted, " \
                "Null as LinkedData, Null as AdditionalItems, Null as ListNumber"
    SQLFrom = " FROM tblEquipmentList"
    SQLOrder = " ORDER BY tblEquipmentList.Level, tblEquipmentList.Order;"

    SQLWhere = BSWhere(Field, Value, Scope, DataType)

    cursor.execute('''INSERT INTO TreeItems(Tree_id, TreeGroup_id, ParentTree_id, DescriptorMaster_id, DescriptorTable_id, Descriptor_id,
                    ItemMaster_id, ItemTable_id, Item_id, DisplayName, ItemOrder, FlattenedOrder, ItemLevel,
                    ForeColor, expanded, Header)
              VALUES(:Tree_id, :TreeGroup_id, :ParentTree_id, :DescriptorMaster_id, :DescriptorTable_id, :Descriptor_id,
                    :ItemMaster_id, :ItemTable_id, :Item_id, :DisplayName, :ItemOrder, :FlattenedOrder, :ItemLevel,
                    :ForeColor, :expanded, :Header)''', treeItemDict)
    newID = cursor.lastrowid

    cursor.execute("UPDATE TreeItems SET Tree_id = {id} WHERE id = {id}". \
                   format(id=newID))

    cursor.close()