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

from OneSpecieClass.help import Help
from OneSpecieClass.panelinit import PanelInit
from OneSpecieClass.tableoperation import TableOperation
from OneSpecieClass.visualization import Visulization
from OneSpecieClass.check import Check
from OneSpecieClass.updatepanel import UpdatePanel
from OneSpecieClass.calculated import Calculate


class OneSpecie(QWidget, Help, PanelInit, TableOperation, Visulization, Check, UpdatePanel, Calculate):
    def __init__(self):
        super().__init__()

        self.time = 0

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.leftmost_panel())
        self.layout.addLayout(self.left_panel())
        # self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())

        # Signals and Slots
        self.species_submit_bt.clicked.connect(self.submit_species_func)
        self.species_clear_bt.clicked.connect(self.clear_species_func)
        self.species_delete_bt.clicked.connect(self.delete_species_func)
        self.clear_table_bt.clicked.connect(self.clear_table_func)
        self.plot.clicked.connect(self.plot_data)
        self.slider_year.valueChanged.connect(self.update_piechart)

        self.species_submit_bt.clicked.connect(self.check_species_table)
        self.species_delete_bt.clicked.connect(self.check_species_table)
        self.species_table.cellChanged.connect(self.check_species_table)
        self.clear_table_bt.clicked.connect(self.check_species_table)

        self.simulate.clicked.connect(self.simulate_logistic_growth_discrete)

        # check
        self.name.textChanged.connect(self.check_disable)
        self.survival_rate.textChanged.connect(self.check_disable)
        self.fecundity.textChanged.connect(self.check_disable)
        self.initial_population.textChanged.connect(self.check_disable)
        self.growth_rate.textChanged.connect(self.check_disable)
        self.carrying_capacity.textChanged.connect(self.check_disable)
        self.natural_life_span.textChanged.connect(self.check_disable)

    def get_widget(self):
        return self