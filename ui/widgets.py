from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Light theme for Matplotlib (Catppuccin Latte)
        plt_style = {
            'figure.facecolor': '#eff1f5',
            'axes.facecolor': '#eff1f5',
            'axes.edgecolor': '#4c4f69',
            'axes.labelcolor': '#4c4f69',
            'xtick.color': '#4c4f69',
            'ytick.color': '#4c4f69',
            'text.color': '#4c4f69',
            'legend.frameon': False,
        }
        matplotlib.rcParams.update(plt_style)
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()
