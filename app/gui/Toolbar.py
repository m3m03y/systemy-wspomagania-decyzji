from PyQt6.QtWidgets import QToolBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal as Signal

class Toolbar(QToolBar):
    file_open = Signal(str)
    file_save = Signal(str)

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
        save_btn.triggered.connect(self.save_file_button_clicked)
        self.addAction(save_btn)

    def open_file_button_clicked(self):
        print("[OPEN] File explorer dialog open")
        file_input = QFileDialog.getOpenFileName(self, 
            'Open file', 
            "./",
            "All Files (*);; CSV files (*.csv);; Text files (*.txt);; Excel files (*.xls, *.xlsx)",)
        path = file_input[0]
        print(f"Open: {path} file from input: {file_input}")
        self.file_open.emit(path)

    def save_file_button_clicked(self):
        print("[SAVE] File explorer dialog open")
        file_input = QFileDialog.getSaveFileName(self, 
            'Open file', 
            "./",
            "CSV files (*.csv);; Text files (*.txt);; Excel files (*.xls, *.xlsx)",)
        path = file_input[0]
        print(f"Get file path: {path} from input: {file_input}")
        self.file_save.emit(path)
