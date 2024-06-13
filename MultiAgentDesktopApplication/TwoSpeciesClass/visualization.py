from OneSpecieClass.visualization import (Visulization, TreeNode, TreeGraphicsView)
import sys
from PySide6.QtCore import Qt, Slot, QPointF, QModelIndex
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu,
                               QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem, QGraphicsObject,
                               QStyleOptionGraphicsItem, QGraphicsView)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries, QBarSeries, QBarSet
import random
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import (QEasingCurve, QLineF,
                            QParallelAnimationGroup, QPointF,
                            QPropertyAnimation, QRectF, Qt)
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
import matplotlib.pyplot as plt
import math
import numpy as np

class VisulizationTwo(Visulization):

    def plot_agent_based_logistic_individual(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Logistic Growth Individual Agent-based Line Chart")

        colors_palette = [Qt.red, Qt.green, Qt.blue]
        for i in range(3):
            # 获取第一列数据
            target_population_data = []
            for row in range(self.result_table.model().rowCount()):
                index = self.result_table.model().index(row, i)  # 第一列的标签为 0 列的标签
                value = self.result_table.model().data(index)
                target_population_data.append(value)

            # 获取第二列数据
            timestep_data = []
            for row in range(self.result_table.model().rowCount()):
                index = self.result_table.model().index(row, 3)  # 第二列的标签为 1 列的标签
                value = self.result_table.model().data(index)
                timestep_data.append(value)

            data = list(map(lambda x, y: (float(x), float(y)), timestep_data, target_population_data))

            # 创建新的QLineSeries
            series = QLineSeries()
            series.setName(self.result_table.horizontalHeaderItem(i).text())

            for x, y in data:
                series.append(x, y)

            # 设置线条样式
            pen = QPen(colors_palette[i])
            pen.setWidth(2)
            series.setPen(pen)

            # 将线系列添加到QChart中
            chart.addSeries(series)

        chart.createDefaultAxes()
        self.linechart.setChart(chart)

    @Slot()
    def plot_predator_on_map(self):
        self.mr_grid_widget.reset_color()
        specie_name = 'predator'
        total_amount = self.model.soil_agent.specie_amount[specie_name]
        if total_amount != 0:
            for y in range(int(self.mr_map_size.text())):
                for x in range(int(self.mr_map_size.text())):
                    if not self.model.soil_agent.map[x][y]['is_inaccessible']:
                        # alpha = (len(self.model.soil_agent.map[x][y]['target_specie']) / total_amount) * 255
                        alpha = (len(self.model.soil_agent.map[x][y][specie_name]) / total_amount)
                        self.mr_grid_widget.update_alpha(specie_name, alpha, [x,y])

            self.mr_grid_widget.draw_species(specie_name)

    @Slot()
    def plot_prey_on_map(self):
        self.mr_grid_widget.reset_color()
        specie_name = 'prey'
        total_amount = self.model.soil_agent.specie_amount[specie_name]
        if total_amount != 0:
            for y in range(int(self.mr_map_size.text())):
                for x in range(int(self.mr_map_size.text())):
                    if not self.model.soil_agent.map[x][y]['is_inaccessible']:
                        # alpha = (len(self.model.soil_agent.map[x][y]['target_specie']) / total_amount) * 255
                        alpha = (len(self.model.soil_agent.map[x][y][specie_name]) / total_amount)
                        self.mr_grid_widget.update_alpha(specie_name, alpha, [x,y])

            self.mr_grid_widget.draw_species(specie_name)

    def plot_predator_age_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'predator'
        age = {}
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]) and agent.is_alive:
                if agent.age not in list(age.keys()):
                    age[str(float(agent.age))] = 1
                else:
                    age[str(float(agent.age))] += 1

        if len(age.keys()) == 0:
            return

        age_unique = list(age.keys())
        age_unique = list(map(lambda x: float(x), age_unique))
        age_unique.sort()
        Q1 = np.percentile(age_unique, 25)
        Q2 = np.percentile(age_unique, 50)
        Q3 = np.percentile(age_unique, 75)

        age_percentile = {}
        age_percentile['%s>' % str(Q1)] = 0
        age_percentile['%s-%s' % (str(Q1), str(Q2))] = 0
        age_percentile['%s-%s' % (str(Q2), str(Q3))] = 0
        age_percentile['>%s' % str(Q3)] = 0
        for sub_age in age_unique:
            if sub_age < Q1:
                age_percentile['%s>' % str(Q1)] += age[str(sub_age)]
            elif sub_age < Q2 and sub_age >= Q1:
                age_percentile['%s-%s' % (str(Q1), str(Q2))] += age[str(sub_age)]
            elif sub_age < Q3 and sub_age >= Q2:
                age_percentile['%s-%s' % (str(Q2), str(Q3))] += age[str(sub_age)]
            else:
                age_percentile['>%s' % str(Q3)] += age[str(sub_age)]


        for name in list(age_percentile.keys()):
            series.append(name, age_percentile[name])

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置图例的位置
        chart.legend().setAlignment(Qt.AlignLeft)
        self.histchart_age_predator.setChart(chart)

    def plot_prey_age_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'prey'
        age = {}
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]) and agent.is_alive:
                if agent.age not in list(age.keys()):
                    age[str(float(agent.age))] = 1
                else:
                    age[str(float(agent.age))] += 1

        if len(age.keys()) == 0:
            return

        age_unique = list(age.keys())
        age_unique = list(map(lambda x: float(x), age_unique))
        age_unique.sort()
        Q1 = np.percentile(age_unique, 25)
        Q2 = np.percentile(age_unique, 50)
        Q3 = np.percentile(age_unique, 75)

        age_percentile = {}
        age_percentile['%s>' % str(Q1)] = 0
        age_percentile['%s-%s' % (str(Q1), str(Q2))] = 0
        age_percentile['%s-%s' % (str(Q2), str(Q3))] = 0
        age_percentile['>%s' % str(Q3)] = 0
        for sub_age in age_unique:
            if sub_age < Q1:
                age_percentile['%s>' % str(Q1)] += age[str(sub_age)]
            elif sub_age < Q2 and sub_age >= Q1:
                age_percentile['%s-%s' % (str(Q1), str(Q2))] += age[str(sub_age)]
            elif sub_age < Q3 and sub_age >= Q2:
                age_percentile['%s-%s' % (str(Q2), str(Q3))] += age[str(sub_age)]
            else:
                age_percentile['>%s' % str(Q3)] += age[str(sub_age)]


        for name in list(age_percentile.keys()):
            series.append(name, age_percentile[name])

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置图例的位置
        chart.legend().setAlignment(Qt.AlignLeft)
        self.histchart_age_prey.setChart(chart)

    def plot_predator_gender_piechart(self):
        # Pie Chart
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'predator'
        gender = {}
        gender['male'] = 0
        gender['female'] = 0
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]):
                if agent.gender == 'male':
                    gender['male'] += 1
                else:
                    gender['female'] += 1

        for name in list(gender.keys()):
            series.append(name, gender[name])

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置图例的位置
        chart.legend().setAlignment(Qt.AlignLeft)
        self.piechart_gender_predator.setChart(chart)

    def plot_prey_gender_piechart(self):
        # Pie Chart
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'prey'
        gender = {}
        gender['male'] = 0
        gender['female'] = 0
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]):
                if agent.gender == 'male':
                    gender['male'] += 1
                else:
                    gender['female'] += 1

        for name in list(gender.keys()):
            series.append(name, gender[name])

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置图例的位置
        chart.legend().setAlignment(Qt.AlignLeft)
        self.piechart_gender_prey.setChart(chart)

    def plot_predator_life_status_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Life Status Pie Chart")

        specie = 'predator'
        life_status = {}
        life_status['alive'] = 0
        life_status['dead'] = 0

        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]):
                if agent.is_alive:
                    life_status['alive'] += 1
                else:
                    life_status['dead'] += 1

        for name in list(life_status.keys()):
            series.append(name, life_status[name])

        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.legend().setAlignment(Qt.AlignLeft)
        self.piechart_life_status_predator.setChart(chart)

    def plot_prey_life_status_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Life Status Pie Chart")

        specie = 'prey'
        life_status = {}
        life_status['alive'] = 0
        life_status['dead'] = 0

        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]):
                if agent.is_alive:
                    life_status['alive'] += 1
                else:
                    life_status['dead'] += 1

        for name in list(life_status.keys()):
            series.append(name, life_status[name])

        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.legend().setAlignment(Qt.AlignLeft)
        self.piechart_life_status_prey.setChart(chart)

    @Slot()
    def plot_data(self):
        # self.right_plot.addTab(self.plot_network(), "Network")
        super().plot_data()

        self.right_plot.addTab(self.piechart_gender_predator, "Predator Gender Pie Chart")
        self.right_plot.addTab(self.piechart_gender_prey, "Prey Gender Pie Chart")

        self.right_plot.addTab(self.histchart_age_predator, "Predator Age Pie Chart")
        self.right_plot.addTab(self.histchart_age_prey, "Prey Age Pie Chart")

        self.right_plot.addTab(self.piechart_life_status_predator, "Predator Life Status Pie Chart")
        self.right_plot.addTab(self.piechart_life_status_prey, "Prey Life Status Pie Chart")

        self.plot_predator_gender_piechart()
        self.plot_prey_gender_piechart()

        self.plot_prey_age_piechart()
        self.plot_age_piechart()

        self.plot_predator_life_status_piechart()
        self.plot_prey_life_status_piechart()

        root = self.create_specie_tree('predator')
        tree_view = TreeGraphicsView(root)
        tree_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tree_view)
        tree_widget.setLayout(layout)

        self.right_plot.addTab(tree_widget, "Predator Tree")

        root = self.create_specie_tree('prey')
        tree_view = TreeGraphicsView(root)
        tree_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tree_view)
        tree_widget.setLayout(layout)

        self.right_plot.addTab(tree_widget, "Prey Tree")





