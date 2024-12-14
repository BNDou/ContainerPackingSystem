#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/config.py
Description  :  配置文件
Author       : BNDou
Date         : 2024-12-13 23:18:42
LastEditTime : 2024-12-14 22:17:20
'''
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSV_FILE = os.path.join(BASE_DIR, 'log.csv')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log') 