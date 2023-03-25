from PyQt6.QtWidgets import QDialog, QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal as Signal


class ShowMinMaxDialog(QDialog):
    column_chosen = Signal(str, int, str)

    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("Color min/max values!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        if 'all' not in self.headers:
            self.headers.append('all')
        self.layout = QVBoxLayout()
        self.columns = QComboBox()
        self.min_max = QComboBox()
        self.columns.addItem(None)
        self.min_max.addItem(None)
        self.columns.addItems(self.headers)
        self.min_max.addItems(['min', 'max', 'all'])
        self.percentage = QSpinBox()
        self.percentage.setMinimum(1)
        self.percentage.setMaximum(100)

        self.layout.addWidget(QLabel("Choose column"))
        self.layout.addWidget(self.columns)
        self.layout.addWidget(QLabel("Choose percentage:"))
        self.layout.addWidget(self.percentage)
        self.layout.addWidget(QLabel("Choose min/max:"))
        self.layout.addWidget(self.min_max)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column = self.columns.currentText()
        percentage = self.percentage.value()
        min_max = self.min_max.currentText()
        # if chosen_column != None:
        print(
            f'MinMaxDialog:: Selected column: {chosen_column} with percentage: {percentage} for {min_max} values')
        self.column_chosen.emit(chosen_column, percentage, min_max)
        self.close()
