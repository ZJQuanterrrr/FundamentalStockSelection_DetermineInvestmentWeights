# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:22:58 2023

@author: C.Z.J
"""
import pandas as pd

df = pd.read_csv("Top20.csv")
df = df.set_index(df.columns[0])

date = df.index

# 计算夏普*
mean_row = df.mean(axis=0)
std_row = df.std(axis=0)
sharp_row = mean_row/std_row

# 消除量纲
sum_sh = sum(sharp_row)
sharp_row = sharp_row/sum_sh

# 计算相关系数矩阵
corr_matrix = df.corr()

# 计算各股票相关系数总/全部股票相关系数总
row_sums = corr_matrix.sum(axis=0)
sum_corr = sum(row_sums)
row_sums = row_sums/sum_corr

# 打分！
score = 100*sharp_row + 10*(1-row_sums)

# 将分数添加到数据帧的末尾
df = df.append(score, ignore_index=True)

# 从数据帧中选择最后一行数据
last_row = df.iloc[-1]

# 从最后一行数据中选择值最大的前5个元素的索引
top_5_cols = last_row.nlargest(5).index

# 从数据帧中选择最后一行数据中最大的前5列数据
new_df = df.loc[:, top_5_cols]

# 删除最后一行数据
new_df = new_df.drop(new_df.index[-1])

# 把日期重新输入
new_df.index = date

# 保存至csv
new_df.to_csv('Selected_5.csv', encoding="utf-8")


