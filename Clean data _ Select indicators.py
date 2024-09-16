# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:54:38 2023

@author: C.Z.J
"""

import pandas as pd
import gc
import time

### compute the time
start = time.time()

df = pd.read_excel("全部主板ee.xlsx")
df = df.drop(index=[0, 1])
df = df.set_index(df.columns[0])
df.index = df.index.strftime("%Y-%m-%d")

# 删除包含空值的所有列并返回被删除的列的列名
dropped_cols = list(df.columns[df.isna().any()])
df = df.dropna(axis=1, how='any')

df1 = pd.read_excel("双创板ee.xlsx")
df1 = df1.drop(index=[0, 1])
df1 = df1.set_index(df1.columns[0])
df1.index = df1.index.strftime("%Y-%m-%d")

# 删除包含空值的所有列并返回被删除的列的列名
dropped_cols1 = list(df1.columns[df1.isna().any()])
df1 = df1.dropna(axis=1, how='any')

# 将两个表格横向拼接
df_concat = pd.concat([df, df1], axis=1)
returns = df_concat.pct_change().dropna()

date = returns.index

# 删除数据帧并执行垃圾回收
del df, df1, df_concat
gc.collect()

# 计算各列的均值和标准差和夏普
mean_row = returns.mean(axis=0)
std_row = returns.std(axis=0)
sharp_row = mean_row/std_row

# 将夏普添加到数据帧的末尾
returns = returns.append(sharp_row, ignore_index=True)

# 从数据帧中选择最后一行数据
last_row = returns.iloc[-1]

# 从最后一行数据中选择值最大的前20个元素的索引
top_20_cols = last_row.nlargest(20).index

# 从数据帧中选择最后一行数据中最大的前20列数据
new_df = returns.loc[:, top_20_cols]

# 删除最后一行数据
new_df = new_df.drop(new_df.index[-1])

# 把日期重新输入
new_df.index = date

# 保存至csv
new_df.to_csv('Top20.csv', encoding="utf-8")

end = time.time()
print("Running time: %s Seconds"%(end - start))




