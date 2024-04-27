import sys
from PySide6.QtCore import Qt, Slot, QPointF, QModelIndex
from PySide6.QtGui import QPainter, QGradient, QPen
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QBoxPlotSeries, QBoxSet, QLineSeries
import random
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Visulization:
    def __init__(self):
        pass

    @Slot()
    def plot_data(self):
        self.plot_piechart()
        self.plot_boxplot()
        self.plot_linechart()
        self.slider_year.setVisible(True)
        self.slider_left.setVisible(True)
        self.slider_right.setVisible(True)
        self.slider.setRange(0, self.table.columnCount())
        self.slider_right.setText(str(self.slider.maximum()) + '/day')
        self.slider_left.setText(str(self.slider.minimum()) + '/day')

    def plot_piechart(self):
        # pie chart
        self.pieseries = QPieSeries()
        for i in range(self.result_table.columnCount()):
            text = self.result_table.item(0, i).text()
            number = float(self.result_table.item(3, i).text())
            self.pieseries.append(text, number)

        self.piechart = QChart()
        self.piechart.addSeries(self.pieseries)
        self.piechart.legend().setAlignment(Qt.AlignLeft)
        self.network.setChart(self.piechart)

    def plot_boxplot(self):
        # Box Plot
        chart = QChart()
        series = QBoxPlotSeries()
        series.setName("Box Plot")

        data = [
            [1, 2, 3, 4, 5],  # 数据集1
            [3, 4, 5, 6, 7],  # 数据集2
            [2, 3, 4, 5, 6],  # 数据集3
        ]

        for i, dataset in enumerate(data):
            set_data = QBoxSet()
            set_data.setValue(i, sum(dataset) / len(dataset))  # 使用平均值作为 y 坐标
            series.append(set_data)

        chart.addSeries(series)
        chart.createDefaultAxes()

        self.boxchart.setChart(chart)

    def plot_linechart(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Line Chart")

        # pop_column_name = "target population"
        # header_model = self.result_table.model().headerData(0, Qt.Horizontal, Qt.DisplayRole)  # 获取水平表头的元数据
        # column_index = header_model.index(pop_column_name, 0, Qt.DisplayRole)  # 在元数据中查找列名对应的索引
        # # 通过行和列索引获取 QModelIndex 对象
        # row = 0  # 行索引
        # column = column_index.column()  # 列索引
        # pop_index = self.result_table.model().index(row, column, QModelIndex())
        #
        # time_column_name = "timestep"
        # header_model = self.result_table.model().headerData(0, Qt.Horizontal, Qt.DisplayRole)  # 获取水平表头的元数据
        # column_index = header_model.index(time_column_name, 0, Qt.DisplayRole)  # 在元数据中查找列名对应的索引
        # # 通过行和列索引获取 QModelIndex 对象
        # row = 0  # 行索引
        # column = column_index.column()  # 列索引
        # time_index = self.result_table.model().index(row, column, QModelIndex())

        # 获取第一列数据
        target_population_data = []
        for row in range(self.result_table.model().rowCount()):
            index = self.result_table.model().index(row, 0)  # 第一列的标签为 0 列的标签
            value = self.result_table.model().data(index)
            target_population_data.append(value)

        # 获取第二列数据
        timestep_data = []
        for row in range(self.result_table.model().rowCount()):
            index = self.result_table.model().index(row, 1)  # 第二列的标签为 1 列的标签
            value = self.result_table.model().data(index)
            timestep_data.append(value)

        data = list(map(lambda x, y: (float(x), float(y)), timestep_data, target_population_data))

        # data = [
        #     (0, 1),
        #     (1, 3),
        #     (2, 4),
        #     (3, 2),
        #     (4, 5)
        # ]

        series = QLineSeries()
        for x, y in data:
            series.append(x, y)

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置线条样式
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        series.setPen(pen)

        self.linechart.setChart(chart)

    @Slot()
    def update_piechart(self):

        index = self.slider.value()
        # x, y = self.table[index]
        # series.replace(index, x, y)

        self.pieseries.clear()
        for i in range(index):
            text = self.table.item(0, i).text()
            number = float(self.table.item(3, i).text())
            self.pieseries.append(text, number)

        self.piechart.addSeries(self.pieseries)
        self.piechart.legend().setAlignment(Qt.AlignLeft)
        self.barchart.setChart(self.piechart)

    def random_plot_linechart(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Line Chart")

        data = [
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random()),
            (random.random(), random.random())
        ]

        for x, y in data:
            series.append(x, y)

        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置线条样式
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        series.setPen(pen)

        self.linechart.setChart(chart)
