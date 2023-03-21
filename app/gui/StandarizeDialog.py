from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal as Signal

class StandarizeDialog(QDialog):
    column_chosen = Signal(str)
    
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("Standarize values!")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.columns = QComboBox()
        self.columns.addItem(None)
        self.columns.addItems(self.headers)
        self.layout.addWidget(QLabel("Choose column"))
        self.layout.addWidget(self.columns)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column = self.columns.currentText()
        if chosen_column != None:
            print(f'StandarizeDialog:: Selected column: {chosen_column}')
            self.column_chosen.emit(chosen_column)
        self.close()