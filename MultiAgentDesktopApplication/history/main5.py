# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial

import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel)
from PySide6.QtCharts import QChartView, QPieSeries, QChart


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.items = 0

        self.name = QLineEdit()
        self.name.setClearButtonEnabled(True)
        self.survival_rate = QLineEdit()
        self.survival_rate.setClearButtonEnabled(True)
        self.fecundity = QLineEdit()
        self.fecundity.setClearButtonEnabled(True)
        self.initial_population = QLineEdit()
        self.initial_population.setClearButtonEnabled(True)
        self.growth_rate = QLineEdit()
        self.growth_rate.setClearButtonEnabled(True)
        self.carrying_capacity = QLineEdit()
        self.carrying_capacity.setClearButtonEnabled(True)
        self.natural_life_span = QLineEdit()
        self.natural_life_span.setClearButtonEnabled(True)

        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.plot = QPushButton("Plot")

        self.add.setEnabled(False)

        self.layout = QGridLayout(self)

        self.layout.addWidget(QLabel("name:"), 0, 0)
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(QLabel("survival rate:"), 1, 0)
        self.layout.addWidget(self.survival_rate, 1, 1)
        self.layout.addWidget(QLabel("fecundity:"), 2, 0)
        self.layout.addWidget(self.fecundity, 2, 1)
        self.layout.addWidget(QLabel("initial population:"), 3, 0)
        self.layout.addWidget(self.initial_population, 3, 1)
        self.layout.addWidget(QLabel("growth rate:"), 4, 0)
        self.layout.addWidget(self.growth_rate, 4, 1)
        self.layout.addWidget(QLabel("carrying capacity:"), 5, 0)
        self.layout.addWidget(self.carrying_capacity, 5, 1)
        self.layout.addWidget(QLabel("natural life span:"), 6, 0)
        self.layout.addWidget(self.natural_life_span, 6, 1)




class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Tutorial")

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
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec())
