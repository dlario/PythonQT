from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
#from PySide6.uic import *

def loadTableCombo(conn, rowCount, columnData, tblTable):
    #Going to have to put this back in the main code till i figure out how to hook the on change
    #This little ditty is used to load data into a column of a table.

    cursor = conn.cursor()
    for row in range(rowCount):
        referenceList = tblTable.model().index(row, columnData["Values"]).data()
    
        if referenceList != None:
    
            SQLSelect = "SELECT id," \
                        "name," \
                        "reference"
            SQLFrom = " FROM %s" % referenceList
            SQLOrder = " ORDER BY name"
    
            strSQL = SQLSelect + SQLFrom + SQLOrder
    
            # cursor = conn2.cursor()
            cursor.execute(strSQL)
            data = cursor.fetchall()
    
            listDataModel2 = QStandardItemModel(0, 2)
    
            for row2, ItemName in enumerate(data):
                itemID = QStandardItem("%i" % ItemName[0])
                listDataModel2.setItem(row2, 0, itemID)
                listDataModel2.setItem(row2, 1, QStandardItem(ItemName[1]))
    
                if ItemName[2] != None:
                    referenceID = QStandardItem("%i" % ItemName[2])
                    listDataModel2.setItem(row2, columnData["Reference Table"], referenceID)
    
            #tblTable.openPersistentEditor(listDataModel2.index(row, columnData["Values"]))
            #c = ComboModel(None, dataModel=listDataModel2, row=row, column=columnData["Values"])
            #i = tblTable.model().index(row, columnData["Values"])
            #tblTable.setIndexWidget(i, c)

    return listDataModel2

    cursor.close()


class TableLineEditModel(QLineEdit):
    textChanged2 = Signal([dict])

    def __init__(self, parent, *args, **kwargs):
        super(TableLineEditModel, self).__init__(parent)

        #self.Attributes = kwargs['attdict']
        self.column = kwargs['column']
        self.row = kwargs['row']
        self.dataout = {}
        self.dataout['column'] = kwargs['column']
        self.dataout['row'] = kwargs['row']
        self.newItemName = ""

        self.textChanged.connect(self.textChangedDictionary)

    def column(self):
        return self.x

    def row(self):
        return self.y

    @Slot(dict)
    def textChangedDictionary(self, text):
        #print("Combo Index changed2:", index)
        self.dataout['Text'] = text
        self.textChanged2.emit(self.dataout)

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
class TableComboModel(QComboBox):
    #Should combine with to customWidgets
    currentIndexChanged2 = Signal([dict])

    def __init__(self, parent, *args, **kwargs):
        super(TableComboModel, self).__init__(parent)
        #super(ComboModel, self).currentIndexChanged[dict].connect(self.currentIndexChangedDictionary)

        self.setModel(kwargs['dataModel'])
        self.setModelColumn(1)
        self.column = kwargs['column']
        self.row = kwargs['row']
        self.dataout = {}
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

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.dbIds)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    def data(self, index, role=Qt.DisplayRole):
        #print('ComboModel data')
        if not index.isValid() or ( role != Qt.DisplayRole and role != Qt.EditRole ):
            print('ComboModel return invalid QVariant')
            return
        if index.column() == 0:
            return self.dbIds[index.row()]
        if index.column() == 1:
            return self.dbValues[index.row()]
        print('ComboModel return invalid QVariant')
        return 

    @Slot(dict)
    def currentIndexChangedDictionary(self, index):
        #print("Combo Index changed2:", index)
        self.dataout['index'] = index
        self.currentIndexChanged2.emit(self.dataout)

    @Slot(str)
    def on_newInformation(self, newName):
        if newName != "":
            self.newItemName = newName
        else:
            #Create a new model that has old and new data
            cmbTableModel = QStandardItemModel(0, 1, self)
            cmbTableModel.setItem(0, 1, QStandardItem(self.newItemName))

            for row in range(self.dataout['dataModel'].rowCount()):
                cmbTableModel.setItem(row+1, 1, QStandardItem(self.dataout['dataModel'].index(row,1).data()))

            self.setModel(cmbTableModel)

    @Slot(int)
    def on_currentIndexChanged(self, index):
        pass
        #print("Combo Index changed:", index) #, self.sender().x(), self.y)
        #self.currentIndexChanged2.emit(self.dataout)


class customTableModel(QAbstractTableModel):
    rowSelected = Signal(QModelIndex)

    def __init__(self, parent=None, *args): 
        super(QAbstractTableModel, self).__init__()
        self.dataTable = None
        self.database = None
        self.ColumnValues = []
        self.headerdata = []

    def update(self, dataIn):
        print('Updating Model')
        self.datatable = dataIn
        print('Datatable : {0}'.format(self.datatable))

    def rowCount(self, parent=QModelIndex()):
        return len(self.datatable.index) 
        
    def columnCount(self, parent=QModelIndex()):
        return len(self.datatable.columns.values)

    def selectionChanged(self, selected, deselected):
        QTableView.selectionChanged(self, selected, deselected)
        print("hi")
        if selected.indexes():
            self.rowSelected.emit(selected.indexes()[0])

    def data(self, index, role=Qt.DisplayRole):
        #print 'Data Call'
        #print index.column(), index.row()
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            #return QtCore.QVariant(str(self.datatable.iget_value(i, j)))
            return '{0}'.format(self.datatable.iget_value(i, j))
        else:
            return
    
    def flags(self, index):
        return Qt.ItemIsEnabled

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return

    def on_action_triggered(self, action):
        self.setColumnHidden(action.index, not action.isChecked())
        header = self.horizontalHeader()
        if action.isChecked() and header.sectionSize(action.index) == 0:
            header.resizeSection(action.index, header.defaultSectionSize())

    def on_unsorted_triggered(self, checked):
        self.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)
        self.model().undoSorting()

    def mousePressEvent(self, event):
        pressed = False
        if event.button() == Qt.RightButton:
            index = self.indexAt(event.pos())
            pressed = True

        QTableView.mousePressEvent(self, event)

        if pressed:
            self.rightButtonPressed.emit(index)

    @Slot()
    def currentIndexChanged(self, ind):
        print("Combo Index changed {0} {1} : {2}".format(ind, self.sender().currentIndex(), self.sender().currentText()))

class sqlTableModel(QSqlTableModel):
    def __init__(self, parent=None):
        super(sqlTableModel, self).__init__(parent)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            value = value.strip() if type(value) == str else value

        return super(sqlTableModel, self).setData(index, value, role)

    def flags(self, index):
        itemFlags = super(sqlTableModel, self).flags(index)

        if index.column() != 0:
            return itemFlags | Qt.ItemIsEditable

        return itemFlags ^ Qt.ItemIsEditable #  First column not editable

    def setDatabase(self, nameDatabase):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(nameDatabase)

        return self.database.open()

    def setTable(self, nameTable):
        self.model = sqlTableModel(self)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setTable(nameTable)
        self.model.select()

        self.view.setModel(self.model)

    def saveTable(self):
        if self.model.submitAll():
            return True

        self.model.database().rollback()
        return False

    class ComboDelegate(QItemDelegate):
        """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):

        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        li = []
        li.append("Zero")
        li.append("One")
        li.append("Two")
        li.append("Three")
        li.append("Four")
        li.append("Five")
        combo.addItems(li)
        #self.connect(combo, SIGNAL("currentIndexChanged(int)"), self, SLOT("currentIndexChanged()"))
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())

    @Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())