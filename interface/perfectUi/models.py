from PyQt5.QtCore import (
    QAbstractListModel, QModelIndex, Qt, pyqtSignal
)
from typing import Any
from genshinstats import errors


class ListModel(QAbstractListModel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.items_data = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.items_data)

    def data(self, index: QModelIndex, role: int) -> Any:
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.items_data[index.row()]
        return None

    def setData(self, index: QModelIndex, value: dict, role: int) -> bool:
        if index.isValid() and role == Qt.EditRole:
            self.items_data[index.row()].update(value)
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def appendRow(self, data: dict, index: QModelIndex = QModelIndex()) -> bool:
        last_row = len(self.items_data)

        if not self.insertRows(last_row, index):
            return False
        self.items_data[last_row] = data

        return True

    def deleteRow(self, row: int, index: QModelIndex = QModelIndex()) -> bool:
        if 0 > row > len(self.items_data):
            return False
        return self.removeRows(row, 1, index)

    def clear(self):
        self.beginResetModel()
        self.items_data.clear()
        self.endResetModel()

    def insertRows(self, position: int, parent: QModelIndex) -> bool:
        self.beginInsertRows(parent, position, position)
        self.items_data.insert(position, {})
        self.endInsertRows()
        return True

    def removeRows(self, position: int, rows: int, parent: QModelIndex) -> bool:
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            try:
                self.items_data.pop(position)
            except IndexError:
                return False
        self.endRemoveRows()
        return True


class PrimosModel(ListModel):
    err_signal = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super(PrimosModel, self).__init__(parent)

    def add_primos(self, primos):
        if type(primos) != list:
            return

        for data in primos:
            self.appendRow(data)


class ResinModel(ListModel):
    err_signal = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super(ResinModel, self).__init__(parent)

    def add_primos(self, primos):
        if type(primos) != list:
            return

        for data in primos:
            self.appendRow(data)


class DailsModel(ListModel):
    err_signal = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super(DailsModel, self).__init__(parent)

    def add_dails(self, data):
        if type(data) in [StopIteration, RuntimeError]:
            return

        for dails in data:
            self.appendRow(dails)


class CharactersModel(ListModel):
    def __init__(self, parent=None):
        super(CharactersModel, self).__init__(parent)

    def add_characters(self, data):
        if type(data) != list:
            return

        self.clear()
        for char in data:
            self.appendRow(char)
