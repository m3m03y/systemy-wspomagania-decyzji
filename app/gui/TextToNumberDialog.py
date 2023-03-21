
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal as Signal

class TextToNumberDialog(QDialog):
    column_chosen = Signal(str, bool)
    
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
        self.change_type = QComboBox()
        self.change_type.addItems(["alphabetically", "by presence"])
        self.layout.addWidget(QLabel("Choose column"))
        self.layout.addWidget(self.columns)
        self.layout.addWidget(QLabel("Choose change type"))
        self.layout.addWidget(self.change_type)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column = self.columns.currentText()
        selected_type = self.change_type.currentText()
        is_by_alph_chosen = (selected_type == "alphabetically")
        if chosen_column != None:
            print(f'TextToNumberDialog:: Selected column: {chosen_column} with type: {selected_type}')
            self.column_chosen.emit(chosen_column, is_by_alph_chosen)
        self.close()