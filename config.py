#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/config.py
Description  :  配置文件
Author       : BNDou
Date         : 2024-12-13 23:18:42
LastEditTime : 2025-01-03 21:19:03
'''
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 日志配置
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log') 