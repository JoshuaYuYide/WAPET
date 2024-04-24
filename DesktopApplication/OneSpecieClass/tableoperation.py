import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class TableOperation:
    def __init__(self):
        pass

    def reset_table(self):
        self.table.setRowCount(8)
        self.table.setColumnCount(0)
        self.table.setVerticalHeaderLabels(["species", "name", "survival rate", "fecundity", "initial population", "growth rate", "carrying capacity", "natural life span"])
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.items = 0

    def reset_result_table(self):
        self.result_table.setRowCount(8)
        self.result_table.setColumnCount(0)
        self.result_table.setVerticalHeaderLabels(["species", "name", "survival rate", "fecundity", "initial population", "growth rate", "carrying capacity", "natural life span"])
        self.result_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

    @Slot()
    def add_data_table_element(self):
        self.table.insertColumn(self.items)
        self.table.setItem(0, self.items, QTableWidgetItem(self.species.currentText()))
        self.table.setItem(1, self.items, QTableWidgetItem(self.name.text()))
        self.table.setItem(2, self.items, QTableWidgetItem(self.survival_rate.text()))
        self.table.setItem(3, self.items, QTableWidgetItem(self.fecundity.text()))
        self.table.setItem(4, self.items, QTableWidgetItem(self.initial_population.text()))
        self.table.setItem(5, self.items, QTableWidgetItem(self.growth_rate.text()))
        self.table.setItem(6, self.items, QTableWidgetItem(self.carrying_capacity.text()))
        self.table.setItem(7, self.items, QTableWidgetItem(self.natural_life_span.text()))
        self.items += 1

    @Slot()
    def clear_table(self):
        self.reset_table()

























