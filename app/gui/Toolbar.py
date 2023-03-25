from PyQt6.QtWidgets import QToolBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal as Signal
from gui.DiscretizeDialog import DiscretizeDialog
from gui.StandarizeDialog import StandarizeDialog
from gui.TextToNumberDialog import TextToNumberDialog
from gui.ChangeDataRangeDialog import ChangeDataRangeDialog
from gui.PlotDialog2D import PlotDialog2D
from gui.ShowMinMaxDialog import ShowMinMaxDialog
from gui.Plot3D import PlotDialog3D
from gui.PlotHistogram import PlotHistogram


class Toolbar(QToolBar):
    file_open = Signal(str)
    file_save = Signal(str)
    column_to_numerize = Signal(str, bool)
    column_to_discretize = Signal(str, int)
    column_to_standarize = Signal(str)
    column_to_change_range = Signal(str, int, int)
    colums_to_display_2Dplot = Signal(str, str, str)
    min_max_colors = Signal(str, int, str)
    columns_to_display_3Dplot = Signal(str, str, str, str)
    columns_to_display_histogram = Signal(str, str)

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
        to_numeric_btn.setStatusTip(
            "Change text variables in column to numeric")
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

        display_2dplot_btn = QAction("2D plot", self)
        display_2dplot_btn.setStatusTip("Choose columns to display 2D plot")
        display_2dplot_btn.setCheckable(False)
        display_2dplot_btn.triggered.connect(
            self.display_2dplot_button_clicked)
        self.addAction(display_2dplot_btn)

        min_max_color_btn = QAction("Min max color", self)
        min_max_color_btn.setStatusTip("Choose percentage of min/max")
        min_max_color_btn.setCheckable(False)
        min_max_color_btn.triggered.connect(
            self.show_min_max_button_clicked)
        self.addAction(min_max_color_btn)

        display_3dplot_btn = QAction("3D plot", self)
        display_3dplot_btn.setStatusTip("Choose columns to display 3D plot")
        display_3dplot_btn.setCheckable(False)
        display_3dplot_btn.triggered.connect(
            self.display_3dplot_button_clicked)
        self.addAction(display_3dplot_btn)

        display_histogram_btn = QAction("Histogram", self)
        display_histogram_btn.setStatusTip("Choose columns to display histogram")
        display_histogram_btn.setCheckable(False)
        display_histogram_btn.triggered.connect(
            self.display_histogram_button_clicked)
        self.addAction(display_histogram_btn)


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
        print(
            f'Toolbar:: Column to numerize: {column}, is alphabetically order chosen: {is_by_alph_chosen}')
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
        dlg = DiscretizeDialog(self.headers)
        dlg.column_chosen.connect(self.column_to_discretize_chosen)
        dlg.exec()

    def column_to_discretize_chosen(self, column: str, division_number: int):
        print(
            f'Toolbar:: Column to standarize: {column} with division number: {division_number}')
        self.column_to_discretize.emit(column, division_number)

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
        dlg = StandarizeDialog(self.headers)
        dlg.column_chosen.connect(self.column_to_standarize_chosen)
        dlg.exec()

    def column_to_standarize_chosen(self, column: str):
        print(f'Toolbar:: Column to standarize: {column}')
        self.column_to_standarize.emit(column)

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
        dlg = ChangeDataRangeDialog(self.headers)
        dlg.column_chosen.connect(self.column_to_change_range_chosen)
        dlg.exec()

    def column_to_change_range_chosen(self, column: str, range_min: int, range_max: int):
        print(
            f'Toolbar:: Column to change_range: {column} with range: ({range_min},{range_max})')
        self.column_to_change_range.emit(column, range_min, range_max)

    def display_2dplot_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return
        dlg = PlotDialog2D(self.headers)
        dlg.columns_chosen.connect(self.column_to_2D_plot_chosen)
        # dlg.y_column_chosen.connect(self.column_to_2D_plot_chosen)
        dlg.exec()

    def column_to_2D_plot_chosen(self, column_x: str, column_y: str, column_class: str):
        print(
            f'Toolbar:: Column to display 2D plot x: {column_x} y: {column_y} class: {column_class}')

        self.columns_to_display_2Dplot.emit(column_x, column_y, column_class)

    def display_3dplot_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return
        dlg = PlotDialog3D(self.headers)
        dlg.columns_chosen.connect(self.column_to_3D_plot_chosen)
        dlg.exec()

    def column_to_3D_plot_chosen(self, column_x: str, column_y: str, column_z: str, column_class: str):
        print(
            f'Toolbar:: Column to display 3D plot x: {column_x} y: {column_y} z: {column_z} class: {column_class}')

        self.columns_to_display_3Dplot.emit(column_x, column_y, column_z, column_class)

    def display_histogram_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return
        dlg = PlotHistogram(self.headers)
        dlg.columns_chosen.connect(self.column_to_histogram_chosen)
        dlg.exec()

    def column_to_histogram_chosen(self, column_x: str, column_class: str):
        print(
            f'Toolbar:: Column to display histogram x: {column_x} class: {column_class}')
        self.columns_to_display_histogram.emit(column_x, column_class)

    def show_min_max_button_clicked(self):
        if self.headers == None:
            QMessageBox.critical(
                self,
                "No data selected!",
                "Dataset must be load from file first.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return
        print(type(self.headers))
        dlg = ShowMinMaxDialog(self.headers)
        dlg.column_chosen.connect(self.min_max_percentage_chosen)

        dlg.exec()

    def min_max_percentage_chosen(self, column: str, percentage: int, min_max: str):
        print(
            f'Toolbar:: Color column: {column} percentage {percentage} % for values: {min_max}')
        self.min_max_colors.emit(column, percentage, min_max)
