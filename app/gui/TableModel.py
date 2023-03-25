from PyQt6 import QtCore
from PyQt6.QtCore import Qt, pyqtSignal as Signal
import pandas as pd
from PyQt6.QtGui import QColor, QColorConstants
from tools.core import *


class TableModel(QtCore.QAbstractTableModel):
    data_edit = Signal(pd.DataFrame)

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._lowest_percent = [None] * len(self._data.columns)
        self._highest_percent = [None] * len(self._data.columns)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
            if role == Qt.ItemDataRole.BackgroundRole:
                value = self._data.iloc[index.row(), index.column()]
                if self._lowest_percent[index.column()] is not None and value <= max(self._lowest_percent[index.column()]):
                    return QColor(QColorConstants.Red)
                if self._highest_percent[index.column()] is not None and value >= min(self._highest_percent[index.column()]):
                    return QColor(QColorConstants.Green)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            print(f'Dataframe updated')
            self.data_edit.emit(self._data)
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def change_color(self, percentage, headers, is_minimum=None, column_name=None):
        self._lowest_percent = [None] * len(self._data.columns)
        self._highest_percent = [None] * len(self._data.columns)
        values = []
        num_rows = 0
        if column_name != 'all':
            col = headers.index(column_name)
            if check_if_only_numeric(self._data[headers[col]]):
                values = [row[col] for row in self._data.iloc]
                values.sort()
                num_rows = len(values)
        else:
            values = [row[:] for row in self._data]

        values.sort()

        if column_name != 'all':
            if is_minimum == 'min' or is_minimum == 'all':
                self._lowest_percent[col] = values[:int(
                    num_rows * percentage/100)]

        # Get the highest values
            if is_minimum == 'max' or is_minimum == 'all':
                self._highest_percent[col] = values[-int(
                    num_rows * percentage/100):]
        else:
            for col in range(len(headers)-1):
                print(f'Column: {headers[col]}')
                if check_if_only_numeric(self._data[headers[col]]):
                    values = [row[col] for row in self._data.iloc]
                    values.sort()
                    num_rows = len(values)

            # Get the lowest values
                    if is_minimum == 'min' or is_minimum == 'all':
                        self._lowest_percent[col] = values[:int(
                            num_rows * percentage/100)]

            # Get the highest values
                    if is_minimum == 'max' or is_minimum == 'all':
                        self._highest_percent[col] = values[-int(
                            num_rows * percentage/100):]

        if column_name != 'all':
            self.dataChanged.emit(self.index(
                0, col), self.index(num_rows-1, col))
        else:
            self.dataChanged.emit(self.index(0, 0), self.index(
                len(self._data)-1, len(headers)-1))
