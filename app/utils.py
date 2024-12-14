#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/utils.py
Description  :  工具函数
Author       : BNDou
Date         : 2024-12-13 23:18:51
LastEditTime : 2024-12-14 22:17:28
'''
import logging
from functools import wraps
from flask import jsonify

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    return decorated_function 