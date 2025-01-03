#!/usr/bin/env python
# coding=utf-8
'''
Description  : 数据迁移脚本 - 将CSV数据迁移到SQLite数据库
Author       : BNDou
'''
import pandas as pd
from app import create_app, db
from app.models import BoxRecord
from datetime import datetime

def migrate_csv_to_db(csv_file='log.csv'):
    print(f"开始从 {csv_file} 迁移数据到数据库...")
    
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_file)
        print(f"成功读取CSV文件，共有 {len(df)} 条记录")
        
        # 创建Flask应用上下文
        app = create_app()
        with app.app_context():
            # 遍历CSV数据并插入到数据库
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # 创建BoxRecord实例
                    record = BoxRecord(
                        date=row['date'],
                        box_range=row['box_range']
                    )
                    # 设置原始id和created_at
                    record.id = row['id']
                    record.created_at = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
                    
                    # 添加到数据库
                    db.session.add(record)
                    success_count += 1
                except Exception as e:
                    print(f"错误: 处理记录 {row['id']} 时失败: {str(e)}")
                    error_count += 1
                    continue
            
            # 提交所有更改
            try:
                db.session.commit()
                print(f"\n数据迁移完成!")
                print(f"成功导入: {success_count} 条记录")
                print(f"失败记录: {error_count} 条")
            except Exception as e:
                db.session.rollback()
                print(f"错误: 提交数据时失败: {str(e)}")
                return False
            
            # 验证数据
            total_records = BoxRecord.query.count()
            print(f"\n数据验证:")
            print(f"数据库中的总记录数: {total_records}")
            
            return True
    except FileNotFoundError:
        print(f"错误: 找不到CSV文件 {csv_file}")
        return False
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == '__main__':
    migrate_csv_to_db() 