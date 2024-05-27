from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class Check:
    def __init__(self):
        pass

    @Slot()
    def check_disable(self):
        enabled = bool(
            self.name.text() and self.survival_rate.text() and self.fecundity.text() and self.initial_population.text() and self.growth_rate.text() and self.carrying_capacity.text() and self.natural_life_span.text())
        if enabled:
            self.species_submit_bt.setEnabled(True)
        else:
            self.species_submit_bt.setEnabled(False)

    @Slot()
    def check_species_table(self):
        if self.species_table.columnCount() > 0:
            self.species_delete_bt.setEnabled(True)
            self.plot.setEnabled(True)
            self.clear_table_bt.setEnabled(True)
            self.simulate.setEnabled(True)
            self.clear_table_bt.setEnabled(True)
        else:
            self.species_delete_bt.setEnabled(False)
            self.plot.setEnabled(False)
            self.clear_table_bt.setEnabled(False)
            self.simulate.setEnabled(False)
            self.clear_table_bt.setEnabled(False)

        if self.species_table.columnCount() == 1:
            self.species_submit_bt.setEnabled(False)
        if self.species_table.columnCount() == 0:
            self.species_submit_bt.setEnabled(True)