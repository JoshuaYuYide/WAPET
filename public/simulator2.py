import mesa
import numpy as np
import seaborn as sns # Data visualization tools.
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp
import random

#  inherent per-capita growth rate
r1 = 0.1  # fisher
r2 = 0.3  # fish
# initial population size
x1 = 10  # fisher
x2 = 100  # fish
# the effect species 2 has on the population of species 1
alpha12 = 0.1 # fisher to fish
alpha21 = 0.001
# carrying capacity
K1 = 100
K2 = 100


def lotka_volterra_model1(params):
    x1 = params['x1']
    x2 = params['x2']
    dx1_dt = r1 * x1 * (1 - ((x1 + alpha12 * x2) / K1))
    return dx1_dt

def lotka_volterra_model2(params):
    x1 = params['x1']
    x2 = params['x2']
    dx2_dt = r2 * x2 * (1 - ((x2 + alpha21 * x1) / K2))
    return dx2_dt


class FishingModel(mesa.Model):
    def __init__(self, num_fish, num_fisher, width, height):
        super().__init__()
        self.num_fish = num_fish
        self.num_fisher = num_fisher
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = True

        for i in range(self.num_fish):
            a = BluefinTunaAgent(i, self)
            self.schedule.add(a)
        for i in range(self.num_fisher):
            a = FisherFolkAgent(i, self)
            self.schedule.add(a)
        a = BankAgent(1, self)
        self.schedule.add(a)

        self.datacollector = mesa.DataCollector(  # 创建 DataCollector 对象
            model_reporters={
                "Fish": lambda m: len(m.fish_agents),
                "Fishers": lambda m: m.num_fishers,
                "Bank Money": lambda m: m.bank_agent.money
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()



class BluefinTunaAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = 1 # 1: alive, 0: dead
        self.gender = random.randint(1,2) # male = 1, female = 2
        self.pregnant = 0 # age constructure, gender constructure
        self.born = 0
        self.age = 0
        self.nature_death_rate = 0.01

    def nature_death(self):
        if random.random() < self.nature_death_rate:
            self.alive = 0


class FisherFolkAgent(mesa.Agent):
    def __init__(self, unique_id, catch_speed, model):
        super().__init__(unique_id, model)
        self.wealth = 0
        self.alive = 1
        # self.catch_speed = catch_speed  # [0-10]
        self.increase_ratio_per_year = 0.1
        self.fish_store = 0

    def catch(self, catch_num):
        self.fish_store += catch_num

# class WeatherAgent(mesa.Agent):
#     def __init__(self, unique_id, model):
#         super().__init__(unique_id, model)
#         self.weather = 0  # {0: snow, 1: rain, 2: sun}
#
#     def step(self):
#         self.weather = random.choice([0,1,2])
#         return self.weather

class BankAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cost_amount = -100
        self.per_fish_price = 10

    def cost(self, balance):
        return balance + self.cost_amount

    def sell(self, balance, num_catch_fish):
        return balance + num_catch_fish * self.per_fish_price

