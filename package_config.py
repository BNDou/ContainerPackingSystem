#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/package_config.py
Description  :  打包配置文件
Author       : BNDou
Date         : 2024-12-14 01:12:30
LastEditTime : 2024-12-14 22:17:09
'''
import sys
import os

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        # PyInstaller 创建临时文件夹 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PackageConfig:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSV_FILE = os.path.join(BASE_DIR, 'log.csv')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    TEMPLATE_FOLDER = resource_path('templates')
    STATIC_FOLDER = resource_path('static') 