# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:05:28 2023

@author: C.Z.J
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# 读取收益率数据
returns = pd.read_csv('Selected_5.csv')

# 计算均值和协方差矩阵
mu = returns.mean()
cov = returns.cov()

# 设置参数
rf = 0.02 # 无风险利率
tau = 0.01 # 调整系数
delta = 2.5 # 风险厌恶系数
q = np.array([0.01, 0.005, -0.01, 0.02, -0.005]) # 观点
p = np.array([[1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1]]) # 观点矩阵

# 计算均值和协方差矩阵的后验分布
omega = np.dot(np.dot(p, cov), p.T) * tau
pi = delta * np.dot(np.dot(cov, p.T), np.linalg.inv(omega + np.dot(np.dot(p, cov), p.T)))
mu_bl = mu + np.dot(np.dot(np.dot(cov, p.T), np.linalg.inv(omega + np.dot(np.dot(p, cov), p.T))), (q - np.dot(p, mu)))
cov_bl = cov + np.dot(np.dot(np.dot(cov, p.T), np.linalg.inv(omega + np.dot(np.dot(p, cov), p.T))), np.dot(np.dot(cov, p.T).T, cov))

# 定义目标函数
n = len(mu)
def obj(w):
    return -np.dot(w, mu_bl) + delta/2 * np.dot(np.dot(w, cov_bl), w)

# 设置约束条件
cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}] # 权重之和为1
bounds = [(0, 1) for i in range(n)] # 权重在[0, 1]之间

# 求解最优资产组合配比
res = minimize(obj, n*[1/n], bounds=bounds, constraints=cons)
w_bl = res.x

# 输出最优资产组合配比和对应的预期收益率和方差
mu_opt = np.dot(w_bl, mu_bl)
var_opt = np.dot(np.dot(w_bl, cov_bl), w_bl)
print('最优资产组合配比:', w_bl)
print('预期收益率:', mu_opt)
print('方差:', var_opt)