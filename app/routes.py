#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/routes.py
Description  :  路由文件
Author       : BNDou
Date         : 2024-12-13 23:18:53
LastEditTime : 2024-12-14 22:17:36
'''
from flask import Blueprint, request, jsonify, render_template
from app.models import BoxRecord
from app.utils import handle_errors
from config import Config
import pandas as pd

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        df = pd.read_csv(Config.CSV_FILE)
        # 检查记录是否存在
        if record_id not in df['id'].values:
            return jsonify({'error': '记录不存在'}), 404
        
        # 删除记录
        df = df[df['id'] != record_id]
        df.to_csv(Config.CSV_FILE, index=False)
        return jsonify({'message': '记录删除成功'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records/<month>', methods=['GET'])
def get_monthly_records(month):
    try:
        df = pd.read_csv(Config.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'])
        monthly_records = df[df['date'].dt.strftime('%Y-%m') == month]
        
        # 计算每条记录的箱数
        def calculate_boxes(box_range):
            try:
                start, end = box_range.split('-')
                start_num = int(''.join(filter(str.isdigit, start)))
                end_num = int(''.join(filter(str.isdigit, end)))
                return end_num - start_num + 1
            except:
                return 0

        # 添加箱数统计和格式化日期
        records = monthly_records.to_dict('records')
        total_boxes = 0
        for record in records:
            # 转换日期为中文格式
            date_obj = pd.to_datetime(record['date'])
            record['formatted_date'] = f"{date_obj.year}年{date_obj.month}月{date_obj.day}日"
            record['created_at'] = record.get('created_at', record['date'])  # 记录时间
            # 计算箱数
            boxes = calculate_boxes(record['box_range'])
            record['boxes_count'] = boxes
            total_boxes += boxes

        return jsonify({
            'records': records,
            'total_boxes': total_boxes,
            'total_records': len(records)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records', methods=['POST'])
def add_record():
    try:
        data = request.get_json()
        record = BoxRecord(
            date=data['date'],
            box_range=data['box_range']
        )
        saved_record = record.save(Config.CSV_FILE)
        return jsonify(saved_record), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500 