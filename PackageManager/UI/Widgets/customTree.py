#http://pyqt.sourceforge.net/Docs/PyQt4/qtreeview.html

import sys
#import pyodbc
import sqlite3

from copy import *
from pickle import dumps, load, loads
from io import *

import os
import datetime
#from PackageManager.Database.DatabaseTools import DatabaseConnection

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

            #self.treeDict = treeDict
            #the first should replace everything else in the future.
            #treemodel.currentTreeItem(self, ID=None) would load the dictionary

            self.treeID = treeDict['treeID']
            self.TreeGroupID = treeDict['treeGroupID']
            self.ParentTreeID = treeDict['parentTreeID']
            self.DescriptorMaster = treeDict['descriptorMasterTable']
            self.DescriptorMasterID = treeDict['descriptorMasterID']
            self.DescriptorTable = treeDict['descriptorTable']
            self.DescriptorTableID = treeDict['descriptorTableID']
            self.Descriptor = treeDict['descriptorID']
            self.DescriptorName = treeDict['descriptorName']
            self.ItemMaster = treeDict['itemMasterTable']
            self.ItemMaster = treeDict['itemMasterID']
            self.ItemTable = treeDict['itemTable']
            self.ItemTableID = treeDict['itemTableID']
            self.Item = treeDict['itemID']
            self.ItemName = treeDict['itemName']
            self.Display = []

            if treeDict['displayName'] != None:
                DisplayValue = treeDict['displayName']
            else:
                DisplayValue = ""
                if self.DescriptorName != None:
                    DisplayValue += str(self.DescriptorName)
                if self.ItemName != None:
                    DisplayValue += str(self.ItemName)
                if self.DisplayName != None:
                    DisplayValue += str(self.DisplayName)

            self.Display.append(DisplayValue)
            self.Order = treeDict['itemOrder']
            self.FlattenedOrder = treeDict['flattenedOrder']
            self.Level = treeDict['itemLevel']
            self.ForeColor = treeDict['foreColor']
            self.Expanded = treeDict['expanded']
            self.Header = treeDict['header']

class treeCategory_class(object):
    '''
    A Specialized SubClass of the TreeItemBaseClass
    '''
    def __init__(self, treeID = None, Category = None, Header = None, Display = None):
        self.treeID = treeID
        self.Category = Category
        self.Header = Header
        self.Display = Display

class sqlStandardItemModel(QStandardItemModel):
    def __init__(self, Parent = None, fileLocation = None, sqlStr = None, **kwargs):
        super(sqlStandardItemModel, self).__init__(**kwargs)

        self.SQLString = sqlStr
        self.fileLocation = fileLocation
        #need to separate this
        self.databaseName = fileLocation
        #print(self.fileLocation)
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None

        #self.setupModelData()

    def setupModelData2(self):
        conn = DatabaseConnection.dbConnect(self.fileLocation)

        cursor = conn.cursor()
        cursor.execute(self.SQLString)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        ColumnName = DatabaseConnection.ColumnNames(self.fileLocation, self.SQLString)

        recordrow = 0
        for record in cursor.fetchall(): # cursors are iterable
            for recordcolumns in range(self.fieldNameCount):
                self.setItem(recordrow, recordcolumns, QStandardItem(str(record[recordcolumns])))
            recordrow += 1
        cursor.close()
        conn.close()

    def setupModelData(self):

        conn = DatabaseConnect.dbConnect(self.fileLocation)

        cursor = conn.cursor()
        cursor.execute(self.SQLString)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        #print(self.SQLString)
        #ColumnName = DatabaseConnect.ColumnNames(self.fileLocation, self.SQLString)

        recordrow = 0
        for record in cursor.fetchall(): # cursors are iterable
            for recordcolumns in range(self.fieldNameCount):
                if self.fieldNames[recordcolumns] == "Display":
                    Display = []
                    Display.append(str(record[6]))
                    self.setItem(recordrow, recordcolumns, QStandardItem(Display[0]))
                else:
                    self.setItem(recordrow, recordcolumns, QStandardItem(str(record[0])))

            recordrow += 1

    def data(self, index, role):
         if not index.isValid():
             return
         elif role != Qt.DisplayRole:
             return
         return self.setItem[index.row()][index.column()]

    def headerCount(self):
        return self.fieldNameCount

    def headerData(self, column = 0, orientation = Qt.Horizontal, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            data = self.fieldNames[column]
        else:
            data = QAbstractTableModel.headerData (self, column, orientation, role)
        return data

    def CloneBranch(self, ParentID, ParentLevel, CloneID):
        pass

class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''
    def __init__(self, TreeClassItem, header, parentItem):
        self.TreeClassItem = TreeClassItem
        self.parentItem = parentItem
        self.header = header #This is the display in tree value
        self.Display = []  #These are the additional column items
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
        #This will have to be updated with the length of the display list
        return self.ColumnsViewed

    def data(self, column):

        FileLocation = ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Icon Location")
        Filelocation = FileLocation + "Excel.bmp"
        iconQPixmap = QPixmap(FileLocation)

        #This Allows a sub class to be put in that can store additional information
        if self.TreeClassItem == None:
            try:
                if column == 0:
                    return self.header
                if column == 1:
                    return

                    return self.Display[column]
            except:
                pass
        else:
            try:
                return self.TreeClassItem.Display[column]
            except:
                pass
        return

    def setData(self,index,value,role=Qt.EditRole):
        if role==Qt.EditRole:
            row =index.row()
            column=index.column()
            ch=(value)

            self.__colors[row][column]=ch
            self.dataChanged.emit(index,index)
            return True

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

class treeModel(QAbstractItemModel):
    def __init__(self, inParent = None, fileLocation = None, sqlStr = None, **kwargs):
        super(treeModel, self).__init__(inParent, **kwargs)

        self.Display = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0 : self.rootItem}
        self.fileLocation = fileLocation
        #Need split
        self.tableName = "treeItems"
        self.sqlStr = sqlStr
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None
        #self.Headers =  ("Category", "Item", "Description")
        self.Headers = []
        self.Headers.append("Item")

        self.RecordCount = 0

    def setFileLocation(self,FileLocation):
        self.fileLocation = FileLocation

    def currentTreeItem(self, ID=None):
        treeItemDict = []

        conn = DatabaseConnect.dbConnect(self.fileLocation)
        cursor = conn.cursor()

#Need to find out the custom database table name

        SQLSelect = "SELECT treeItems.id," \
                    "descriptorMasterTable.name AS descriptorMasterTable," \
                    "itemMasterTable.name AS itemMasterTable," \
                    "descriptorTable.referenceTable AS descriptorTable," \
                    "itemTable.referenceTable AS itemTable"

        SQLFrom = " FROM treeItems " \
                  "LEFT JOIN descriptorMasterTable ON (treeItems.descriptorMasterID = descriptorMasterTable.id)" \
                  "LEFT JOIN itemTable ON (treeItems.itemTableID = itemTable.id)" \
                  "LEFT JOIN descriptorTable ON (treeItems.descriptorTableID = descriptorTable.id)" \
                  "LEFT JOIN itemMasterTable ON (treeItems.itemMasterID = itemMasterTable.id)"

        SQLWhere = " WHERE treeItems.id = %i" % ID

        SQLQuery = SQLSelect + SQLFrom + SQLWhere
        cursor.execute(SQLQuery)

        record = cursor.fetchone()

        #print(record[0], record[1], record[2], record[3], record[4])

        SQLSelect = "SELECT treeItems.id, " \
                    "treeItems.treeGroupID, " \
                    "treeItems.treeID, " \
                    "treeItems.parentTreeID, " \
                    "treeItems.descriptorMasterID, " \
                    "treeItems.descriptorTableID, " \
                    "treeItems.descriptorID, " \
                    "treeItems.itemMasterID, " \
                    "treeItems.itemTableID, " \
                    "treeItems.itemID, " \
                    "treeItems.displayName, " \
                    "treeItems.itemOrder, " \
                    "treeItems.flattenedOrder, " \
                    "treeItems.itemLevel, " \
                    "treeItems.foreColor, " \
                    "treeItems.expanded, " \
                    "treeItems.header, " \
                    "descriptorMasterTable.name AS descriptorMasterTable," \
                    "itemMasterTable.name AS itemMasterTable "

        AddNone = []

        if record[1] != None:
            SQLSelect += ", %s.referenceTable AS descriptorTable " % record[1]
        else:
            AddNone.append("descriptorTable")
        if record[2] != None:
            SQLSelect += ", %s.referenceTable AS itemTable " % record[2]
        else:
            AddNone.append("itemTable")
        if record[3] != None:
            SQLSelect += ", %s.name AS descriptorName " % record[3]
        else:
            AddNone.append("descriptorName")
        if record[4] != None:
            SQLSelect += ", %s.name AS itemName" % record[4]
        else:
            AddNone.append("itemName")

        SQLFrom = " FROM treeItems " \
                  "LEFT JOIN descriptorMasterTable ON (treeItems.descriptorMasterID = descriptorMasterTable.id) " \
                  "LEFT JOIN itemMasterTable ON (treeItems.itemMasterID = itemMasterTable.id) "

        if record[1] != None:
            SQLFrom += "LEFT JOIN %s ON (treeItems.%sID = %s.id) " % (record[1], record[1], record[1])
        if record[2] != None:
            SQLFrom += "LEFT JOIN %s ON (treeItems.%sID = %s.id) " % (record[2], record[2], record[2])
        if record[3] != None:
            SQLFrom += "LEFT JOIN %s ON (treeItems.descriptorID = %s.id) " % (record[3], record[3])
        if record[4] != None:
            SQLFrom += "LEFT JOIN %s ON (treeItems.itemID = %s.id)" % (record[4], record[4])

        SQLWhere = " WHERE treeItems.id = %i" % ID

        SQLQuery = SQLSelect + SQLFrom + SQLWhere

        cursor.execute(SQLQuery)

        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]

        record = cursor.fetchone()

        treeItemDict = {self.fieldNames[i]: record[i] for i, item in enumerate(range(0,self.fieldNameCount))}

        for item in AddNone:
            treeItemDict[item] = None

        #print(treeItemDict)
        return treeItemDict

    def addTreeItem(self, currentSelectedIndex, treeItemDict):
        conn = DatabaseConnect.dbConnect(self.fileLocation)
        cursor = conn.cursor()

        #print(treeItemDict)
        cursor.execute('''INSERT INTO treeItems(treeID, treeGroupID, parentTreeID, descriptorMasterID, descriptorTableID, descriptorID,
                        itemMasterID, itemTableID, itemID, displayName, itemOrder, flattenedOrder, itemLevel,
                        foreColor, expanded, header)
                  VALUES(:treeID, :treeGroupID, :parentTreeID, :descriptorMasterID, :descriptorTableID, :descriptorID,
                        :itemMasterID, :itemTableID, :itemID, :displayName, :itemOrder, :flattenedOrder, :itemLevel,
                        :foreColor, :expanded, :header)''', treeItemDict)
        newID = cursor.lastrowid

        cursor.execute("UPDATE treeItems SET treeID = {id} WHERE id = {id}".\
                       format(id=newID))
        conn.commit()

        #treeItemDict = self.currentTreeItem(newID)

        cursor.close()
        conn.close()

        TIC = treeItem_class(treeItemDict)
        #print("level", treeItemDict['itemLevel'])

        if treeItemDict['itemLevel'] == 0:
            #Root Level Entries
            newparent = TreeItem(TIC, treeItemDict['header'], self.rootItem)
            self.rootItem.appendChild(newparent)
            #Create the Dictonary Linking Values
            self.parents[treeItemDict['treeID']] = newparent
        else:
            #print("parent", treeItemDict['parentTreeID'])
            #print(self.parents)
            parentItem = self.parents[int(treeItemDict['parentTreeID'])]
            newItem = TreeItem(TIC, treeItemDict['header'], parentItem)

            parentItem.appendChild(newItem)
            self.parents[treeItemDict['treeID']] = newItem

            #self.insertRow(0, currentSelectedIndex)

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

    def setupModelData(self):
        conn = DatabaseConnect.dbConnect(self.fileLocation)
        cursor = conn.cursor()
        cursor.execute(self.sqlStr)

        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        self.RecordCount = cursor.rowcount

        for treeRecords in cursor.fetchall():
            #So that we can display stuff in different columns.
            Display = []

            Display.append(treeRecords[self.fieldDict['displayName']])

            treeItemDict = self.currentTreeItem(treeRecords[self.fieldDict['id']])
            #print(treeItemDict)
            TIC = treeItem_class(treeItemDict)

            if treeItemDict['itemLevel'] == 0:
                #Root Level Entries
                newparent = TreeItem(TIC, treeRecords[4], self.rootItem)
                self.rootItem.appendChild(newparent)
                #Create the Dictonary Linking Values
                self.parents[treeItemDict['treeID']] = newparent
            else:
                parentItem = self.parents[treeItemDict['parentTreeID']]
                newItem = TreeItem(TIC, treeRecords[4], parentItem)
                parentItem.appendChild(newItem)
                self.parents[treeItemDict['treeID']] = newItem
                ItemDisplay = parentItem.TreeClassItem.Display
                #ItemDisplay.append(treeRecords[4])
                #newItem.TreeClassItem.Display = ItemDisplay
                #Display.insert(0,parentItem.TreeClassItem.Display)
                #TIC.Display.insert(0,parentItem.TreeClassItem.Display)
                #print(parentItem.TreeClassItem.Display)
        cursor.close()
        conn.close()

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
        self.insertRow(len(parentNode)-1, parentIndex)
        #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),parentIndex, parentIndex)
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
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            try:
                return item.data(index.column())
            except:
                pass

        if role == Qt.UserRole:
            if item:
                return item.header
        return

    def returnHeaderData(self):
        SQLQuery = 'select * from %s' % (self.datatable)

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
        role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

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

    def treeTableModel(self, SWhere = None, Orientation = "Vertical"):
        modelData = QAbstractItemModel

        conn = DatabaseConnect.dbConnect(self.fileLocation)
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = None
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        if Orientation == "Vertical":
            recordrow = 0
            for record in cursor.fetchall(): # cursors are iterable
                for columns in range(self.fieldNames):
                    modelData.setItem(recordrow, columns, QStandardItem(str(record[columns])))
                recordrow += 1

            #Header Data
            modelData.sort(3,Qt.AscendingOrder)

            fieldColumn = 0
            for headerName in cursor.description:
                #print(headerName[0])
                modelData.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
                fieldColumn += 1
        else:
            recordcolumn = 0
            for record in cursor.fetchall(): # cursors are iterable
                for rows in range(self.fieldNames):
                    modelData.setItem(rows, recordcolumn, QStandardItem(str(record[rows])))
                recordcolumn += 1

            #Header Data
            #modelData.sort(3,Qt.AscendingOrder)

            #fieldColumn = 0
            #for headerName in cursor.description:
                #print(headerName[0])
                #modelData.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
                #fieldColumn += 1

        cursor.close()
        conn.close()

        return modelData

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
            if category.cname == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

    def paintEvent(self, event):
        painter = QPainter(self.viewport()) #See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        painter.drawEllipse(self.center,10,10)
        QTableWidget.paintEvent(self,event)

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
            pass #QTreeView.mouseMoveEvent(self, event)
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

        sellst = self.selectedList() # bruce 070507 move earlier

        DEBUG2 = True

        if index.isValid():
            thisnode = index.internalPointer().node

            #bruce 070507 bring in some code from modelTreeGui.py
            alreadySelected = (thisnode in sellst)

            item = index.internalPointer()
            rect = self.visualRect(index)
            if DEBUG2:
                print("visualRect coords",rect.left(), rect.right(), rect.top(), rect.bottom())
            #qfm = QFontMetrics(QLineEdit(self).font())
            #rect.setWidth(qfm.width(item.node.name) + _ICONSIZE[0] + 4)
            if DEBUG2:
                print ("visualRect coords, modified:",rect.left(), rect.right(), rect.top(), rect.bottom())
                # looks like icon and text, a bit taller than text (guesses)
            eventInRect = rect.contains(event.pos())
            if DEBUG2:
                print ("valid index: eventInRect = %r, item = %r, index = %r, alreadySelected = %r" % \
                      (eventInRect, item, index, alreadySelected))#######
        else:
            thisnode = item = None
            alreadySelected = eventInRect = False

        if not eventInRect:
            # nothing to drag, but [bruce 070507] let super handle it (for dragging over nodes to select)
            self.drag_is_not_DND = True ### not yet used
            #QTreeView.mouseMoveEvent(self, event)
            return

        if thisnode in sellst:
            # if dragging something selected, drag along all other selected ones
            dragged_nodes = sellst
        else:
            # if dragging something unselected, ignore any selected ones
            dragged_nodes = [ thisnode ]
        qdrag = QDrag(self)
        drag_type = 'move'  # how do I decide between 'move' and 'copy'?
        self.drag = (dragged_nodes, drag_type, qdrag)
        mimedata = QMimeData()
        mimedata.setText("need a string here for a valid mimetype")
        qdrag.setMimeData(mimedata)
        display_prefs = { }
        pixmap = dragged_nodes[0].node_icon(display_prefs)
        qdrag.setPixmap(pixmap)
        qdrag.setHotSpot(QPoint(-8, 8))
        qdrag.start()

    def mousePressEvent(self, event):
        self.drag_is_not_DND = False # don't know yet
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
            #QTreeView.mousePressEvent(self, self.mouse_press_event)
        self.drag = None
        #QTreeView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        #menu = QMenu(self)
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            item = self.indexAt(pos).internalPointer()
            node = self.item_to_node_dict[item]
            nodeset = [ node ] # ? ? ? ?
            optflag = False  # ? ? ? ?
            cmenu_spec = self.treemodel.make_cmenuspec_for_set(nodeset, optflag)
            for x in cmenu_spec:
                if x is not None:
                    str, thunk = x[:2]
                    #act = QAction(str, self)
                    #act.setEnabled("disabled" not in x[2:])
                    #self.connect(act, SIGNAL("triggered()"), thunk)
                    #menu.addAction(act)
                    pass
                else:
                    pass
                    #menu.addSeparator()
            #menu.exec_(event.globalPos())

    def flags(self, index):
        #Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable

class treeCategoryModel(QAbstractItemModel):
    def __init__(self, fileLocation = None, headers = ("Item", "Value", "Description"),
                 DisplayItems = ['title', 'key', 'desc'], sqlStr = None, inParent = None):
        super(treeCategoryModel, self).__init__(inParent)

        self.fileLocation = fileLocation

        self.categories = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0 : self.rootItem}
        self.strSQL = sqlStr
        self.Headers = headers
        self.fieldNameCount = None
        self.fieldNames = None
        self.fieldDict = None
        self.DisplayItems = DisplayItems
        self.ColumnsViewed = len(self.DisplayItems)
        self.categorylist = []

    def setFileLocation(self,FileLocation):
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
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(index.column())
        if role == Qt.UserRole:
            if item:
                return item.header
        else:
            pass
        return

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
        role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

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
        conn = DatabaseConnect.dbConnect(self.fileLocation)
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount

        recordrow = 0
        for record in cursor.fetchall(): # cursors are iterable
            for column in range(self.fieldNameCount):
                modelData.setItem(recordrow, column, QStandardItem(str(record[column])))
                recordrow += 1

        #Header Data
        modelData.sort(3,Qt.AscendingOrder)

        fieldColumn = 0
        for headerName in cursor.description:
            #print(headerName[0])
            modelData.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
            fieldColumn += 1

        cursor.close()
        conn.close()

        return modelData

    def setupModelData(self):
        #0- TreeID
        #1 - Category
        #2 - Data in list format set by ColumnCount

        conn = sqlite3.connect(self.fileLocation)
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}
        #print(self.fieldNames)

        for treeRecords in cursor.fetchall():
            #treeID, Category, Display
            Display = []

            for item in self.DisplayItems:

                Display.append(treeRecords[self.fieldDict[item]])

            TIC = treeCategory_class(treeID = treeRecords[self.fieldDict['id']],
                                     Category = treeRecords[self.fieldDict['section']],
                                     Display = Display)
            CatExist = False
            for category in self.categories:
                if category.Category == treeRecords[self.fieldDict['section']]:
                    CatExist = True
                    break

            if not CatExist:
                #Root Level Entries
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
                #Need to figure how header is involved
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
        print(retarg)
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
    def __init__(self, parent = None):
        QTableView.__init__(self, parent)

    def paintEvent(self, event):
        super(customStyledTable, self).paintEvent(event)

        #set the pen
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
    #This is used to put the entire contents of a branch into another branch.  It can be the same table or another table.
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


    cursor.execute('''INSERT INTO treeItems(treeID, treeGroupID, parentTreeID, descriptorMasterID, descriptorTableID, descriptorID,
                    itemMasterID, itemTableID, itemID, displayName, itemOrder, flattenedOrder, itemLevel,
                    foreColor, expanded, header)
              VALUES(:treeID, :treeGroupID, :parentTreeID, :descriptorMasterID, :descriptorTableID, :descriptorID,
                    :itemMasterID, :itemTableID, :itemID, :displayName, :itemOrder, :flattenedOrder, :itemLevel,
                    :foreColor, :expanded, :header)''', treeItemDict)
    newID = cursor.lastrowid

    cursor.execute("UPDATE treeItems SET treeID = {id} WHERE id = {id}".\
                   format(id=newID))

    cursor.close()