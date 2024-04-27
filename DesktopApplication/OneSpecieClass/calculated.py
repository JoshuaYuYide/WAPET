import math
from public.mathmatics_model import MathmaticsModel
import pandas as pd
from PySide6.QtWidgets import (QTableWidgetItem)
from PySide6.QtCore import Slot

class Calculate(MathmaticsModel):
    def __init__(self):
        pass

    @Slot()
    def simulate_logistic_growth_discrete(self):
        print('1')
        total_time = float(self.simulation_years.text())
        growth_rate = float(self.growth_rate.text())
        carrying_capacity = float(self.carrying_capacity.text())
        time = 0
        N = float(self.initial_population.text())
        for i in range(int(total_time)):
            self.result_table.insertRow(time)
            self.result_table.setItem(time, 0, QTableWidgetItem(str(N)))
            self.result_table.setItem(time, 1, QTableWidgetItem(str(time)))
            N_next = self.logistic_solution_discrete(N, growth_rate, carrying_capacity, time)
            time += 1
            N = N_next

