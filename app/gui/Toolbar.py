from PyQt6.QtWidgets import QToolBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal as Signal
from gui.TextToNumberDialog import TextToNumberDialog

class Toolbar(QToolBar):
    file_open = Signal(str)
    file_save = Signal(str)
    column_to_numerize = Signal(str, bool)

    def __init__(self, name) -> None:
        super(Toolbar, self).__init__()
        self.headers = None

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

        to_numeric_btn = QAction("TextToNumber", self)
        to_numeric_btn.setStatusTip("Change text variables in column to numeric")
        to_numeric_btn.setCheckable(False)
        to_numeric_btn.triggered.connect(self.text_to_numeric_button_clicked)
        self.addAction(to_numeric_btn)

        discretize_btn = QAction("Discretize", self)
        discretize_btn.setStatusTip("Discretize variables in column")
        discretize_btn.setCheckable(False)
        discretize_btn.triggered.connect(self.discretize_button_clicked)
        self.addAction(discretize_btn)

        standarize_btn = QAction("Standarize", self)
        standarize_btn.setStatusTip("Standarize variables in column")
        standarize_btn.setCheckable(False)
        standarize_btn.triggered.connect(self.standarize_button_clicked)
        self.addAction(standarize_btn)

        change_range_btn = QAction("Change range", self)
        change_range_btn.setStatusTip("Change range of variables in column")
        change_range_btn.setCheckable(False)
        change_range_btn.triggered.connect(self.change_range_button_clicked)
        self.addAction(change_range_btn)

    def open_file_button_clicked(self):
        print("[OPEN] File explorer dialog open")
        file_input = QFileDialog.getOpenFileName(self, 
            'Open file', 
            "./",
            "All Files (*);; CSV files (*.csv);; Text files (*.txt);; Excel files (*.xls, *.xlsx)",)
        path = file_input[0]
        if path == "" or path == None:
            print(f'Toolbar:: No file selected')
            return 
        print(f"Toolbar:: Open: {path} file from input: {file_input}")
        self.file_open.emit(path)

    def save_file_button_clicked(self):
        print("[SAVE] File explorer dialog open")
        file_input = QFileDialog.getSaveFileName(self, 
            'Open file', 
            "./",
            "CSV files (*.csv);; Text files (*.txt);; Excel files (*.xls, *.xlsx)",)
        path = file_input[0]
        if path == "" or path == None:
            print(f'Toolbar:: No file selected')
            return 
        print(f"Toolbar:: Get file path: {path} from input: {file_input}")
        self.file_save.emit(path)

    def update_headers(self, headers):
        print(f'Toolbar:: Update headers {headers}')
        self.headers = headers

    def text_to_numeric_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return
        dlg = TextToNumberDialog(self.headers)
        dlg.column_chosen.connect(self.column_to_numerize_chosen)
        dlg.exec()

    def column_to_numerize_chosen(self, column: str, is_by_alph_chosen: bool):
        print(f'Toolbar:: Column to numerize: {column}, is alphabetically order chosen: {is_by_alph_chosen}')
        self.column_to_numerize.emit(column, is_by_alph_chosen)

    def discretize_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return

    def standarize_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return

    def change_range_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return