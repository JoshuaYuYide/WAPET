import math
from public.mathmatics_model import MathmaticsModel
from public.agentbasedsimulation import TargetSpecieAgent, EnvModel, PredatorAgent, PreyAgent, ClimateAgent, SoilAgent
import pandas as pd
from PySide6.QtWidgets import (QTableWidgetItem)
from PySide6.QtCore import Slot

class Calculate(MathmaticsModel):
    def __init__(self):
        pass

    @Slot()
    def simulate_one_specie_individual(self):
        result = {}
        result['target_specie'] = {}
        result['predator'] = {}
        result['prey'] = {}

        for i in range(self.species_table.columnCount()):
            if self.species_table.item(0,i).text() == 'target_specie':
                for j in range(self.species_table.rowCount()):
                    result['target_specie'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()
            elif self.species_table.item(0,i).text() == 'predator':
                for j in range(self.species_table.rowCount()):
                    result['predator'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()
            elif self.species_table.item(0,i).text() == 'prey':
                for j in range(self.species_table.rowCount()):
                    result['prey'][self.specie_table_rowname[j]] = self.species_table.item(j,i).text()

        total_time = result['target_specie'][self.simulation_years.objectName()]
        self.specie_dict = {'target_specie': {'population': result['target_specie'][self.initial_population.objectName()]}}

        self.model = EnvModel(self)
        for time in range(int(total_time)):
            self.model.step()
            self.result_table.insertRow(time)
            self.result_table.setItem(time, 0, QTableWidgetItem(str(self.model.specie_dict['target_specie']['population'])))
            self.result_table.setItem(time, 1, QTableWidgetItem(str(time)))



