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
from artificialspecies import ArtificialSpecies

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    tabWidget = QTabWidget()

    screen_size = tabWidget.screen().size()
    minimum_size = QSize(screen_size.width() / 1.2, screen_size.height() / 1.5)

    # Create bar graph
    one_specie = OneSpecie()
    two_species = TwoSpecies()
    artificial_species = ArtificialSpecies()

    tabWidget.addTab(one_specie.get_widget(), "One Specie")
    tabWidget.addTab(two_species.get_widget(), "Two Species")
    tabWidget.addTab(artificial_species, "Artificial Species")
    tabWidget.addTab(QWidget(), "Policy Analysis")

    tabWidget.resize(minimum_size)
    tabWidget.show()
    sys.exit(app.exec())

