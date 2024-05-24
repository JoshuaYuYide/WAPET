import mesa
import numpy as np
import pandas as pd
from mesa import Agent, Model
from PySide6.QtCore import Slot
from mathmatics_model import MathmaticsModelGroup, MathmaticsModelIndividual
import random
from collections import Counter


class Animal(MathmaticsModelIndividual):
    def __init__(self, specie, move_speed_mean, move_speed_std, increase_rate, life_time = 100, marriage_age = 10):
        self.cell_neighbors_occupy = 3
        MathmaticsModelIndividual.__init__(self, self.cell_neighbors_occupy)
        self.age = random.randint(0, 10)
        self.gender = random.choice(['male', 'female'])
        self.kids = []
        self.kids_count = 0
        self.parents = []
        self.parents_count = 0
        self.partner = None
        self.specie = specie
        self.move_speed = 1
        self.position = [-1, -1]
        self.hunger = 100
        self.move_speed_mean = move_speed_mean
        self.move_speed_std = move_speed_std
        self.is_married = False
        self.increase_rate = increase_rate
        self.life_time = life_time
        self.is_alive = True
        self.married_min_age = marriage_age

    def is_live(self):
        if self.hunger <= 0 and self.age > self.life_time:
            self.model.soil_agent.delete_specie_on_soil(self.specie, self, self.position)
            self.model.schedule.remove(self)
            self.is_alive = False
            return False
        else:
            return True

    def attach(self):
        pass

    def escape(self):
        pass

    def can_married(self, partner_gender):
        if self.age > self.married_min_age and not self.is_married and self.is_alive and self.gender != partner_gender:
            return True
        else:
            return False

    def get_married(self):
        if not self.is_married and self.age > 10:
            married_candidate = self.model.soil_agent.map[self.position[0], self.position[1]][self.specie]
            for partner_agent in married_candidate:
                if self.can_married(partner_agent.gender) and partner_agent.can_married(self.gender):
                    self.partner = partner_agent.unique_id
                    self.is_married = True
                    partner_agent.partner = self.unique_id
                    partner_agent.is_married = True
                    break

    def give_birth(self):
        if self.is_married:
            N = sum(list(map(lambda x: len(x), self.soil_agent.map[self.position[0], self.position[1]][self.specie], self.soil_agent.specie_list)))
            K = self.model.soil_agent.map[self.position[0], self.position[1]]['carry_ability']
            is_birth = self.logistic_growth_individual(N, K, self.increase_rate)
            if is_birth:
                new_agent_id = self.model.next_id
                new_agent = TargetSpecieAgent(new_agent_id, self.model)
                new_agent.position = self.position
                new_agent.parents = [self.unique_id, self.partner]
                new_agent.parents_count = 2
                new_agent.age = 0
                self.kids_count += 1
                self.kids.append(new_agent_id)
                partner_agent = self.find_agent_by_id(self.partner_id)
                partner_agent.kids_count += 1
                partner_agent.kids.append(new_agent_id)
                self.model.soil_agent.add_specie_on_soil(self.specie, new_agent, self.position)
                self.model.new_agents.append(new_agent)

    def move(self, map):
        self.position = self.random_walk(self.move_speed_mean, self.move_speed_std, self.position, map)
        return self.position

class TargetSpecieAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'target_specie'
        Animal.__init__(self, self.specie_name, 1, 1, 0.1)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def step(self):
        self.hunger -= 2
        self.move(self.model.soil_agent.map)
        self.age += 1
        if self.model.soil_agent.can_eat(self.specie_name, self.position, self.increase_rate):
            if 100 - self.hunger < self.eat_volume:
                self.hunger = 100
            else:
                self.hunger += self.eat_volume
        self.get_married()
        self.give_birth()
        self.is_live()

class PredatorAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(unique_id, model)
        Animal.__init__(self, 'predator')

class PreyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        Animal.__init__(self, 'prey')

class HumanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        Animal.__init__(self, 'human')
        self.money = 100

class ClimateAgent(Agent):
    # 季风气候、热带雨林气候、热带草原气候、热带沙漠气候、热带季风气候、热带雨林气候、热带草原气候、热带沙漠气候
    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.type = type
        self.climate_dict = {'sunshine': 0, 'wind': 0, 'rainfall': 0, 'cloudy': 0}
        self.climate = random.choice(list(self.climate_dict.keys()))
        # self.temperature_dict = {'sunshine': {'temperature': [], 'prob': []}, 'wind': {'temperature': [], 'prob': []}, 'rainfall': {'temperature': [], 'prob': []}, 'cloudy': {'temperature': [], 'prob': []}}
        #
        # self.temperature_dict['sunshine']['temperature'] = np.linspace(25, 40, 100)
        # self.temperature_dict['sunshine']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['sunshine']['temperature'] - 35) ** 2 / (2 * 1 ** 2))
        #
        # self.temperature_dict['wind']['temperature'] = np.linspace(20, 35, 100)
        # self.temperature_dict['wind']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['wind']['temperature'] - 27) ** 2 / (2 * 1 ** 2))
        #
        # self.temperature_dict['rainfall']['temperature'] = np.linspace(15, 30, 100)
        # self.temperature_dict['rainfall']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['rainfall']['temperature'] - 27) ** 2 / (2 * 1 ** 2))
        #
        # self.temperature_dict['cloudy']['temperature'] = np.linspace(20, 35, 100)
        # self.temperature_dict['cloudy']['prob'] = (1 / (1 * np.sqrt(2 * np.pi))) * np.exp(-(self.temperature['cloudy']['temperature'] - 27) ** 2 / (2 * 1 ** 2))

        # mu = 0  # 均值
        # sigma = 1  # 标准差

        # 计算自定义横坐标对应的概率密度函数值
        #pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


    def climate_style_init(self):
        if self.type == 'tropical rain forest climate':
            self.climate_dict['sunshine'] = 0.3
            self.climate_dict['wind'] = 0.1
            self.climate_dict['rainfall'] = 0.5
            self.climate_dict['cloudy'] = 0.1

    def step(self):
        self.climate = np.random.choice(list(self.climate_dict.keys()), p = list(self.climate_dict.values()))
        # self.temperature = random.choice(self.temperature[self.weather]['temperature'], weights = self.temperature[self.weather]['prob'])
        # if self.climate == 'rainfall':
        #     self.model.water_agents.rainfall()

class SoilAgent(Agent, MathmaticsModelIndividual):
    def __init__(self, unique_id, model, specie_list, inaccessible_num):
        super().__init__(unique_id=unique_id, model=model)
        self.cell_neighbors_occupy = 3
        MathmaticsModelIndividual.__init__(self, self.cell_neighbors_occupy)


        self.map_width = 100
        self.map_height = 100
        self.map = np.empty([self.map_width, self.map_height], dtype=object)
        self.specie_list = specie_list
        self.soil_type_all = ['inaccessible', 'empty']
        self.soil_type_all.extend(self.specie_list)
        self.inaccessible_num = inaccessible_num
        self.specie_occupy_density = 0.2
        for i in range(self.map_width):
            for j in range(self.map_height):
                self.map[i, j] = {}
                self.map[i, j]['is_empty'] = True
                self.map[i, j]['is_inaccessible'] = False
                self.map[i, j]['main_specie'] = 'empty'
                self.map[i, j]['carry_ability'] = random.randint(10, 100)
                for name in self.soil_type_all:
                    self.map[i, j][name] = []
        self.climate_history = []

    def land_init(self):
        remain_inaccessible_position_number = self.inaccessible_num
        while remain_inaccessible_position_number > 0:
            x = random.randint(0, self.map_width-1)
            y = random.randint(0, self.map_height-1)

            if self.map[x, y]['is_empty']:
                self.map[x, y]['is_empty'] = False
                self.map[x, y]['is_inaccessible'] = True
                self.map[x, y]['main_specie'] = 'inaccessible'
                remain_inaccessible_position_number -= 1

    def get_valid_soil(self):
        valid_soil = []
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i, j]['is_empty']:
                    valid_soil.append((i, j))
        return valid_soil

    def specie_occupy(self, specie):
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i][j]['is_empty']:
                    if self.specie_occupy_density < len(self.map[i][j][specie]):
                        self.map[i][j]['main_specie'] = specie

    # add the specie on the soil
    def add_specie_on_soil(self, specie, specie_agent, position):
        if not self.map[position[0], position[1]]['is_inaccessible']:
            if len(self.map[position[0], position[1]][specie]) > 0 or self.map[position[0], position[1]]['is_empty']:
                if specie_agent not in self.map[position[0], position[1]][specie]:
                    self.map[position[0], position[1]][specie].append(specie_agent)

    def delete_specie_on_soil(self, specie, specie_agent, position):
        if len(self.map[position[0], position[1]][specie]) > 0 and specie_agent in self.map[position[0], position[1]][specie]:
            self.map[position[0], position[1]][specie].remove(specie_agent)
        else:
            print('cannot delete %s on %s' % (specie, str(position)))

    def change_soil_carry_ability(self):
        self.climate_history.append(self.model.climate_agent.climate)
        frequency = Counter(self.climate_history)
        var = np.var(list(frequency.values()))
        if var == 0 and len(self.climate_history) < 10:
            var = 1
        elif var == 0 and len(self.climate_history) >= 10:
            var = 0.1

        for i in range(self.map_width):
            for j in range(self.map_height):
                self.map[i][j]['carry_ability'] = self.map[i][j]['carry_ability'] * var

    def can_eat(self, specie, position, increase_rate):
        N = sum(list(map(lambda x: len(self.map[position[0], position[1]][x]), self.specie_list)))
        K = self.map[position[0], position[1]]['carry_ability']
        return self.logistic_growth_individual(N, K, increase_rate)

    def step(self):
        for specie in self.specie_list:
            self.specie_occupy(specie)
        self.change_soil_carry_ability()

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
    def __init__(self, time, specie_dict, inaccessible_num):
        self.schedule = mesa.time.SimultaneousActivation(self)
        soil_unique_id = self.next_id
        self.soil_agent = SoilAgent(soil_unique_id, self, list(specie_dict.keys()), inaccessible_num)
        self.soil_agent.land_init()
        self.schedule.add(self.soil_agent)
        climate_unique_id = self.next_id
        self.climate_agent = ClimateAgent(climate_unique_id, self, 'tropical rain forest climate')
        self.climate_agent.climate_style_init()
        self.schedule.add(self.climate_agent)
        # self.water_agents = WaterAgent(self.next_id, self)

        for specie in specie_dict.keys():
            for i in range(int(specie_dict[specie])):
                new_target_id = self.next_id
                target_specie = TargetSpecieAgent(new_target_id, self)
                target_specie.position = random.choice(self.soil_agent.get_valid_soil())
                self.soil_agent.add_specie_on_soil(specie, target_specie, target_specie.position)
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

# parameters
specie_dict = {'target_specie': 100}
inaccessible_num = 10

# run the model
env_model = EnvModel(100, specie_dict, inaccessible_num)
for i in range(10):
    env_model.step()
    print(env_model.initial_population)






















