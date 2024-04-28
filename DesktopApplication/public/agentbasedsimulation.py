import mesa
import numpy as np
import pandas as pd
from mesa import Agent, Model
from PySide6.QtCore import Slot
from public.mathmatics_model import MathmaticsModel
import random


class TargetSpecieAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.health = 100
        self.age = random.randint(0, 10)
        self.gender = random.choice(['male', 'female'])
        self.kids = []
        self.kids_count = 0
        self.parents = []
        self.parents_count = 0
        self.partner = None
        self.mathmatics_model = MathmaticsModel()

    def step(self):
        if self.mathmatics_model.logistic_growth_individual(self.model.initial_population, self.model.carrying_capacity, self.model.grwoth_rate):
            new_agent_id = self.model.next_id
            new_agent = TargetSpecieAgent(new_agent_id, self.model)  # create a new agent
            self.model.new_agents.append(new_agent)  # add the new agent into the model
            # self.model.schedule.add(new_agent)  # add the new agent into the schedule in the Model, not here

            self.kids_count += 1
            self.kids.append(new_agent_id)

            # self.model.specie_agents[self.unique_id] = self

class EnvModel(Model):
    def __init__(self, population, grwoth_rate, carrying_capacity, time):
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.new_agents = []
        self.next_id = 0
        self.initial_population = population
        self.grwoth_rate = grwoth_rate
        self.carrying_capacity = carrying_capacity
        self.time = time

        for i in range(int(self.initial_population)):
            target_specie = TargetSpecieAgent(self.next_id, self)
            self.schedule.add(target_specie)

        # self.datacollector = mesa.DataCollector(
        #     model_reporters={
        #         "population": lambda m: len(m.fish_agents),
        #         "Fishers": lambda m: m.num_fishers,
        #         "Bank Money": lambda m: m.bank_agent.money
        #     }
        # )

    def step(self):
        self.schedule.step()
        # 在下一个时间步骤中添加新代理
        for new_agent in self.new_agents:
            self.schedule.add(new_agent)

        self.initial_population += len(self.new_agents)
        self.new_agents = []


        # self.datacollector.collect(self)

























