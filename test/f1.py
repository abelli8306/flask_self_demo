#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import os.path

# 教程： http://codingdict.com/article/8270

# 加载excel数据
# for windows
# d1 = pd.read_excel("C:\\Users\\markuszhu\\Desktop\\scf_tokyo_0325.xlsx", sep='\t', sheet_name="vpc_proxy")
d1 = pd.read_excel("C:\\Users\\markuszhu\\Desktop\\aaa.xlsx", sep='\t')

# for linux
# d1 = pd.read_excel("/tmp/scf_tokyo_0325.xlsx", sep='\t', sheet_name="vpc_proxy")

# 打印所有列名
print(d1.columns)

# 按某一列进行筛选，显示所有内容的前5行
s1 = d1[(d1['工单状态'] == '已结单')]
print(s1.head(5))

# 按某一列进行筛选，显示该列的前5行
# print(d1['客户代表'].head(5))

# 按 客户代表 进行分组，统计其工单数量
# s2 = d1.groupby(['客户代表'])['工单ID'].count()

# 按 客户代表、工单来源 进行分组，统计其工单数量
# s2 = d1.groupby(['客户代表', '工单来源'])['工单ID'].count()
# print(s2)

# 新增1列MM，使用  经手人数 - 催单次数 得到
# d1['MM'] = d1[' 经手人数'] - d1['催单次数']
# print(d1.to_csv('111.csv'))  ##保存
# print(d1)

# 按 客户代表 进行分组，统计其工单平均值
# s3 = d1.groupby(['客户代表'])['工单ID'].mean()
# print(s3)
