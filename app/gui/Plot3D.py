from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal as Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns


class PlotDialog3D(QDialog):
    columns_chosen = Signal(str, str, str, str)
    nonclass_column_prefixes = ["numerized", "discretized", "standarized", "ranged"]

    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.edit = False
        self.setWindowTitle("3D Plot")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.columns_x = QComboBox()
        self.columns_y = QComboBox()
        self.columns_z = QComboBox()
        self.columns_class = QComboBox()
        self.columns_x.addItem(None)
        self.columns_y.addItem(None)
        self.columns_z.addItem(None)
        self.columns_x.addItems(headers)
        self.columns_x.currentTextChanged.connect(self.get_y_headers_left)
        self.columns_y.currentTextChanged.connect(self.get_z_headers_left)
        self.columns_class.addItems(
                [x for x in self.headers if x.split('_')[0] not in self.nonclass_column_prefixes])

        self.layout.addWidget(QLabel("Choose column x"))
        self.layout.addWidget(self.columns_x)
        self.layout.addWidget(QLabel("Choose column y"))
        self.layout.addWidget(self.columns_y)
        self.layout.addWidget(QLabel("Choose column z"))
        self.layout.addWidget(self.columns_z)
        self.layout.addWidget(QLabel("Choose class"))
        self.layout.addWidget(self.columns_class)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column_x = self.columns_x.currentText()
        chosen_column_y = self.columns_y.currentText()
        chosen_column_z = self.columns_z.currentText()
        chosen_class = self.columns_class.currentText()
        if (chosen_column_x != None and chosen_column_y != None and chosen_column_z != None and chosen_class != None) and (chosen_column_x != '' and chosen_column_y != '' and chosen_column_z != '' and chosen_class != ''):
            print(
                f'Plot 3D Dialog:: Selected column x: {chosen_column_x}  y: {chosen_column_y} z: {chosen_column_z} class: {chosen_class}')
            self.columns_chosen.emit(chosen_column_x, chosen_column_y, chosen_column_z, chosen_class)
        self.close()

    def get_y_headers_left(self):
        choosen_column = self.columns_x.currentText()
        if (choosen_column != None):
            self.edit = True
            self.columns_z.clear()
            self.columns_z.addItem(None)
            self.columns_y.clear()
            self.columns_y.addItem(None)
            self.columns_y.addItems(
                [x for x in self.headers if x != choosen_column])
            self.edit = False

    def get_z_headers_left(self):
        if self.edit:
            return
        choosen_columns = []
        if self.columns_x.currentText() != None:
            choosen_columns.append(self.columns_x.currentText())        
        if self.columns_y.currentText() != None:
            choosen_columns.append(self.columns_y.currentText())
        if len(choosen_columns) != 0:
            self.columns_z.clear()
            self.columns_z.addItem(None)
            self.columns_z.addItems(
                [x for x in self.headers if x not in choosen_columns])

    def update_list(self, to_edit_list: QComboBox):
        if to_edit_list.currentText() != None:
            to_edit_list.clear()
            to_edit_list.addItems([x for x in self.headers if x not in self.selected_columns])

    def add_column_if_not_none(self, column_name: str):
        if column_name != None:
            self.selected_columns.append(column_name)

class Display3DPlot(QDialog):
    def __init__(self, x_range, y_range, z_range, x_name, y_name, z_name, classes, class_numbers):
        super().__init__()
        self.x = x_range
        self.y = y_range
        self.z = z_range
        self.x_axis = x_name
        self.y_axis = y_name
        self.z_axis = z_name
        self.class_name = classes
        self.class_numbers = class_numbers

        self.setWindowTitle('3D Plot')
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(projection='3d')
        unique_elements = []

        for item in self.class_name:
            if item not in unique_elements:
                unique_elements.append(item)
        cmap = plt.get_cmap('viridis')
        scatter = ax.scatter(self.x, self.y, self.z,  c=self.class_numbers, cmap=cmap)
        print(f'Display3DPlot:: Class names: {unique_elements}')

        ax.legend(handles=scatter.legend_elements()[0], labels=unique_elements)

        ax.set_xlabel(self.x_axis)
        ax.set_ylabel(self.y_axis)
        ax.set_zlabel(self.z_axis)
        ax.set_title('3D Plot')
