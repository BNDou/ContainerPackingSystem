#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/models.py
Description  :  模型文件
Author       : BNDou
Date         : 2024-12-13 23:18:50
LastEditTime : 2024-12-14 22:17:47
'''
import pandas as pd
from datetime import datetime
import uuid

class BoxRecord:
    def __init__(self, date, box_range):
        self.id = str(uuid.uuid4())
        self.date = date
        self.box_range = box_range
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_monthly_records(csv_file, month):
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date'])
        monthly_records = df[df['date'].dt.strftime('%Y-%m') == month]
        return monthly_records.to_dict('records')

    def save(self, csv_file):
        new_record = {
            'id': self.id,
            'date': self.date,
            'box_range': self.box_range,
            'created_at': self.created_at
        }
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['id', 'date', 'box_range', 'created_at'])
        
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        return new_record