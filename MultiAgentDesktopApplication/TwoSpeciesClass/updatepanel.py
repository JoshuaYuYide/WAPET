from OneSpecieClass.updatepanel import UpdatePanel
from PySide6.QtWidgets import QHeaderView

class UpdatePanelTwo(UpdatePanel):
    def __init__(self):
        super().__init__()

    def reset_result_table(self):
        self.result_table.setColumnCount(4)
        self.result_table.setRowCount(0)
        self.result_table.setHorizontalHeaderLabels(["target", "predator", "prey", "timestep"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_items = 0

