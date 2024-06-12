from OneSpecieClass.visualization import Visulization
import sys
from PySide6.QtCore import Qt, Slot, QPointF, QModelIndex
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu,
                               QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem, QGraphicsObject,
                               QStyleOptionGraphicsItem, QGraphicsView)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries, QBarSeries, QBarSet
import random
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import (QEasingCurve, QLineF,
                            QParallelAnimationGroup, QPointF,
                            QPropertyAnimation, QRectF, Qt)
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
import matplotlib.pyplot as plt
import math
import numpy as np

class VisulizationTwo(Visulization):

    def plot_agent_based_logistic_individual(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Logistic Growth Individual Agent-based Line Chart")

        colors_palette = [Qt.red, Qt.green, Qt.blue]
        for i in range(3):
            # 获取第一列数据
            target_population_data = []
            for row in range(self.result_table.model().rowCount()):
                index = self.result_table.model().index(row, i)  # 第一列的标签为 0 列的标签
                value = self.result_table.model().data(index)
                target_population_data.append(value)

            # 获取第二列数据
            timestep_data = []
            for row in range(self.result_table.model().rowCount()):
                index = self.result_table.model().index(row, 3)  # 第二列的标签为 1 列的标签
                value = self.result_table.model().data(index)
                timestep_data.append(value)

            data = list(map(lambda x, y: (float(x), float(y)), timestep_data, target_population_data))

            # 创建新的QLineSeries
            series = QLineSeries()
            series.setName(self.result_table.horizontalHeaderItem(i).text())

            for x, y in data:
                series.append(x, y)

            # 设置线条样式
            pen = QPen(colors_palette[i])
            pen.setWidth(2)
            series.setPen(pen)

            # 将线系列添加到QChart中
            chart.addSeries(series)

        chart.createDefaultAxes()
        self.linechart.setChart(chart)
