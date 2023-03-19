from PyQt6.QtWidgets import QToolBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal as Signal

class Toolbar(QToolBar):
    file_open = Signal(str)

    def __init__(self, name) -> None:
        super(Toolbar, self).__init__()

        open_btn = QAction("Open", self)
        open_btn.setStatusTip("Open file")
        open_btn.setCheckable(False)
        open_btn.triggered.connect(self.open_file_button_clicked)
        self.addAction(open_btn)

        save_btn = QAction("Save", self)
        save_btn.setStatusTip("Save file")
        save_btn.setCheckable(False)
        self.addAction(save_btn)

    def open_file_button_clicked(self):
        print("File explorer dialog open")
        file_input = QFileDialog.getOpenFileName(self, 'Open file', "./")
        path = file_input[0]
        print(f"Open: {path} file from input: {file_input}")
        self.file_open.emit(path)