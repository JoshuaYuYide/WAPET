from OneSpecieClass.check import Check
from PySide6.QtCore import Qt, Slot, QPointF


class CheckTwo(Check):

    @Slot()
    def check_table(self):
        if self.species_table.columnCount() > 0:
            self.clear_table_bt.setEnabled(True)
            self.clear_table_bt.setEnabled(True)
            if self.result_table.rowCount() == 0 and self.species_table.columnCount() == 3:
                self.simulate_bt.setEnabled(True)
            else:
                self.simulate_bt.setEnabled(False)
        else:
            self.clear_table_bt.setEnabled(False)
            self.simulate_bt.setEnabled(False)
            self.clear_table_bt.setEnabled(False)

        if self.species_table.columnCount() >= 3:
            self.species_submit_bt.setEnabled(False)
        else:
            self.species_submit_bt.setEnabled(True)

        if self.result_table.rowCount() > 0:
            self.plot_bt.setEnabled(True)
        else:
            self.plot_bt.setEnabled(False)
