# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 09:59:48 2023

@author: C.Z.J
"""
import pandas as pd
import numpy as np
from cvxopt import matrix, solvers
import cvxopt
import matplotlib.pyplot as plt
import time

# compute the time
start = time.time()

plt.style.use('seaborn')

# 从CSV文件中加载股票数据
stock_data = pd.read_csv('Selected_5.csv')

# 设置日期为索引
stock_data = stock_data.set_index(stock_data.columns[0])

# 计算股票收益率并根据此数据计算投资组合的期望收益率和协方差矩阵
# returns = stock_data.pct_change().dropna()
mean_returns = np.array(stock_data.mean())
cov_matrix = np.array(stock_data.cov())

# 定义投资组合优化问题的变量和参数
n = len(mean_returns)
P = matrix(cov_matrix)
q = matrix(np.zeros((n, 1)))
G = cvxopt.matrix(np.vstack((-np.eye(n), np.eye(n))))
# G = matrix(np.vstack((-np.eye(n), np.eye(n))))
h = cvxopt.matrix(np.vstack((np.zeros((n,1)), np.ones((n,1)))))
# h = matrix(np.vstack((eps*np.zeros(n), np.ones(n))).reshape(-1, 1))
A = matrix(np.vstack((mean_returns, np.ones(n))))
##下一行可改
b = matrix(np.array([0.01, 1.0]))

# 定义优化问题的约束条件
solvers.options['show_progress'] = False
weights_list = []
returns_list = []
risk_list = []

# 下一行可改
for frontier_y in np.linspace(0.0, 0.0024, 10000):
    constraints = [G, h, A, matrix(np.array([frontier_y, 1.0]))]
    sol = solvers.qp(P, q, *constraints)
    weights = np.array(sol['x']).flatten()
    if np.dot(weights, mean_returns) <= 0.0025:
        if np.dot(weights, mean_returns) >= 0.0000:
            returns_list.append(np.dot(weights, mean_returns))
            risk_list.append(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))
            weights_list.append(weights)
            
    # returns_list.append(np.dot(weights, mean_returns))
    # risk_list.append(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))
    # weights_list.append(weights)

# 使用Matplotlib绘制投资组合的散点图和有效前沿曲线
plt.figure(figsize=(10, 6))
# plt.scatter(risk_list, returns_list)
plt.scatter(risk_list, returns_list, c=np.array(returns_list)/np.array(risk_list), cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Expected Return')
plt.title('Markowitz Efficient Frontier')
# plt.plot(risk_list, returns_list, 'r--')
plt.show()

# 输出时间
end = time.time()
print("Running time: %s Seconds"%(end - start))

