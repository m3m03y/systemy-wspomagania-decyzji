from PyQt6.QtWidgets import QMainWindow, QTableView, QStatusBar
from gui.TableModel import TableModel
from gui.Toolbar import Toolbar
from tools.core import read_file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # initialize main window
        self.setWindowTitle("Systemy wspomagania decyzji - K. Lipiszko, K. Matuszak")
        self.table = QTableView()
        self.setGeometry(100,100,1280,720)

        # add toolbar and status bar
        toolbar = Toolbar("Toolbar")
        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))
        toolbar.file_open.connect(self.file_open)

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
    
    def file_open(self, path: str):
        print(f'Open file: {path}')
        df = read_file(path)
        print(df)