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
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        record = BoxRecord.query.get(record_id)
        if not record:
            return jsonify({'error': '记录不存在'}), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': '记录删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/records/<month>', methods=['GET'])
def get_monthly_records(month):
    try:
        records = BoxRecord.get_monthly_records(month)
        records_dict = [record.to_dict() for record in records]
        
        # 计算总箱数
        total_boxes = sum(record.calculate_boxes() for record in records)
        
        return jsonify({
            'records': records_dict,
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
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 