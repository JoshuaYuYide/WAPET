import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
from ArtificialSpecies.panelinit import PanelInit


class ArtificialSpecies(QWidget, PanelInit):
    def __init__(self):
        super().__init__()

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.leftmost_panel())
        self.layout.addLayout(self.left_panel())
        self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())
        self.layout.addLayout(self.rightmost_panel())

    def get_widget(self):
        return self