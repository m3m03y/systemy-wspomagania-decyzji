from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal as Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns

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
        self.setWindowTitle('Histogram')
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

        sns.set(style="darkgrid")

        sns.histplot(data=self.data, x=self.x_axis, hue=self.class_name, kde=True, ax=ax)

