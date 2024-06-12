import mesa
import numpy as np
import pandas as pd
from mesa import Agent, Model
from PySide6.QtCore import Slot
from public.mathmatics_model import MathmaticsModel
import random
from collections import Counter

class Animal(MathmaticsModel):
    def __init__(self, specie):
        self.classification = 'animal'
        self.specie = specie
        MathmaticsModel.__init__(self)

        rownames = self.model.widget_obj.specie_table_rowname
        params = {}
        for column in range(self.model.widget_obj.species_table.columnCount()):
            for row in range(self.model.widget_obj.species_table.rowCount()):
                params[rownames[row]] = self.model.widget_obj.species_table.item(row, column).text()
            if params['species'] == self.specie:
                break

        self.age = random.randint(0, 10)
        self.gender = random.choice(['male', 'female'])
        self.kids = []
        self.kids_count = 0
        self.parents = []
        self.parents_count = 0
        self.partner = None
        self.position = [-1, -1]
        self.hunger = 100
        self.move_speed_mean = float(params[self.model.widget_obj.move_speed_mean.objectName()])
        self.move_speed_std = float(params[self.model.widget_obj.move_speed_std.objectName()])
        self.is_married = False
        self.increase_rate = float(params[self.model.widget_obj.growth_rate.objectName()])
        self.life_time = float(params[self.model.widget_obj.natural_life_span.objectName()])
        self.is_alive = True
        self.married_min_age = float(params[self.model.widget_obj.marriage_age.objectName()])
        self.fertility_change = float(params[self.model.widget_obj.fecundity_attenuation.objectName()])
        self.alive_ability_change_per_time = float(params[self.model.widget_obj.alive_ability_change_per_time.objectName()])
        self.attack_ability = float(params[self.model.widget_obj.attack_ability.objectName()])
        self.escape_ability = float(params[self.model.widget_obj.escape_ability.objectName()])
        self.hunger_increment = float(params[self.model.widget_obj.hunger_increment.objectName()])

        self.age_increment = float(params[self.model.widget_obj.age_increment.objectName()])
        self.monogamous = params[self.model.widget_obj.monogamous.objectName()]

        self.cell_neighbors_occupy = float(params[self.model.widget_obj.cell_neighbors_occupy.objectName()])
        self.is_cellular = params[self.model.widget_obj.is_cellular.objectName()]

    def is_live(self):
        if self.hunger <= 0 or self.age > self.life_time:
            self.model.soil_agent.delete_specie_on_soil(self, remove_schedule = False)
            self.is_alive = False
            return False
        else:
            return True

    def new_attack_ability(self):
        if self.age <= self.married_min_age:
            attack_ability = self.age * self.alive_ability_change_per_time * self.attack_ability
        else:
            attack_ability = (self.age - self.married_min_age)**(1/2) * self.age * self.alive_ability_change_per_time * self.attack_ability
        if attack_ability < 0:
            attack_ability = 0
        if attack_ability > 1:
            attack_ability = 1
        return attack_ability

    def new_escape_ability(self):
        if self.age <= self.married_min_age:
            escape_ability = self.age * self.alive_ability_change_per_time * self.escape_ability
        else:
            escape_ability = (self.age - self.married_min_age)**(1/2) * self.age * self.alive_ability_change_per_time * self.escape_ability
        if escape_ability < 0:
            escape_ability = 0
        if escape_ability > 1:
            escape_ability = 1
        return escape_ability

    def attack(self, prey_specie_name):
        if len(self.model.soil_agent.map[self.position[0], self.position[1]][prey_specie_name]) > 0:
            prey_agent = random.choice(self.model.soil_agent.map[self.position[0], self.position[1]][prey_specie_name])
            prey_escape = [True, False]
            predator_attack = [True, False]
            prey_escape_prob = [prey_agent.new_escape_ability(), 1 - prey_agent.new_escape_ability()]
            predator_attack_prob = [self.new_attack_ability(), 1 - self.new_attack_ability()]
            escape = np.random.choice(prey_escape, p = prey_escape_prob)
            attack = np.random.choice(predator_attack, p = predator_attack_prob)
            if attack and not escape:
                prey_agent.is_alive = False
                self.model.soil_agent.delete_specie_on_soil(prey_agent, remove_schedule = False)
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
        if self.age > self.married_min_age and self.is_alive and self.gender != partner_gender:
            if self.monogamous:
                if not self.is_married:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def get_married(self):
        if not self.is_married and self.age > self.married_min_age:
            married_candidate = self.model.soil_agent.map[self.position[0], self.position[1]][self.specie]
            for partner_agent in married_candidate:
                if self.can_married(partner_agent.gender) and partner_agent.can_married(self.gender):
                    self.partner = partner_agent
                    self.is_married = True
                    partner_agent.partner = self.partner
                    partner_agent.is_married = True
                    break

    def give_birth(self):
        if self.is_married:
            N = sum(list(map(lambda x: len(self.model.soil_agent.map[self.position[0], self.position[1]][x]), self.model.soil_agent.specie_list)))
            K = self.model.soil_agent.map[self.position[0], self.position[1]]['carry_ability']
            is_birth = self.logistic_growth_individual(N, K, self.increase_rate, self.fertility_change * (self.age - self.married_min_age))
            if is_birth:
                new_agent_id = self.model.get_next_id()
                new_agent = self.new_agent_obj(new_agent_id, self.model)
                new_agent.position = self.position
                new_agent.parents = [self, self.partner]
                new_agent.parents_count = 2
                new_agent.age = 0
                new_agent.birthday = self.model.schedule.time
                self.kids_count += 1
                self.kids.append(new_agent_id)
                # partner_agent = self.find_agent_by_id(self.partner_id)
                # partner_agent = self.model.specie_all_agents[self.specie][self.partner.unique_id]
                partner_agent = self.partner
                partner_agent.kids_count += 1
                partner_agent.kids.append(new_agent_id)
                self.model.soil_agent.add_specie_on_soil(new_agent, self.position)
                self.model.new_agents_dict[self.specie] += 1

    def move(self, map):
        self.model.soil_agent.delete_specie_on_soil(self)
        self.position = self.random_walk(self.specie, self.move_speed_mean, self.move_speed_std, self.position, map, self.cell_neighbors_occupy, self.is_cellular)
        self.model.soil_agent.add_specie_on_soil(self, self.position)
        return self.position

    def growth(self):
        self.age += self.age_increment
        self.hunger -= self.hunger_increment

class TargetSpecieAgent(Agent, Animal):
    def __init__(self, unique_id, model, is_single = True):
        super().__init__(unique_id, model)
        self.specie_name = 'target_specie'
        Animal.__init__(self, self.specie_name)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time
        self.is_single = is_single

    def new_agent_obj(self, id, model):
        return TargetSpecieAgent(id, model, self.is_single)

    def step(self):
        if self.is_alive:
            self.move(self.model.soil_agent.map)
            # self.attack('prey')
            if self.is_single:
                if self.model.soil_agent.can_eat(self, self.position, self.increase_rate):
                    if 100 - self.hunger < self.eat_volume:
                        self.hunger = 100
                    else:
                        self.hunger += self.eat_volume
            else:
                if self.attack('prey'):
                    if 100 - self.hunger < self.eat_volume:
                        self.hunger = 100
                    else:
                        self.hunger += self.eat_volume

            self.get_married()
            self.give_birth()
            self.growth()
            self.is_live()

# 捕猎者
class PredatorAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'predator'
        Animal.__init__(self, self.specie_name)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def new_agent_obj(self, id, model):
        return PredatorAgent(id, model)

    def step(self):
        if self.is_alive:
            self.move(self.model.soil_agent.map)
            # self.attack('prey')
            if self.attack('target_specie'):
                if 100 - self.hunger < self.eat_volume:
                    self.hunger = 100
                else:
                    self.hunger += self.eat_volume

            self.get_married()
            self.give_birth()
            self.growth()
            self.is_live()

# 猎物
class PreyAgent(Agent, Animal):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.specie_name = 'prey'
        Animal.__init__(self, self.specie_name)
        self.eat_volume = 10  # the volume of food that the agent can eat at one time

    def new_agent_obj(self, id, model):
        return PreyAgent(id, model)

    def step(self):
        if self.is_alive:
            self.move(self.model.soil_agent.map)
            # self.attack('prey')
            if self.model.soil_agent.can_eat(self, self.position, self.increase_rate):
                if 100 - self.hunger < self.eat_volume:
                    self.hunger = 100
                else:
                    self.hunger += self.eat_volume

            self.get_married()
            self.give_birth()
            self.growth()
            self.is_live()

class ClimateAgent(Agent):
    # 季风气候、热带雨林气候、热带草原气候、热带沙漠气候、热带季风气候、热带雨林气候、热带草原气候、热带沙漠气候
    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.classification = 'climate'
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
    def __init__(self, unique_id, model):
        super().__init__(unique_id=unique_id, model=model)
        MathmaticsModel.__init__(self)
        self.classification = 'soil'
        self.map_width = self.model.widget_obj.mr_grid_widget.grid_size
        self.map_height = self.model.widget_obj.mr_grid_widget.grid_size
        self.inaccessible_list = self.model.widget_obj.inaccessible_list
        self.map = np.empty([self.map_width, self.map_height], dtype=object)
        self.specie_list = list(self.model.specie_dict.keys())
        self.soil_type_all = ['inaccessible', 'empty']
        self.soil_type_all.extend(self.specie_list)
        self.specie_occupy_density = 0.2
        for i in range(self.map_width):
            for j in range(self.map_height):
                self.map[i, j] = {}
                self.map[i, j]['is_empty'] = True
                self.map[i, j]['is_inaccessible'] = False
                self.map[i, j]['main_specie'] = 'empty'
                self.map[i, j]['carry_ability'] = random.normalvariate(float(self.model.widget_obj.carrying_capacity.text()), float(self.model.widget_obj.carrying_cap_std.text()))
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

    def get_invalid_soil(self):
        invalid_soil = []
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i, j]['is_inaccessible']:
                    invalid_soil.append((i, j))
        return invalid_soil

    def update_species_amount(self):
        for specie in self.specie_list:
            self.specie_amount[specie] = 0
        for i in range(self.map_width):
            for j in range(self.map_height):
                for specie in self.specie_list:
                    self.specie_amount[specie] += len(self.map[i, j][specie])

    def specie_occupy(self, specie):
        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map[i][j]['is_empty'] and not self.map[i][j]['is_inaccessible']:
                    if self.specie_occupy_density < (len(self.map[i][j][specie])/self.specie_amount[specie]):
                        self.map[i][j]['main_specie'] = specie
                        self.map[i][j]['is_empty'] = False

    # add the specie on the soil
    def add_specie_on_soil(self, specie_agent, position):
        specie = specie_agent.specie
        if not self.map[position[0], position[1]]['is_inaccessible']:
            if len(self.map[position[0], position[1]][specie]) > 0 or self.map[position[0], position[1]]['is_empty']:
                if specie_agent not in self.map[position[0], position[1]][specie]:
                    self.map[position[0], position[1]][specie].append(specie_agent)
                    self.model.schedule.add(specie_agent)

    def delete_specie_on_soil(self, specie_agent, remove_schedule = True):
        specie = specie_agent.specie_name
        position = specie_agent.position
        if len(self.map[position[0], position[1]][specie]) > 0 and specie_agent in self.map[position[0], position[1]][specie]:
            self.map[position[0], position[1]][specie].remove(specie_agent)
            if remove_schedule:
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

    def can_eat(self, specie_agent, position, increase_rate, is_eat = True):
        N = sum(list(map(lambda x: len(self.map[position[0], position[1]][x]), self.specie_list)))
        K = self.map[position[0], position[1]]['carry_ability']
        if specie_agent.married_min_age > specie_agent.age:
            return self.logistic_growth_individual(N, K, increase_rate, 1, is_eat)
        else:
            return self.logistic_growth_individual(N, K, increase_rate, specie_agent.fertility_change * (specie_agent.age - specie_agent.married_min_age), is_eat)

    def step(self):
        self.update_species_amount()
        # for specie in list(self.specie_list):
        #     self.specie_occupy(specie)
        self.change_soil_carry_ability()



class EnvModel(Model):
    def __init__(self, widget_obj, is_single = True):
        self.reset_next_id()
        self.widget_obj = widget_obj
        self.specie_dict = self.widget_obj.specie_dict
        self.schedule = mesa.time.SimultaneousActivation(self)
        soil_unique_id = self.get_next_id()
        self.soil_agent = SoilAgent(soil_unique_id, self)

        self.soil_agent.land_init()
        self.schedule.add(self.soil_agent)
        climate_unique_id = self.get_next_id()
        self.climate_agent = ClimateAgent(climate_unique_id, self, 'tropical rain forest climate')
        self.climate_agent.climate_style_init()
        self.schedule.add(self.climate_agent)
        self.new_agents_dict = {}
        self.specie_all_agents = {}

        for specie in self.specie_dict.keys():
            self.new_agents_dict[specie] = 0

        # self.water_agents = WaterAgent(self.next_id, self)

        self.statistics = {}
        for specie in self.specie_dict.keys():
            self.specie_all_agents[specie] = {}
            self.specie_dict[specie]['population'] = int(self.specie_dict[specie]['population'])
            for _ in range(self.specie_dict[specie]['population']):
                new_target_id = self.get_next_id()
                if specie == 'target_specie':
                    target_specie_agent = TargetSpecieAgent(new_target_id, self, is_single)
                    target_specie_agent.position = random.choice(self.soil_agent.get_valid_soil())
                    self.soil_agent.add_specie_on_soil(target_specie_agent, target_specie_agent.position)
                    self.specie_all_agents[specie][new_target_id] = target_specie_agent
                    if 'target_specie' not in list(self.statistics.keys()):
                        self.statistics['target_specie'] = TargetSpecieAgent
                elif specie == 'predator':
                    predator_agent = PredatorAgent(new_target_id, self)
                    predator_agent.position = random.choice(self.soil_agent.get_valid_soil())
                    self.soil_agent.add_specie_on_soil(predator_agent, predator_agent.position)
                    self.specie_all_agents[specie][new_target_id] = predator_agent
                    if 'predator' not in list(self.statistics.keys()):
                        self.statistics['predator'] = PredatorAgent
                elif specie == 'prey':
                    prey_agent = PreyAgent(new_target_id, self)
                    prey_agent.position = random.choice(self.soil_agent.get_valid_soil())
                    self.soil_agent.add_specie_on_soil(prey_agent, prey_agent.position)
                    self.specie_all_agents[specie][new_target_id] = prey_agent
                    if 'prey' not in list(self.statistics.keys()):
                        self.statistics['prey'] = PreyAgent
        # self.datacollector = mesa.DataCollector(
        #     model_reporters={
        #         "population": lambda m: len(m.fish_agents),
        #         "Fishers": lambda m: m.num_fishers,
        #         "Bank Money": lambda m: m.bank_agent.money
        #     }
        # )


    def get_next_id(self):
        self.next_id += 1
        return self.next_id

    def reset_next_id(self):
        self.next_id = 0

    def step(self):
        self.schedule.step()

        # # 在下一个时间步骤中添加新代理
        # for new_agent in self.target_specie_new_agents:
        #     self.schedule.add(new_agent)

        # for specie in self.specie_dict.keys():
        #     self.specie_dict[specie]['population'] += len(self.specie)
        #     self.new_agents_dict[specie] = 0
        for specie in self.specie_dict.keys():
            self.specie_dict[specie]['population'] = 0

        all_species_name = list(self.statistics.keys())
        for agent in self.schedule.agents:
            for specie_name in all_species_name:
                if isinstance(agent, self.statistics[specie_name]) and agent.is_alive:
                    self.specie_dict[specie_name]['population'] += 1


        # self.datacollector.collect(self)

'''
class EnvModel(Model):
    def __init__(self, specie_dict, inaccessible_list, grid_size, carry_ability_mean):
        self.specie_dict = specie_dict
        self.schedule = mesa.time.SimultaneousActivation(self)
        soil_unique_id = self.next_id
        self.soil_agent = SoilAgent(soil_unique_id, self, list(self.specie_dict.keys()), inaccessible_list, grid_size, carry_ability_mean, float(self.carrying_cap_std.text()))
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
'''




