import sys
from PySide6.QtCore import Qt, Slot, QPointF, QSize
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu, QTabWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
from onespecie import OneSpecie

# class MainWindow(QMainWindow):
#     def __init__(self, OneSpecie):
#         super().__init__()
#         self.setWindowTitle("Landscape Natural Deduction")
#
#         # Menu
#         self.menu = self.menuBar()
#         self.file_menu = self.menu.addMenu("File")
#
#         # Exit QAction
#         exit_action = self.file_menu.addAction("Exit", self.close)
#         exit_action.setShortcut("Ctrl+Q")
#
#         # policy
#         self.file_menu = self.menu.addMenu("Policy")
#         self.file_menu.addAction("Random Policy", OneSpecie.random_plot_linechart)
#
#         # role change
#         self.file_menu = self.menu.addMenu("Role Selection")
#         self.file_menu.addAction("one specie nature deduction")
#         self.file_menu.addAction("two species nature deduction")
#         self.file_menu.addAction("two species artificial deduction")
#
#         # help
#         self.help_menu = self.menu.addMenu("Help")
#         self.help_menu.addAction("Help", OneSpecie.show_help)
#
#         self.setCentralWidget(OneSpecie)
#         self.setLayout(OneSpecie.layout)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    tabWidget = QTabWidget()

    screen_size = tabWidget.screen().size()
    minimum_size = QSize(screen_size.width() / 1.2, screen_size.height() / 1.75)

    # Create bar graph
    one_specie = OneSpecie()

    tabWidget.addTab(one_specie.get_widget(), "One Specie")

    tabWidget.resize(minimum_size)
    tabWidget.show()
    sys.exit(app.exec())

