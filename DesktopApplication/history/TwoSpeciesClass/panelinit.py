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

    def leftmost_element(self):
        self.leftmost_table_title = QLabel("Simulation Result Table")
        self.leftmost_table_title.setAlignment(Qt.AlignCenter)
        font = self.leftmost_table_title.font()
        font.setBold(True)
        self.leftmost_table_title.setFont(font)

        self.result_table = QTableWidget()
        self.reset_result_table()


    def leftmost_panel(self):
        self.leftmost_element()
        self.leftmost = QVBoxLayout()
        self.leftmost.addWidget(self.leftmost_table_title)
        self.leftmost.addWidget(self.result_table)
        return self.leftmost

    def left_element(self):
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
        self.species.addItem("target species")
        self.species.addItems("food species")
        self.species.addItems("predator species")

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
        self.feed_rate = QLineEdit()
        self.feed_rate.setClearButtonEnabled(True)
        self.feed_rate.setText("0.1")
        self.preyed_rate = QLineEdit()
        self.preyed_rate.setClearButtonEnabled(True)
        self.preyed_rate.setText("0.1")

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
        self.env_submit = QPushButton("Submit")
        self.env_cancel = QPushButton("Cancel")
        self.env_op_random = QPushButton("Random")

        self.table = QTableWidget()
        self.reset_table()

    def left_panel(self):
        # left layout
        self.left_element()
        # small layout construction
        self.sepcie = QGridLayout()
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

        self.env_data = QGridLayout()
        self.env_data.addWidget(QLabel("food initial amount:"), 0, 0)
        self.env_data.addWidget(self.env_food_initial_amount, 0, 1)
        self.env_data.addWidget(QLabel("random disaster:"), 0, 2)
        self.env_data.addWidget(self.env_random_disaster, 0, 3)
        self.env_data.addWidget(QLabel("food growth rate:"), 2, 0)
        self.env_data.addWidget(self.env_food_growth_rate, 2, 1)
        self.env_data.addWidget(QLabel("diease rate:"), 2, 2)
        self.env_data.addWidget(self.env_diease_rate, 2, 3)
        self.env_data.addWidget(QLabel("simulation years:"), 3, 0)
        self.env_data.addWidget(self.simulation_years, 3, 1)

        self.env_operation = QHBoxLayout()
        self.env_operation.addWidget(self.env_submit)
        self.env_operation.addWidget(self.env_cancel)
        self.env_operation.addWidget(self.env_op_random)

        self.left = QVBoxLayout()
        self.left.addWidget(self.left_specie_title)
        self.left.addLayout(self.sepcie)
        self.left.addLayout(self.sepcie_operation)
        self.left.addWidget(self.left_environment_title)
        self.left.addLayout(self.env_data)
        self.left.addLayout(self.env_operation)
        self.left.addWidget(self.left_specie_table_title)
        self.left.addWidget(self.table)
        return self.left

    def middle_element(self):
        self.submit = QPushButton("Submit")
        self.clear_table_bt = QPushButton("Clear Table")
        self.clear_plot_bt = QPushButton("Clear Plot")
        self.plot = QPushButton("Plot")
        self.export_table = QPushButton("Export Table")
        self.export_plot = QPushButton("Export Plot")

        self.submit.setEnabled(True)
        self.export_table.setEnabled(False)
        self.export_plot.setEnabled(False)

        # barchart
        self.barchart = QChartView()
        self.barchart.setRenderHint(QPainter.Antialiasing)

    def middle_panel(self):
        self.middle_element()
        # operation layout
        self.operation_panel = QGridLayout()
        self.operation_panel.addWidget(self.submit, 1, 0)
        self.operation_panel.addWidget(self.plot, 1, 1)
        self.operation_panel.addWidget(self.clear_table_bt, 2, 0)
        self.operation_panel.addWidget(self.clear_plot_bt, 2, 1)
        self.operation_panel.addWidget(self.export_table, 3, 0)
        self.operation_panel.addWidget(self.export_plot, 3, 1)

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





