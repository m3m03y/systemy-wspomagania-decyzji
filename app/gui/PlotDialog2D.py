from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal as Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns


class PlotDialog2D(QDialog):
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
        self.columns_y = QComboBox()
        self.columns_x.addItem(None)
        self.columns_y.addItem(None)
        self.columns_x.addItems(headers)
        self.columns_y.addItems(headers)
        self.columns_x.currentTextChanged.connect(self.get_y_headers_left)

        self.layout.addWidget(QLabel("Choose column x"))
        self.layout.addWidget(self.columns_x)
        self.layout.addWidget(QLabel("Choose column y"))
        self.layout.addWidget(self.columns_y)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        chosen_column_x = self.columns_x.currentText()
        chosen_column_y = self.columns_y.currentText()
        if chosen_column_x != None and chosen_column_y != None:
            print(
                f'Plot 2D Dialog:: Selected column x: {chosen_column_x}  y: {chosen_column_y}')
            self.columns_chosen.emit(chosen_column_x, chosen_column_y)

        self.close()

    def get_y_headers_left(self):
        choosen_column = None
        if (self.columns_x.currentText() != None):
            choosen_column = self.columns_x.currentText()
            self.columns_y.clear()
            self.columns_y.addItems(
                [x for x in self.headers if x != choosen_column])


class DisplayPlot(QDialog):
    def __init__(self, x_range, y_range, x_name, y_name, classes, class_numbers):
        super().__init__()
        self.x = x_range
        self.y = y_range
        self.x_axis = x_name
        self.y_axis = y_name
        self.class_name = classes
        self.class_numbers = class_numbers

        self.setWindowTitle('2D Plot')
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        unique_elements = []

        for item in self.class_name:
            if item not in unique_elements:
                unique_elements.append(item)
        cmap = plt.get_cmap('viridis', 3)
        scatter = ax.scatter(self.x, self.y, c=self.class_numbers, cmap=cmap)
        print(f'Class names: {unique_elements}')
        ax.legend(handles=scatter.legend_elements()[0], labels=unique_elements)

        ax.set_xlabel(self.x_axis)
        ax.set_ylabel(self.y_axis)
        ax.set_title('2D Plot')
