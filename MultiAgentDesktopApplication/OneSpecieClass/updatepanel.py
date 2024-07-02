import random
import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel,
                               QComboBox, QSlider, QMessageBox, QMenu, QCheckBox,
                               QTabWidget, QFileDialog)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
import pandas as pd

class UpdatePanel:
    def __init__(self):
        # self.specie_table_rowname = ["species", "name", "survival rate", "fecundity",
        #                              "initial population", "growth rate",
        #                              "maximum age", "speed mean", "speed std", "marriage age",
        #                              "attack ability", "escape ability", "alive ability change rate",
        #                              "fecundity attenuation", "climate type", "carrying capacity",
        #                              "hunger increment",
        #                              "simulation step", "map"]
        self.specie_table_obj =[self.species, self.name, self.survival_rate,
                                    self.fecundity, self.initial_population,
                                    self.growth_rate, self.natural_life_span,
                                    self.move_speed_mean, self.move_speed_std,
                                    self.marriage_age, self.attack_ability,
                                    self.escape_ability, self.alive_ability_change_per_time,
                                    self.fecundity_attenuation, self.climate_type,
                                    self.carrying_capacity, self.carrying_cap_std,
                                    self.hunger_increment, self.age_increment,
                                    self.monogamous, self.is_cellular,
                                    self.cell_neighbors_occupy, self.simulation_years,
                                    self.mr_grid_widget]
        self.specie_table_rowname = list(map(lambda x: x.objectName(), self.specie_table_obj))

        self.specie_table_length = len(self.specie_table_rowname)
        self.inaccessible_list = []

    @Slot()
    def submit_species_func(self):
        self.species_table.insertColumn(self.species_items)
        for i in range(len(self.specie_table_obj)):
            widget_obj = self.specie_table_obj[i]
            if isinstance(widget_obj, QLineEdit):
                row_name = widget_obj.text()
            elif isinstance(widget_obj, QComboBox):
                row_name = widget_obj.currentText()
            elif isinstance(widget_obj, QCheckBox):
                row_name = str(widget_obj.isChecked())
            self.species_table.setItem(i, self.species_items, QTableWidgetItem(row_name))
        self.species_items += 1

        # self.species_table.setItem(0, self.species_items, QTableWidgetItem(self.species.currentText()))
        # self.species_table.setItem(1, self.species_items, QTableWidgetItem(self.name.text()))
        # self.species_table.setItem(2, self.species_items, QTableWidgetItem(self.survival_rate.text()))
        # self.species_table.setItem(3, self.species_items, QTableWidgetItem(self.fecundity.text()))
        # self.species_table.setItem(4, self.species_items, QTableWidgetItem(self.initial_population.text()))
        # self.species_table.setItem(5, self.species_items, QTableWidgetItem(self.growth_rate.text()))
        # self.species_table.setItem(6, self.species_items, QTableWidgetItem(self.natural_life_span.text()))
        # self.species_table.setItem(7, self.species_items, QTableWidgetItem(self.move_speed_mean.text()))
        # self.species_table.setItem(8, self.species_items, QTableWidgetItem(self.move_speed_std.text()))
        # self.species_table.setItem(9, self.species_items, QTableWidgetItem(self.marriage_age.text()))
        # self.species_table.setItem(10, self.species_items, QTableWidgetItem(self.attack_ability.text()))
        # self.species_table.setItem(11, self.species_items, QTableWidgetItem(self.escape_ability.text()))
        # self.species_table.setItem(12, self.species_items, QTableWidgetItem(self.alive_ability_change_per_time.text()))
        # self.species_table.setItem(13, self.species_items, QTableWidgetItem(self.fecundity_attenuation.text()))
        # self.species_table.setItem(14, self.species_items, QTableWidgetItem(self.climate_type.currentText()))
        # self.species_table.setItem(15, self.species_items, QTableWidgetItem(self.carrying_capacity.text()))
        # self.species_table.setItem(16, self.species_items, QTableWidgetItem(self.carrying_cap_std.text()))
        # self.species_table.setItem(17, self.species_items, QTableWidgetItem(self.hunger_increment.text()))
        # self.species_table.setItem(18, self.species_items, QTableWidgetItem(self.age_increment.text()))
        # self.species_table.setItem(19, self.species_items, QTableWidgetItem(str(self.monogamous.isChecked())))
        # self.species_table.setItem(19, self.species_items, QTableWidgetItem(str(self.is_cellular.isChecked())))
        # self.species_table.setItem(20, self.species_items, QTableWidgetItem(self.cell_neighbors_occupy.text()))
        # self.species_table.setItem(21, self.species_items, QTableWidgetItem(self.simulation_years.text()))
        # self.species_table.setItem(22, self.species_items, QTableWidgetItem(self.mr_grid_widget.get_map_name()))
        # self.species_items += 1

    def reset_result_table(self):
        self.result_table.setColumnCount(2)
        self.result_table.setRowCount(0)
        self.result_table.setHorizontalHeaderLabels(["target population", "timestep"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

    def reset_species_table(self):
        self.species_table.setRowCount(self.specie_table_length)
        self.species_table.setColumnCount(0)
        self.species_table.setVerticalHeaderLabels(self.specie_table_rowname)
        self.species_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.species_items = 0

    @Slot()
    def clear_table_func(self):
        self.reset_species_table()
        self.reset_result_table()

    @Slot()
    def clear_species_func(self):
        self.name.clear()
        self.survival_rate.clear()
        self.fecundity.clear()
        self.initial_population.clear()
        self.growth_rate.clear()
        self.carrying_capacity.clear()
        self.natural_life_span.clear()
        self.move_speed_mean.clear()
        self.move_speed_std.clear()
        self.marriage_age.clear()
        self.attack_ability.clear()
        self.escape_ability.clear()
        self.alive_ability_change_per_time.clear()
        self.fecundity_attenuation.clear()
        self.climate_type.setCurrentIndex(0)
        self.simulation_years.clear()
        self.hunger_increment.clear()
        self.age_increment.clear()
        self.cell_neighbors_occupy.clear()
        self.carrying_cap_std.clear()

    @Slot()
    def random_species_func(self):
        random.seed(1)
        self.survival_rate.setText(str(round(random.random(), 2)))
        self.fecundity.setText(str(round(random.random(), 2)))
        self.initial_population.setText(str(random.randint(1, 100)))
        self.growth_rate.setText(str(round(random.random(), 2)))
        self.carrying_capacity.setText(str(random.randint(1, 100)))
        self.natural_life_span.setText(str(random.randint(1, 100)))
        self.move_speed_mean.setText(str(round(random.random(), 2)))
        self.move_speed_std.setText(str(round(random.random(), 2)))
        self.marriage_age.setText(str(random.randint(1, 100)))
        self.attack_ability.setText(str(round(random.random(), 2)))
        self.escape_ability.setText(str(round(random.random(), 2)))
        self.alive_ability_change_per_time.setText(str(round(random.random(), 2)))
        self.fecundity_attenuation.setText(str(-round(random.random(), 2)))
        self.climate_type.setCurrentIndex(random.randint(0, 3))
        self.simulation_years.setText(str(random.randint(1, 100)))

    @Slot()
    def delete_species_func(self):
        self.species_table.removeColumn(self.species_table.currentColumn())
        column_count = self.species_table.columnCount()
        self.species_table.setColumnCount(column_count - 1)
        self.species_items -= 1

    @Slot()
    def generate_map_inaccessible(self):
        self.mr_grid_widget.clear()
        max_num = int(self.mr_map_size.text())
        self.mr_grid_widget.resize_map(max_num)
        inaccessible_num = int(self.mr_inaccessible_number.text())
        self.inaccessible_list = []

        for _ in range(inaccessible_num):
            inaccessible_pos = [random.randint(0, max_num - 1), random.randint(0, max_num - 1)]
            if inaccessible_pos not in self.inaccessible_list:
                self.mr_grid_widget.draw_inaccessible(inaccessible_pos)
                self.inaccessible_list.append(inaccessible_pos)

    @Slot()
    def clear_map(self):
        self.mr_map_size.clear()
        self.mr_inaccessible_number.clear()
        self.mr_grid_widget.clear()

    @Slot()
    def read_map(self):
        self.mr_grid_widget.read_map()

    @Slot()
    def random_map_parameter(self):
        map_size = random.randint(1, 10)
        self.mr_map_size.setText(str(map_size))
        self.mr_inaccessible_number.setText(str(random.randint(1, map_size)))

    @Slot()
    def confirm_map(self):
        if self.mr_button_box.isChecked():
            self.mr_map_size.setEnabled(False)
            self.mr_inaccessible_number.setEnabled(False)
            self.mr_generate_bt.setEnabled(False)
            self.mr_clear_bt.setEnabled(False)
            self.mr_random_bt.setEnabled(False)
            self.mr_button_draw_1.setEnabled(False)
            self.mr_button_draw_2.setEnabled(False)
        else:
            self.mr_map_size.setEnabled(True)
            self.mr_inaccessible_number.setEnabled(True)
            self.mr_generate_bt.setEnabled(True)
            self.mr_clear_bt.setEnabled(True)
            self.mr_random_bt.setEnabled(True)
            self.mr_button_draw_1.setEnabled(True)
            self.mr_button_draw_2.setEnabled(True)

    @Slot()
    def clear_plot(self):
        while self.right_plot.count() > 0:
            self.right_plot.removeTab(0)


    @Slot()
    def export_table_func(self):

        species_data = []
        for i in range(self.species_table.columnCount()):
            species_data.append([self.species_table.item(j, i).text() for j in range(self.species_table.rowCount())])
        species_df = pd.DataFrame(species_data, columns=self.specie_table_rowname)

        file_path, _ = QFileDialog.getSaveFileName(
            self,  # parent widget
            "Save Species Table CSV",  # 对话框标题
            "",  # 默认目录，空字符串表示使用上次的目录或默认目录
            "CSV Files (*.csv);;All Files (*)"  # 文件类型过滤器
        )

        # 检查用户是否选择了文件路径
        if file_path:
            # 如果用户没有指定 .csv 扩展名，添加它
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            # 保存 DataFrame 到选择的文件路径
            species_df.to_csv(file_path, index=False)
            print(f"Result saved to {file_path}")
        else:
            print("Save operation cancelled")

        # -------------------------

        result_data = []
        for i in range(self.result_table.rowCount()):
            result_data.append([self.result_table.item(i, 0).text(), self.result_table.item(i, 1).text()])
        result_df = pd.DataFrame(result_data, columns=["target population", "timestep"])

        file_path, _ = QFileDialog.getSaveFileName(
            self,  # parent widget
            "Save Result Table CSV",  # 对话框标题
            "",  # 默认目录，空字符串表示使用上次的目录或默认目录
            "CSV Files (*.csv);;All Files (*)"  # 文件类型过滤器
        )

        # 检查用户是否选择了文件路径
        if file_path:
            # 如果用户没有指定 .csv 扩展名，添加它
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            # 保存 DataFrame 到选择的文件路径
            result_df.to_csv(file_path, index=False)
            print(f"Result saved to {file_path}")
        else:
            print("Save operation cancelled")

        #
        #
        # save_dir = self.save_dir.text()
        # if save_dir:
        #     species_data = []
        #     for i in range(self.species_table.columnCount()):
        #         species_data.append([self.species_table.item(j, i).text() for j in range(self.species_table.rowCount())])
        #     species_df = pd.DataFrame(species_data, columns=self.specie_table_rowname)
        #     species_df.to_csv(save_dir + "/species.csv", index=False)
        #
        #     result_data = []
        #     for i in range(self.result_table.rowCount()):
        #         result_data.append([self.result_table.item(i, 0).text(), self.result_table.item(i, 1).text()])
        #     result_df = pd.DataFrame(result_data, columns=["target population", "timestep"])
        #     result_df.to_csv(save_dir + "/result.csv", index=False)
        #
        # else:
        #     QMessageBox.critical(self, "Error", "Please input the save directory.")

    def save_plotting(self, plot_name, file_path, file_caption):
        size = plot_name.size()
        pixmap = QPixmap(size)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        self.piechart_gender.render(painter)
        painter.end()

        file_path, _ = QFileDialog.getSaveFileName(self, file_caption, file_path, "PNG Files (*.png);;All Files (*)")

        if file_path:
            pixmap.save(file_path, "PNG")
            print(f"Chart saved to {file_path}")

    @Slot()
    def export_plot_func(self):
        for i in range(self.right_plot.count()):
            plot_name = self.right_plot.widget(i)
            if isinstance(plot_name, QChartView):
                self.save_plotting(plot_name, "", "Save Plot No.%s" % str(i))
        # else:
        #     QMessageBox.critical(self, "Error", "Please input the save directory.")

