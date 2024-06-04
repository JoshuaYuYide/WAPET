import sys
from PySide6.QtCore import Qt, Slot, QPointF, QSize
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu, QTabWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
from onespecie import OneSpecie
from twospecies import TwoSpecies


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    tabWidget = QTabWidget()

    screen_size = tabWidget.screen().size()
    minimum_size = QSize(screen_size.width() / 1.5, screen_size.height() / 1.5)

    # Create bar graph
    one_specie = OneSpecie()
    two_species = TwoSpecies()

    tabWidget.addTab(one_specie.get_widget(), "Single Specie")
    tabWidget.addTab(two_species.get_widget(), "Multiple Species")

    tabWidget.resize(minimum_size)
    tabWidget.show()
    sys.exit(app.exec())

