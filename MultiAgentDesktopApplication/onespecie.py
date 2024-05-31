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
from OneSpecieClass.panelinit import PanelInit, GridWidget
from OneSpecieClass.visualization import Visulization
from OneSpecieClass.check import Check
from OneSpecieClass.updatepanel import UpdatePanel
from OneSpecieClass.calculated import Calculate


class OneSpecie(QWidget, Help, PanelInit, Visulization, Check, UpdatePanel, Calculate):
    def __init__(self):
        super().__init__()
        UpdatePanel.__init__(self)

        self.time = 0

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.leftmost_panel())
        self.layout.addWidget(self.left_panel())
        # self.layout.addLayout(self.middle_right_panel())
        # self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())

        # Signals and Slots
        self.species_submit_bt.clicked.connect(self.submit_species_func)
        self.species_clear_bt.clicked.connect(self.clear_species_func)
        self.species_delete_bt.clicked.connect(self.delete_species_func)
        self.species_random_bt.clicked.connect(self.random_species_func)

        self.clear_table_bt.clicked.connect(self.clear_table_func)
        self.plot.clicked.connect(self.plot_data)
        self.slider_year.valueChanged.connect(self.update_piechart)

        self.species_submit_bt.clicked.connect(self.check_species_table)
        self.species_delete_bt.clicked.connect(self.check_species_table)
        self.species_table.cellChanged.connect(self.check_species_table)
        self.clear_table_bt.clicked.connect(self.check_species_table)

        self.mr_clear_bt.clicked.connect(self.clear_map)
        self.mr_generate_bt.clicked.connect(self.generate_map_inaccessible)
        self.mr_random_bt.clicked.connect(self.random_map_parameter)

        self.simulate.clicked.connect(self.simulate_one_specie_individual)
        # self.simulate.clicked.connect(self.simulate_logistic_growth_discrete_individual)

        # check
        self.name.textChanged.connect(self.check_disable_specie_data)
        self.survival_rate.textChanged.connect(self.check_disable_specie_data)
        self.fecundity.textChanged.connect(self.check_disable_specie_data)
        self.initial_population.textChanged.connect(self.check_disable_specie_data)
        self.growth_rate.textChanged.connect(self.check_disable_specie_data)
        self.carrying_capacity.textChanged.connect(self.check_disable_specie_data)
        self.natural_life_span.textChanged.connect(self.check_disable_specie_data)
        self.move_speed_mean.textChanged.connect(self.check_disable_specie_data)
        self.move_speed_std.textChanged.connect(self.check_disable_specie_data)
        self.marriage_age.textChanged.connect(self.check_disable_specie_data)
        self.attack_ability.textChanged.connect(self.check_disable_specie_data)
        self.escape_ability.textChanged.connect(self.check_disable_specie_data)
        self.alive_ability_change_per_time.textChanged.connect(self.check_disable_specie_data)
        self.fecundity_attenuation.textChanged.connect(self.check_disable_specie_data)

        self.mr_button_draw_1.clicked.connect(lambda: set_color(self.mr_grid_widget, 'empty'))
        self.mr_button_draw_2.clicked.connect(lambda: set_color(self.mr_grid_widget, 'inaccessible'))
        self.plot_map_target_specie.clicked.connect(self.plot_target_specie_on_map)

        def set_color(grid_widget, color_index):
            grid_widget.current_color = color_index

    def get_widget(self):
        return self