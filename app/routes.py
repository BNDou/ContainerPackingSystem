#!/usr/bin/env python
# coding=utf-8
'''
FilePath     : /ContainerPackingSystem/app/routes.py
Description  :  路由文件
Author       : BNDou
Date         : 2024-12-13 23:18:53
LastEditTime : 2026-04-02 00:58:23
'''
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models import BoxRecord, User
from app.utils import handle_errors
from app import db

bp = Blueprint('main', __name__)

def login_required(f):
    """认证装饰器，确保用户已登录"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login_page'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """获取当前用户"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def get_user_role():
    """获取用户角色，未登录返回guest"""
    user = get_current_user()
    return user.role if user else 'guest'

@bp.route('/')
def index():
    user_role = get_user_role()
    return render_template('index.html', user_role=user_role)

# 注意：原来的delete_record函数已被delete_record_protected替代
# 因为它包含了必要的管理员权限检查
# 现在所有删除操作都需要管理员权限

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

# 认证相关路由
@bp.route('/login', methods=['GET'])
def login_page():
    """显示登录页面"""
    # 检查是否已存在管理员用户
    admin_exists = User.query.filter_by(role='admin').first() is not None
    return render_template('login.html', admin_exists=admin_exists)

@bp.route('/login', methods=['POST'])
def login():
    """处理登录请求"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '请提供用户名和密码'}), 400
            
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return jsonify({'message': '登录成功', 'role': user.role}), 200
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
            
    except Exception as e:
        return jsonify({'error': '登录失败: ' + str(e)}), 500

@bp.route('/api/admin/check')
def check_admin_exists():
    """检查是否存在管理员账户"""
    try:
        # 确保数据库表已创建
        admin_exists = User.query.filter_by(role='admin').first() is not None
        return jsonify({
            'admin_exists': admin_exists
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/admin/register', methods=['POST'])
def register_admin():
    """注册管理员账户 - 只有当没有管理员时可用"""
    try:
        # 检查是否已存在管理员
        if User.query.filter_by(role='admin').first():
            return jsonify({'error': '管理员账户已存在'}), 400
            
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not username or not password or not confirm_password:
            return jsonify({'error': '请填写完整信息'}), 400
            
        if password != confirm_password:
            return jsonify({'error': '两次输入的密码不一致'}), 400
            
        if len(password) < 6:
            return jsonify({'error': '密码长度至少为6位'}), 400
            
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': '用户名已存在'}), 400
            
        # 创建管理员用户
        admin_user = User(
            username=username,
            password=password,
            role='admin'
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        # 自动登录
        session['user_id'] = admin_user.id
        session.permanent = True
        
        return jsonify({
            'message': '管理员账户创建成功',
            'role': 'admin'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建管理员账户失败: ' + str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """登出"""
    session.clear()
    return jsonify({'message': '登出成功'}), 200

@bp.route('/api/user/status')
def get_user_status():
    """获取当前用户状态"""
    try:
        user_role = get_user_role()
        user_info = None
        if user_role != 'guest':
            user = get_current_user()
            if user:
                user_info = user.to_dict()
        
        return jsonify({
            'role': user_role,
            'user': user_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/records', methods=['POST'])
def add_record():
    """添加记录 - 需要管理员权限"""
    try:
        # 只有管理员可以添加记录
        user_role = get_user_role()
        if user_role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
            
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

@bp.route('/records/<record_id>', methods=['DELETE'])
def delete_record_protected(record_id):
    """删除记录 - 需要管理员权限"""
    try:
        # 只有管理员可以删除记录
        user_role = get_user_role()
        if user_role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
            
        record = BoxRecord.query.get(record_id)
        if not record:
            return jsonify({'error': '记录不存在'}), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': '记录删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
