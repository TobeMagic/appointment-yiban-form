#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/6 22:24
# @Author  : AI_magician
# @File    : form_service.py
# @Project : PyCharm
# @Version : 1.0,
# @Contact : 1928787583@qq.com",
# @License : (C)Copyright 2003-2023, AI_magician",
# @Function:

from datetime import datetime, timedelta
import pywebio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import pandas as pd
import logging
import csv

# 配置日志记录器
logging.basicConfig(filename='form.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 存储已预约的时间段
reserved_slots = {}
form_data = []


def save_appointment_data(data):
    df = pd.DataFrame(data)
    df.to_excel('appointment_data.xlsx', index=False)


html_code = '''
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f5f5f5;
    color: #333;
    text-align: center;
    padding: 10px;
}
</style>

<div class="">
    &copy; 2023 Power by <a href="https://blog.csdn.net/weixin_66526635?spm=1000.2115.3001.5343">AI_magician</a>. All rights reserved.
</div>
'''


def appointment_form():
    put_html(html_code)

    # 选择日期范围
    def check_date(p):  # return None when the check passes, otherwise return the error message
        date = datetime.strptime(p, '%Y-%m-%d')
        if date < datetime(year=2023, month=9, day=12) or date > datetime(year=2023, month=9, day=28):
            return '仅可选择9月12号到9月28号'

    def check_single(data):
        # 检查时间段是否已经被预约
        slot = f"{data['campus']} {data['date_range']} {data['time_step']}"  # 例： 2023-09-23
        if slot in reserved_slots:
            toast(f"{data['campus']}时间段 {slot} 已被预约，请选择其他时间段", color='warning')
            return

        # 将预约信息存储到已预约的时间段中
        step = f"{data['campus']} {data['date_range']} {data['time_step']}"
        reserved_slots[step] = data['class']
        with open("./form_data.csv") as f:
            writer = csv.writer(f)  # todo unittest
            writer.writerow([data['i'] for i in data.keys()])  # 动态写入
        form_data.append(data)

    data = input_group("预约表单", [
        radio("请选择校区", options=['江湾校区', '仙溪校区'], required=True, name="campus"),
        input("请选择日期范围", type=DATE, name="date_range", required=True,
              validate=check_date),
        select("请选择时间段",
               options=['13:30—14:00', '14:00—14:30', '14:30—15:00', '15:00—15:30', '15:30—16:00', '16:00—16:30'],
               required=True, name="time_step"),
        input("请输入学院 + 班级全称", help_text="例：数据与大数据学院21数据科学与大数据2班", type=TEXT, required=True, name="class"),
        input("联系方式", type=TEXT, required=True, name="contact")
    ], validate=check_single)

    # 显示预约成功的信息
    toast("预约成功！", color='success')

    # 保存预约数据到xlsx文件
    # data = {'校区': [campus], '日期范围': [date_range], '时间段': [time_slot], '班级名称': [class_name]}
    # data = dict(form_table)
    # save_appointment_data(data)
    logging.info(data)
    logging.info(reserved_slots)
    logging.info(form_data)


if __name__ == '__main__':
    pywebio.config(title='易班预约系统', theme="minty")
    start_server(appointment_form, port=8080)
