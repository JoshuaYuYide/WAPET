import mesa
import numpy as np
import pandas as pd
from mesa import Agent, Model
from PySide6.QtCore import Slot
from public.mathmatics_model import MathmaticsModel
import random
from collections import Counter

class Animal(MathmaticsModel):
    def __init__(self, specie, move_speed_mean, move_speed_std, increase_rate, life_time = 100, marriage_age = 10,
                 fertility_change = -0.001, alive_ability_change_per_time = 0.001, attack_ability = 0.5, escape_ability = 0.5):
        self.cell_neighbors_occupy = 3
        MathmaticsModel.__init__(self, self.cell_neighbors_occupy)
        self.age = random.randint(0, 10)
        self.gender = random.choice(['male', 'female'])
        self.kids = []
        self.kids_count = 0
        self.parents = []
        self.parents_count = 0
        self.partner = None
        self.specie = specie
        self.position = [-1, -1]
        self.hunger = 100
        self.move_speed_mean = move_speed_mean
        self.move_speed_std = move_speed_std
        self.is_married = False
        self.increase_rate = increase_rate
        self.life_time = life_time
        self.is_alive = True
        self.married_min_age = marriage_age
        self.fertility_change = fertility_change
        self.alive_ability_change_per_time = alive_ability_change_per_time
        self.attack_ability = attack_ability
        self.escape_ability = escape_ability

    def is_live(self):
        if self.hunger <= 0 and self.age > self.life_time:
            self.model.soil_agent.delete_specie_on_soil(self)
            self.is_alive = False
            return False
        else:
            return True

    def new_attack_ability(self):
        if self.age <= self.married_min_age:
            attack_ability = self.age * self.alive_ability_change_per_time * self.attack_ability
        else:
            attack_ability = (self.age - self.married_min_age)**(1/2) * self.age * self.alive_ability_change_per_time * self.attack_ability
        return attack_ability

    def new_escape_ability(self):
        if self.age <= self.married_min_age:
            escape_ability = self.age * self.alive_ability_change_per_time * self.escape_ability
        else:
            escape_ability = (self.age - self.married_min_age)**(1/2) * self.age * self.alive_ability_change_per_time * self.escape_ability
        return escape_ability

    def attack(self, prey_specie_name):
        if prey_specie_name in list(self.model.soil_agent.map[self.position[0], self.position[1]][prey_specie_name].keys()):
            prey_agent = random.choice(self.model.soil_agent.map[self.position[0], self.position[1]][prey_specie_name])
            prey_escape = [True, False]
            predator_attack = [True, False]
            prey_escape_prob = [prey_agent.new_escape_ability(), 1 - prey_agent.new_escape_ability()]
            predator_attack_prob = [self.new_attack_ability(), 1 - self.new_attack_ability()]
            escape = np.random.choice(prey_escape, p = prey_escape_prob)
            attack = np.random.choice(predator_attack, p = predator_attack_prob)
            if attack and not escape:
                prey_agent.is_alive = False
                self.model.soil_agent.delete_specie_on_soil(prey_agent)
                self.hunger += self.eat_volume
                # self.model.soil_agent.map[self.position[0], self.position[1]]
                return True
            else:
                return False
        else:
            return False

    def escape(self, predator_agent):
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
            N = sum(list(map(lambda x: len(self.model.soil_agent.map[self.position[0], self.position[1]][x]), self.model.soil_agent.specie_list)))
            K = self.model.soil_agent.map[self.position[0], self.position[1]]['carry_ability']
            is_birth = self.logistic_growth_individual(N, K, self.increase_rate, self.fertility_change * (self.age - self.married_min_age))
            if is_birth:
                new_agent_id = self.model.next_id
                new_agent = TargetSpecieAgent(new_agent_id, self.model)
                new_agent.position = self.position
                new_agent.parents = [self.unique_id, self.partner]
                new_agent.parents_count = 2
                new_agent.age = 0
                new_agent.birthday = self.model.schedule.time
                self.kids_count += 1
                self.kids.append(new_agent_id)
                # partner_agent = self.find_agent_by_id(self.partner_id)
                partner_agent = self.model.specie_all_agents[self.specie][self.partner]
                partner_agent.kids_count += 1
                partner_agent.kids.append(new_agent_id)
                self.model.soil_agent.add_specie_on_soil(self.specie, new_agent, self.position)
                self.model.new_agents_dict[self.specie] += 1
                self.model.schedule.add(new_agent)

    def move(self, map):
        self.position = self.random_walk(self.move_speed_mean, self.move_speed_std, self.position, map)
        return self.position

    def growth(self):
        self.age += 1
        self.hunger -= 2

class TargetSpecieAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'target_specie'
        Animal.__init__(self, self.specie_name, 1, 1, 0.1, 100, 20, -0.001, 0.001)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def step(self):
        self.move(self.model.soil_agent.map)
        # self.attack('prey')
        if self.model.soil_agent.can_eat(self, self.position, self.increase_rate):
            if 100 - self.hunger < self.eat_volume:
                self.hunger = 100
            else:
                self.hunger += self.eat_volume

        self.get_married()
        self.give_birth()
        self.is_live()
        self.growth()

# 捕猎者
class PredatorAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'predator'
        Animal.__init__(self, self.specie_name, 1, 1, 0.1, 100, 20, -0.001, 0.001)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def step(self):
        self.move(self.model.soil_agent.map)
        self.attack('target_specie')
        self.get_married()
        self.give_birth()
        self.is_live()
        self.growth()

# 猎物
class PreyAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'prey'
        Animal.__init__(self, self.specie_name, 1, 1, 0.1, 100, 20, -0.001, 0.001)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def step(self):
        self.move(self.model.soil_agent.map)
        if self.model.soil_agent.can_eat(self, self.position, self.increase_rate):
            if 100 - self.hunger < self.eat_volume:
                self.hunger = 100
            else:
                self.hunger += self.eat_volume
        self.get_married()
        self.give_birth()
        self.is_live()
        self.growth()

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

class SoilAgent(Agent, MathmaticsModel):
    def __init__(self, unique_id, model, specie_list, inaccessible_list, grid_size):
        super().__init__(unique_id=unique_id, model=model)
        self.cell_neighbors_occupy = 3
        MathmaticsModel.__init__(self, self.cell_neighbors_occupy)

        self.map_width = grid_size
        self.map_height = grid_size
        self.inaccessible_list = inaccessible_list
        self.map = np.empty([self.map_width, self.map_height], dtype=object)
        self.specie_list = specie_list
        self.soil_type_all = ['inaccessible', 'empty']
        self.soil_type_all.extend(self.specie_list)
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
        self.specie_amount = {}
        for specie in self.specie_list:
            self.specie_amount[specie] = 0

    def land_init(self):
        for i in self.inaccessible_list:
            x = i[0]
            y = i[1]
            if self.map[x, y]['is_empty']:
                self.map[x, y]['is_empty'] = False
                self.map[x, y]['is_inaccessible'] = True
                self.map[x, y]['main_specie'] = 'inaccessible'

    def get_valid_soil(self):
        valid_soil = []
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i, j]['is_empty']:
                    valid_soil.append((i, j))
        return valid_soil

    def update_species_amount(self):
        for i in range(self.map_width):
            for j in range(self.map_height):
                for specie in self.specie_list:
                    self.specie_amount[specie] += len(self.map[i, j][specie])

    def specie_occupy(self, specie):
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i][j]['is_empty']:
                    if self.specie_occupy_density < (len(self.map[i][j][specie])/self.specie_amount[specie]):
                        self.map[i][j]['main_specie'] = specie
                        self.map[i][j]['is_empty'] = False

    # add the specie on the soil
    def add_specie_on_soil(self, specie, specie_agent, position):
        if not self.map[position[0], position[1]]['is_inaccessible']:
            if len(self.map[position[0], position[1]][specie]) > 0 or self.map[position[0], position[1]]['is_empty']:
                if specie_agent not in self.map[position[0], position[1]][specie]:
                    self.map[position[0], position[1]][specie].append(specie_agent)

    def delete_specie_on_soil(self, specie_agent):
        specie = specie_agent.specie_name
        position = specie_agent.position
        if len(self.map[position[0], position[1]][specie]) > 0 and specie_agent in self.map[position[0], position[1]][specie]:
            self.map[position[0], position[1]][specie].remove(specie_agent)
            self.model.schedule.remove(specie_agent)
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

    def can_eat(self, specie_agent, position, increase_rate):
        N = sum(list(map(lambda x: len(self.map[position[0], position[1]][x]), self.specie_list)))
        K = self.map[position[0], position[1]]['carry_ability']
        if specie_agent.married_min_age > specie_agent.age:
            return self.logistic_growth_individual(N, K, increase_rate, 1)
        else:
            return self.logistic_growth_individual(N, K, increase_rate, specie_agent.fertility_change * (specie_agent.age - specie_agent.married_min_age))

    def step(self):
        self.update_species_amount()
        for specie in list(self.specie_list):
            self.specie_occupy(specie)
        self.change_soil_carry_ability()

class EnvModel(Model):
    def __init__(self, specie_dict, inaccessible_list, grid_size):
        self.specie_dict = specie_dict
        self.schedule = mesa.time.SimultaneousActivation(self)
        soil_unique_id = self.next_id
        self.soil_agent = SoilAgent(soil_unique_id, self, list(self.specie_dict.keys()), inaccessible_list, grid_size)
        self.soil_agent.land_init()
        self.schedule.add(self.soil_agent)
        climate_unique_id = self.next_id
        self.climate_agent = ClimateAgent(climate_unique_id, self, 'tropical rain forest climate')
        self.climate_agent.climate_style_init()
        self.schedule.add(self.climate_agent)
        self.new_agents_dict = {}
        self.specie_all_agents = {}

        for specie in self.specie_dict.keys():
            self.new_agents_dict[specie] = 0

        # self.water_agents = WaterAgent(self.next_id, self)

        for specie in self.specie_dict.keys():
            self.specie_all_agents[specie] = {}
            self.specie_dict[specie]['population'] = int(self.specie_dict[specie]['population'])
            for i in range(self.specie_dict[specie]['population']):
                new_target_id = self.next_id
                if specie == 'target_specie':
                    target_specie = TargetSpecieAgent(new_target_id, self)
                elif specie == 'predator':
                    target_specie = PredatorAgent(new_target_id, self)
                elif specie == 'prey':
                    target_specie = PreyAgent(new_target_id, self)
                # target_specie = TargetSpecieAgent(new_target_id, self)
                target_specie.position = random.choice(self.soil_agent.get_valid_soil())
                self.soil_agent.add_specie_on_soil(specie, target_specie, target_specie.position)
                self.schedule.add(target_specie)
                self.specie_all_agents[specie][new_target_id] = target_specie
        # self.datacollector = mesa.DataCollector(
        #     model_reporters={
        #         "population": lambda m: len(m.fish_agents),
        #         "Fishers": lambda m: m.num_fishers,
        #         "Bank Money": lambda m: m.bank_agent.money
        #     }
        # )

    def step(self):
        self.schedule.step()

        # # 在下一个时间步骤中添加新代理
        # for new_agent in self.target_specie_new_agents:
        #     self.schedule.add(new_agent)

        for specie in self.specie_dict.keys():
            self.specie_dict[specie]['population'] += self.new_agents_dict[specie]
            self.new_agents_dict[specie] = 0
        # self.datacollector.collect(self)


