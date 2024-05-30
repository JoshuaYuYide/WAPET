import random
import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu, QCheckBox, QTabWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class UpdatePanel:
    def __init__(self):
        self.specie_table_rowname = ["species", "name", "survival rate", "fecundity",
                                                    "initial population", "growth rate",
                                                    "maximum age", "speed mean", "speed std", "marriage age",
                                                    "attack ability", "escape ability", "alive ability change rate",
                                                    "fecundity attenuation", "climate type", "carrying capacity",
                                                    "simulation months", "map"]

    @Slot()
    def submit_species_func(self):
        self.species_table.insertColumn(self.species_items)
        self.species_table.setItem(0, self.species_items, QTableWidgetItem(self.species.currentText()))
        self.species_table.setItem(1, self.species_items, QTableWidgetItem(self.name.text()))
        self.species_table.setItem(2, self.species_items, QTableWidgetItem(self.survival_rate.text()))
        self.species_table.setItem(3, self.species_items, QTableWidgetItem(self.fecundity.text()))
        self.species_table.setItem(4, self.species_items, QTableWidgetItem(self.initial_population.text()))
        self.species_table.setItem(5, self.species_items, QTableWidgetItem(self.growth_rate.text()))
        self.species_table.setItem(6, self.species_items, QTableWidgetItem(self.natural_life_span.text()))
        self.species_table.setItem(7, self.species_items, QTableWidgetItem(self.move_speed_mean.text()))
        self.species_table.setItem(8, self.species_items, QTableWidgetItem(self.move_speed_std.text()))
        self.species_table.setItem(9, self.species_items, QTableWidgetItem(self.marriage_age.text()))
        self.species_table.setItem(10, self.species_items, QTableWidgetItem(self.attack_ability.text()))
        self.species_table.setItem(11, self.species_items, QTableWidgetItem(self.escape_ability.text()))
        self.species_table.setItem(12, self.species_items, QTableWidgetItem(self.alive_ability_change_per_time.text()))
        self.species_table.setItem(13, self.species_items, QTableWidgetItem(self.fecundity_attenuation.text()))
        self.species_table.setItem(14, self.species_items, QTableWidgetItem(self.climate_type.currentText()))
        self.species_table.setItem(15, self.species_items, QTableWidgetItem(self.carrying_capacity.text()))
        self.species_table.setItem(16, self.species_items, QTableWidgetItem(self.simulation_years.text()))
        self.species_table.setItem(17, self.species_items, QTableWidgetItem(self.mr_grid_widget.get_map_name()))
        self.species_items += 1

    def reset_result_table(self):
        self.result_table.setColumnCount(2)
        self.result_table.setRowCount(0)
        self.result_table.setVerticalHeaderLabels(["target population", "timestep"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

    def reset_species_table(self):
        self.species_table.setRowCount(18)
        self.species_table.setColumnCount(0)
        self.species_table.setVerticalHeaderLabels(self.specie_table_rowname)
        self.species_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.species_items = 0

    @Slot()
    def clear_table_func(self):
        self.reset_species_table()
        self.reset_result_table()

    @Slot()
    def clear_species_func(self):
        self.name.clear()
        self.survival_rate.clear()
        self.fecundity.clear()
        self.initial_population.clear()
        self.growth_rate.clear()
        self.carrying_capacity.clear()
        self.natural_life_span.clear()
        self.move_speed_mean.clear()
        self.move_speed_std.clear()
        self.marriage_age.clear()
        self.attack_ability.clear()
        self.escape_ability.clear()
        self.alive_ability_change_per_time.clear()
        self.fecundity_attenuation.clear()
        self.climate_type.setCurrentIndex(0)
        self.simulation_years.clear()

    @Slot()
    def random_species_func(self):
        random.seed(1)
        self.survival_rate.setText(str(random.random()))
        self.fecundity.setText(str(random.random()))
        self.initial_population.setText(str(random.randint(1, 100)))
        self.growth_rate.setText(str(random.random()))
        self.carrying_capacity.setText(str(random.randint(1, 100)))
        self.natural_life_span.setText(str(random.randint(1, 100)))
        self.move_speed_mean.setText(str(random.random()))
        self.move_speed_std.setText(str(random.random()))
        self.marriage_age.setText(str(random.randint(1, 100)))
        self.attack_ability.setText(str(random.random()))
        self.escape_ability.setText(str(random.random()))
        self.alive_ability_change_per_time.setText(str(random.random()))
        self.fecundity_attenuation.setText(str(-random.random()))
        self.climate_type.setCurrentIndex(random.randint(0, 3))
        self.simulation_years.setText(str(random.randint(1, 100)))

    @Slot()
    def delete_species_func(self):
        self.species_table.removeColumn(self.species_table.currentColumn())
        column_count = self.species_table.columnCount()
        self.species_table.setColumnCount(column_count - 1)
        self.species_items -= 1

    @Slot()
    def generate_map_inaccessible(self):
        self.mr_grid_widget.clear()
        max_num = int(self.mr_map_size.text())
        self.mr_grid_widget.resize_map(max_num)
        inaccessible_num = int(self.mr_inaccessible_number.text())
        self.inaccessible_list = []

        for _ in range(inaccessible_num):
            inaccessible_pos = [random.randint(0, max_num - 1), random.randint(0, max_num - 1)]
            if inaccessible_pos not in self.inaccessible_list:
                self.mr_grid_widget.draw_inaccessible(inaccessible_pos)
                self.inaccessible_list.append(inaccessible_pos)

    @Slot()
    def clear_map(self):
        self.mr_grid_widget.clear()

    @Slot()
    def read_map(self):
        self.mr_grid_widget.read_map()

    @Slot()
    def random_map_parameter(self):
        map_size = random.randint(1, 10)
        self.mr_map_size.setText(str(map_size))
        self.mr_inaccessible_number.setText(str(random.randint(1, map_size)))
