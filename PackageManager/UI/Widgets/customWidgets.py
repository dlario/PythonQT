from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class widgetdata(object):
    def widgetchildren(self):
        for widget in self.centralWidget.children():
            if 1==2:
                if isinstance(widget, QLineEdit):
                    print("linedit: %s  - %s" %(widget.objectName(),widget.text()))

                if isinstance(widget, QComboBox):
                    print("combobox: %s" %(widget.objectName()))

                if isinstance(widget, QTabBar):
                    for widget2 in self.widget.children():
                        print(widget2.objectName())
                else:
                    print(widget.objectName())

            for widget in self.children():
                if isinstance(widget, QLineEdit):
                    print("linedit: %s  - %s" % (widget.objectName(), widget.text()))

                if isinstance(widget, QComboBox):
                    print("combobox: %s" % (widget.objectName()))

                else:
                    print(widget.objectName())

            #print(self.layout())

        self.loadchildren(self)


class ComboBox(QComboBox):
    """Extends QComboBox with some extra functionality:
    - remembers argument to setValue, restores correct selection after contents have been cleared/repopulated
    """

    def __init__(self, *args):
        QComboBox.__init__(self, *args)
        self.value = None
        self.currentIndexChanged.connect(self.indexChanged)

    def setValue(self, value):
        self.value = value
        ind = self.findText(value)
        if ind == -1:
            return
        self.setCurrentIndex(ind)

    def updateItems(self, values):
        """Set the list of items. Restore the last requested value, if possible"""
        val = self.value
        if val in values:
            self.blockSignals(True)  ## value will not ultimately change; don't generate any signals

        self.clear()
        self.addItems(values)

        if val in values:
            self.setCurrentItem(values.index(val))

        self.blockSignals(False)
        self.value = val  ## might have changed while we weren't looking

    def indexChanged(self, ind):
        self.value = self.itemText(ind)


    def widgetGroupInterface(self):
        return (self.currentIndexChanged, ComboBox.saveState, ComboBox.restoreState)

    def saveState(self):
        ind = self.currentIndex()
        data = self.itemData(ind)
        if not data.isValid():
            return self.itemText(ind)
        else:
            return data.toInt()[0]

    def restoreState(self, w, v):
        if type(v) is int:
            #ind = self.findData(QtCore.QVariant(v))
            ind = self.findData(v)
            if ind > -1:
                self.setCurrentIndex(ind)
                return
        #self.setCurrentIndex(self.findText(str(v)))__author__ = 'David'

class ExtendedCombo( QComboBox ):
    def __init__( self,  parent = None):
        super( ExtendedCombo, self ).__init__( parent )

        self.setFocusPolicy( Qt.StrongFocus )
        self.setEditable( True )
        self.completer = QCompleter( self )

        # always show all completions
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.pFilterModel = QSortFilterProxyModel( self )
        self.pFilterModel.setFilterCaseSensitivity( Qt.CaseInsensitive )

        self.completer.setPopup( self.view() )

        self.setCompleter( self.completer )

        self.lineEdit().textEdited.connect( self.pFilterModel.setFilterFixedString )
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel( self, model ):
        super(ExtendedCombo, self).setModel( model )
        self.pFilterModel.setSourceModel( model )
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn( column )
        self.pFilterModel.setFilterKeyColumn( column )
        super(ExtendedCombo, self).setModelColumn( column )


    def view( self ):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
      if text:
        index = self.findText(text)
        self.setCurrentIndex(index)

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

class ListModel(QAbstractListModel):
#http://duganchen.ca/a-pythonic-qt-list-model-implementation/
    Mimetype = 'application/vnd.row.list'

    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = ['line 1', 'line 2', 'line 3', 'line 4']

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() > len(self.__data):
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.__data[index.row()]

        return None

    def dropMimeData(self, data, action, row, column, parent):
        if action == Qt.IgnoreAction:
            return True
        if not data.hasFormat(self.Mimetype):
            return False
        if column > 0:
            return False

        strings = str(data.data(self.Mimetype)).split('\n')
        self.insertRows(row, len(strings))
        for i, text in enumerate(strings):
            self.setData(self.index(row + i, 0), text)

        return True

    def flags(self, index):
        flags = super(ListModel, self).flags(index)

        if index.isValid():
            flags |= Qt.ItemIsEditable
            flags |= Qt.ItemIsDragEnabled
        else:
            flags = Qt.ItemIsDropEnabled

        return flags

    def insertRows(self, row, count, parent=QModelIndex()):

        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.__data[row:row] = [''] * count
        self.endInsertRows()
        return True

    def mimeData(self, indexes):
        sortedIndexes = sorted([index for index in indexes
            if index.isValid()], key=lambda index: index.row())
        encodedData = '\n'.join(self.data(index, Qt.DisplayRole)
                for index in sortedIndexes)
        mimeData = QMimeData()
        mimeData.setData(self.Mimetype, encodedData)
        return mimeData

    def mimeTypes(self):
        return [self.Mimetype]

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self.__data[row:row + count]
        self.endRemoveRows()
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self.__data)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        self.__data[index.row()] = value
        self.dataChanged.emit(index, index)
        return True

    def supportedDropActions(self):
        return Qt.MoveAction

class SQLStandardItemModel(QStandardItemModel):
    def __init__(self ,parent = None, Database = None, SQLStr = None, **kwargs):
        QStandardItemModel.__init__(self,parent, Database, SQLStr, **kwargs)
        self.d = QStandardItem("asd")
        self.d.setCheckable(True)
        self.d.setFlags(Qt.ItemIsUserCheckable| Qt.ItemIsEnabled)
        self.appendRow(self.d)

    def data(self , index , role):
        if role == Qt.ToolTipRole:
            return self.d

        if role == Qt.DisplayRole:
            return self.d.text()
        return QStandardItemModel.data(self, index, role)