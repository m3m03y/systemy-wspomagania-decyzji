from PyQt6.QtWidgets import QMainWindow, QTableView, QStatusBar, QMessageBox
from gui.TableModel import TableModel
from gui.Toolbar import Toolbar
from tools.core import *
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None

        # initialize main window
        self.setWindowTitle("Systemy wspomagania decyzji - K. Lipiszko, K. Matuszak")
        self.setGeometry(100,100,1280,720)

        # add toolbar and status bar
        self.toolbar = Toolbar("Toolbar")
        self.addToolBar(self.toolbar)
        self.setStatusBar(QStatusBar(self))
        self.toolbar.file_open.connect(self.file_open)
        self.toolbar.file_save.connect(self.file_save)
        self.toolbar.column_to_numerize.connect(self.numerize_column)

        # create table
        self.table = QTableView()

        self.setCentralWidget(self.table)
    
    def file_open(self, path: str):
        print(f'MainWindow:: Open file: {path}')
        try:
            df = read_file(path)
            self.update_table(df)
            self.toolbar.update_headers(df.columns.to_list())
        except:
            QMessageBox.critical(
            self,
            "File read error!",
            "Invalid file extension.",
            buttons=QMessageBox.StandardButton.Discard,
            defaultButton=QMessageBox.StandardButton.Discard,
        )

    def file_save(self, path: str):
        print(f'Save file: {path}')
        try:
            save_file(path, self.data)
            QMessageBox.information(
            self,
            "Save!",
            "File saved successfully",
            buttons=QMessageBox.StandardButton.Discard,
            defaultButton=QMessageBox.StandardButton.Discard,
        )
        except:
            QMessageBox.critical(
            self,
            "File save error!",
            "Invalid file extension.",
            buttons=QMessageBox.StandardButton.Discard,
            defaultButton=QMessageBox.StandardButton.Discard,
        )

    def update_table(self, df: pd.DataFrame):
        print(f'MainWindow:: Updated table: {df}')
        self.data = df
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.model.data_edit.connect(self.data_changed)
        self.update()

    def data_changed(self, df: pd.DataFrame):
        print(f'MainWindow:: DataFrame changed: {df}')
        self.data = df

    def numerize_column(self, column_name: str, is_by_alph_chosen: bool):
        print(f'MainWindow:: Selected column: {column_name} values: {self.data[column_name]}')
        if is_by_alph_chosen:
            numerized_column = convert_text_to_numeric_by_alphabet_order(self.data[column_name])
        else:
            numerized_column = convert_text_to_numeric_by_presence(self.data[column_name])
        if numerized_column == None:
            print(f'MainWindow:: No values changed to numeric')
            return
        print(f'MainWindow:: Numerized column values: {numerized_column}')
        self.data[column_name] = numerized_column
        self.update_table(self.data)
