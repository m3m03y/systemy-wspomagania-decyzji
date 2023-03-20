
from PyQt6.QtWidgets import QDialog, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel

class TextToNumberDialog(QDialog):
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("Change text to numbers!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(str(self.headers))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)