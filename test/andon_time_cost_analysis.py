# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Description :
Author : weseey
-------------------------------------------------
Change Activity:
-------------------------------------------------
"""

__author__ = 'weseey'

import pandas as pd
import numpy as np
from openpyxl import load_workbook

# 加载excel数据
read_excel_file = "D:\\xiaoboli-WorkStudioTX\\01-腾讯云服务\\腾讯云SLA\\2020.4月二线数据 to QA-定制SLA.xlsx"
write_excel_file = "D:\\xiaoboli-WorkStudioTX\\01-腾讯云服务\\腾讯云SLA\\time_cost.xlsx"

excel_read = pd.read_excel(read_excel_file, sep='\t')
time_cost = excel_read[
    (
            excel_read['产品中心'] == '容器产品中心'
    ) & (
            excel_read['运维处理人中心(考核)'] == '技术运营中心'
    )
    ].groupby(['运维处理人(考核)']).agg(
    {
        '二线运维处理时长(折算)h': ['min', 'max', np.mean, np.count_nonzero],
        '是否转产研': 'sum'
    })

print(time_cost)
#对现有的excel 追加表格
book = load_workbook(read_excel_file)

with pd.ExcelWriter(write_excel_file) as excel_writer:
    excel_writer.book = book
    time_cost.to_excel(excel_writer, sheet_name="time_cost")
    excel_writer.save()


# # merge 测试
# left = pd.DataFrame({
#     'id': [1, 2, 3, 4, 5],
#     'Name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
#     'subject_id': ['sub1', 'sub2', 'sub4', 'sub6', 'sub5']})
# right = pd.DataFrame(
#     {'id': [1, 2, 3, 4, 5],
#      'Name': ['Billy', 'Brian', 'Bran', 'Bryce', 'Betty'],
#      'subject_id': ['sub2', 'sub4', 'sub3', 'sub6', 'sub5']})
# print(left)
# print("========================================")
# print(right)
#
# rs = pd.merge(left, right, on=['id', 'subject_id'])
# print(rs)
