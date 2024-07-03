import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen, QColor, QPixmap
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu,
                               QCheckBox, QTabWidget, QGroupBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class PanelInit:
    def __init__(self):
        # self.leftmost_element()
        self.left_element()
        # self.right_element()

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

        self.leftmost.setFixedWidth(300)
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

        # self.extreme_title = QLabel("Extreme Environments")
        # self.extreme_title.setAlignment(Qt.AlignCenter)
        # font = self.extreme_title.font()
        # font.setBold(True)
        # self.extreme_title.setFont(font)

        self.operation_title = QLabel("Operation Panel")
        self.operation_title.setAlignment(Qt.AlignCenter)
        font = self.operation_title.font()
        font.setBold(True)
        self.operation_title.setFont(font)

        # self.features = ["name", "survival rate", "fecundity", "initial_population", "growth_rate", "carrying_capacity",
        #                  "natural_life_span", "move_speed_mean", "move_speed_std"]

        # specie data management
        self.species = QComboBox()
        self.species.addItem("target_specie")
        self.species.setObjectName("species")
        self.name = QLineEdit()
        self.name.setObjectName("name")
        self.name.setClearButtonEnabled(True)
        self.name.setText('fish')
        self.survival_rate = QLineEdit()
        self.survival_rate.setObjectName("survival rate")
        self.survival_rate.setClearButtonEnabled(True)
        self.survival_rate.setText("10000")
        self.fecundity = QLineEdit()
        self.fecundity.setObjectName("fecundity")
        self.fecundity.setClearButtonEnabled(True)
        self.fecundity.setText("10000")
        self.initial_population = QLineEdit()
        self.initial_population.setObjectName("initial population")
        self.initial_population.setClearButtonEnabled(True)
        self.initial_population.setText("100")
        self.growth_rate = QLineEdit()
        self.growth_rate.setObjectName("growth rate")
        self.growth_rate.setClearButtonEnabled(True)
        self.growth_rate.setText("0.1")
        self.natural_life_span = QLineEdit()
        self.natural_life_span.setObjectName("maximum age")
        self.natural_life_span.setClearButtonEnabled(True)
        self.natural_life_span.setText("100")
        self.move_speed_mean = QLineEdit()
        self.move_speed_mean.setObjectName("speed mean")
        self.move_speed_mean.setClearButtonEnabled(True)
        self.move_speed_mean.setText("2")
        self.move_speed_std = QLineEdit()
        self.move_speed_std.setObjectName("speed std")
        self.move_speed_std.setClearButtonEnabled(True)
        self.move_speed_std.setText("1")
        self.marriage_age = QLineEdit()
        self.marriage_age.setObjectName("marriage age")
        self.marriage_age.setClearButtonEnabled(True)
        self.marriage_age.setText("20")
        self.attack_ability = QLineEdit()
        self.attack_ability.setObjectName("attack ability")
        self.attack_ability.setClearButtonEnabled(True)
        self.attack_ability.setText("0.1")
        self.escape_ability = QLineEdit()
        self.escape_ability.setObjectName("escape ability")
        self.escape_ability.setClearButtonEnabled(True)
        self.escape_ability.setText("0.1")
        self.alive_ability_change_per_time = QLineEdit()
        self.alive_ability_change_per_time.setObjectName("alive ability change rate")
        self.alive_ability_change_per_time.setClearButtonEnabled(True)
        self.alive_ability_change_per_time.setText("0.1")
        self.fecundity_attenuation = QLineEdit()
        self.fecundity_attenuation.setObjectName("fecundity attenuation")
        self.fecundity_attenuation.setClearButtonEnabled(True)
        self.fecundity_attenuation.setText("-0.000001")
        self.hunger_increment = QLineEdit()
        self.hunger_increment.setObjectName("hunger increment")
        self.hunger_increment.setClearButtonEnabled(True)
        self.hunger_increment.setText("10")
        self.monogamous = QCheckBox()
        self.monogamous.setText("Monogamous")
        self.monogamous.setChecked(True)
        self.monogamous.setObjectName("monogamous")
        self.age_increment = QLineEdit()
        self.age_increment.setObjectName("age increment")
        self.age_increment.setClearButtonEnabled(True)
        self.age_increment.setText("1")
        self.cell_neighbors_occupy = QLineEdit()
        self.cell_neighbors_occupy.setObjectName("cell neighbors occupy")
        self.cell_neighbors_occupy.setClearButtonEnabled(True)
        self.cell_neighbors_occupy.setText("1")
        self.is_cellular = QCheckBox()
        self.is_cellular.setText("Cellular Automata")
        self.is_cellular.setChecked(True)
        self.is_cellular.setObjectName("is cellular")
        self.init_min_age = QLineEdit()
        self.init_min_age.setObjectName("init min age")
        self.init_min_age.setText("0")
        self.init_max_age = QLineEdit()
        self.init_max_age.setObjectName("init min age")
        self.init_max_age.setText("10")

        # specie operation
        self.species_submit_bt = QPushButton("Submit")
        self.species_submit_bt.setEnabled(False)
        self.species_clear_bt = QPushButton("Clear")
        self.species_random_bt = QPushButton("Random")
        self.species_random_seed = QLineEdit()
        self.species_random_seed.setEnabled(False)
        self.species_random_seed.setText("0")
        self.species_random_seed_check = QCheckBox()
        self.species_random_seed_check.setText("Random Seed")
        self.species_random_seed_check.setChecked(False)

        # environment data management
        self.carrying_capacity = QLineEdit()
        self.carrying_capacity.setObjectName("carrying capacity")
        self.carrying_capacity.setClearButtonEnabled(True)
        self.carrying_capacity.setText("10")
        self.carrying_cap_std = QLineEdit()
        self.carrying_cap_std.setObjectName("carrying capacity std")
        self.carrying_cap_std.setClearButtonEnabled(True)
        self.carrying_cap_std.setText("1")
        self.climate_type = QComboBox()
        self.climate_type.addItem("tropical rain forest climate")
        self.climate_type.setObjectName("climate type")
        self.simulation_years = QLineEdit()
        self.simulation_years.setObjectName("simulation step")
        self.simulation_years.setClearButtonEnabled(True)
        self.simulation_years.setText("100")
        self.extreme_climate_threshold = QLineEdit()
        self.extreme_climate_threshold.setObjectName("extreme climate threshold")
        self.extreme_climate_threshold.setText("10")

        self.simulate_bt = QPushButton("Simulate")
        self.simulate_bt.setEnabled(False)
        self.clear_table_bt = QPushButton("Clear Table")
        self.clear_table_bt.setEnabled(False)
        self.clear_plot_bt = QPushButton("Clear Plot")
        self.clear_plot_bt.setEnabled(False)
        self.plot_bt = QPushButton("Plot")
        self.plot_bt.setEnabled(False)
        self.export_table = QPushButton("Export Table")
        self.export_plot = QPushButton("Export Plot")
        # self.save_dir = QLineEdit()
        # self.save_dir.setFixedWidth(350)


        # landscape map
        self.mr_operation_layout = QHBoxLayout()

        self.mr_map_size = QLineEdit()
        self.mr_map_size.setClearButtonEnabled(True)
        self.mr_map_size.setText("10")
        self.mr_map_size.setFixedWidth(60)

        self.mr_grid_widget = GridWidget(int(self.mr_map_size.text()))

        self.mr_inaccessible_number = QLineEdit()
        self.mr_inaccessible_number.setClearButtonEnabled(True)
        self.mr_inaccessible_number.setText("10")
        self.mr_inaccessible_number.setFixedWidth(60)

        self.mr_generate_bt = QPushButton("Generate")
        self.mr_clear_bt = QPushButton("Clear")
        self.mr_random_bt = QPushButton("Random")
        self.mr_button_draw_1 = QPushButton("Add Empty Land")
        self.mr_button_draw_2 = QPushButton("Add Inaccessible Land")
        self.mr_button_box = QCheckBox()
        self.mr_button_box.setText("Lock")
        self.mr_button_box.setChecked(False)


        self.plot_map_target_specie = QPushButton("Plot Target Specie Distribution")
        self.plot_map_carry_ability = QPushButton("Plot Carry Ability Distribution")

        self.middle_right_plot_layout = QGridLayout()
        self.middle_right_plot_layout.addWidget(QLabel("Plot on Map:"), 0, 0)
        self.middle_right_plot_layout.addWidget(self.plot_map_target_specie, 0, 1)
        self.middle_right_plot_layout.addWidget(self.plot_map_carry_ability, 0, 2)



        # self.plot_map_thresholds = QLineEdit()
        # self.plot_map_thresholds.setClearButtonEnabled(True)
        # self.plot_map_thresholds.setText("10")

    def left_panel(self):
        # self.left_element()

        # specie data layout
        self.specie = QVBoxLayout()

        self.specie_basic_info_group = QGroupBox("User Information")
        self.specie.addWidget(self.specie_basic_info_group)
        self.specie_basic_info_layout = QGridLayout()
        self.specie_basic_info_group.setLayout(self.specie_basic_info_layout)
        self.specie_basic_info_layout.addWidget(QLabel("species:"), 0, 0)
        self.specie_basic_info_layout.addWidget(self.species, 0, 1)
        self.specie_basic_info_layout.addWidget(QLabel("name:"), 0, 2)
        self.specie_basic_info_layout.addWidget(self.name, 0, 3)
        self.specie_basic_info_layout.addWidget(QLabel("maximum age:"), 1, 0)
        self.specie_basic_info_layout.addWidget(self.natural_life_span, 1, 1)
        self.specie_basic_info_layout.addWidget(QLabel("marriage age:"), 1, 2)
        self.specie_basic_info_layout.addWidget(self.marriage_age, 1, 3)
        self.specie_basic_info_layout.addWidget(QLabel("speed mean:"), 2, 0)
        self.specie_basic_info_layout.addWidget(self.move_speed_mean, 2, 1)
        self.specie_basic_info_layout.addWidget(QLabel("speed std:"), 2, 2)
        self.specie_basic_info_layout.addWidget(self.move_speed_std, 2, 3)

        self.specie_survive_group = QGroupBox("Survivability")
        self.specie.addWidget(self.specie_survive_group)
        self.specie_survive_layout = QGridLayout()
        self.specie_survive_group.setLayout(self.specie_survive_layout)
        self.specie_survive_layout.addWidget(QLabel("survival rate:"), 0, 0)
        self.specie_survive_layout.addWidget(self.survival_rate, 0, 1)
        self.specie_survive_layout.addWidget(QLabel("alive ability change rate:"), 0, 2)
        self.specie_survive_layout.addWidget(self.alive_ability_change_per_time, 0, 3)
        self.specie_survive_layout.addWidget(QLabel("fecundity:"), 1, 0)
        self.specie_survive_layout.addWidget(self.fecundity, 1, 1)
        self.specie_survive_layout.addWidget(QLabel("fecundity attenuation:"), 1, 2)
        self.specie_survive_layout.addWidget(self.fecundity_attenuation, 1, 3)
        self.specie_survive_layout.addWidget(QLabel("attack ability:"), 2, 0)
        self.specie_survive_layout.addWidget(self.attack_ability, 2, 1)
        self.specie_survive_layout.addWidget(QLabel("escape ability:"), 2, 2)
        self.specie_survive_layout.addWidget(self.escape_ability, 2, 3)
        self.specie_survive_layout.addWidget(QLabel("hunger increment:"), 3, 0)
        self.specie_survive_layout.addWidget(self.hunger_increment, 3, 1)

        self.specie_population_setting_group = QGroupBox("Population Settings")
        self.specie.addWidget(self.specie_population_setting_group)
        self.specie_population_setting_layout = QGridLayout()
        self.specie_population_setting_group.setLayout(self.specie_population_setting_layout)
        self.specie_population_setting_layout.addWidget(QLabel("growth rate:"), 0, 0)
        self.specie_population_setting_layout.addWidget(self.growth_rate, 0, 1)
        self.specie_population_setting_layout.addWidget(QLabel("extreme climate threshold:"), 0, 2)
        self.specie_population_setting_layout.addWidget(self.extreme_climate_threshold, 0, 3)
        self.specie_population_setting_layout.addWidget(QLabel("age increment:"), 1, 0)
        self.specie_population_setting_layout.addWidget(self.age_increment, 1, 1)
        self.specie_population_setting_layout.addWidget(QLabel("cell neighbors occupy:"), 1, 2)
        self.specie_population_setting_layout.addWidget(self.cell_neighbors_occupy, 1, 3)
        self.specie_population_setting_layout.addWidget(QLabel("init population:"), 2, 0)
        self.specie_population_setting_layout.addWidget(self.initial_population, 2, 1)
        self.specie_population_setting_layout.addWidget(QLabel("init min age:"), 2, 2)
        self.specie_population_setting_layout.addWidget(self.init_min_age, 2, 3)
        self.specie_population_setting_layout.addWidget(QLabel("init max age:"), 3, 0)
        self.specie_population_setting_layout.addWidget(self.init_max_age, 3, 1)
        self.specie_population_setting_layout.addWidget(self.monogamous, 4, 0)
        self.specie_population_setting_layout.addWidget(self.is_cellular, 4, 1)

        self.specie_operation = QHBoxLayout()
        self.specie_operation.addWidget(self.species_submit_bt)
        self.specie_operation.addWidget(self.species_clear_bt)
        self.specie_operation.addWidget(self.species_random_bt)
        self.specie_operation.addWidget(QLabel("random seed:"))
        self.specie_operation.addWidget(self.species_random_seed)
        self.specie_operation.addWidget(self.species_random_seed_check)


        # environment layout
        self.env_data = QGridLayout()
        self.env_data.addWidget(QLabel("climate type:"), 0, 0)
        self.env_data.addWidget(self.climate_type, 0, 1)
        self.env_data.addWidget(QLabel("simulation steps:"), 0, 2)
        self.env_data.addWidget(self.simulation_years, 0, 3)
        self.env_data.addWidget(QLabel("carrying capacity mean:"), 1, 0)
        self.env_data.addWidget(self.carrying_capacity, 1, 1)
        self.env_data.addWidget(QLabel("carrying capacity std:"), 1, 2)
        self.env_data.addWidget(self.carrying_cap_std, 1, 3)

        # extreme environment test layout
        # self.env_extreme = QGridLayout()
        # self.env_extreme.addWidget(self.extreme_env_inf_ison, 0, 0)
        # self.env_extreme.addWidget(self.extreme_env_inf_carrying_capacity, 0, 1)

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
        self.operation_panel.addWidget(self.simulate_bt, 1, 0)
        self.operation_panel.addWidget(self.plot_bt, 1, 1)
        self.operation_panel.addWidget(self.clear_table_bt, 2, 0)
        self.operation_panel.addWidget(self.clear_plot_bt, 2, 1)
        self.operation_panel.addWidget(self.export_table, 3, 0)
        self.operation_panel.addWidget(self.export_plot, 3, 1)
        # self.operation_panel.addWidget(QLabel("save dir:"), 4, 0)
        # self.operation_panel.addWidget(self.save_dir, 4, 1)

        self.left = QVBoxLayout()
        self.left.addWidget(self.left_specie_title)
        self.left.addLayout(self.specie)
        self.left.addWidget(self.left_environment_title)
        self.left.addLayout(self.env_data)
        self.left.addLayout(self.specie_operation)
        self.left.addWidget(self.operation_title)
        self.left.addLayout(self.operation_panel)

        self.middle_right = QVBoxLayout()
        self.middle_right.addWidget(self.mr_grid_widget)

        self.middle_right_operation_layout1 = QHBoxLayout()
        self.middle_right_operation_layout1.addWidget(QLabel("Map Setting:"))
        self.middle_right_operation_layout1.addWidget(QLabel("map size:"))
        self.middle_right_operation_layout1.addWidget(self.mr_map_size)
        self.middle_right_operation_layout1.addWidget(QLabel("inaccessible number:"))
        self.middle_right_operation_layout1.addWidget(self.mr_inaccessible_number)
        self.middle_right_operation_layout1.addWidget(self.mr_generate_bt)
        self.middle_right_operation_layout1.addWidget(self.mr_clear_bt)
        self.middle_right_operation_layout1.addWidget(self.mr_random_bt)
        self.middle_right.addLayout(self.middle_right_operation_layout1)

        self.middle_right_button_layout = QHBoxLayout()
        self.middle_right_button_layout.addWidget(QLabel("Edit Map:"))
        self.middle_right_button_layout.addWidget(self.mr_button_draw_1)
        self.middle_right_button_layout.addWidget(self.mr_button_draw_2)
        self.middle_right_button_layout.addWidget(self.mr_button_box)
        self.middle_right.addLayout(self.middle_right_button_layout)


        self.middle_right.addLayout(self.middle_right_plot_layout)


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

        self.piechart_gender = QChartView()
        self.piechart_gender.setRenderHint(QPainter.Antialiasing)

        self.histchart_age = QChartView()
        self.histchart_age.setRenderHint(QPainter.Antialiasing)

        self.piechart_life_status = QChartView()
        self.piechart_life_status.setRenderHint(QPainter.Antialiasing)

        self.linechart = QChartView()
        self.linechart.setRenderHint(QPainter.Antialiasing)

        # self.network = QChartView()
        # self.network.setRenderHint(QPainter.Antialiasing)

    def right_panel(self):
        self.right_element()

        self.right_plot = QTabWidget()

        # self.right_plot.addTab(self.network, "Network")

        self.right = QVBoxLayout()
        self.right.addWidget(self.right_title)
        self.right.addWidget(self.right_plot)

        return self.right



class GridWidget(QWidget):
    def __init__(self, num_grid):
        super().__init__()

        self.grid_size = num_grid  # 格子的大小
        self.grid = [['empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # 格子的状态
        self.reset_color()
        self.current_color = 'empty'  # 当前选中的颜色

    def mousePressEvent(self, event):
        cell_size = min(self.width(), self.height()) / self.grid_size
        x = int(event.pos().x() / cell_size)
        y = int(event.pos().y() / cell_size)

        if x >= 0 and x < self.grid_size and y >= 0 and y < self.grid_size:
            self.grid[y][x] = self.current_color
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.cell_size = min(self.width(), self.height()) / self.grid_size

        # 绘制格子边框
        border_pen = QPen(Qt.black, 1)
        painter.setPen(border_pen)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

        # 绘制格子颜色
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = self.colors[self.grid[y][x]]
                painter.fillRect(x * self.cell_size + 1, y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1, color)

    def clear(self):
        self.grid = [['empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.update()

    def draw_inaccessible(self, inaccessible_pos):
        self.grid[inaccessible_pos[1]][inaccessible_pos[0]] = 'inaccessible'
        self.update()

    def resize_map(self, num_grid):
        self.grid_size = num_grid
        self.grid = [['empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.update()

    def read_map(self):
        result = {"inaccessible": [], "empty": [], "target specie": [], "predator": [], "prey": []}
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                result[self.grid[i][j]].append((i, j))
        return result

    def get_map_name(self):
        return str(self.grid_size)

    def calculate_color(self, origin_color, alpha):
        # 白色和深绿色的 RGB 值
        white = (255, 255, 255)  # 白色
        # 计算当前颜色分量，确保 alpha 的范围在 0 到 1 之间
        alpha = max(0, min(1, alpha))
        green_r = int(white[0] + (origin_color.red() - white[0]) * alpha)
        green_g = int(white[1] + (origin_color.green() - white[1]) * alpha)
        green_b = int(white[2] + (origin_color.blue() - white[2]) * alpha)

        # 创建新的颜色
        new_color = QColor(green_r, green_g, green_b)

        return new_color

    def update_alpha(self, specie_name, alpha, position):
        x = position[0]
        y = position[1]

        new_color = self.calculate_color(self.colors[specie_name], alpha)
        self.colors[f'{specie_name}_{x}_{y}'] = new_color

    def reset_color(self):
        '''
        inaccessable: red
        target specie: green
        predator: blue
        prey: yellow
        empty: white
        carry_ability: cyan
        '''
        self.colors = {'empty': QColor(255, 255, 255), 'inaccessible':QColor(255, 0, 0), 'target_specie': QColor(0, 255, 0), 'predator': QColor(0, 0, 255),
                       'prey': QColor(255, 255, 0), 'carry_ability': QColor(0, 255, 255)}  # grid colors

    def draw_species(self, specie_name):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                new_key = f'{specie_name}_{x}_{y}'
                if new_key in list(self.colors.keys()):
                    self.grid[y][x] = f'{specie_name}_{x}_{y}'
                    self.update()

    def objectName(self):
        return 'map'

    def render_to_pixmap(self):
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.white)  # 填充白色背景
        self.render(pixmap)
        return pixmap

        # painter = QPainter(self)
        # color = self.colors[specie_type]
        # color.setAlpha(alpha)
        # x = specie_pos[0]
        # y = specie_pos[1]
        # painter.fillRect(x * self.cell_size + 1, y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1, color)
        # self.update_alpha(specie_type, alpha)
        # self.grid[specie_pos[0]][specie_pos[1]] = specie_type
        # self.update()
        # self.reset_color()