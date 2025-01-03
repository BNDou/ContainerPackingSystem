#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/package_config.py
Description  :  打包配置文件
Author       : BNDou
Date         : 2024-12-14 01:12:30
LastEditTime : 2025-01-03 22:15:00
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
    BASE_DIR = os.path.abspath(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__))
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 日志配置
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    # 资源路径配置
    TEMPLATE_FOLDER = resource_path('templates')
    STATIC_FOLDER = resource_path('static') 