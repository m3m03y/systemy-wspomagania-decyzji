from PyQt6.QtWidgets import QMainWindow, QTableView, QStatusBar, QMessageBox
from gui.TableModel import TableModel
from gui.Toolbar import Toolbar
from tools.core import read_file, save_file
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

        # create table
        self.table = QTableView()

        self.setCentralWidget(self.table)
    
    def file_open(self, path: str):
        print(f'Open file: {path}')
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
        print(f'Read table: {df}')
        self.data = df
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.model.data_edit.connect(self.data_changed)
        self.update()

    def data_changed(self, df: pd.DataFrame):
        print(f'DataFrame changed: {df}')
        self.data = df

