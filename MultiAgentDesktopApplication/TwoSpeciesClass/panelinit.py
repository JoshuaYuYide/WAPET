from OneSpecieClass.panelinit import PanelInit, GridWidget
import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen, QColor
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu,
                               QCheckBox, QTabWidget, QGroupBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class PanelInitTwo(PanelInit):
    def left_element(self):
        super().left_element()
        self.species.addItem("prey")
        self.species.addItem("predator")

        self.plot_map_predator = QPushButton("Plot Predator Distribution")
        self.plot_map_prey = QPushButton("Plot Prey Distribution")

        self.middle_right_plot_layout.addWidget(self.plot_map_predator, 1, 1)
        self.middle_right_plot_layout.addWidget(self.plot_map_prey, 1, 2)

    def right_element(self):
        super().right_element()

        self.piechart_gender_predator = QChartView()
        self.piechart_gender_predator.setRenderHint(QPainter.Antialiasing)

        self.piechart_gender_prey = QChartView()
        self.piechart_gender_prey.setRenderHint(QPainter.Antialiasing)

        self.histchart_age_predator = QChartView()
        self.histchart_age_predator.setRenderHint(QPainter.Antialiasing)

        self.histchart_age_prey = QChartView()
        self.histchart_age_prey.setRenderHint(QPainter.Antialiasing)

        self.piechart_life_status_predator = QChartView()
        self.piechart_life_status_predator.setRenderHint(QPainter.Antialiasing)

        self.piechart_life_status_prey = QChartView()
        self.piechart_life_status_prey.setRenderHint(QPainter.Antialiasing)

