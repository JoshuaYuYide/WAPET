from PySide6.QtCore import Qt, Slot, QPointF, QSize
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu, QTabWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries


class PanelInit:
    def __init__(self):
        pass

    def leftmost_element(self):
        self.extreme_title = QLabel("Extreme Environments")
        self.extreme_title.setAlignment(Qt.AlignCenter)
        font = self.extreme_title.font()
        font.setBold(True)
        self.extreme_title.setFont(font)

    def leftmost_panel(self):
        self.leftmost_element()

        self.leftmost = QVBoxLayout()
        return self.leftmost

    def left_element(self):
        pass

    def left_panel(self):
        self.left = QVBoxLayout()
        return self.left

    def right_element(self):
        pass

    def right_panel(self):
        self.right = QVBoxLayout()
        return self.right

    def rightmost_element(self):
        pass

    def rightmost_panel(self):
        self.rightmost = QVBoxLayout()
        return self.rightmost

    def middle_element(self):
        pass

    def middle_panel(self):
        self.middle = QVBoxLayout()
        return self.middle




























