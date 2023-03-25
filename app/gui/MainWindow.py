from PyQt6.QtWidgets import QMainWindow, QTableView, QStatusBar, QMessageBox
from gui.TableModel import TableModel
from gui.Toolbar import Toolbar
from gui.PlotDialog2D import DisplayPlot
from gui.Plot3D import Display3DPlot
from gui.PlotHistogram import DisplayHistogram
from tools.core import *
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None

        # initialize main window
        self.setWindowTitle(
            "Systemy wspomagania decyzji - K. Lipiszko, K. Matuszak")
        self.setGeometry(100, 100, 1280, 720)

        # add toolbar and status bar
        self.toolbar = Toolbar("Toolbar")
        self.addToolBar(self.toolbar)
        self.setStatusBar(QStatusBar(self))
        self.toolbar.file_open.connect(self.file_open)
        self.toolbar.file_save.connect(self.file_save)
        self.toolbar.column_to_numerize.connect(self.numerize_column)
        self.toolbar.column_to_discretize.connect(self.discretize_column)
        self.toolbar.column_to_standarize.connect(self.standarize_column)
        self.toolbar.column_to_change_range.connect(self.change_range_column)
        self.toolbar.colums_to_display_2Dplot.connect(self.plot2D)
        self.toolbar.min_max_colors.connect(self.min_max_color_change)
        self.toolbar.columns_to_display_2Dplot.connect(self.plot2D)
        self.toolbar.columns_to_display_3Dplot.connect(self.plot3D)
        self.toolbar.columns_to_display_histogram.connect(self.displayHistogram)

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
        self.toolbar.update_headers(df.columns.to_list())
        self.update()

    def data_changed(self, df: pd.DataFrame):
        print(f'MainWindow:: DataFrame changed: {df}')
        self.data = df

    def numerize_column(self, column_name: str, is_by_alph_chosen: bool):
        print(
            f'MainWindow:: Selected column to numerize: {column_name} values: {self.data[column_name]}')
        if is_by_alph_chosen:
            numerized_column = convert_text_to_numeric_by_alphabet_order(
                self.data[column_name])
        else:
            numerized_column = convert_text_to_numeric_by_presence(
                self.data[column_name])
        if numerized_column == None:
            print(f'MainWindow:: No values changed to numeric')
            return
        print(f'MainWindow:: Numerized column values: {numerized_column}')
        prefix = "alph" if is_by_alph_chosen else "by_presence"
        self.data[f'numerized_{prefix}_{column_name}'] = numerized_column
        self.update_table(self.data)

    def discretize_column(self, column_name: str, division_number: int):
        print(
            f'MainWindow:: Selected column to discretize: {column_name} values: {self.data[column_name]}')
        discretized_column = discretisation(
            self.data[column_name], division_number)
        if discretized_column is None:
            print(f'MainWindow:: No values discretized')
            return
        print(f'MainWindow:: Discretized column values: {discretized_column}')
        self.data[f'discretized_{division_number}_{column_name}'] = discretized_column
        self.update_table(self.data)

    def standarize_column(self, column_name: str):
        print(
            f'MainWindow:: Selected column to standarize: {column_name} values: {self.data[column_name]}')
        standarized_column = standarization(self.data[column_name])
        if standarized_column is None:
            print(f'MainWindow:: No values standarized')
            return
        print(f'MainWindow:: Standarized column values: {standarized_column}')
        self.data[f'standarized_{column_name}'] = standarized_column
        self.update_table(self.data)

    def change_range_column(self, column_name: str, min_val: int, max_val: int):
        print(
            f'MainWindow:: Selected column to change_range: {column_name} values: {self.data[column_name]}')
        changed_range_column = change_data_range(
            self.data[column_name], min_val, max_val)
        if changed_range_column is None:
            print(f'MainWindow:: No values changed range')
            return
        print(
            f'MainWindow:: Changed range column column values: {changed_range_column}')
        self.data[f'ranged_{min_val}_{max_val}_{column_name}'] = changed_range_column
        self.update_table(self.data)

    def plot2D(self, x_column_name: str, y_column_name: str, class_column_name: str):
        print(
            f'MainWindow:: Selected column to plot x: {x_column_name} y: {y_column_name} class: {class_column_name}')
        x_range = self.data[x_column_name]
        y_range = self.data[y_column_name]
        if not (check_if_only_numeric(x_range) and check_if_only_numeric(y_range)):
            QMessageBox.critical(
                self,
                "String values selected!",
                "Values in selected columns must be first changed to number.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return 
        class_column = self.data[class_column_name]

        print(f'x range: {x_range}; y_range: {y_range}; class: {class_column}')
        if not check_if_only_numeric(class_column):
            class_column_numerized = convert_text_to_numeric_by_alphabet_order(
                class_column)
        else:
            class_column_numerized = class_column
        print(f'Class to numbers: {class_column_numerized}')
        dlg = DisplayPlot(x_range, y_range, x_column_name,
                          y_column_name, class_column, class_column_numerized)
        dlg.exec()

    def min_max_color_change(self, column: str, percentage: int, min_max: str):
        print(
            f'MainWindow:: Color column: {column} percentage {percentage} % for values: {min_max}')
        print(f'Headers: {self.toolbar.headers}')
        self.model.change_color(percentage, self.toolbar.headers, min_max,
                                column)

    def plot3D(self, x_column_name: str, y_column_name: str, z_column_name: str, class_column_name: str):
        print(
            f'MainWindow:: Selected column to plot x: {x_column_name} y: {y_column_name} z: {z_column_name}, class: {class_column_name}')
        x_range = self.data[x_column_name]
        y_range = self.data[y_column_name]
        z_range = self.data[z_column_name]
        if not (check_if_only_numeric(x_range) and check_if_only_numeric(y_range) and check_if_only_numeric(z_range)):
            QMessageBox.critical(
                self,
                "String values selected!",
                "Values in selected columns must be first changed to number.",
                buttons=QMessageBox.StandardButton.Discard,
                defaultButton=QMessageBox.StandardButton.Discard,
            )
            return 
        class_column = self.data[class_column_name]
        print(f'x range: {x_range}; y_range: {y_range}; z: {z_range}; class: {class_column}')
        if not check_if_only_numeric(class_column):
            class_column_numerized = convert_text_to_numeric_by_alphabet_order(class_column)
        else:
            class_column_numerized = class_column
        dlg = Display3DPlot(x_range, y_range, z_range, x_column_name,
                          y_column_name, z_column_name, class_column, class_column_numerized)
        dlg.exec()

    def displayHistogram(self, x_column_name: str, class_column_name: str):
        print(
            f'MainWindow:: Selected column to plot histogram: {x_column_name}, class: {class_column_name}')
        dlg = DisplayHistogram(x_column_name, class_column_name, self.data)
        dlg.exec()

