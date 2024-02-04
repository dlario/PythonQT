from PySide6.QtCore import QAbstractTableModel, Qt

class DictTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = [{'dict': outer_key, 'item': inner_key, **value} for outer_key, inner_dict in data.items() for inner_key, value in inner_dict.items()]
        self._keys = self._data[0].keys()

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._keys)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][list(self._keys)[index.column()]])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return list(self._keys)[section]