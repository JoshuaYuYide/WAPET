# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial

import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.features = ["name", "survival rate", "fecundity", "initial_population", "growth_rate", "carrying_capacity", "natural_life_span"]

        self.species = QComboBox()
        self.species.addItem("species1")
        self.species.addItem("species2")
        self.species.addItem("species3")

        self.name = QLineEdit()
        self.name.setClearButtonEnabled(True)
        self.name.setText('fish')
        self.survival_rate = QLineEdit()
        self.survival_rate.setClearButtonEnabled(True)
        self.survival_rate.setText("10000")
        self.fecundity = QLineEdit()
        self.fecundity.setClearButtonEnabled(True)
        self.fecundity.setText("10000")
        self.initial_population = QLineEdit()
        self.initial_population.setClearButtonEnabled(True)
        self.initial_population.setText("10000")
        self.growth_rate = QLineEdit()
        self.growth_rate.setClearButtonEnabled(True)
        self.growth_rate.setText("10000")
        self.carrying_capacity = QLineEdit()
        self.carrying_capacity.setClearButtonEnabled(True)
        self.carrying_capacity.setText("10000")
        self.natural_life_span = QLineEdit()
        self.natural_life_span.setClearButtonEnabled(True)
        self.natural_life_span.setText("10000")

        self.table = QTableWidget()
        self.reset_table()

        self.submit = QPushButton("Submit")
        self.clear = QPushButton("Clear")
        self.plot = QPushButton("Plot")

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.submit.setEnabled(True)

        # left panel
        self.left = QVBoxLayout()
        self.left1 = QGridLayout()
        self.left1.addWidget(QLabel("species:"), 0, 0)
        self.left1.addWidget(self.species, 0, 1)
        self.left1.addWidget(QLabel("name:"), 0, 2)
        self.left1.addWidget(self.name, 0, 3)
        self.left1.addWidget(QLabel("survival rate:"), 1, 2)
        self.left1.addWidget(self.survival_rate, 1, 3)
        self.left1.addWidget(QLabel("fecundity:"), 1, 0)
        self.left1.addWidget(self.fecundity, 1, 1)
        self.left1.addWidget(QLabel("initial population:"), 3, 2)
        self.left1.addWidget(self.initial_population, 3, 3)
        self.left1.addWidget(QLabel("growth rate:"), 2, 0)
        self.left1.addWidget(self.growth_rate, 2, 1)
        self.left1.addWidget(QLabel("carrying capacity:"), 2, 2)
        self.left1.addWidget(self.carrying_capacity, 2, 3)
        self.left1.addWidget(QLabel("natural life span:"), 3, 0)
        self.left1.addWidget(self.natural_life_span, 3, 1)
        self.left.addLayout(self.left1)
        self.left.addWidget(self.table)

        # right panel
        self.right = QVBoxLayout()
        self.right.addWidget(self.submit)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.chart_view)

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)

        # Signals and Slots
        self.submit.clicked.connect(self.add_element)
        self.clear.clicked.connect(self.clear_table)
        self.plot.clicked.connect(self.plot_data)
        self.name.textChanged.connect(self.check_disable)
        self.survival_rate.textChanged.connect(self.check_disable)
        self.fecundity.textChanged.connect(self.check_disable)
        self.initial_population.textChanged.connect(self.check_disable)
        self.growth_rate.textChanged.connect(self.check_disable)
        self.carrying_capacity.textChanged.connect(self.check_disable)
        self.natural_life_span.textChanged.connect(self.check_disable)

    @Slot()
    def check_disable(self):
        enabled = bool(self.name.text() and self.survival_rate.text() and self.fecundity.text() and self.initial_population.text() and self.growth_rate.text() and self.carrying_capacity.text() and self.natural_life_span.text())
        if enabled:
            self.submit.setEnabled(True)
        else:
            self.submit.setEnabled(False)

    @Slot()
    def add_element(self):
        self.table.insertColumn(self.items)
        self.table.setItem(0, self.items, QTableWidgetItem(self.name.text()))
        self.table.setItem(1, self.items, QTableWidgetItem(self.survival_rate.text()))
        self.table.setItem(2, self.items, QTableWidgetItem(self.fecundity.text()))
        self.table.setItem(3, self.items, QTableWidgetItem(self.initial_population.text()))
        self.table.setItem(4, self.items, QTableWidgetItem(self.growth_rate.text()))
        self.table.setItem(5, self.items, QTableWidgetItem(self.carrying_capacity.text()))
        self.table.setItem(6, self.items, QTableWidgetItem(self.natural_life_span.text()))
        self.items += 1


    @Slot()
    def clear_table(self):
        self.reset_table()

    def reset_table(self):
        self.table.setRowCount(7)
        self.table.setColumnCount(0)
        self.table.setVerticalHeaderLabels(["name", "survival rate", "fecundity", "initial population", "growth rate", "carrying capacity", "natural life span"])
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.items = 0

    @Slot()
    def plot_data(self):
        # Get table information
        series = QPieSeries()
        for i in range(self.table.columnCount()):
            text = self.table.item(0, i).text()
            number = float(self.table.item(3, i).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Landscape Natural Deduction")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = self.file_menu.addAction("Exit", self.close)
        exit_action.setShortcut("Ctrl+Q")

        self.setCentralWidget(widget)
        self.setLayout(widget.layout)


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(1000, 600)
    window.show()

    # Execute application
    sys.exit(app.exec())
