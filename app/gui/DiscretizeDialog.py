from PyQt6.QtWidgets import QDialog, QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal as Signal

class DiscretizeDialog(QDialog):
    column_chosen = Signal(str, int)
    
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("Change text to numbers!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.columns = QComboBox()
        self.columns.addItem(None)
        self.columns.addItems(self.headers)
        self.division_number = QSpinBox()
        self.division_number.setMinimum(2)
        # TODO: set maximum based on numbers in column range
        self.layout.addWidget(QLabel("Choose column"))
        self.layout.addWidget(self.columns)
        self.layout.addWidget(QLabel("Choose range:"))
        self.layout.addWidget(self.division_number)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column = self.columns.currentText()
        division_number = self.division_number.value()
        if chosen_column != None:
            print(f'DiscretizeDialog:: Selected column: {chosen_column} with division number: {division_number}')
            self.column_chosen.emit(chosen_column, division_number)
        self.close()