import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries


class PanelInit:
    def __init__(self):
        pass

    def leftmost_panel(self):
        self.leftmost = QVBoxLayout()
        self.result_table = QTableWidget()
        self.reset_result_table()
        self.leftmost.addWidget(self.result_table)
        return self.leftmost

    def left_panel(self):
        # left layout
        self.left_specie_title = QLabel("Species Data Management Panel")
        self.left_specie_title.setAlignment(Qt.AlignCenter)
        font = self.left_specie_title.font()
        font.setBold(True)
        self.left_specie_title.setFont(font)

        self.left_environment_title = QLabel("Environment Data Management Panel")
        self.left_environment_title.setAlignment(Qt.AlignCenter)
        font = self.left_environment_title.font()
        font.setBold(True)
        self.left_environment_title.setFont(font)

        self.left_specie_table_title = QLabel("Specie Data Table")
        self.left_specie_table_title.setAlignment(Qt.AlignCenter)
        font = self.left_specie_table_title.font()
        font.setBold(True)
        self.left_specie_table_title.setFont(font)


        self.features = ["name", "survival rate", "fecundity", "initial_population", "growth_rate", "carrying_capacity",
                         "natural_life_span"]

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
        self.simulation_years = QLineEdit()
        self.simulation_years.setClearButtonEnabled(True)
        self.simulation_years.setText("10000")

        self.species_submit = QPushButton("Submit")
        self.species_clear = QPushButton("Clear")
        self.species_random = QPushButton("Random")
        self.species_random_seed = QLineEdit()
        self.species_random_seed.setClearButtonEnabled(True)
        self.species_random_seed.setText("0")

        self.env_random_disaster = QLineEdit()
        self.env_random_disaster.setClearButtonEnabled(True)
        self.env_random_disaster.setText("0")
        self.env_food_initial_amount = QLineEdit()
        self.env_food_initial_amount.setClearButtonEnabled(True)
        self.env_food_initial_amount.setText("10000")
        self.env_food_growth_rate = QLineEdit()
        self.env_food_growth_rate.setClearButtonEnabled(True)
        self.env_food_growth_rate.setText("0.1")
        self.env_diease_rate = QLineEdit()
        self.env_diease_rate.setClearButtonEnabled(True)
        self.env_diease_rate.setText("0.1")

        # small layout construction
        self.sepcie = QGridLayout()
        self.sepcie.addWidget(QLabel("simulation years:"), 0, 0)
        self.sepcie.addWidget(self.simulation_years, 0, 1)
        self.sepcie.addWidget(QLabel("species:"), 1, 0)
        self.sepcie.addWidget(self.species, 1, 1)
        self.sepcie.addWidget(QLabel("name:"), 1, 2)
        self.sepcie.addWidget(self.name, 1, 3)
        self.sepcie.addWidget(QLabel("survival rate:"), 2, 0)
        self.sepcie.addWidget(self.survival_rate, 2, 1)
        self.sepcie.addWidget(QLabel("fecundity:"), 2, 2)
        self.sepcie.addWidget(self.fecundity, 2, 3)
        self.sepcie.addWidget(QLabel("growth rate:"), 3, 0)
        self.sepcie.addWidget(self.growth_rate, 3, 1)
        self.sepcie.addWidget(QLabel("initial population:"), 3, 2)
        self.sepcie.addWidget(self.initial_population, 3, 3)
        self.sepcie.addWidget(QLabel("natural life span:"), 4, 0)
        self.sepcie.addWidget(self.natural_life_span, 4, 1)
        self.sepcie.addWidget(QLabel("carrying capacity:"), 4, 2)
        self.sepcie.addWidget(self.carrying_capacity, 4, 3)

        self.sepcie_operation = QHBoxLayout()
        self.sepcie_operation.addWidget(self.species_submit)
        self.sepcie_operation.addWidget(self.species_clear)
        self.sepcie_operation.addWidget(self.species_random)
        self.sepcie_operation.addWidget(QLabel("random seed:"))
        self.sepcie_operation.addWidget(self.species_random_seed)

        self.env = QGridLayout()
        self.env.addWidget(QLabel("food initial amount:"), 0, 0)
        self.env.addWidget(self.env_food_initial_amount, 0, 1)
        self.env.addWidget(QLabel("random disaster:"), 0, 2)
        self.env.addWidget(self.env_random_disaster, 0, 3)
        self.env.addWidget(QLabel("food growth rate:"), 2, 0)
        self.env.addWidget(self.env_food_growth_rate, 2, 1)
        self.env.addWidget(QLabel("diease rate:"), 2, 2)
        self.env.addWidget(self.env_diease_rate, 2, 3)



        self.table = QTableWidget()
        self.reset_table()

        self.left = QVBoxLayout()
        self.left.addWidget(self.left_specie_title)
        self.left.addLayout(self.sepcie)
        self.left.addLayout(self.sepcie_operation)
        self.left.addWidget(self.left_environment_title)
        self.left.addLayout(self.env)
        self.left.addWidget(self.left_specie_table_title)
        self.left.addWidget(self.table)
        return self.left

    def middle_panel(self):
        # operation layout
        self.submit = QPushButton("Submit")
        self.clear = QPushButton("Clear")
        self.plot = QPushButton("Plot")
        self.export_table = QPushButton("Export Table")
        self.export_plot = QPushButton("Export Plot")

        self.submit.setEnabled(True)
        self.export_table.setEnabled(False)
        self.export_plot.setEnabled(False)

        self.operation_panel = QGridLayout()
        self.operation_panel.addWidget(self.submit, 1, 0)
        self.operation_panel.addWidget(self.plot, 1, 1)
        self.operation_panel.addWidget(self.clear, 2, 0)
        self.operation_panel.addWidget(self.export_table, 2, 1)
        self.operation_panel.addWidget(self.export_plot, 3, 0)

        # barchart
        self.barchart = QChartView()
        self.barchart.setRenderHint(QPainter.Antialiasing)

        # middle title
        self.middle_title = QLabel("Operation Panel")
        self.middle_title.setAlignment(Qt.AlignCenter)
        font = self.middle_title.font()
        font.setBold(True)
        self.middle_title.setFont(font)

        # slider layout
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setRange(0, 1000)
        self.slider.setVisible(False)
        self.slider_left = QLabel("0")
        self.slider_right = QLabel("0")
        self.slider_left.setVisible(False)
        self.slider_right.setVisible(False)
        self.slider_layout = QHBoxLayout()
        self.slider_layout.addWidget(self.slider_left)
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.slider_right)

        # middle layout
        self.middle = QVBoxLayout()
        self.middle.addWidget(self.middle_title)
        self.middle.addLayout(self.operation_panel)
        self.middle.addLayout(self.slider_layout)
        self.middle.addWidget(self.barchart)

        return self.middle

    def right_panel(self):
        self.boxchart = QChartView()
        self.boxchart.setRenderHint(QPainter.Antialiasing)

        self.linechart = QChartView()
        self.linechart.setRenderHint(QPainter.Antialiasing)

        self.right = QVBoxLayout()
        self.right.addWidget(self.boxchart)
        self.right.addWidget(self.linechart)

        return self.right





