import math
from public.mathmatics_model import MathmaticsModel
from public.agentbasedsimulation import TargetSpecieAgent, EnvModel, PredatorAgent, PreyAgent, ClimateAgent, SoilAgent
import pandas as pd
from PySide6.QtWidgets import (QTableWidgetItem)
from PySide6.QtCore import Slot

class Calculate(MathmaticsModel):
    def __init__(self):
        pass
    #
    # @Slot()
    # def simulate_logistic_growth_discrete_specie(self):
    #     total_time = float(self.simulation_years.text())
    #     growth_rate = float(self.growth_rate.text())
    #     carrying_capacity = float(self.carrying_capacity.text())
    #     time = 0
    #     N = float(self.initial_population.text())
    #     for i in range(int(total_time)):
    #         self.result_table.insertRow(time)
    #         self.result_table.setItem(time, 0, QTableWidgetItem(str(N)))
    #         self.result_table.setItem(time, 1, QTableWidgetItem(str(time)))
    #         N_next = self.logistic_solution_discrete(N, growth_rate, carrying_capacity, time)
    #         time += 1
    #         N = N_next
    #
    # @Slot()
    # def simulate_logistic_growth_discrete_individual(self):
    #     total_time = float(self.simulation_years.text())
    #     growth_rate = float(self.growth_rate.text())
    #     carrying_capacity = float(self.carrying_capacity.text())
    #     time = 0
    #     N = float(self.initial_population.text())
    #     for i in range(int(total_time)):
    #         self.result_table.insertRow(time)
    #         self.result_table.setItem(time, 0, QTableWidgetItem(str(N)))
    #         self.result_table.setItem(time, 1, QTableWidgetItem(str(time)))
    #         model = EnvModel(N, growth_rate, carrying_capacity, time)
    #         model.step()
    #         N_next = model.initial_population
    #         # N_next = self.logistic_solution_discrete(N, growth_rate, carrying_capacity, time)
    #         time += 1
    #         N = N_next

    @Slot()
    def simulate_one_specie_individual(self):
        result = {}
        result['target specie'] = {}
        result['predator'] = {}
        result['prey'] = {}

        for i in range(self.species_table.columnCount()):
            if self.species_table.item(0,i).text() == 'target specie':
                for j in range(self.species_table.rowCount()):
                    result['target specie'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()
            elif self.species_table.item(0,i).text() == 'predator':
                for j in range(self.species_table.rowCount()):
                    result['predator'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()
            elif self.species_table.item(0,i).text() == 'prey':
                for j in range(self.species_table.rowCount()):
                    result['prey'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()

        total_time = result['target specie']['simulation months']
        self.specie_dict = {'target_specie': {'population': result['target specie']['initial population']}}

        self.model = EnvModel(self)
        for time in range(int(total_time)):
            self.model.step()
            self.result_table.insertRow(time)
            self.result_table.setItem(time, 0, QTableWidgetItem(str(self.model.specie_dict['target_specie']['population'])))
            self.result_table.setItem(time, 1, QTableWidgetItem(str(time)))



