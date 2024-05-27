import math
from scipy.integrate import odeint
import numpy as np
import random
from scipy.stats import norm

class MathmaticsModel:
    def __init__(self, cell_neighbors_occupy):
        self.cell_neighbors_occupy = cell_neighbors_occupy

    def LefkovitchMatrix(self, years):
        # 定义阶段的生存率和转换概率
        s1, s2, s3, s4 = 0.2, 0.5, 0.8, 0.9  # 生存率
        g1, g2, g3 = 0.1, 0.3, 0.5  # 从一个阶段到另一个阶段的转换概率
        f1, f2, f3 = 0, 10, 50  # 繁殖率

        # 构建Lefkovitch矩阵
        A = np.array([
            [s1, f1, f2, f3],  # 幼年期的生存率和不同繁殖阶段的贡献
            [g1, s2, 0, 0],  # 亚成年期的进度和生存率
            [0, g2, s3, 0],  # 初成年期的进度和生存率
            [0, 0, g3, s4]  # 成年期的进度和生存率
        ])

        # 计算矩阵的特征值
        eigenvalues, _ = np.linalg.eig(A)

        # 获取最大特征值（种群增长率）
        lambda1 = max(eigenvalues)

        print("Lefkovitch 矩阵:")
        print(A)
        print("\n最大特征值（种群增长率 lambda）: {:.2f}".format(lambda1))

        # 判断种群趋势
        if lambda1 > 1:
            print("种群预期会增长。")
        elif lambda1 < 1:
            print("种群预期会衰减。")
        else:
            print("种群大小保持稳定。")

    def allee_effect_model(self, N, t, r, K, A):
        dNdt = r * N * ((N / K) - 1) * ((N / A) - 1)
        return dNdt

    def walk_model(self, N, t, r, K):
        dNdt = r * N * (1 - (N / K))
        return dNdt

    def logistic_growth_model(self, N, t, r, K):
        dNdt = r * N * (1 - (N / K))
        return dNdt

    def logistic_growth_model_solution(self, r, K, N0, t):
        solution = odeint(self.logistic_growth, N0, t, args=(r, K))
        return solution

    def logistic_solution_discrete(self, N0, r, K, t):
        return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

    def logistic_growth_individual(self, N, K, r, change_rate):
        """
        个体层面的连续时间Logistic增长模型。
        :param N: the population size
        :param K: the carrying capacity
        :param r: the intrinsic growth rate
        :return: the change of the individual growth and eating
        """
        # 第一次随机：环境调控，决定是否有机会繁殖
        if random.random() < (1 - N / K):
            # 第二次随机：繁殖成功率
            if random.random() < (1 + change_rate) * r:
                return True
            else:
                return False
        else:
            return False

    def allee_effect_individual(self, r, K, A, N0, t):
        """
        个体层面的离散时间Allen模型模拟。
        参数:
        r : float
            内在增长率。
        K : int
            环境承载力。
        alpha : float
            种群密度负面影响系数。
        N0 : int
            初始种群大小。
        t : int
            模拟时间节点。
        返回:
        N : list
            时间序列中的种群大小。
        """
        current_population = N0
        new_population = 0
        for _ in range(current_population):
            survival_probability = (current_population/ K - 1) * (current_population/ A - 1)
            if np.random.rand() < survival_probability:
                # 个体存活并产生一个后代
                return True
            else:
                return False

    # species cellular automata model
    def cellular_automata(self, map, specie):
        candidate_position = []
        for i in range(len(map.map_width)):
            for j in range(len(map.map_height)):
                if map[i][j] == 'empty':
                    specie_neighbors_count = 0
                    for x in range(i - 1, i + 2):
                        for y in range(j - 1, j + 2):
                            if map[x][y] == specie:
                                specie_neighbors_count += 1
                    if specie_neighbors_count >= self.cell_neighbors_occupy:
                        candidate_position.append((i, j))
        return candidate_position

    # random walk model for species
    def random_walk(self, speed_mean, speed_std, start_point, map):
        speed = self.speed_gaussian(speed_mean, speed_std)
        position = self.position_transfer(speed, map, start_point)
        return position

    def speed_gaussian(self, mean = 1, std = 1):
        return norm.rvs(loc=mean, scale=std, size=1)

    def position_transfer(self, speed, map, start):
        candidate_position = []
        width, height = map.shape
        width_min = math.ceil(start[0] - speed)
        width_max = math.floor(start[0] + speed)
        height_min = math.ceil(start[1] - speed)
        height_max = math.floor(start[1] + speed)
        if width_min > width - 1:
            width_min = width - 1
        elif width_max < 0:
            width_max = 0
        if width_max > width - 1:
            width_max = width - 1
        elif width_min < 0:
            width_min = 0
        if height_min > height - 1:
            height_min = height - 1
        elif height_max < 0:
            height_max = 0
        if height_max > height - 1:
            height_max = height - 1
        elif height_min < 0:
            height_min = 0

        for i in range(width_min, width_max):
            for j in range(height_min, height_max):
                if not map[i, j]['is_inaccessible']:
                    candidate_position.append([i, j])
        if len(candidate_position) == 0:
            return start
        else:
            return random.choice(candidate_position)
