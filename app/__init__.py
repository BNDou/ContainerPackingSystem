#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/__init__.py
Description  :  初始化文件
Author       : BNDou
Date         : 2024-12-13 23:18:45
LastEditTime : 2024-12-14 22:17:54
'''
from flask import Flask
import logging
import os
import sys

# 判断是否是打包环境
if getattr(sys, 'frozen', False):
    from package_config import PackageConfig as Config
else:
    from config import Config

def create_app():
    # 如果是打包环境，使用特定的模板和静态文件路径
    if getattr(sys, 'frozen', False):
        app = Flask(__name__,
                   template_folder=Config.TEMPLATE_FOLDER,
                   static_folder=Config.STATIC_FOLDER)
    else:
        app = Flask(__name__)
    
    app.config.from_object(Config)

    # 设置日志
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    logging.basicConfig(
        filename=app.config['LOG_FILE'],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 确保CSV文件存在
    if not os.path.exists(app.config['CSV_FILE']):
        with open(app.config['CSV_FILE'], 'w', encoding='utf-8') as f:
            f.write('id,date,box_range,created_at\n')

    from app.routes import bp
    app.register_blueprint(bp)

    return app 