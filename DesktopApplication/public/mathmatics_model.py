import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import random

class MathmaticsModel:
    def __init__(self):
        pass

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

    def logistic_growth_model(self, N, t, r, K):
        dNdt = r * N * (1 - (N / K))
        return dNdt

    def logistic_growth_model_solution(self, r, K, N0, t):
        solution = odeint(self.logistic_growth, N0, t, args=(r, K))
        return solution

    def logistic_solution_discrete(self, N0, r, K, t):
        return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

    def logistic_growth_individual(self, N, K, r):
        # 第一次随机：环境调控，决定是否有机会繁殖
        if random.random() < (1 - N / K):
            # 第二次随机：繁殖成功率
            if random.random() < r:
                return True
            else:
                return False
        else:
            return False
#
# a = MathmaticsModel()
# # 参数
# r = 1.0  # 最大固有增长率
# K = 1000  # 环境承载力
# A = 50    # Allee阈值
#
# # 时间轴
# t = np.linspace(0, 50, 1000)  # 从0到50年，共1000个时间点
#
# # 不同的初始种群规模
# N0_below_allee = 10   # 初始种群规模低于Allee阈值
# N0_above_allee = 100  # 初始种群规模高于Allee阈值
#
# # 种群模拟
# sol_below_allee = odeint(allee_effect_model, N0_below_allee, t, args=(r, K, A))
# sol_above_allee = odeint(allee_effect_model, N0_above_allee, t, args=(r, K, A))
#
# # 绘图
# plt.figure(figsize=(10, 6))
# plt.plot(t, sol_below_allee, label='Below Allee Threshold (N0={})'.format(N0_below_allee))
# plt.plot(t, sol_above_allee, label='Above Allee Threshold (N0={})'.format(N0_above_allee))
# plt.axhline(y=A, color='r', linestyle='--', label='Allee Threshold (A={})'.format(A))
# plt.title('Allee Effect Model')
# plt.xlabel('Time')
# plt.ylabel('Population Size')
# plt.legend()
# plt.show()



