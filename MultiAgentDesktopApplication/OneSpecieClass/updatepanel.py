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
        # self.specie_table_rowname = ["species", "name", "survival rate", "fecundity",
        #                              "initial population", "growth rate",
        #                              "maximum age", "speed mean", "speed std", "marriage age",
        #                              "attack ability", "escape ability", "alive ability change rate",
        #                              "fecundity attenuation", "climate type", "carrying capacity",
        #                              "hunger increment",
        #                              "simulation step", "map"]
        self.specie_table_rowname =[self.species.objectName(), self.name.objectName(), self.survival_rate.objectName(),
                                    self.fecundity.objectName(), self.initial_population.objectName(),
                                    self.growth_rate.objectName(), self.natural_life_span.objectName(),
                                    self.move_speed_mean.objectName(), self.move_speed_std.objectName(),
                                    self.marriage_age.objectName(), self.attack_ability.objectName(),
                                    self.escape_ability.objectName(), self.alive_ability_change_per_time.objectName(),
                                    self.fecundity_attenuation.objectName(), self.climate_type.objectName(),
                                    self.carrying_capacity.objectName(), self.hunger_increment.objectName(),
                                    self.simulation_years.objectName(), self.mr_grid_widget.objectName()]
        self.inaccessible_list = []

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
        self.species_table.setItem(16, self.species_items, QTableWidgetItem(self.hunger_increment.text()))
        self.species_table.setItem(17, self.species_items, QTableWidgetItem(self.simulation_years.text()))
        self.species_table.setItem(18, self.species_items, QTableWidgetItem(self.mr_grid_widget.get_map_name()))
        self.species_items += 1

    def reset_result_table(self):
        self.result_table.setColumnCount(2)
        self.result_table.setRowCount(0)
        self.result_table.setVerticalHeaderLabels(["target population", "timestep"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

    def reset_species_table(self):
        self.species_table.setRowCount(len(self.specie_table_rowname))
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
        self.hunger_increment.clear()
        self.age_increment.clear()
        self.cell_neighbors_occupy.clear()
        self.carrying_cap_std.clear()

    @Slot()
    def random_species_func(self):
        random.seed(1)
        self.survival_rate.setText(str(round(random.random(), 2)))
        self.fecundity.setText(str(round(random.random(), 2)))
        self.initial_population.setText(str(random.randint(1, 100)))
        self.growth_rate.setText(str(round(random.random(), 2)))
        self.carrying_capacity.setText(str(random.randint(1, 100)))
        self.natural_life_span.setText(str(random.randint(1, 100)))
        self.move_speed_mean.setText(str(round(random.random(), 2)))
        self.move_speed_std.setText(str(round(random.random(), 2)))
        self.marriage_age.setText(str(random.randint(1, 100)))
        self.attack_ability.setText(str(round(random.random(), 2)))
        self.escape_ability.setText(str(round(random.random(), 2)))
        self.alive_ability_change_per_time.setText(str(round(random.random(), 2)))
        self.fecundity_attenuation.setText(str(-round(random.random(), 2)))
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
        self.mr_map_size.clear()
        self.mr_inaccessible_number.clear()
        self.mr_grid_widget.clear()

    @Slot()
    def read_map(self):
        self.mr_grid_widget.read_map()

    @Slot()
    def random_map_parameter(self):
        map_size = random.randint(1, 10)
        self.mr_map_size.setText(str(map_size))
        self.mr_inaccessible_number.setText(str(random.randint(1, map_size)))

    @Slot()
    def confirm_map(self):
        if self.mr_button_box.isChecked():
            self.mr_map_size.setEnabled(False)
            self.mr_inaccessible_number.setEnabled(False)
            self.mr_generate_bt.setEnabled(False)
            self.mr_clear_bt.setEnabled(False)
            self.mr_random_bt.setEnabled(False)
            self.mr_button_draw_1.setEnabled(False)
            self.mr_button_draw_2.setEnabled(False)
        else:
            self.mr_map_size.setEnabled(True)
            self.mr_inaccessible_number.setEnabled(True)
            self.mr_generate_bt.setEnabled(True)
            self.mr_clear_bt.setEnabled(True)
            self.mr_random_bt.setEnabled(True)
            self.mr_button_draw_1.setEnabled(True)
            self.mr_button_draw_2.setEnabled(True)

    @Slot()
    def clear_plot(self):
        while self.right_plot.count() > 0:
            self.right_plot.removeTab(0)


