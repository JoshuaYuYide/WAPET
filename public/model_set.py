from mesa import Agent, Model
from mesa.time import RandomActivation


# 贫穷地区的模型
class PoorModel(Model):
    def __init__(self, num_fish, num_fishers):
        self.schedule = RandomActivation(self)

# 富有地区的模型
class RichModel(Model):
    def __init__(self, num_fish, num_fishers):
        self.schedule = RandomActivation(self)






