<!--
 * @FilePath     : /ContainerPackingSystem/README.md
 * @Description  :  装箱记录管理系统
 * @Author       : BNDou
 * @Date         : 2024-12-14 01:27:05
 * @LastEditTime : 2024-12-14 22:22:10
-->
# 装箱记录管理系统

一个基于 Flask 的装箱记录管理系统，用于记录、删除和查询装箱信息。

## 功能特点

- 查询月度装箱记录
  - 按月份查询装箱记录
  - 显示每条记录的箱数统计
  - 显示月度总箱数和记录数
  - 日期显示采用中文格式
- 添加新的装箱记录
  - 支持日期选择
  - 支持箱号区间输入
  - 自动生成唯一记录ID
  - 自动记录创建时间
- 删除装箱记录
  - 支持删除指定记录ID的装箱记录

## 技术框架

- 后端框架：Flask
- 数据存储：CSV文件
- 前端框架：Bootstrap 5
- 数据处理：Pandas
- 日期处理：Python-dateutil

## 项目结构

```
project/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── utils.py
├── logs/
├── config.py
├── package_config.py
├── requirements.txt
├── run.py
└── log.csv
```

## 运行方法

### 开发环境
```bash
python run.py
```

### 生产环境
1. 修改 run.py 中的 host 和 port
2. 关闭 debug 模式
3. 运行程序

## 使用说明

1. 查询记录：
   - 选择月份（格式：YYYY-MM）
   - 点击查询按钮
   - 查看结果表格和统计信息

2. 添加记录：
   - 选择日期
   - 输入箱号区间（格式：A001-A100）
   - 点击添加按钮

3. 删除记录：
   - 选择月份
   - 点击删除按钮

## 打包说明

使用 auto-py-to-exe 打包：

1. 安装打包工具
```bash
pip install auto-py-to-exe
```

2. 配置打包选项
- Script Location: run.py
- Onefile: One Directory
- Console Window: Console Based
- Additional Files:
  - app/templates -> templates
  - app/static -> static
  - config.py -> .
  - package_config.py -> .

## 注意事项

1. 确保 logs 目录存在且有写入权限
2. 箱号区间格式必须统一（如：A001-A100）
3. 日期选择不能为空
4. CSV文件会自动创建

## 系统要求

- Python 3.7+
- 支持现代浏览器
- 操作系统：Windows/Linux/MacOS

## 日志记录

- 位置：logs/app.log
- 记录内容：操作日志和错误信息
- 格式：时间 - 名称 - 级别 - 消息