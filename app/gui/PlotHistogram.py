from PyQt6.QtWidgets import QDialog, QWidget, QCheckBox, QDialogButtonBox, QVBoxLayout, QSpinBox, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal as Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt6.QtCore import Qt
from tools.core import discretisation
import pandas as pd
class PlotHistogram(QDialog):
    columns_chosen = Signal(str, str)

    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setWindowTitle("2D Plot")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.columns_x = QComboBox()
        self.columns_class = QComboBox()
        self.columns_x.addItem(None)
        self.columns_x.addItems(headers)
        self.columns_class.addItem(None)
        self.columns_class.addItems(headers)

        self.layout.addWidget(QLabel("Choose column x"))
        self.layout.addWidget(self.columns_x)
        self.layout.addWidget(QLabel("Choose class"))
        self.layout.addWidget(self.columns_class)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column_x = self.columns_x.currentText()
        chosen_class = self.columns_class.currentText()
        if (chosen_column_x != None and chosen_class != None) and (chosen_column_x != '' and chosen_class != ''):
            print(
                f'Plot 2D Dialog:: Selected column x: {chosen_column_x}  class: {chosen_class}')
            self.columns_chosen.emit(chosen_column_x, chosen_class)
        self.close()


class DisplayHistogram(QDialog):
    def __init__(self, x_name, classes, data):
        super().__init__()
        self.x_axis = x_name
        self.class_name = classes
        self.data = data
        self.data_to_draw = self.data

        self.setWindowTitle('Histogram')
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)
        
        plt.ion()
        layout = QVBoxLayout()
        discretize_checkbox_layout = QHBoxLayout()
        discretize_input_layout = QHBoxLayout()
        discretize_menu_layout = QHBoxLayout()
        
        self.discretize_menu = QWidget()
        self.discretize_menu.setLayout(discretize_menu_layout)
        self.enable_discretize = QCheckBox()
        self.enable_discretize.stateChanged.connect(self.change_discretization_state)
        
        self.discretize_chechbox = QWidget()
        self.discretize_chechbox.setLayout(discretize_checkbox_layout)        
        self.discretize_input = QWidget()
        self.discretize_input.setLayout(discretize_input_layout)
        self.discretize_input.setDisabled(True)
        self.division_number = QSpinBox()
        self.division_number.setMinimum(2)
        self.division_number.valueChanged.connect(self.plot_discretize)

        discretize_checkbox_layout.addWidget(self.enable_discretize)
        discretize_checkbox_layout.addWidget(QLabel("Discretize"))
        discretize_input_layout.addWidget(QLabel("Choose division number:"))
        discretize_input_layout.addWidget(self.division_number)
        discretize_menu_layout.addWidget(self.discretize_chechbox)
        discretize_menu_layout.addWidget(self.discretize_input)

        layout.addWidget(self.discretize_menu)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot()
    
    def change_discretization_state(self, s):
        print(f'DisplayHistogram:: checked state: {s}')
        if s == 0:
            self.discretize_input.setDisabled(True)
            self.division_number.setDisabled(True)
            self.data_to_draw = self.data
            self.plot()
            self.update()
        else:
            self.discretize_input.setEnabled(True)
            self.division_number.setEnabled(True)
            self.update()

    def plot_discretize(self, i):
        print(f'DisplayHistogram:: discretize with {i} divisions')
        discretized_column = discretisation(
            self.data[self.x_axis], i)
        if discretized_column is None:
            ...
            #TODO: do something

        df = self.data.copy()
        df[self.x_axis] = discretized_column
        print(f'DisplayHistogram:: current dataset: {df}')
        self.data_to_draw = df
        self.plot()

    def plot(self):
        self.figure.clear(True)
        print(f'DisplayHistogram:: dataset to draw: {self.data_to_draw}')
        ax = self.figure.add_subplot(111)

        sns.set(style="darkgrid")

        sns.histplot(data=self.data_to_draw, x=self.x_axis, hue=self.class_name, kde=True, ax=ax)
        
        self.figure.canvas.draw()
        self.canvas.flush_events()

