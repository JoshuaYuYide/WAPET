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
        pass

    @Slot()
    def submit_species_func(self):
        self.species_table.insertColumn(self.species_items)
        self.species_table.setItem(0, self.species_items, QTableWidgetItem(self.species.currentText()))
        self.species_table.setItem(1, self.species_items, QTableWidgetItem(self.name.text()))
        self.species_table.setItem(2, self.species_items, QTableWidgetItem(self.survival_rate.text()))
        self.species_table.setItem(3, self.species_items, QTableWidgetItem(self.fecundity.text()))
        self.species_table.setItem(4, self.species_items, QTableWidgetItem(self.initial_population.text()))
        self.species_table.setItem(5, self.species_items, QTableWidgetItem(self.growth_rate.text()))
        self.species_table.setItem(6, self.species_items, QTableWidgetItem(self.carrying_capacity.text()))
        self.species_table.setItem(7, self.species_items, QTableWidgetItem(self.natural_life_span.text()))
        self.species_items += 1

    def reset_result_table(self):
        self.result_table.setColumnCount(2)
        self.result_table.setRowCount(0)
        self.result_table.setVerticalHeaderLabels(["target population", "timestep"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

    def reset_species_table(self):
        self.species_table.setRowCount(8)
        self.species_table.setColumnCount(0)
        self.species_table.setVerticalHeaderLabels(["species", "name", "survival rate", "fecundity", "initial population", "growth rate", "carrying capacity", "natural life span"])
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

    @Slot()
    def delete_species_func(self):
        self.species_table.removeColumn(self.species_table.currentColumn())
        column_count = self.species_table.columnCount()
        self.species_table.setColumnCount(column_count - 1)
        self.species_items -= 1
