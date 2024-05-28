import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen, QColor
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu, QCheckBox, QTabWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class PanelInit():
    def __init__(self):
        pass

    def leftmost_element(self):
        self.species_table_title = QLabel("Species Data Table")
        self.species_table_title.setAlignment(Qt.AlignCenter)
        font = self.species_table_title.font()
        font.setBold(True)
        self.species_table_title.setFont(font)

        self.result_table_title = QLabel("Simulation Result Table")
        self.result_table_title.setAlignment(Qt.AlignCenter)
        font = self.result_table_title.font()
        font.setBold(True)
        self.result_table_title.setFont(font)

        self.species_table = QTableWidget()
        self.reset_species_table()

        self.result_table = QTableWidget()
        self.reset_result_table()

    def leftmost_panel(self):
        self.leftmost_element()

        self.species_table_widget = QWidget()
        self.species_table_panel = QVBoxLayout(self.species_table_widget)
        self.species_table_panel.addWidget(self.species_table_title)
        self.species_table_panel.addWidget(self.species_table)

        self.result_table_widget = QWidget()
        self.result_table_panel = QVBoxLayout(self.result_table_widget)
        self.result_table_panel.addWidget(self.result_table_title)
        self.result_table_panel.addWidget(self.result_table)

        self.leftmost = QTabWidget()
        self.leftmost.addTab(self.species_table_widget, "Species Data Table")
        self.leftmost.addTab(self.result_table_widget, "Simulation Result Table")
        return self.leftmost

    def left_element(self):
        self.left_specie_title = QLabel("Species Data Management Panel (units of time: month)")
        self.left_specie_title.setAlignment(Qt.AlignCenter)
        font = self.left_specie_title.font()
        font.setBold(True)
        self.left_specie_title.setFont(font)

        self.left_environment_title = QLabel("Environment Data Management Panel")
        self.left_environment_title.setAlignment(Qt.AlignCenter)
        font = self.left_environment_title.font()
        font.setBold(True)
        self.left_environment_title.setFont(font)

        self.extreme_title = QLabel("Extreme Environments")
        self.extreme_title.setAlignment(Qt.AlignCenter)
        font = self.extreme_title.font()
        font.setBold(True)
        self.extreme_title.setFont(font)

        self.operation_title = QLabel("Operation Panel")
        self.operation_title.setAlignment(Qt.AlignCenter)
        font = self.operation_title.font()
        font.setBold(True)
        self.operation_title.setFont(font)

        # self.features = ["name", "survival rate", "fecundity", "initial_population", "growth_rate", "carrying_capacity",
        #                  "natural_life_span", "move_speed_mean", "move_speed_std"]

        # specie data management
        self.species = QComboBox()
        self.species.addItem("target species")
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
        self.initial_population.setText("100")
        self.growth_rate = QLineEdit()
        self.growth_rate.setClearButtonEnabled(True)
        self.growth_rate.setText("0.1")
        self.natural_life_span = QLineEdit()
        self.natural_life_span.setClearButtonEnabled(True)
        self.natural_life_span.setText("10000")
        self.move_speed_mean = QLineEdit()
        self.move_speed_mean.setClearButtonEnabled(True)
        self.move_speed_mean.setText("2")
        self.move_speed_std = QLineEdit()
        self.move_speed_std.setClearButtonEnabled(True)
        self.move_speed_std.setText("1")
        self.marriage_age = QLineEdit()
        self.marriage_age.setClearButtonEnabled(True)
        self.marriage_age.setText("20")
        self.attack_ability = QLineEdit()
        self.attack_ability.setClearButtonEnabled(True)
        self.attack_ability.setText("0.1")
        self.escape_ability = QLineEdit()
        self.escape_ability.setClearButtonEnabled(True)
        self.escape_ability.setText("0.1")
        self.alive_ability_change_per_time = QLineEdit()
        self.alive_ability_change_per_time.setClearButtonEnabled(True)
        self.alive_ability_change_per_time.setText("0.1")
        self.fecundity_attenuation = QLineEdit()
        self.fecundity_attenuation.setClearButtonEnabled(True)
        self.fecundity_attenuation.setText("-0.000001")

        # specie operation
        self.species_submit_bt = QPushButton("Submit")
        self.species_clear_bt = QPushButton("Clear")
        self.species_delete_bt = QPushButton("Delete")
        self.species_delete_bt.setEnabled(False)
        self.species_random_bt = QPushButton("Random")
        self.species_random_seed = QLineEdit()
        self.species_random_seed.setClearButtonEnabled(True)
        self.species_random_seed.setText("0")

        # environment data management
        self.carrying_capacity = QLineEdit()
        self.carrying_capacity.setClearButtonEnabled(True)
        self.carrying_capacity.setText("10000")
        self.climate_type = QComboBox()
        self.climate_type.addItem("tropical rain forest climate")
        self.simulation_years = QLineEdit()
        self.simulation_years.setClearButtonEnabled(True)
        self.simulation_years.setText("100")

        # extreme environment test
        self.extreme_env_inf_ison = QCheckBox()
        self.extreme_env_inf_ison.setText("Extreme Environment")
        self.extreme_env_inf_ison.setChecked(False)
        self.extreme_env_inf_carrying_capacity = QCheckBox()
        self.extreme_env_inf_carrying_capacity.setText("Infinite Carrying Capacity")
        self.extreme_env_inf_carrying_capacity.setChecked(False)
        self.extreme_env_inf_carrying_capacity.setDisabled(True)

        self.simulate = QPushButton("Simulate")
        self.simulate.setEnabled(False)
        self.clear_table_bt = QPushButton("Clear Table")
        self.clear_table_bt.setEnabled(False)
        self.clear_plot_bt = QPushButton("Clear Plot")
        self.plot = QPushButton("Plot")
        self.export_table = QPushButton("Export Table")
        self.export_plot = QPushButton("Export Plot")

        self.slider_year = QSlider(Qt.Horizontal)
        self.slider_year.setEnabled(False)
        self.slider_left = QLabel("0")
        self.slider_right = QLabel("0")

        # landscape map
        self.mr_operation_layout = QHBoxLayout()

        self.mr_map_size = QLineEdit()
        self.mr_map_size.setClearButtonEnabled(True)
        self.mr_map_size.setText("10")

        self.mr_grid_widget = GridWidget(int(self.mr_map_size.text()))

        self.mr_inaccessible_number = QLineEdit()
        self.mr_inaccessible_number.setClearButtonEnabled(True)
        self.mr_inaccessible_number.setText("10")

        self.mr_generate_bt = QPushButton("Generate")
        self.mr_clear_bt = QPushButton("Clear")
        self.mr_random_bt = QPushButton("Random")

        # self.mr_button_layout = QHBoxLayout()
        self.mr_button_draw_1 = QPushButton("empty land")
        self.mr_button_draw_2 = QPushButton("inaccessible land")

    def left_panel(self):
        self.left_element()

        # specie data layout
        self.specie = QGridLayout()
        self.specie.addWidget(QLabel("species:"), 1, 0)
        self.specie.addWidget(self.species, 1, 1)
        self.specie.addWidget(QLabel("name:"), 1, 2)
        self.specie.addWidget(self.name, 1, 3)

        self.specie.addWidget(QLabel("survival rate:"), 2, 0)
        self.specie.addWidget(self.survival_rate, 2, 1)
        self.specie.addWidget(QLabel("fecundity:"), 2, 2)
        self.specie.addWidget(self.fecundity, 2, 3)

        self.specie.addWidget(QLabel("growth rate:"), 3, 0)
        self.specie.addWidget(self.growth_rate, 3, 1)
        self.specie.addWidget(QLabel("init population:"), 3, 2)
        self.specie.addWidget(self.initial_population, 3, 3)

        self.specie.addWidget(QLabel("maximum age:"), 4, 0)
        self.specie.addWidget(self.natural_life_span, 4, 1)
        self.specie.addWidget(QLabel("fecundity attenuation:"), 4, 2)
        self.specie.addWidget(self.fecundity_attenuation, 4, 3)

        self.specie.addWidget(QLabel("speed mean:"), 5, 0)
        self.specie.addWidget(self.move_speed_mean, 5, 1)
        self.specie.addWidget(QLabel("speed std:"), 5, 2)
        self.specie.addWidget(self.move_speed_std, 5, 3)

        self.specie.addWidget(QLabel("marriage age:"), 6, 0)
        self.specie.addWidget(self.marriage_age, 6, 1)
        self.specie.addWidget(QLabel("attack ability:"), 6, 2)
        self.specie.addWidget(self.attack_ability, 6, 3)

        self.specie.addWidget(QLabel("escape ability:"), 7, 0)
        self.specie.addWidget(self.escape_ability, 7, 1)
        self.specie.addWidget(QLabel("alive ability change rate:"), 7, 2)
        self.specie.addWidget(self.alive_ability_change_per_time, 7, 3)

        self.specie_operation = QHBoxLayout()
        self.specie_operation.addWidget(self.species_submit_bt)
        self.specie_operation.addWidget(self.species_clear_bt)
        self.specie_operation.addWidget(self.species_delete_bt)
        self.specie_operation.addWidget(self.species_random_bt)
        self.specie_operation.addWidget(QLabel("random seed:"))
        self.specie_operation.addWidget(self.species_random_seed)

        # environment layout
        self.env_data = QGridLayout()

        self.env_data.addWidget(QLabel("climate type:"), 0, 0)
        self.env_data.addWidget(self.climate_type, 0, 1)
        self.env_data.addWidget(QLabel("init carrying capacity:"), 0, 2)
        self.env_data.addWidget(self.carrying_capacity, 0, 3)

        self.env_data.addWidget(QLabel("simulation months:"), 1, 0)
        self.env_data.addWidget(self.simulation_years, 1, 1)

        # extreme environment test layout
        self.env_extreme = QGridLayout()
        self.env_extreme.addWidget(self.extreme_env_inf_ison, 0, 0)
        self.env_extreme.addWidget(self.extreme_env_inf_carrying_capacity, 0, 1)

        # self.env_operation = QHBoxLayout()
        # self.env_operation.addWidget(self.env_submit)
        # self.env_operation.addWidget(self.env_cancel)
        # self.env_operation.addWidget(self.env_op_random)
        # self.env_operation.addWidget(QLabel("random seed:"))
        # self.env_operation.addWidget(self.env_random_seed)

        # self.table = QTableWidget()
        # self.reset_table()

        self.export_table.setEnabled(False)
        self.export_plot.setEnabled(False)

        self.operation_panel = QGridLayout()
        self.operation_panel.addWidget(self.simulate, 1, 0)
        self.operation_panel.addWidget(self.plot, 1, 1)
        self.operation_panel.addWidget(self.clear_table_bt, 2, 0)
        self.operation_panel.addWidget(self.clear_plot_bt, 2, 1)
        self.operation_panel.addWidget(self.export_table, 3, 0)
        self.operation_panel.addWidget(self.export_plot, 3, 1)

        self.slider_panel = QHBoxLayout()
        # self.slider.setRange(0, 1000)
        self.slider_panel.addWidget(self.slider_left)
        self.slider_panel.addWidget(self.slider_year)
        self.slider_panel.addWidget(self.slider_right)

        self.left = QVBoxLayout()
        self.left.addWidget(self.left_specie_title)
        self.left.addLayout(self.specie)
        self.left.addWidget(self.left_environment_title)
        self.left.addLayout(self.env_data)
        # self.left.addLayout(self.env_operation)
        self.left.addLayout(self.specie_operation)
        self.left.addWidget(self.extreme_title)
        self.left.addLayout(self.env_extreme)
        self.left.addWidget(self.operation_title)
        self.left.addLayout(self.operation_panel)
        self.left.addLayout(self.slider_panel)
        # self.left.addWidget(self.left_specie_table_title)
        # self.left.addWidget(self.table)

        self.middle_right = QVBoxLayout()
        self.middle_right.addWidget(self.mr_grid_widget)

        self.middle_right_operation_layout1 = QHBoxLayout()
        self.middle_right_operation_layout1.addWidget(QLabel("map size:"))
        self.middle_right_operation_layout1.addWidget(self.mr_map_size)
        self.middle_right_operation_layout1.addWidget(QLabel("inaccessible number:"))
        self.middle_right_operation_layout1.addWidget(self.mr_inaccessible_number)
        self.middle_right_operation_layout1.addWidget(self.mr_generate_bt)
        self.middle_right_operation_layout1.addWidget(self.mr_clear_bt)
        self.middle_right_operation_layout1.addWidget(self.mr_random_bt)
        self.middle_right.addLayout(self.middle_right_operation_layout1)


        self.middle_right_button_layout = QHBoxLayout()
        self.middle_right_button_layout.addWidget(self.mr_button_draw_1)
        self.middle_right_button_layout.addWidget(self.mr_button_draw_2)
        self.middle_right.addLayout(self.middle_right_button_layout)

        self.middle_right_panel = QWidget()
        self.middle_right_panel.setLayout(self.middle_right)

        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left)
        self.left_panel = QTabWidget()
        self.left_panel.addTab(self.left_widget, "Species Data Management")
        self.left_panel.addTab(self.middle_right_panel, "Landscape Map")

        return self.left_panel

    def right_element(self):
        self.right_title = QLabel("Plotting Panel")
        self.right_title.setAlignment(Qt.AlignCenter)
        font = self.right_title.font()
        font.setBold(True)
        self.right_title.setFont(font)

        self.boxchart = QChartView()
        self.boxchart.setRenderHint(QPainter.Antialiasing)

        self.linechart = QChartView()
        self.linechart.setRenderHint(QPainter.Antialiasing)

        self.network = QChartView()
        self.network.setRenderHint(QPainter.Antialiasing)

    def right_panel(self):
        self.right_element()

        self.right_plot = QTabWidget()
        self.right_plot.addTab(self.boxchart, "Box Chart")
        self.right_plot.addTab(self.linechart, "Line Chart")

        self.right = QVBoxLayout()
        self.right.addWidget(self.right_title)
        self.right.addWidget(self.right_plot)

        return self.right



class GridWidget(QWidget):
    def __init__(self, num_grid):
        super().__init__()

        self.grid_size = num_grid  # 格子的大小
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # 格子的状态
        self.colors = [QColor(255, 255, 255), QColor(255, 0, 0), QColor(0, 255, 0)]  # 格子的颜色
        self.current_color = 0  # 当前选中的颜色

    def mousePressEvent(self, event):
        cell_size = min(self.width(), self.height()) / self.grid_size
        x = int(event.pos().x() / cell_size)
        y = int(event.pos().y() / cell_size)

        if x >= 0 and x < self.grid_size and y >= 0 and y < self.grid_size:
            self.grid[y][x] = self.current_color
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        cell_size = min(self.width(), self.height()) / self.grid_size

        # 绘制格子边框
        border_pen = QPen(Qt.black, 1)
        painter.setPen(border_pen)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                painter.drawRect(x * cell_size, y * cell_size, cell_size, cell_size)

        # 绘制格子颜色
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = self.colors[self.grid[y][x]]
                painter.fillRect(x * cell_size + 1, y * cell_size + 1, cell_size - 1, cell_size - 1, color)

    def clear(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.update()

    def draw_inaccessible(self, inaccessible_pos):
        self.grid[inaccessible_pos[0]][inaccessible_pos[1]] = 1
        self.update()
