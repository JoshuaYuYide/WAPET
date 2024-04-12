from mesa import Agent, Model
from mesa.time import RandomActivation
import mesa
import matplotlib.pyplot as plt
import seaborn as sns # Data visualization tools.
import pandas as pd

class FishAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.health = 100

    def step(self):
        self.health -= self.model.fish_death_rate
        self.model.fish_agents[self.unique_id] = self

class FisherAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = 0

    def step(self):
        available_fish_ids = list(self.model.fish_agents.keys())
        if available_fish_ids:
            fish_id = self.random.choice(available_fish_ids)
            fish_agent = self.model.fish_agents.pop(fish_id)
            self.money += self.model.fish_price
            self.model.schedule.remove(fish_agent)

        self.money -= self.model.bank_fee

class BankAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = 0

    def step(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, FisherAgent):
                self.money += self.model.bank_fee
                agent.money -= self.model.bank_fee

class FishModel(Model):
    def __init__(self, num_fish, num_fishers):
        self.schedule = RandomActivation(self)
        self.num_fish = num_fish
        self.num_fishers = num_fishers
        self.fish_death_rate = 0.1
        self.fish_price = 1
        self.bank_fee = 10
        self.fish_agents = {}  # 存储鱼代理的字典
        self.running = True

        for i in range(self.num_fish):
            fish_agent = FishAgent(i, self)
            self.schedule.add(fish_agent)

        for i in range(self.num_fishers):
            fisher_agent = FisherAgent(i + self.num_fish, self)
            self.schedule.add(fisher_agent)

        self.bank_agent = BankAgent(self.num_fish + self.num_fishers, self)
        self.schedule.add(self.bank_agent)

        self.datacollector = mesa.DataCollector(  # 创建 DataCollector 对象
            model_reporters={
                "Fish": lambda m: len(m.fish_agents),
                "Fishers": lambda m: m.num_fishers,
                "Bank Money": lambda m: m.bank_agent.money
            }
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        # print(f"Fish: {len(self.fish_agents)}")
        # print(f"Fishers: {self.num_fishers}")
        # print(f"Bank: {self.bank_agent.money}")

model = FishModel(100, 3)
for i in range(10):
    model.step()
    # 访问收集的数据
    model_data = model.datacollector.get_model_vars_dataframe()
    print(model_data)

sns.lineplot(data=model_data, x=model_data.index, y="Fish", label="Fish")
sns.lineplot(data=model_data, x=model_data.index, y="Fishers", label="Fishers")
sns.lineplot(data=model_data, x=model_data.index, y="Bank Money", label="Bank Money")
plt.xlabel("Time")
plt.ylabel("Count/Money")
plt.title("Simulation Results")
plt.legend()
plt.show()


# params = {"num_fish": range(50, 500, 50), "num_fishers": range(1, 5, 1)}
#
# results = mesa.batch_run(
#     FishModel,
#     parameters=params,
#     iterations=1,
#     max_steps=200,
#     number_processes=1,
#     data_collection_period=1,
#     display_progress=True,
# )
#
# results_df = pd.DataFrame(results)
# print(results_df.keys())













