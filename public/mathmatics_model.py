import math

class SpeciesModel:
    def __init__(self, name, population, growth_rate):
        self.name = name
        self.population = population
        self.growth_rate = growth_rate

    def predict_population(self, years):
        return self.population * math.exp(self.growth_rate * years)










