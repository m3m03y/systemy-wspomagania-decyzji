from PyQt6.QtWidgets import QDialog, QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal as Signal

class ChangeDataRangeDialog(QDialog):
    column_chosen = Signal(str, int, int)
    
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("Change text to numbers!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.number_layout = QHBoxLayout()
        self.number_range = QWidget()
        self.number_range.setLayout(self.number_layout)
        self.columns = QComboBox()
        self.columns.addItem(None)
        self.columns.addItems(self.headers)
        self.min_value = QSpinBox()
        self.max_value = QSpinBox()
        self.number_layout.addWidget(QLabel("Min:"))
        self.number_layout.addWidget(self.min_value)
        self.number_layout.addWidget(QLabel("Max:"))
        self.number_layout.addWidget(self.max_value)
        # TODO: add some validation 
        self.layout.addWidget(QLabel("Choose column"))
        self.layout.addWidget(self.columns)
        self.layout.addWidget(QLabel("Choose range:"))
        self.layout.addWidget(self.number_range)
        self.layout.addWidget(self.buttonBox)
        self.error_label = QLabel("")
        self.layout.addWidget(self.error_label)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column = self.columns.currentText()
        min_number = self.min_value.value()
        max_number = self.max_value.value()
        if chosen_column != None and max_number > min_number:
            print(f'DiscretizeDialog:: Selected column: {chosen_column} with range: ({min_number},{max_number})')
            self.column_chosen.emit(chosen_column, min_number, max_number)
            self.close()
        elif max_number <= min_number:
            self.error_label.setText("Max value must be greater than min value")
            return
        else:
            self.close()
