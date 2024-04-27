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

from ArtificialSpeciesClass.help import Help
from ArtificialSpeciesClass.panelinit import PanelInit
from ArtificialSpeciesClass.tableoperation import TableOperation
from ArtificialSpeciesClass.visualization import Visulization
from ArtificialSpeciesClass.check import Check


class ArtificialSpecies(QWidget, Help, PanelInit, TableOperation, Visulization, Check):
    def __init__(self):
        super().__init__()

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.leftmost_panel())
        self.layout.addLayout(self.left_panel())
        # self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())

        # Signals and Slots
        self.submit.clicked.connect(self.add_data_table_element)
        self.clear_table_bt.clicked.connect(self.clear_table)
        self.plot.clicked.connect(self.plot_data)
        self.slider.valueChanged.connect(self.update_piechart)
        self.name.textChanged.connect(self.check_disable)
        self.survival_rate.textChanged.connect(self.check_disable)
        self.fecundity.textChanged.connect(self.check_disable)
        self.initial_population.textChanged.connect(self.check_disable)
        self.growth_rate.textChanged.connect(self.check_disable)
        self.carrying_capacity.textChanged.connect(self.check_disable)
        self.natural_life_span.textChanged.connect(self.check_disable)

    def get_widget(self):
        return self