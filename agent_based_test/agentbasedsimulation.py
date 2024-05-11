import mesa
import numpy as np
import pandas as pd
from mesa import Agent, Model
from PySide6.QtCore import Slot
from mathmatics_model import MathmaticsModel
import random


class animal:
    def __init__(self, specie):
        self.health = 100
        self.age = random.randint(0, 10)
        self.gender = random.choice(['male', 'female'])
        self.kids = []
        self.kids_count = 0
        self.parents = []
        self.parents_count = 0
        self.partner = None
        self.mathmatics_model = MathmaticsModel()
        self.specie = specie
        self.move_speed = 1
        self.position = [0, 0]
        self.is_illness = False
        self.diease = None
        self.hydration = 100

    def is_live(self):
        if self.health <= 0:
            return False
        else:
            return True

    def attach(self):
        pass

    def escape(self):
        pass

    def get_married(self):
        pass

    def pregnet(self):
        pass

    def give_birth(self):
        pass

    def drink(self, water_id):
        water_agent = self.model.water_agents.get(water_id)
        water_agent.reduce_volumn()

# class family:
#     def __init__(self):
#         self.family_id = 0
#         self.members = []
#         self.kids = []
#         self.parents = []
#         self.position = [0, 0]
#
#     def get_new_family_id(self):
#         self.family_id += 1
#         return self.family_id
#
#     def build_family(self, members):
#         self.members = members
#         pass



class TargetSpecieAgent(Agent, animal):
    def __init__(self, unique_id, model):
        Agent.__init__(unique_id, model)
        animal.__init__(self, 'target_specie')

    def step(self):
        pass

class predatorAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(unique_id, model)
        animal.__init__(self, 'predator')

class preyAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(unique_id, model)
        animal.__init__(self, 'prey')

class HumanAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(unique_id, model)
        animal.__init__(self, 'human')
        self.money = 100

class BankAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = 10000
        self.interest_rate = 0.05

    def step(self):
        self.money = self.money * (1 + self.interest_rate)


class diseaseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.infection_rate = 0.1
        self.dead_rate = 0.01
        self.time = 0

    def is_infect(self):
        if random.random() < self.infection_rate:
            return True
        else:
            return False

    def change_rate(self):
        if self.time > 10:
            self.infection_rate += 0.01
            self.dead_rate -= 0.01

    def step(self, time):
        self.time = time
        self.change_rate()




class climateAgent(Agent):
    # 季风气候、热带雨林气候、热带草原气候、热带沙漠气候、热带季风气候、热带雨林气候、热带草原气候、热带沙漠气候
    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.type = type
        self.climate_dict = {'sunshine': 0, 'wind': 0, 'rainfall': 0, 'cloudy': 0}
        self.temperature_dict = {'sunshine': {'temperature': [], 'prob': []}, 'wind': {'temperature': [], 'prob': []}, 'rainfall': {'temperature': [], 'prob': []}, 'cloudy': {'temperature': [], 'prob': []}}

        self.temperature_dict['sunshine']['temperature'] = np.linspace(25, 40, 100)
        self.temperature_dict['sunshine']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['sunshine']['temperature'] - 35) ** 2 / (2 * 1 ** 2))

        self.temperature_dict['wind']['temperature'] = np.linspace(20, 35, 100)
        self.temperature_dict['wind']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['wind']['temperature'] - 27) ** 2 / (2 * 1 ** 2))

        self.temperature_dict['rainfall']['temperature'] = np.linspace(15, 30, 100)
        self.temperature_dict['rainfall']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['rainfall']['temperature'] - 27) ** 2 / (2 * 1 ** 2))

        self.temperature_dict['cloudy']['temperature'] = np.linspace(20, 35, 100)
        self.temperature_dict['cloudy']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['cloudy']['temperature'] - 27) ** 2 / (2 * 1 ** 2))

        # mu = 0  # 均值
        # sigma = 1  # 标准差

        # 计算自定义横坐标对应的概率密度函数值
        #pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


    def climate_style_init(self):
        if self.type == 'tropical rain forest climate':
            self.climate_dict['sunshine'] = 0.5
            self.climate_dict['wind'] = 0.2
            self.climate_dict['rainfall'] = 0.8
            self.climate_dict['cloudy'] = 0.3

    def step(self):
        self.climate = random.choice(list(self.climate.keys()), weights = list(self.climate.values()))
        self.temperature = random.choice(self.temperature[self.weather]['temperature'], weights = self.temperature[self.weather]['prob'])
        if self.climate == 'rainfall':
            self.model.water_agents.rainfall()

class TreeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = random.randint(0, 10)
        self.position = []

class WaterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.volumn = random.randint(0, 100)
        self.pure_prob = random.random()
        self.position = []


    def rainfall(self):
        self.rate = random.uniform(0.1, 0.3)
        self.rainfall()
        self.increase_volumn()
        self.purify()

    def purify(self):
        self.pure_prob += self.rate

    def reduce_volumn(self):
        self.pure_prob -= 0.01

    def increase_volumn(self):
        self.pure_prob += self.rate * 10

    def can_drink(self):
        if self.pure_prob > 0.8:
            return True
        else:
            return False


class SoilAgent(Agent):
    def __init__(self, unique_id, model, soil_type):
        super().__init__(unique_id, model)
        self.map_width = 100
        self.map_height = 100
        self.map = np.zeros([self.map_width, self.map_height])
        self.soil_type = soil_type

    def land_init(self):
        if self.soil_type == 'tropical rain forest':
            self.num_forest = 50
            self.num_grassland = 30
            self.num_water = 10
            self.num_bare = 10
            self.num_humanland = 0

            number_resource = {'forest': 50, 'grassland': 30, 'water': 10, 'bare': 10, 'humanland': 0}

        for i in range(self.map_width):
            for j in range(self.map_height):
                type = random.choice(list(number_resource.keys()))
                if type == 'forest':
                    self.map[i][j] = self.model.TreeAgent(self.model.next_id, self.model.TreeAgent)

                self.map[i][j] = type
                number_resource[type] -= 1
                if number_resource[type] == 0:
                    number_resource.pop(type)



    def remodel(self):
        pass

    def unavailable(self):
        pass

class HumanLandAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = random.randint(0, 10)

    def school(self):
        pass

    def factory(self):
        pass

    def farm(self):
        pass

    def house(self):
        pass

    def park(self):
        pass

    def step(self):
        pass

class CatastrophesAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def earthquake(self):
        pass

    def flood(self):
        pass

    def drought(self):
        pass

    def step(self):
        pass


class EnvModel(Model):
    def __init__(self, time):
        self.schedule = mesa.time.SimultaneousActivation(self)
        solid_agent = SoilAgent(0, self, 'tropical rain forest')
        solid_agent.land_init()
        self.schedule.add(solid_agent)
        self.climate_agent = climateAgent(0, self, 'tropical rain forest climate')
        self.climate_agent.climate_style_init()
        self.schedule.add(self.climate_agent)
        self.water_agents = WaterAgent(0, self)







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
        if self.climate_agent.climate == 'rainfall':
            self.water_agents.rainfall()
            self.water_agents.increase_volumn()
            self.water_agents.purify()

        # 在下一个时间步骤中添加新代理
        for new_agent in self.new_agents:
            self.schedule.add(new_agent)

        self.initial_population += len(self.new_agents)
        self.new_agents = []


        # self.datacollector.collect(self)


# parameters

water_source_num = 3




# run the model
env_model = EnvModel(100, 1.0, 1000, 50)
for i in range(10):
    env_model.step()
    print(env_model.initial_population)






















