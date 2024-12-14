#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/run.py
Description  :  启动文件
Author       : BNDou
Date         : 2024-12-13 23:18:57
LastEditTime : 2024-12-14 22:16:18
'''
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=12222, debug=True)
    # app.run(host="192.168.31.120", port=12222, debug=False)