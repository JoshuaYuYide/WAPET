import mesa
import numpy as np
import seaborn as sns # Data visualization tools.
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_ivp

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
    def __init__(self, N1, N2, width, height):
        super().__init__()
        self.num_fish = N1
        self.num_fisher = N2
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        for i in range(self.num_agents):
            a = BluefinTunaAgent(i, self)

            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth", "Steps_not_given": "steps_not_given"},
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()




class FisherFolkAgent(mesa.Agent):
    def __init__(self, unique_id, catch_speed, model):
        super().__init__(unique_id, model)
        self.wealth = 0
        self.alive = 1
        self.catch_speed = catch_speed  # [0-10]

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


class WeatherAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.weather = 0  # {0: snow, 1: rain, 2: sun}

    def step(self):
        self.weather = self.random.randint(0, 10)


class BankAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cost_amount = -100
        self.per_fish_price = 10

    def cost(self, balance):
        return balance + self.cost_amount

    def sell(self, balance, num_catch_fish):
        return balance + num_catch_fish * self.per_fish_price

