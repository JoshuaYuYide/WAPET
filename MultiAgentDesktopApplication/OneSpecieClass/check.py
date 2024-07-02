from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries

class Check:
    def __init__(self):
        pass

    @Slot()
    def check_disable_specie_data(self):
        enabled = bool(
            self.name.text() and self.survival_rate.text() and self.fecundity.text() and self.initial_population.text()
            and self.growth_rate.text() and self.carrying_capacity.text() and self.natural_life_span.text() and
            self.move_speed_mean.text() and self.move_speed_std.text() and self.marriage_age.text() and
            self.attack_ability.text() and self.escape_ability.text() and self.alive_ability_change_per_time.text() and
            self.fecundity_attenuation.text() and self.mr_button_box.isChecked() and self.age_increment.text())
        if enabled:
            self.species_submit_bt.setEnabled(True)
        else:
            self.species_submit_bt.setEnabled(False)

    @Slot()
    def check_disable_env_data(self):
        enabled = bool(
        )

    @Slot()
    def check_table(self):
        if self.species_table.columnCount() > 0:
            # self.species_delete_bt.setEnabled(True)
            self.clear_table_bt.setEnabled(True)
            self.clear_table_bt.setEnabled(True)
            if self.result_table.rowCount() == 0:
                self.simulate_bt.setEnabled(True)
            else:
                self.simulate_bt.setEnabled(False)
        else:
            # self.species_delete_bt.setEnabled(False)
            self.clear_table_bt.setEnabled(False)
            self.simulate_bt.setEnabled(False)
            self.clear_table_bt.setEnabled(False)

        if self.species_table.columnCount() == 1:
            self.species_submit_bt.setEnabled(False)
        if self.species_table.columnCount() == 0:
            self.species_submit_bt.setEnabled(True)

        if self.result_table.rowCount() > 0:
            self.plot_bt.setEnabled(True)
            self.export_table.setEnabled(True)
        else:
            self.plot_bt.setEnabled(False)
            self.export_table.setEnabled(False)

    @Slot()
    def check_plot(self):
        if self.right_plot.count() > 0:
            self.clear_plot_bt.setEnabled(True)
            self.export_plot.setEnabled(True)
        else:
            self.clear_plot_bt.setEnabled(False)
            self.export_plot.setEnabled(False)

    @Slot()
    def check_cell_neighbor(self):
        if self.is_cellular.isChecked():
            self.cell_neighbors_occupy.setEnabled(True)
        else:
            self.cell_neighbors_occupy.setEnabled(False)



    @Slot()
    def check_random_seed_func(self):
        if self.species_random_seed_check.isChecked():
            self.species_random_seed.setEnabled(True)
        else:
            self.species_random_seed.setEnabled(False)

    # @Slot()
    # def check_save_dir(self):
    #     if self.save_dir.text():
    #         self.export_table.setEnabled(True)
    #         self.export_plot.setEnabled(True)
    #     else:
    #         self.export_table.setEnabled(False)
    #         self.export_plot.setEnabled(False)
