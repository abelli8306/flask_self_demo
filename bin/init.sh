#!/bin/bash

appName=$(pwd | awk -F '/' '{print $5}')
source /etc/profile
source /home/product/py_framework/python_venv_mount.sh

if_venv_existed ## 移除旧的虚拟环境
venv_mount ## 创建新的虚拟环境
