# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 09:39:43 2023

@author: C.Z.J
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use('seaborn')

df = pd.read_csv("Selected_5.csv")
df = df.set_index(df.columns[0])

# 数据列的统计特征
# 计算各列的平均值
means = df.mean()
print("平均值:\n", means)

# 计算各列的标准差
stds = df.std()
print("标准差:\n", stds)

# 计算各列的偏度
skews = df.skew()
print("偏度:\n", skews)

# 计算各列的峰度
kurts = df.kurtosis()
print("峰度:\n", kurts)

# df_index = pd.read_excel("index.xlsx")
# df_index = df_index.set_index(df_index.columns[0])

# returns = df_index.pct_change().dropna()

# returns.to_csv('index_re.csv', encoding="utf-8")

# 绘图
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(8, 6))
# 在第一行第一列的子图中绘制折线图
x = df.index
y = df[df.columns[0]]
axs[0, 0].plot(x, y)
axs[0, 0].set_title('603688.SH')

# 在第一行第二列的子图中绘制折线图
x = df.index
y = df[df.columns[1]]
axs[0, 1].plot(x, y)
axs[0, 1].set_title('000733.SZ')

# 在第二行第一列的子图中绘制折线图
x = df.index
y = df[df.columns[2]]
axs[1, 0].plot(x, y)
axs[1, 0].set_title('002865.SZ')

# 在第二行第二列的子图中绘制折线图
x = df.index
y = df[df.columns[3]]
axs[1, 1].plot(x, y)
axs[1, 1].set_title('603605.SH')

# 在第二行第二列的子图中绘制折线图
x = df.index
y = df[df.columns[4]]
axs[2, 0].plot(x, y)
axs[2, 0].set_title('002487.SZ')

for ax in axs:
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

# 自动调整x轴的标签角度
fig.autofmt_xdate()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()




