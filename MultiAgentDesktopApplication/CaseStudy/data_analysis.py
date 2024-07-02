import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('changes-uk-butterfly.csv')
data = data[data['Entity'] == 'All UK resident species']

data['Entity']
data['Year']
data['butterfly_population_smoothed_index']

plt.plot(data['Year'], data['butterfly_population_unsmoothed_index'], marker='o', label='All UK resident species')
# 添加图例
plt.legend()

# 显示网格
plt.grid(True, linestyle='--', alpha=0.7)

# 显示图表
plt.show()
