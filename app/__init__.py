#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/__init__.py
Description  :  初始化文件
Author       : BNDou
Date         : 2024-12-13 23:18:45
LastEditTime : 2026-04-02 01:15:04
'''
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import sys
import secrets

# 判断是否是打包环境
if getattr(sys, 'frozen', False):
    from package_config import PackageConfig as Config
else:
    from config import Config

db = SQLAlchemy()
# 提前导入User模型
from app.models import User

def create_app():
    # 如果是打包环境，使用特定的模板和静态文件路径
    if getattr(sys, 'frozen', False):
        app = Flask(__name__,
                   template_folder=Config.TEMPLATE_FOLDER,
                   static_folder=Config.STATIC_FOLDER)
    else:
        app = Flask(__name__)
    
    app.config.from_object(Config)
    
    # 设置会话密钥
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = secrets.token_hex(32)
        
    # 设置会话永久
    app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 1小时

    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # 检查是否有管理员账户，如果没有用户会自动在登录页面提示创建

    # 设置日志
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    logging.basicConfig(
        filename=app.config['LOG_FILE'],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from app.routes import bp
    app.register_blueprint(bp)

    return app 