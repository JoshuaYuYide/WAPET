# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial

import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from OneSpecieClass.help import Help
from OneSpecieClass.panelinit import PanelInit
from OneSpecieClass.tableoperation import TableOperation
from OneSpecieClass.visualization import Visulization


class OneSpecie(QWidget, Help, PanelInit, TableOperation, Visulization):
    def __init__(self):
        super().__init__()

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.leftmost_panel())
        self.layout.addLayout(self.left_panel())
        self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())

        # Signals and Slots
        self.submit.clicked.connect(self.add_data_table_element)
        self.clear.clicked.connect(self.clear_table)
        self.plot.clicked.connect(self.plot_data)
        self.slider.valueChanged.connect(self.update_piechart)
        self.name.textChanged.connect(self.check_disable)
        self.survival_rate.textChanged.connect(self.check_disable)
        self.fecundity.textChanged.connect(self.check_disable)
        self.initial_population.textChanged.connect(self.check_disable)
        self.growth_rate.textChanged.connect(self.check_disable)
        self.carrying_capacity.textChanged.connect(self.check_disable)
        self.natural_life_span.textChanged.connect(self.check_disable)

    @Slot()
    def check_disable(self):
        enabled = bool(self.name.text() and self.survival_rate.text() and self.fecundity.text() and self.initial_population.text() and self.growth_rate.text() and self.carrying_capacity.text() and self.natural_life_span.text())
        if enabled:
            self.submit.setEnabled(True)
        else:
            self.submit.setEnabled(False)

    def random_plot_linechart(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Line Chart")

        data = [
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random())
        ]

        for x, y in data:
            series.append(x, y)

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置线条样式
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        series.setPen(pen)

        self.linechart.setChart(chart)

    def get_widget(self):
        return self