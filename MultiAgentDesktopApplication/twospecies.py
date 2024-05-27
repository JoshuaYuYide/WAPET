from PySide6.QtWidgets import (QHBoxLayout, QWidget)
from TwoSpeciesClass.panelinit import PanelInit
from TwoSpeciesClass.visualization import Visulization
from TwoSpeciesClass.tableoperation import TableOperation


class TwoSpecies(QWidget, PanelInit, Visulization, TableOperation):
    def __init__(self):
        super().__init__()

        # main
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.leftmost_panel())
        self.layout.addLayout(self.left_panel())
        # self.layout.addLayout(self.middle_panel())
        self.layout.addLayout(self.right_panel())

    def get_widget(self):
        return self