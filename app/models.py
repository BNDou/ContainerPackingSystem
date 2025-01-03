#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/models.py
Description  :  模型文件
Author       : BNDou
Date         : 2024-12-13 23:18:50
LastEditTime : 2024-12-14 22:17:47
'''
from datetime import datetime
import uuid
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
            start, end = self.box_range.split('-')
            start_num = int(''.join(filter(str.isdigit, start)))
            end_num = int(''.join(filter(str.isdigit, end)))
            return end_num - start_num + 1
        except:
            return 0