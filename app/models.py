#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/models.py
Description  :  模型文件
Author       : BNDou
Date         : 2024-12-13 23:18:50
LastEditTime : 2026-04-02 00:03:20
'''
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class BoxRecord(db.Model):
    __tablename__ = 'box_records'
    
    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    box_range = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, date, box_range):
        self.id = str(uuid.uuid4())
        self.date = datetime.strptime(date, '%Y-%m-%d').date() if isinstance(date, str) else date
        # 自动格式化单个数字为区间格式
        if box_range and '-' not in box_range:
            self.box_range = f"{box_range}-{box_range}"
        else:
            self.box_range = box_range
        self.created_at = datetime.now()

    @staticmethod
    def get_monthly_records(month):
        start_date = datetime.strptime(f"{month}-01", '%Y-%m-%d').date()
        if start_date.month == 12:
            end_date = datetime(start_date.year + 1, 1, 1).date()
        else:
            end_date = datetime(start_date.year, start_date.month + 1, 1).date()
        
        return BoxRecord.query.filter(
            BoxRecord.date >= start_date,
            BoxRecord.date < end_date
        ).order_by(BoxRecord.date.desc()).all()

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'box_range': self.box_range,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'formatted_date': f"{self.date.year}年{self.date.month}月{self.date.day}日",
            'boxes_count': self.calculate_boxes()
        }

    def calculate_boxes(self):
        try:
            # 处理单个数字（如"1200"）和区间格式（如"1987-1996"）两种情况
            if '-' in self.box_range:
                start, end = self.box_range.split('-')
                start_num = int(''.join(filter(str.isdigit, start)))
                end_num = int(''.join(filter(str.isdigit, end)))
            else:
                # 单个数字情况，将其视为起始和结束相同的区间
                start_num = end_num = int(''.join(filter(str.isdigit, self.box_range)))
            
            return end_num - start_num + 1
        except:
            return 0


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='guest')  # 'admin' or 'guest'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __init__(self, username, password, role='guest'):
        self.username = username
        self.set_password(password)
        self.role = role
        
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
        
    @staticmethod
    def get_guest_user():
        """获取访客用户"""
        return User(username='guest', password='guest', role='guest')
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
