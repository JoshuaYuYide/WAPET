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

class Visulization:
    def __init__(self):
        pass

    @Slot()
    def plot_data(self):
        # self.right_plot.addTab(self.plot_network(), "Network")
        self.right_plot.addTab(self.piechart_gender, "Gender Pie Chart")
        self.right_plot.addTab(self.histchart_age, "Age Pie Chart")
        self.right_plot.addTab(self.piechart_life_status, "Life Status Pie Chart")
        self.right_plot.addTab(self.linechart, "Population Line Chart")

        root = self.create_specie_tree('target_specie')
        tree_view = TreeGraphicsView(root)
        tree_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tree_view)
        tree_widget.setLayout(layout)

        self.right_plot.addTab(tree_widget, "Tree")
        self.plot_agent_based_logistic_individual()
        self.plot_gender_piechart()
        self.plot_age_piechart()
        self.plot_life_status_piechart()

        '''
        # self.slider_year.setVisible(True)
        # self.slider_left.setVisible(True)
        # self.slider_right.setVisible(True)
        # self.slider_year.setRange(0, self.result_table.rowCount())
        # self.slider_right.setText(str(self.slider_year.maximum()) + '/month')
        # self.slider_left.setText(str(self.slider_year.minimum()) + '/month')
        '''

    '''
        # def plot_network(self):
    #     G = nx.Graph()
    #     G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])
    #     widget = NetworkxWidget(G)
    #     return widget

    # def plot_boxplot(self):
    #     # Box Plot
    #     chart = QChart()
    #     series = QBoxPlotSeries()
    #     series.setName("Box Plot")
    # 
    #     data = [
    #         [1, 2, 3, 4, 5],  # 数据集1
    #         [3, 4, 5, 6, 7],  # 数据集2
    #         [2, 3, 4, 5, 6],  # 数据集3
    #     ]
    # 
    #     for i, dataset in enumerate(data):
    #         set_data = QBoxSet()
    #         set_data.setValue(i, sum(dataset) / len(dataset))  # 使用平均值作为 y 坐标
    #         series.append(set_data)
    # 
    #     chart.addSeries(series)
    #     chart.createDefaultAxes()
    # 
    #     self.boxchart.setChart(chart)
    '''


    def plot_agent_based_logistic_individual(self):
        # Line Chart
        chart = QChart()
        series = QLineSeries()
        series.setName("Logistic Growth Individual Agent-based Line Chart")

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

    def plot_age_histogram(self):
        # Histogram Chart

        chart = QChart()
        series = QBarSeries()

        specie = 'target_specie'
        age = {}
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]):
                if agent.age not in list(age.keys()):
                    age[agent.age] = 1
                else:
                    age[agent.age] += 1

        for name in list(age.keys()):
            set = QBarSet(str(name))
            set << age[name]
            series.append(set)

        chart.addSeries(series)
        chart.setTitle("Age Histogram")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()

        # 设置图例的位置
        chart.legend().setAlignment(Qt.AlignLeft)

        self.histchart_age.setChart(chart)

    def plot_age_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'target_specie'
        age = {}
        for agent in self.model.schedule.agents:
            if isinstance(agent, self.model.statistics[specie]) and agent.is_alive:
                if agent.age not in list(age.keys()):
                    age[str(agent.age)] = 1
                else:
                    age[str(agent.age)] += 1

        if len(age.keys()) == 0:
            return

        age_unique = list(age.keys())
        age_unique = list(map(lambda x: int(x), age_unique))
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
        self.histchart_age.setChart(chart)

    def plot_gender_piechart(self):
        # Pie Chart
        chart = QChart()
        series = QPieSeries()
        series.setName("Age Pie Chart")

        specie = 'target_specie'
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
        self.piechart_gender.setChart(chart)

    def plot_life_status_piechart(self):
        chart = QChart()
        series = QPieSeries()
        series.setName("Life Status Pie Chart")

        specie = 'target_specie'
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
        self.piechart_life_status.setChart(chart)


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

    def create_specie_tree(self, specie_name):
        root = TreeNode(specie_name)
        visited = []
        current_generation = {}
        next_generation = {}
        current_gen_num = 0
        all_animal_agents = [agent for agent in self.model.schedule.agents if agent.classification == 'animal']
        specific_specie_agents = [agent for agent in all_animal_agents if agent.specie == specie_name]
        while len(visited) < len(specific_specie_agents):
            if current_gen_num == 0:
                for agent in specific_specie_agents:
                    if agent.parents_count == 0 and agent not in visited:
                        agent_tree = TreeNode(agent)
                        current_generation[agent] = agent_tree
                        visited.append(agent)
                        root.add_child(agent_tree)
                current_gen_num += 1
            else:
                for agent in specific_specie_agents:
                    if agent not in visited:
                        for parent in agent.parents:
                            if parent in list(current_generation.keys()):
                                agent_tree = TreeNode(agent)
                                next_generation[agent] = agent_tree
                                visited.append(agent)
                                current_generation[parent].add_child(agent_tree)
                current_generation = next_generation
                next_generation = {}
                current_gen_num += 1
        return root

    @Slot()
    def plot_target_specie_on_map(self):
        self.mr_grid_widget.reset_color()
        specie_name = 'target_specie'
        total_amount = self.model.soil_agent.specie_amount[specie_name]
        for y in range(int(self.mr_map_size.text())):
            for x in range(int(self.mr_map_size.text())):
                if not self.model.soil_agent.map[x][y]['is_inaccessible']:
                    # alpha = (len(self.model.soil_agent.map[x][y]['target_specie']) / total_amount) * 255
                    alpha = (len(self.model.soil_agent.map[x][y][specie_name]) / total_amount)
                    self.mr_grid_widget.update_alpha(specie_name, alpha, [x,y])

        self.mr_grid_widget.draw_species(specie_name)

    @Slot()
    def plot_carry_on_map(self):
        self.mr_grid_widget.reset_color()
        specie_name = 'carry_ability'
        max_carry = float('-inf')
        for y in range(int(self.mr_map_size.text())):
            for x in range(int(self.mr_map_size.text())):
                if not self.model.soil_agent.map[x][y]['is_inaccessible']:
                    if self.model.soil_agent.map[x][y][specie_name] > max_carry:
                        max_carry = self.model.soil_agent.map[x][y][specie_name]

        for y in range(int(self.mr_map_size.text())):
            for x in range(int(self.mr_map_size.text())):
                if not self.model.soil_agent.map[x][y]['is_inaccessible']:
                    # alpha = (len(self.model.soil_agent.map[x][y]['target_specie']) / total_amount) * 255
                    alpha = self.model.soil_agent.map[x][y][specie_name] / max_carry
                    self.mr_grid_widget.update_alpha(specie_name, alpha, [x, y])

        self.mr_grid_widget.draw_species(specie_name)

class TreeNode:
    def __init__(self, label):
        self.label = label
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class TreeGraphicsView(QGraphicsView):
    def __init__(self, root, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.root = root
        self.node_radius = 2
        self.vertical_spacing = 80
        self.horizontal_spacing = self.node_radius * 2
        self.draw_tree()

    def draw_tree(self):
        self._draw_subtree(self.root, 0, 0, 0)

    def _draw_subtree(self, node, x, y, depth):
        # Draw the node
        ellipse = QGraphicsEllipseItem(x, y, self.node_radius * 2, self.node_radius * 2)
        ellipse.setBrush(QBrush(Qt.blue))
        ellipse.setPen(QPen(Qt.black))
        self.scene.addItem(ellipse)

        # # Draw the label
        # text = QGraphicsTextItem(str(node.label))
        # text.setPos(x + self.node_radius - text.boundingRect().width() / 2, y + self.node_radius - text.boundingRect().height() / 2)
        # self.scene.addItem(text)

        # Draw the children
        child_x = x - (len(node.children) - 1) * self.horizontal_spacing / 2
        child_y = y + self.vertical_spacing
        pen = QPen(Qt.red)
        pen.setWidth(2)
        color = QColor(Qt.red)
        color.setAlphaF(0.2)
        pen.setColor(color)
        for child in node.children:
            child_pos = (child_x + self.node_radius, child_y + self.node_radius)
            # Draw the line to the child
            line = self.scene.addLine(x + self.node_radius, y + self.node_radius * 2, child_pos[0],
                                      child_pos[1], pen)
            # Recursively draw the child
            self._draw_subtree(child, child_x, child_y, depth + 1)
            child_x += self.horizontal_spacing

# class NetworkxWidget(QWidget):
#     def __init__(self, graph):
#         super().__init__()
#         self.graph = graph
#         self.figure = plt.figure(figsize=(5, 5))
#         self.canvas = FigureCanvas(self.figure)
#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.canvas)
#         self.setLayout(self.layout)
#
#     def paintEvent(self, event):
#         self.plot_graph()
#
#     def plot_graph(self):
#         pos = nx.spring_layout(self.graph)  # 定义节点的布局
#         nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', font_size=8)  # 绘制图形
#         self.canvas.draw()
#
# class Node(QGraphicsObject):
#
#     """A QGraphicsItem representing node in a graph"""
#
#     def __init__(self, name: str, parent=None):
#         """Node constructor
#
#         Args:
#             name (str): Node label
#         """
#         super().__init__(parent)
#         self._name = name
#         self._edges = []
#         self._color = "#5AD469"
#         self._radius = 30
#         self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
#
#         self.setFlag(QGraphicsItem.ItemIsMovable)
#         self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
#         self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
#
#     def boundingRect(self) -> QRectF:
#         """Override from QGraphicsItem
#
#         Returns:
#             QRect: Return node bounding rect
#         """
#         return self._rect
#
#     def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
#         """Override from QGraphicsItem
#
#         Draw node
#
#         Args:
#             painter (QPainter)
#             option (QStyleOptionGraphicsItem)
#         """
#         painter.setRenderHints(QPainter.Antialiasing)
#         painter.setPen(
#             QPen(
#                 QColor(self._color).darker(),
#                 2,
#                 Qt.SolidLine,
#                 Qt.RoundCap,
#                 Qt.RoundJoin,
#             )
#         )
#         painter.setBrush(QBrush(QColor(self._color)))
#         painter.drawEllipse(self.boundingRect())
#         painter.setPen(QPen(QColor("white")))
#         painter.drawText(self.boundingRect(), Qt.AlignCenter, self._name)
#
#     def add_edge(self, edge):
#         """Add an edge to this node
#
#         Args:
#             edge (Edge)
#         """
#         self._edges.append(edge)
#
#     def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
#         """Override from QGraphicsItem
#
#         Args:
#             change (QGraphicsItem.GraphicsItemChange)
#             value (Any)
#
#         Returns:
#             Any
#         """
#         if change == QGraphicsItem.ItemPositionHasChanged:
#             for edge in self._edges:
#                 edge.adjust()
#
#         return super().itemChange(change, value)
#
# class Edge(QGraphicsItem):
#     def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
#         """Edge constructor
#
#         Args:
#             source (Node): source node
#             dest (Node): destination node
#         """
#         super().__init__(parent)
#         self._source = source
#         self._dest = dest
#
#         self._tickness = 2
#         self._color = "#2BB53C"
#         self._arrow_size = 20
#
#         self._source.add_edge(self)
#         self._dest.add_edge(self)
#
#         self._line = QLineF()
#         self.setZValue(-1)
#         self.adjust()
#
#     def boundingRect(self) -> QRectF:
#         """Override from QGraphicsItem
#
#         Returns:
#             QRect: Return node bounding rect
#         """
#         return (
#             QRectF(self._line.p1(), self._line.p2())
#             .normalized()
#             .adjusted(
#                 -self._tickness - self._arrow_size,
#                 -self._tickness - self._arrow_size,
#                 self._tickness + self._arrow_size,
#                 self._tickness + self._arrow_size,
#             )
#         )
#
#     def adjust(self):
#         """
#         Update edge position from source and destination node.
#         This method is called from Node::itemChange
#         """
#         self.prepareGeometryChange()
#         self._line = QLineF(
#             self._source.pos() + self._source.boundingRect().center(),
#             self._dest.pos() + self._dest.boundingRect().center(),
#         )
#
#     def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF):
#         """Draw arrow from start point to end point.
#
#         Args:
#             painter (QPainter)
#             start (QPointF): start position
#             end (QPointF): end position
#         """
#         painter.setBrush(QBrush(self._color))
#
#         line = QLineF(end, start)
#
#         angle = math.atan2(-line.dy(), line.dx())
#         arrow_p1 = line.p1() + QPointF(
#             math.sin(angle + math.pi / 3) * self._arrow_size,
#             math.cos(angle + math.pi / 3) * self._arrow_size,
#         )
#         arrow_p2 = line.p1() + QPointF(
#             math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
#             math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
#         )
#
#         arrow_head = QPolygonF()
#         arrow_head.clear()
#         arrow_head.append(line.p1())
#         arrow_head.append(arrow_p1)
#         arrow_head.append(arrow_p2)
#         painter.drawLine(line)
#         painter.drawPolygon(arrow_head)
#
#     def _arrow_target(self) -> QPointF:
#         """Calculate the position of the arrow taking into account the size of the destination node
#
#         Returns:
#             QPointF
#         """
#         target = self._line.p1()
#         center = self._line.p2()
#         radius = self._dest._radius
#         vector = target - center
#         length = math.sqrt(vector.x() ** 2 + vector.y() ** 2)
#         if length == 0:
#             return target
#         normal = vector / length
#         target = QPointF(center.x() + (normal.x() * radius), center.y() + (normal.y() * radius))
#
#         return target
#
#     def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
#         """Override from QGraphicsItem
#
#         Draw Edge. This method is called from Edge.adjust()
#
#         Args:
#             painter (QPainter)
#             option (QStyleOptionGraphicsItem)
#         """
#
#         if self._source and self._dest:
#             painter.setRenderHints(QPainter.Antialiasing)
#
#             painter.setPen(
#                 QPen(
#                     QColor(self._color),
#                     self._tickness,
#                     Qt.SolidLine,
#                     Qt.RoundCap,
#                     Qt.RoundJoin,
#                 )
#             )
#             painter.drawLine(self._line)
#             self._draw_arrow(painter, self._line.p1(), self._arrow_target())
#             self._arrow_target()
#
# class GraphView(QGraphicsView):
#     def __init__(self, graph: nx.DiGraph, parent=None):
#         """GraphView constructor
#
#         This widget can display a directed graph
#
#         Args:
#             graph (nx.DiGraph): a networkx directed graph
#         """
#         super().__init__()
#         self._graph = graph
#         self._scene = QGraphicsScene()
#         self.setScene(self._scene)
#
#         # Used to add space between nodes
#         self._graph_scale = 200
#
#         # Map node name to Node object {str=>Node}
#         self._nodes_map = {}
#
#         # List of networkx layout function
#         self._nx_layout = {
#             "circular": nx.circular_layout,
#             "planar": nx.planar_layout,
#             "random": nx.random_layout,
#             "shell_layout": nx.shell_layout,
#             "kamada_kawai_layout": nx.kamada_kawai_layout,
#             "spring_layout": nx.spring_layout,
#             "spiral_layout": nx.spiral_layout,
#         }
#
#         self._load_graph()
#         self.set_nx_layout("circular")
#
#     def get_nx_layouts(self) -> list:
#         """Return all layout names
#
#         Returns:
#             list: layout name (str)
#         """
#         return self._nx_layout.keys()
#
#     def set_nx_layout(self, name: str):
#         """Set networkx layout and start animation
#
#         Args:
#             name (str): Layout name
#         """
#         if name in self._nx_layout:
#             self._nx_layout_function = self._nx_layout[name]
#
#             # Compute node position from layout function
#             positions = self._nx_layout_function(self._graph)
#
#             # Change position of all nodes using an animation
#             self.animations = QParallelAnimationGroup()
#             for node, pos in positions.items():
#                 x, y = pos
#                 x *= self._graph_scale
#                 y *= self._graph_scale
#                 item = self._nodes_map[node]
#
#                 animation = QPropertyAnimation(item, b"pos")
#                 animation.setDuration(1000)
#                 animation.setEndValue(QPointF(x, y))
#                 animation.setEasingCurve(QEasingCurve.OutExpo)
#                 self.animations.addAnimation(animation)
#
#             self.animations.start()
#
#     def _load_graph(self):
#         """Load graph into QGraphicsScene using Node class and Edge class"""
#
#         self.scene().clear()
#         self._nodes_map.clear()
#
#         # Add nodes
#         for node in self._graph:
#             item = Node(node)
#             self.scene().addItem(item)
#             self._nodes_map[node] = item
#
#         # Add edges
#         for a, b in self._graph.edges:
#             source = self._nodes_map[a]
#             dest = self._nodes_map[b]
#             self.scene().addItem(Edge(source, dest))


# def create_sample_tree():
#
#     root = TreeNode("A")
#     b = TreeNode("B")
#     c = TreeNode("C")
#     d = TreeNode("D")
#     e = TreeNode("E")
#     f = TreeNode("F")
#     g = TreeNode("G")
#     root.add_child(b)
#     root.add_child(c)
#     b.add_child(d)
#     b.add_child(e)
#     c.add_child(f)
#     c.add_child(g)
#     return root
